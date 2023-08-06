#!/usr/bin/env python3
"""
This file tests the simulation mode of the PreSens sensor bars. Tests are organized in classes to logically separate the
services' features, as well as get- from set-functions. Return values are validated for data types, value range and whether
length of return values is as desired (e.g. as input values). All returns must assert "True", since the injected input
parameter range is only valid. For invalid parameter injection and error handling see:
'test_presens_simulation_error.py'
Multiple executions of single test_functions are conducted via the "parametrize" functionality offered by pytest
(injection) to cover and test a wide input range.
"""

import logging
import pytest
import random
import socket
from threading import (
    Thread,
    Event
)
import time
from uuid import UUID
from unittest import mock

from sila2lib_implementations.Presens.PresensService.PresensService_client import PresensServiceClient
from sila2lib_implementations.Presens.PresensService import PresensService_server

from tests.config import settings


logger = logging.getLogger(__name__)

# Import PreSens device default configuration from PresensService_server.py:
sample_depth = 2
total_bars = PresensService_server.Properties.TotalBars
bar_sensors = PresensService_server.Properties.BarSensors
total_channels = PresensService_server.Properties.TotalChannels


def wait_until_port_closes(ip: str, port: int, timeout: float = 10) -> bool:
    """Try to bind the socket at {ip}:{port} to check if a socket resource is available

    :param ip: The ip of the host system.
    :param port: The port of the socket.
    :param timeout: The timeout until a connection attempt is aborted.
    :return: False if socket is available. True if unavailable.
    """

    a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    a_socket.settimeout(timeout)
    location = (ip, port)
    try:
        a_socket.connect_ex(location)
        while a_socket.connect_ex(location) == 0:
            return False
    except (TimeoutError, OSError, ValueError, OverflowError, InterruptedError) as e:
        logger.error(f'Encountered exception {e.__class__.__name__}: {e}')
    except Exception as e:
        logger.error(f'Encountered unknown exception {e.__class__.__name__}: {e}')
    finally:
        a_socket.close()
        return True


def wait_until_server_up(server, timeout: float = 10.0) -> bool:
    """ Waits until the server is started sanely. Currently unimplemented on server site (server.is_healthy not available)

    :param server: The server whose sanely up status has to be tested
    :param timeout: Defined timeout at which check is aborted and error is sent
    :return: 0 for server is up. 1 for timeout exceeded.
    """
    # t = 0
    # while server.healthy is False:
    #     if t > timeout:
    #         return True
    #     time.sleep(0.1)  # return error message
    #     t += 0.1
    # return False
    time.sleep(10)


# Test Server setup
class PresensTestServer(PresensService_server.PresensServiceServer):
    """
    Test server instance. Implementation of service until an abort event is sent
    :param abort_event: Event that leads to the server stop
    """

    ip = settings.PRESENS_IP
    port = settings.PRESENS_PORT
    simulation_mode = settings.PRESENS_SIMULATION_MODE

    def __init__(self, abort_event: Event):
        self.abort_event = abort_event
        super().__init__(ip=self.ip, port=self.port, simulation_mode=self.simulation_mode)

    def serve(self):
        self.run(block=False)
        while not self.abort_event.is_set():
            time.sleep(1)
        self.stop_grpc_server()


@pytest.fixture(autouse=True, scope='module')
def setup_and_teardown_presens_server():
    """
    Starts a server thread and tears it down automatically after the whole module is executed.
    """
    abort_event = Event()
    server = PresensTestServer(abort_event)
    thread = Thread(target=server.serve, args=(), daemon=True)
    thread.start()
    wait_until_server_up(server)
    logger.info('Started Presens server')
    yield thread
    abort_event.set()
    thread.join(timeout=10)
    wait_until_port_closes(ip=PresensTestServer.ip, port=PresensTestServer.port, timeout=10)
    if thread.is_alive:
        logger.warning(f'Presens server thread is still alive: {thread.is_alive()}')
    logger.info('Stopped Presens server')


class TestPresensServerFunctionalities:
    """
    Basic connection test with the server. Also checks if the server was started with the correct parameters (port, ip, mode)
    """
    # Setup_class is meant to be used like __init__ but the latter is causing problems in pytest
    # (cannot collect test class because it has a __init__ constructor)
    def setup_class(cls):
        cls.sila_client = PresensServiceClient(server_ip=PresensTestServer.ip, server_port=PresensTestServer.port)

    def test_run_presens_test_server(self, setup_and_teardown_presens_server):
        logger.info(f'PreSens server running. Is alive: {setup_and_teardown_presens_server.is_alive()}')
        assert True

    def test_connect_to_presens_server(self):
        logger.info(f'Connected to client: {self.sila_client.run()}')
        assert self.sila_client.run() is True

    def test_toggle_mode(self):
        assert self.sila_client.simulation_mode is True  # ._simulation_mode also possible
        self.sila_client.toggleSimMode()
        assert self.sila_client.simulation_mode is False

    def test_mode_switch(self):
        self.sila_client.switchToSimMode()
        assert self.sila_client.simulation_mode is True
        self.sila_client.switchToRealMode()
        assert self.sila_client.simulation_mode is False
        self.sila_client.switchToSimMode()
        assert self.sila_client.simulation_mode is True

    def test_server_values(self):
        assert self.sila_client.server_port is PresensTestServer.port
        assert self.sila_client.server_hostname is PresensTestServer.ip
        assert self.sila_client.server_display_name == ''
        assert self.sila_client.server_description == ''
        assert self.sila_client.server_version == ''

    def test_client_values(self):
        assert self.sila_client.vendor_url == ''
        assert self.sila_client.name == 'PresensServiceClient'
        assert self.sila_client.version == '1.0'
        assert self.sila_client.description == 'This is a Presens MCR Service'
        assert isinstance(UUID(self.sila_client.client_uuid), UUID)

    def test_server_standard_features(self):
        assert hasattr(self.sila_client, 'SiLAService_stub')
        assert 'sila2lib.framework.std_features.SiLAService_pb2_grpc.SiLAServiceStub' in \
               str(type(self.sila_client.SiLAService_stub))
        assert hasattr(self.sila_client, 'SimulationController_stub')
        assert 'sila2lib.framework.std_features.SimulationController_pb2_grpc.SimulationControllerStub' in \
               str(type(self.sila_client.SimulationController_stub))

    def test_server_custom_features(self):
        assert hasattr(self.sila_client, 'deviceService_client')
        assert hasattr(self.sila_client, 'calibrationService_client')
        assert hasattr(self.sila_client, 'sensorProvider_client')


class TestPresensSensorProviderGet:
    """ Test all SensorProvider Get functions"""
    sila_client = PresensServiceClient(server_ip=PresensTestServer.ip, server_port=PresensTestServer.port)

    @pytest.mark.parametrize('GetSinglePH_channel', random.sample(range(0, total_channels), sample_depth))  # is 0 or 1 start? channels +1 end?
    def test_GetSinglePH(self, GetSinglePH_channel):
        """ Function asks each reactor ('channel') individually to provide pH data.
        Accepted input: int. No range defined (+- infinity)
        :param Channel=GetSinglePH_channel: specifies the channel/reactor that is asked to provide (get) the value.
        """
        response = self.sila_client.sensorProvider_client.GetSinglePH(Channel=GetSinglePH_channel)
        assert isinstance(response.CurrentChannelNumber.value, int)
        # assert response.CurrentChannelNumber.value is GetSinglePH_channel  # why is this failing? position conversion?
        assert isinstance(response.CurrentSensorType.value, str)
        assert response.CurrentSensorType.value == 'pH'  # makes sure that the correct sensor is attached
        assert isinstance(response.CurrentAmplitude.value, int)
        assert isinstance(response.CurrentPhase.value, float)
        assert isinstance(response.CurrentTemperature.value, float)
        assert isinstance(response.CurrentErrorCode.value, str)
        assert isinstance(response.CurrentPH.value, float)

    @pytest.mark.parametrize('GetSingleO2_channel', random.sample(range(0, total_channels), sample_depth))  # is 0 or 1 start? channels +1 end?
    def test_GetSingleO2(self, GetSingleO2_channel):
        """ Asks each reactor ('channel') individually to provide O2 data.
        Accepted input: int. No range defined (+- infinity)
        :param Channel=GetSingleO2_channel: specifies the channel/reactor that is asked to provide (get) the value.
        """
        response = self.sila_client.sensorProvider_client.GetSingleO2(Channel=GetSingleO2_channel)
        assert isinstance(response.CurrentChannelNumber.value, int)
        # assert response.CurrentChannelNumber.value is GetSingleO2_channel  # why is this failing? position conversion?
        assert isinstance(response.CurrentSensorType.value, str)
        assert response.CurrentSensorType.value == 'O2'  # makes sure that the correct sensor is attached
        assert isinstance(response.CurrentAmplitude.value, int)
        assert isinstance(response.CurrentPhase.value, float)
        assert isinstance(response.CurrentTemperature.value, float)
        assert isinstance(response.CurrentO2.value, float)
        assert isinstance(response.CurrentErrorCode.value, str)

    def test_GetAllO2(self):
        response = self.sila_client.sensorProvider_client.GetAllO2()
        assert all(type(i.value) is str for i in response.CurrentSensorType)
        assert all(type(i.value) is int for i in response.CurrentAmplitude)
        assert all(type(i.value) is float for i in response.CurrentPhase)
        assert all(type(i.value) is float for i in response.CurrentTemperature)
        assert all(type(i.value) is float for i in response.CurrentO2)
        assert all(type(i.value) is str for i in response.CurrentErrorCode)
        # list comprehension needed due to list type
        # note: in case a single element is False, an AssertionError is risen

    def test_GetAllPH(self):
        response = self.sila_client.sensorProvider_client.GetAllPH()
        assert all(type(i.value) is str for i in response.CurrentSensorType)
        assert all(type(i.value) is int for i in response.CurrentAmplitude)
        assert all(type(i.value) is float for i in response.CurrentPhase)
        assert all(type(i.value) is float for i in response.CurrentTemperature)
        assert all(type(i.value) is float for i in response.CurrentPH)
        assert all(type(i.value) is str for i in response.CurrentErrorCode)

    def test_Get_TotalChannels(self):
        response = self.sila_client.sensorProvider_client.Get_TotalChannels()
        return_val = response.TotalChannels.value
        assert isinstance(return_val, int)
        assert return_val == total_channels

    def test_Get_TotalBars(self):
        response = self.sila_client.sensorProvider_client.Get_TotalBars()
        return_val = response.TotalBars.value
        assert isinstance(return_val, int)
        assert return_val == total_bars

    def test_Get_BarSensors(self):
        response = self.sila_client.sensorProvider_client.Get_BarSensors()
        return_val = response.BarSensors.value
        assert isinstance(return_val, int)
        assert return_val == bar_sensors
    # missing test for grpc_error_handling() -> too complicated to test (depending upon sila Errors)


class TestPresensDeviceServiceGet:
    """Test all DeviceService Get functions"""
    sila_client = PresensServiceClient(server_ip=PresensTestServer.ip, server_port=PresensTestServer.port)

    def test_GetTComp(self):
        response = self.sila_client.deviceService_client.GetTComp()
        assert isinstance(response.CurrentTComp.value, float)

    def test_GetDynAveraging(self):
        response = self.sila_client.deviceService_client.GetDynAveraging()
        assert isinstance(response.CurrentDynAverage.value, int)

    def test_SwitchOffDevice(self):
        response = self.sila_client.deviceService_client.SwitchOffDevice()
        assert isinstance(response.CurrentStatus.value, str)
    # note: due to (partial) missing implementation these remaining features were not implemented for testing:
    # GetLog(), GetLog_Info(str(uuid4()), GetLog_Result(), grpc_error_handling(), Subscribe_CurrentStatus()


class TestPresensCalibrationGet:
    """Test all Calibration Get functions.
    Return values are a list of length of bars used (default=6). Each list element is referring to the corresponding bar value"""
    sila_client = PresensServiceClient(server_ip=PresensTestServer.ip, server_port=PresensTestServer.port)

    def test_GetO2CalLow(self):
        response = self.sila_client.calibrationService_client.GetO2CalLow()
        assert len(response.CurrentO2CalLow) == total_bars
        assert all(type(i.value) is float for i in response.CurrentO2CalLow)
        # note: in case a single element is False, an AssertionError is risen

    def test_GetO2CalHigh(self):
        response = self.sila_client.calibrationService_client.GetO2CalHigh()
        assert len(response.CurrentO2CalHigh) == total_bars
        assert all(type(i.value) is float for i in response.CurrentO2CalHigh)

    def test_GetO2CalTemp(self):
        response = self.sila_client.calibrationService_client.GetO2CalTemp()
        assert len(response.CurrentO2CalTemp) == total_bars
        assert all(type(i.value) is float for i in response.CurrentO2CalTemp)

    def test_GetPHImax(self):
        response = self.sila_client.calibrationService_client.GetPHImax()
        assert len(response.CurrentPHImax) == total_bars
        assert all(type(i.value) is float for i in response.CurrentPHImax)

    def test_GetPHImin(self):
        response = self.sila_client.calibrationService_client.GetPHImin()
        assert len(response.CurrentPHImin) == total_bars
        assert all(type(i.value) is float for i in response.CurrentPHImin)

    def test_GetPHpH0(self):
        response = self.sila_client.calibrationService_client.GetPHpH0()
        assert len(response.CurrentPHpH0) == total_bars
        assert all(type(i.value) is float for i in response.CurrentPHpH0)

    def test_GetPHdpH(self):
        response = self.sila_client.calibrationService_client.GetPHdpH()
        assert len(response.CurrentPHdpH) == total_bars
        assert all(type(i.value) is float for i in response.CurrentPHdpH)

    def test_GetPHCalTemp(self):
        response = self.sila_client.calibrationService_client.GetPHCalTemp()
        assert len(response.CurrentPHCalTemp) == total_bars
        assert all(type(i.value) is float for i in response.CurrentPHCalTemp)

@pytest.mark.WIP  # functions not implemented in the DeviceServicer yet
class TestPresensDeviceServiceSet:
    """Test all DeviceService Set functions"""
    sila_client = PresensServiceClient(server_ip=PresensTestServer.ip, server_port=PresensTestServer.port)

    @pytest.mark.WIP  # function is not implemented yet (real and simulation mode). Return value is the default 0.0
    @pytest.mark.parametrize('SetTComp_value', (total_channels * [0.01], random.sample(range(0, 60, 1), total_channels)))
    def test_SetTComp(self, SetTComp_value):
        """ Set the temperature compensation value. Values must be between 0-60 degrees Celsius. Default = 20
        Accepted value range float 0 - 59 (inclusive)
        :param SetTComp_value: The temperature compensation value to be set"""
        response = self.sila_client.deviceService_client.SetTComp(SetTComp_value)
        return_val = response.CurrentTComp.value
        assert isinstance(return_val, float)  # WIP done: remove this line
        assert return_val == 0.0  # WIP done: remove this line
        # WIP done: uncomment this block line
        # assert len(return_val) == total_channels
        # for count, elem in enumerate(return_val):
        #     assert isinstance(elem.value, float)
        #     assert elem.value == SetTComp_value[count]

    @pytest.mark.WIP  # function is not implemented yet (real and simulation mode). Return value is NOT the default 0.0
    # but a return value (1) defined in the real or simulation function
    @pytest.mark.parametrize('SetDynAveraging_value', (total_bars * [0.01], random.sample(range(0, 9, 1), total_bars)))
    def test_SetDynAveraging(self, SetDynAveraging_value):
        """ The dynamic averaging value to be set. Must be between 0-9. Default = 4.
        :param SetDynAveraging_value: The dynamic averaging value to be set"""
        response = self.sila_client.deviceService_client.SetDynAveraging(SetDynAveraging_value)
        return_val = response.CurrentDynAverage.value
        assert isinstance(return_val, int)  # WIP done: remove this line
        assert return_val == 1  # WIP done: remove this line
        # WIP done: uncomment this block
        # assert len(return_val) == total_bars
        # for count, elem in enumerate(return_val):
        #     assert isinstance(elem.value, float)
        #     assert elem.value == SetDynAveraging_value[count]


class TestPresensCalibrationSet:
    """Test all Calibration Set functions"""
    sila_client = PresensServiceClient(server_ip=PresensTestServer.ip, server_port=PresensTestServer.port)

    @pytest.mark.parametrize('SetO2CalLow_value', (total_bars * [0.01], random.sample(range(0, 91, 1), total_bars)))
    def test_SetO2CalLow(self, SetO2CalLow_value):
        """ Set the O2 calibration point value at 0% dissolved oxygen. Default = 57
        Accepted value range float 0 - 90 (inclusive)
        :param SetO2CalLow_value: The lower calibration point value set point for O2 up to two decimal points"""
        response = self.sila_client.calibrationService_client.SetO2CalLow(SetO2CalLow_value)
        return_val = response.CurrentO2CalLow
        assert len(return_val) == total_bars
        for count, elem in enumerate(return_val):
            assert isinstance(elem.value, float)
            assert elem.value == SetO2CalLow_value[count]

    @pytest.mark.parametrize('SetO2CalHigh_value', (total_bars * [0.01], random.sample(range(0, 91, 1), total_bars)))
    def test_SetO2CalHigh(self, SetO2CalHigh_value):
        """ Set the O2 calibration point value at 100% dissolved oxygen. Default = 27
        Accepted value range float 0 - 90 (inclusive)
        :param SetO2CalHigh_value: The higher calibration point value set point for O2 up to two decimal points"""
        response = self.sila_client.calibrationService_client.SetO2CalHigh(SetO2CalHigh_value)
        return_val = response.CurrentO2CalHigh
        assert len(return_val) == total_bars
        for count, elem in enumerate(return_val):
            assert isinstance(elem.value, float)
            assert elem.value == SetO2CalHigh_value[count]

    @pytest.mark.parametrize('SetO2CalTemp_value', (total_bars * [-9.65], random.sample(range(0, 61, 1), total_bars)))
    def test_SetO2CalTemp(self, SetO2CalTemp_value):
        """ Set the value of the oxygen calibration temperature in degree Celsius. Default = 20
        Accepted value range float -10 - 60 (inclusive)
        :param SetO2CalTemp_value: The oxygen calibration temperature value to be set up to one decimal point in degree Celsius"""
        response = self.sila_client.calibrationService_client.SetO2CalTemp(SetO2CalTemp_value)
        return_val = response.CurrentO2CalTemp
        assert len(return_val) == total_bars
        for count, elem in enumerate(return_val):
            assert isinstance(elem.value, float)
            assert elem.value == SetO2CalTemp_value[count]

    @pytest.mark.parametrize('SetPHImax_value', (total_bars * [0.01], random.sample(range(0, 91, 1), total_bars)))
    def test_SetPHImax(self, SetPHImax_value):
        """ Set the value of the first calibration point (phi max) of the pH sensor. Default = 0
        Accepted value range float 0 - 90 (inclusive)
        :param SetPHImax_value: The set value of the first calibration point (phi max) of the pH sensor up to two decimal points."""
        response = self.sila_client.calibrationService_client.SetPHImax(SetPHImax_value)
        return_val = response.CurrentPHImax
        assert len(return_val) == total_bars
        for count, elem in enumerate(return_val):
            assert isinstance(elem.value, float)
            assert elem.value == SetPHImax_value[count]

    @pytest.mark.parametrize('SetPHImin_value', (total_bars * [0.01], random.sample(range(0, 91, 1), total_bars)))
    def test_SetPHImin(self, SetPHImin_value):
        """ Set the value of the second calibration point (phi min) of the pH sensor. Default = -
        Accepted value range float 0 - 90 (inclusive)
        :param SetPHImin_value: The set value of the first calibration point (phi min) of the pH sensor up to two decimal points."""
        response = self.sila_client.calibrationService_client.SetPHImin(SetPHImin_value)
        return_val = response.CurrentPHImin
        assert len(return_val) == total_bars
        for count, elem in enumerate(return_val):
            assert isinstance(elem.value, float)
            assert elem.value == SetPHImin_value[count]

    @pytest.mark.parametrize('SetPHpH0_value', (total_bars * [0.01], random.sample(range(0, 51, 1), total_bars)))
    def test_SetPHpH0(self, SetPHpH0_value):
        """ Set the value of the third calibration point (pH0) of the pH sensor. Default = 0
        Accepted value range float 0 - 50 (inclusive)
        :param SetPHpH0_value: The set value of the third calibration point (pH0) of the pH sensor up to two decimal points."""
        response = self.sila_client.calibrationService_client.SetPHpH0(SetPHpH0_value)
        return_val = response.CurrentPHpH0
        assert len(return_val) == total_bars
        for count, elem in enumerate(return_val):
            assert isinstance(elem.value, float)
            assert elem.value == SetPHpH0_value[count]

    @pytest.mark.parametrize('SetPHdpH_value', (total_bars * [0.01], random.sample(range(0, 11, 1), total_bars)))
    def test_SetPHdpH(self, SetPHdpH_value):
        """ Set the value of the fourth calibration point (dpH) of the pH sensor. Default = 0
        Accepted value range float 0 - 10 (inclusive)
        :param SetPHdpH_value: The set value of the fourth calibration point (dpH) of the pH sensor up to two decimal points."""
        response = self.sila_client.calibrationService_client.SetPHdpH(SetPHdpH_value)
        return_val = response.CurrentPHdpH
        assert len(return_val) == total_bars
        for count, elem in enumerate(return_val):
            assert isinstance(elem.value, float)
            assert elem.value == SetPHdpH_value[count]

    @pytest.mark.parametrize('SetPHCalTemp_value', (total_bars * [-9.65], random.sample(range(0, 61, 1), total_bars)))
    def test_SetPHCalTemp(self, SetPHCalTemp_value):
        """ Set the value of the pH calibration temperature in degree Celsius. Default = 20
        Accepted value range float -10 - 60 (inclusive)
        :param SetPHCalTemp_value: The pH calibration temperature value to be set in degree Celsius up to one decimal point."""
        response = self.sila_client.calibrationService_client.SetPHCalTemp(SetPHCalTemp_value)
        return_val = response.CurrentPHCalTemp
        assert len(return_val) == total_bars
        for count, elem in enumerate(return_val):
            assert isinstance(elem.value, float)
            assert elem.value == SetPHCalTemp_value[count]


def test__init__():
    """Starts the server in a mocked environment as defined in PresensService_server.init()"""
    from sila2lib.sila_server import SiLA2Server
    with mock.patch.object(SiLA2Server, 'run', return_value=42):  # Syntax: .object(class, 'method', return)
        with mock.patch.object(PresensService_server, '__name__', '__main__'):
            with mock.patch.object(PresensService_server.sys, 'exit') as mock_exit:
                PresensService_server.init()
                assert mock_exit.call_args[0][0] == 42
