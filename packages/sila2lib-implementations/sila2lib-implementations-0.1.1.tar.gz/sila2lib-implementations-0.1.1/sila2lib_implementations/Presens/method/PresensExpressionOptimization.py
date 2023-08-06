import time
import os
import sys
import threading
import datetime
import csv
import shutil

from ..._framework import _process_routine_lib as prl
from ..._framework._logger import Logger
from sila2lib_implementations.Presens.PresensService.PresensService_client import PresensServiceClient


class PresensExpressionOptimization:

    # Todo: Pass measurement intervals down to __init__ and subsequently to data collection loop.
    # Todo: Restructure lib files and class functions. Move class functions to lib.

    def __init__(self, thread_queue, influx_client=None, meta_data=None, device_data=None):
        self.q = thread_queue
        self.name = 'Presens_handler_data_acquisition'
        self.meta_data = meta_data
        self.logger = Logger(name=self.name, meta_data=self.meta_data).logger
        self.influx_client = influx_client
        self.influx_client.database_connect(logger=self.logger)
        if device_data is not None:
            self.device_data = prl.ExperimentDeviceData(device_name=device_data.name, server_ip=device_data.server_ip,
                                                        server_port=device_data.server_port, logger=self.logger)
        else:
            self.device_data = None

        self.process_data = prl.ExperimentProcessData(logger=self.logger,
                                                      active_positions=self.meta_data.initial_active_positions)
        self.initialize_db_measurements()

        self.measurements: list = ['pH', 'O2']
        self.measurement_interval: int = 10
        self.device = None
        self.data: dict = {}
        self.thread = None

        self.pH_data: list = []
        self.pH_data_amplitude: list = []
        self.pH_data_phase_shift: list = []
        self.pH_data_error: list = []

        self.DO_data: list = []
        self.DO_data_amplitude: list = []
        self.DO_data_error: list = []

        self.influx_client = influx_client
        # self.server = server.Server()

        # Todo: Get a better name for this class
        self.name = "presens_handler"

    def connect_device(self):
        # self.device = PresensServiceClient(server_ip='10.152.248.15', server_port=50002)
        self.device = PresensServiceClient(server_ip=self.device_data.server_ip,
                                           server_port=self.device_data.server_port)
        self.logger.info("Presens device connected")

    def initialize_db_measurements(self):
        if self.device_data is not None:
            self.device_data.restart_flag_positions_to_db(client_object=self.influx_client,
                                                          experiment_name=self.meta_data.run_name,
                                                          restart_flag=0)

    def synchronize_process_data_with_db(self):
        self.process_data.update(client_object=self.influx_client, run_name=self.meta_data.run_name)
        # if self.device_data is not None:
        #    self.device_data.update(client_object=self.influx_client.db_client)

    def read_data_calibration_from_csv(self, path):
        try:
            with open(path, "r", newline='') as csv_file:
                reader = csv.DictReader(csv_file, delimiter=';')
                _calibration_dict = dict()
                for i, row in enumerate(reader):
                    if i == 0:
                        for key in row.keys():
                            _calibration_dict[key] = [row[key]]
                    else:
                        for key in row.keys():
                            _calibration_dict[key].append(row[key])
                return _calibration_dict
        except ImportWarning:
            self.logger.warning(f'Error reading file at {path}')
            _calibration_dict = self.get_data_calibration()
            self.logger.warning(f'Currently stored calibration data on device is being used and stored in {path} '
                                'as \'presens_calibration_data.csv\'!')
            self.save_data_calibration_as_csv(_calibration_dict)
            return _calibration_dict

    def save_data_calibration_as_csv(self, calibration_dict, path):
        """
        If the user has not supplied a csv-file or the file could not be read, the used calibration data is saved in the
        run directory.
        :param calibration_dict: The calibration data to be stored
        :param path:
        :return:
        """
        if os.path.isfile(path):
            shutil.rmtree(path, ignore_errors=True)
            self.logger.info('Removing existing file.')
        with open(path, "w", newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=';')
            keys = calibration_dict.keys()
            writer.writerow(keys)
            for i in range(0, calibration_dict['Number_of_bars'][0], 1):
                if i == 0:
                    writer.writerow([calibration_dict[key][i] for key in keys])
                if i >= 1:
                    writer.writerow(['\t', '\t', ] + [calibration_dict[key][i] for key in list(keys)[2:]])
            # writer.writerow([f'Time_of_creation: \t {datetime.datetime.now().strftime("%Y_%m_%dT%H_%M_%SZ")}'])
            # writer.writerow([f'Number_of_bars:\t{calibration_dict["Number_of_bars"]}'])
            # writer.writerow([f'CurrentO2CalLow:\t{calibration_dict["CurrentO2CalLow"]}'])
            # writer.writerow([f'CurrentO2CalHigh:\t{calibration_dict["CurrentO2CalHigh"]}'])
            # writer.writerow([f'CurrentO2CalTemp:\t{calibration_dict["CurrentO2CalTemp"]}'])
            # writer.writerow([f'CurrentPHlmax:\t{calibration_dict["CurrentPHlmax"]}'])
            # writer.writerow([f'CurrentPHlmin:\t{calibration_dict["CurrentPHlmin"]}'])
            # writer.writerow([f'CurrentPHpH0:\t{calibration_dict["CurrentPHpH0"]}'])
            # writer.writerow([f'CurrentPHdpH:\t{calibration_dict["CurrentPHdpH"]}'])
            # writer.writerow([f'CurrentPHCalTemp:\t{calibration_dict["CurrentPHCalTemp"]}'])
        # Todo: Simply expression and generalize it using some dict_to_csv function

    def get_data_calibration(self):
        """
        In case no csv-file is supplied with specific calibration data, the calibration data stored on the device will
        be retrieved and stored for documentation purposes.
        :return: The calibration data stored on the device retrieved via the devices SiLA2 server. The returned data is
        a dictionary with entries for each calibration parameter as a list for each respective bar.
        """
        _calibration_dict = dict()
        _number_of_bars = self.device.Get_SensorProvider_TotalBars().TotalBars.value

        _O2CalLow = self.device.CalibrationServicer_GetO2CalLow()
        _O2CalHigh = self.device.CalibrationServicer_GetO2CalHigh()
        _O2CalTemp = self.device.CalibrationServicer_GetO2CalTemp()
        _PHImax = self.device.CalibrationServicer_GetPHlmax()
        _PHImin = self.device.CalibrationServicer_GetPHlmin()
        _PHpH0 = self.device.CalibrationServicer_GetPHpH0()
        _PHdpH = self.device.CalibrationServicer_GetPHdpH()
        _PHCalTemp = self.device.CalibrationServicer_GetPHCalTemp()

        _calibration_dict['Time_of_creation'] = [datetime.datetime.now().strftime("%Y_%m_%dT%H_%M_%SZ")]
        _calibration_dict['Number_of_bars'] = [_number_of_bars]  # list(range(0, _number_of_bars,1))

        for i in range(0, _number_of_bars, 1):
            if i == 0:
                _calibration_dict['CurrentO2CalLow'] = [_O2CalLow.CurrentO2CalLow[i].value]
                _calibration_dict['CurrentO2CalHigh'] = [_O2CalHigh.CurrentO2CalHigh[i].value]
                _calibration_dict['CurrentO2CalTemp'] = [_O2CalTemp.CurrentO2CalTemp[i].value]
                _calibration_dict['CurrentPHlmax'] = [_PHImax.CurrentPHlmax[i].value]
                _calibration_dict['CurrentPHlmin'] = [_PHImin.CurrentPHlmin[i].value]
                _calibration_dict['CurrentPHpH0'] = [_PHpH0.CurrentPHpH0[i].value]
                _calibration_dict['CurrentPHdpH'] = [_PHdpH.CurrentPHdpH[i].value]
                _calibration_dict['CurrentPHCalTemp'] = [_PHCalTemp.CurrentPHCalTemp[i].value]
            else:
                _calibration_dict['CurrentO2CalLow'].append(_O2CalLow.CurrentO2CalLow[i].value)
                _calibration_dict['CurrentO2CalHigh'].append(_O2CalHigh.CurrentO2CalHigh[i].value)
                _calibration_dict['CurrentO2CalTemp'].append(_O2CalTemp.CurrentO2CalTemp[i].value)
                _calibration_dict['CurrentPHlmax'].append(_PHImax.CurrentPHlmax[i].value)
                _calibration_dict['CurrentPHlmin'].append(_PHImin.CurrentPHlmin[i].value)
                _calibration_dict['CurrentPHpH0'].append(_PHpH0.CurrentPHpH0[i].value)
                _calibration_dict['CurrentPHdpH'].append(_PHdpH.CurrentPHdpH[i].value)
                _calibration_dict['CurrentPHCalTemp'].append(_PHCalTemp.CurrentPHCalTemp[i].value)
        return _calibration_dict

    def set_data_calibration(self, calibration_dict):
        """
        If calibration data is available, the data will be sent to the device. Calibration data stored on the device
        prior to this operation will be overwritten and lost.
        :param calibration_dict: The calibration data to be transmitted to the devices SiLA2 server.
        :return:
        """
        _number_of_bars = calibration_dict['Number_of_bars']
        self.device.CalibrationServicer_SetO2CalLow(calibration_dict['CurrentO2CalLow'])
        self.device.CalibrationServicer_SetO2CalHigh(calibration_dict['CurrentO2CalHigh'])
        self.device.CalibrationServicer_SetO2CalTemp(calibration_dict['CurrentO2CalTemp'])
        self.device.CalibrationServicer_SetPHlmax(calibration_dict['CurrentPHlmax'])
        self.device.CalibrationServicer_SetPHlmin(calibration_dict['CurrentPHlmin'])
        self.device.CalibrationServicer_SetPHpH0(calibration_dict['CurrentPHpH0'])
        self.device.CalibrationServicer_SetPHdpH(calibration_dict['CurrentPHdpH'])
        self.device.CalibrationServicer_SetPHCalTemp(calibration_dict['CurrentPHCalTemp'])

    def transfer_calibration_data(self):
        """
        Before each run, the calibration data should be submitted to the devices to ensure that the correct ones are
        being used. In case no calibration data is supplied, the currently stored information on the device is retrieved
        and stored for documentation purposes.
        """
        _path = f'{self.meta_data.parent_path}/presens_calibration_data.csv'
        if os.path.isfile(_path):
            _data = self.read_data_calibration_from_csv(_path)
            self.logger.info(f'Successfully read in calibration data from file: {_path}')
        else:
            self.logger.warning(f'Could not find file at {_path}')
            _data = self.get_data_calibration()
            self.logger.warning(f'Currently stored calibration data on device is being used and stored in {_path} '
                                'as \'presens_calibration_data.csv\'!')
            self.save_data_calibration_as_csv(_data, _path)

        self.set_data_calibration(_data)
        self.logger.info(f'Successfully communicated calibration data to device')

    def get_data(self):
        # Function to get current data from the Presens SiLA2 server and write them to DB
        _data_collection = dict()
        _value = []
        _amplitude = []
        _phase_shift = []
        _error = []

        _data = self.device.SensorProvider_GetAllO2()
        for i in range(0, len(_data.CurrentO2), 1):
            _value.append(_data.CurrentO2[i].value)
            _amplitude.append(_data.CurrentAmplitude[i].value)
            _error.append(_data.CurrentErrorCode[i].value)
        _data_collection['O2'] = _value.copy()
        _data_collection['O2_amplitude'] = _amplitude.copy()
        _data_collection['O2_error'] = _error.copy()
        _value.clear(), _amplitude.clear(), _error.clear()
        time.sleep(self.measurement_interval / 2)
        _data = self.device.SensorProvider_GetAllPH()
        for i in range(0, len(_data.CurrentPH), 1):
            _value.append(_data.CurrentPH[i].value)
            _amplitude.append(_data.CurrentAmplitude[i].value)
            _phase_shift.append(_data.CurrentPhase[i].value)
            _error.append(_data.CurrentErrorCode[i].value)
        _data_collection['pH'] = _value.copy()
        _data_collection['pH_amplitude'] = _amplitude.copy()
        _data_collection['pH_phase_shift'] = _phase_shift.copy()
        _data_collection['pH_error'] = _error.copy()
        _value.clear(), _amplitude.clear(), _phase_shift.clear(), _error.clear()
        return _data_collection

    def shutdown_device(self):
        self.logger.info(f'Shutdown of {self.name}')
        # There is no shutdown procedure for this device

    def save_data(self):
        data_points = list()
        for key in list(self.data.keys()):
            measurement_tag = None
            for measurement_name in self.measurements:
                if measurement_name in key:
                    measurement_tag = measurement_name
                # else:
                #     measurement_tag = 'undefined_tag_error'
            for position, value in enumerate(self.data[key]):
                data_point = {
                    "measurement": "schedulerMeasurementPresensData",
                    "tags": {
                        "experiment_name": self.meta_data.run_name,

                        "task_kind": self.name,
                        "measurement": measurement_tag,
                        "parameter": key,
                        "position": int(position)
                    },
                    "time": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "fields": {
                        # f"PV_{key}_{position}": value
                        f"PV_{key}": value
                    }
                }
            data_points.append(data_point)
        self.logger.info("Thread: {}; Data written to DB!".format(self.name))
        self.influx_client.db_client.write_points(data_points)

    def start_data_acquisition(self):
        self.thread = threading.Thread(target=self.worker, name=('%s' % self.name), daemon=True)
        self.thread.start()

    def run(self):
        try:
            self.connect_device()
            # Todo: Add read_data_calibration_from_csv() and set_data_calibration() via transfer_calibration_data()
            self.transfer_calibration_data()
            self.start_data_acquisition()
        except KeyboardInterrupt:
            self.thread.join()

    def abstract_func(self):
        pass



    def worker(self):
        while True:
            try:
                self.synchronize_process_data_with_db()
                self.data = self.get_data()
                self.pH_data, self.pH_data_amplitude, self.pH_data_phase_shift, self.pH_data_error = \
                    self.data['pH'], self.data['pH_amplitude'], self.data['pH_phase_shift'], self.data['pH_error']
                self.DO_data, self.DO_data_amplitude, self.DO_data_error = \
                    self.data['O2'], self.data['O2_amplitude'], self.data['O2_error']
                self.logger.debug(f'Current positions {self.meta_data.positions}')
                # Todo: Use a boolean position flag to filter out only the pH data of interest in logging statement
                self.logger.debug(f'Current pH data {self.pH_data}')
                self.logger.debug(f'Current pH sensor amplitude{self.pH_data_amplitude}')
                self.logger.debug(f'Current pH sensor phase shift{self.pH_data_phase_shift}')
                self.logger.debug(f'Current pH sensor error code{self.pH_data_error}')
                self.logger.debug(f'Current DO data {self.DO_data}')
                self.logger.debug(f'Current DO sensor amplitude{self.DO_data_amplitude}')
                self.logger.debug(f'Current DO sensor error code{self.DO_data_error}')
                self.save_data()
                time.sleep(self.measurement_interval / 2)

                # Check for abort command
                if not self.q.empty():
                    q_item = self.q.get()
                    print(f'{self.name} received message: {q_item}')
                    self.q.task_done()
                    if 'abort' in q_item:
                        if q_item == f'abort':
                            self.q.put(q_item)
                            self.exit()
                            break
                        elif q_item == f'{self.name}_abort':
                            self.exit()
                            break
                        else:
                            self.q.put(q_item)

            except ConnectionError:
                tb = sys.exc_info()[2]
                self.logger.critical('Data could not be acquired! Potential connection error.')
                self.logger.critical(tb)
                time.sleep(self.measurement_interval / 2)
                raise ConnectionError(...).with_traceback(tb)
                pass

    def exit(self):
        print(f'Exiting {self.name}')
        self.shutdown_device()

    def __exit__(self):
        # Kill started servers once program is finished
        pass
