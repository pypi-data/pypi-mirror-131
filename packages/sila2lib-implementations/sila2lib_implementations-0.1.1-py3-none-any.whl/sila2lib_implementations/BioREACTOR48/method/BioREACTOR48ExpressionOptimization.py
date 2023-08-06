import time
import sys
import threading
import datetime

from ..._framework import _process_routine_lib as prl
from ..._framework._logger import Logger
from sila2lib_implementations.BioREACTOR48.BioREACTOR48Service.BioREACTOR48Service_client import BioREACTOR48ServiceClient


class BioREACTOR48ExpressionOptimization:
    # Todo: Pass measurement intervals down to __init__ and subsequently to data collection loop.
    # Todo: Restructure lib files and class functions. Move class functions to lib.

    def __init__(self, thread_queue, influx_client=None, meta_data=None, device_data=None):
        self.q = thread_queue
        self.name = 'BioREACTOR48_handler_data_acquisition'
        self.meta_data = meta_data
        self.logger = Logger(name=self.name, meta_data=self.meta_data).logger
        self.influx_client = influx_client
        self.influx_client.database_connect(logger=self.logger)

        if device_data is not None:
            self.device_data = prl.ExperimentDeviceData(device_name=device_data.name, server_ip=device_data.server_ip,
                                                        server_port=device_data.server_port, logger=self.logger)
        else:
            self.device_data = None
        self.process_data: prl.ExperimentProcessData = \
            prl.ExperimentProcessData(logger=self.logger, active_positions=self.meta_data.initial_active_positions)
        self.initialize_db_measurements()
        self.measurements: list = ['rpm', 'power']
        self.measurement_interval = 10
        self.device = None
        self.data: dict = {}
        self.thread = None
        self.influx_client = influx_client
        # self.server = server.Server()

    def connect_device(self):
        # self.device = PresensServiceClient(server_ip='10.152.248.15', server_port=50003)
        self.device = BioREACTOR48ServiceClient(server_ip=self.device_data.server_ip,
                                                server_port=self.device_data.server_port)
        self.logger.info("BioREACTOR48 device connected")

    def initialize_db_measurements(self):
        if self.device_data is not None:
            self.device_data.restart_flag_positions_to_db(client_object=self.influx_client, experiment_name=self.meta_data.run_name,
                                                          restart_flag=0)

    def synchronize_process_data_with_db(self):
        self.process_data.update(client_object=self.influx_client, run_name=self.meta_data.run_name)
        if self.device_data is not None:
            self.device_data.update(client_object=self.influx_client)

    def get_data(self):
        # Function to get current data from the BioREACTOR48 SiLA2 server and write them to DB
        _data_collection = dict()
        _rpm = list()
        _power = list()
        _status = list()

        _data = self.device.MotorServicer_GetRPM()
        _rpm.append(_data.CurrentRPM.value)
        _data_collection['rpm'] = _rpm.copy()
        time.sleep(self.measurement_interval / 4)
        _data = self.device.MotorServicer_GetPower()
        _power.append(_data.CurrentPower.value)
        _data_collection['power'] = _power.copy()
        time.sleep(self.measurement_interval / 4)
        _data = self.device.DeviceServicer_GetReactorStatus()
        for i in range(0, len(_data.ReactorStatus), 1):
            _status.append(_data.ReactorStatus[i].value)
        _data_collection['rpm_status'] = _status.copy()
        return _data_collection

    def restart_stirrer(self):
        # Reset the restart flag
        self.logger.info(f'Restarting stirrers of {self.name}')
        self.device.MotorServicer_StopStirrer()
        time.sleep(1)
        self.device.MotorServicer_StartStirrer()
        time.sleep(20)
        self.device_data.restart_flag_positions_to_db(client_object=self.influx_client, experiment_name=self.meta_data.run_name,
                                                      restart_flag=0)
        self.logger.debug(f'Resetting the restart_flag of device in DB {self.name}')

    def shutdown_device(self):
        self.logger.info(f'Shutdown of {self.name}')
        self.device.MotorServicer_SetPower(Power=0)
        self.device.MotorServicer_SetRPM(RPM=0)
        self.device.MotorServicer_StopStirrer()


    def save_data(self):
        data_points = list()
        for key in list(self.data.keys()):
            measurement_tag = 'undefined_tag_error'
            for measurement_name in self.measurements:
                if measurement_name in key:
                    measurement_tag = measurement_name
            for position, value in enumerate(self.data[key]):

                data_point = {
                    "measurement": "schedulerMeasurementBioREACTOR48Data",
                    "tags": {
                        "experiment_name": self.meta_data.run_name,
                        "task_kind": self.name,
                        "measurement": measurement_tag,
                        "parameter": key,
                        "position": int(position)
                    },
                    "time": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "fields": {
                        f"PV_{key}": value
                    }
                }
                data_points.append(data_point)
        self.logger.info("Thread: {}; Data written to DB!".format(self.name))
        self.influx_client.db_client.write_points(data_points)

    def start_data_acquisition(self):
        self.thread = threading.Thread(target=self.worker, name=('%s' % self.name),
                                       daemon=True)
        self.thread.start()

    def run(self):
        try:
            self.connect_device()
            self.start_data_acquisition()
        except KeyboardInterrupt:
            self.thread.join()

    def abstract_func(self):
        pass



    def worker(self):
        self.device.MotorServicer_SetPower(Power=100)
        self.device.MotorServicer_SetRPM(RPM=1500)
        while True:
            try:
                self.synchronize_process_data_with_db()
                self.data = self.get_data()
                self.logger.debug(f'Current positions {self.meta_data.positions}')
                for key in list(self.data.keys()):
                    self.logger.debug(f'Current {key} data {self.data[key]}')
                self.save_data()
                if self.device_data.restart_flag == 1:
                    self.restart_stirrer()
                else:
                    time.sleep(self.measurement_interval/2)
                    pass

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

    def exit(self):
        print(f'Exiting {self.name}')
        self.shutdown_device()

    def __exit__(self):
        #  Kill started servers once program is finished
        pass
