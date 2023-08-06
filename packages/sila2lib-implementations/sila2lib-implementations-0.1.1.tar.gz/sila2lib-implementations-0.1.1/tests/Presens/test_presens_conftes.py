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
from unittest import mock

from sila2lib_implementations.Presens.PresensService.PresensService_client import PresensServiceClient
from sila2lib_implementations.Presens.PresensService import PresensService_server

from tests.config import settings


logger = logging.getLogger(__name__)

# Import PreSens device default configuration from PresensService_server.py:
total_bars = PresensService_server.Properties.TotalBars
bar_sensors = PresensService_server.Properties.BarSensors
total_channels = PresensService_server.Properties.TotalChannels

# temporary
ip = settings.PRESENS_IP
port = settings.PRESENS_PORT


"""
# # # test setup and teardown for presens server
# @pytest.mark.parametrize('server', ['presens'])
# @pytest.mark.usefixtures("setup_and_teardown_server")  # located in conftest.py
# def test_run_presens_test_server(setup_and_teardown_server):
#     logger.info(f'PreSens server running. Is alive: {setup_and_teardown_server.is_alive()}')
#     assert True
#
# @pytest.mark.parametrize('server', ['presens'])
# @pytest.mark.usefixtures("test_server_functionality")  # located in conftest.py
# def test_run_presens_test_server():
#     logger.info('Presens server tests started')
#     print('Presens server tests started')
#     assert True

# def test_server_functionality():
#     import inspect
#     from tests import conftest
#     f = conftest.TestServerFunctionalities()
#     attrs = (getattr(f, name) for name in dir(f))
#     methods = filter(inspect.ismethod, attrs)
#     for method in methods:
#         try:
#             method()
#         except TypeError as e:
#             logger.error(f'Encountered exception {e.__class__.__name__}: {e}. Server tests not started')


# @pytest.mark.usefixtures("TestServerFunctionalities")  # class fixtures are not supported yet
# walk around - try to execute all functions of the class manually:
# from tests import conftest
# def test_function_caller():
#     a = conftest.TestServerFunctionalities()
#     method_list = [method for method in dir(conftest.TestServerFunctionalities) if method.startswith('__') is False]
#     method_list = method_list[1:]  # exclude function_caller itself
#     for func_name in method_list:
#         a.function_caller(func_name)

# # @pytest.mark.usefixtures("TestServerFunctionalities")  # class fixtures are not supported yet
# # walk around - with class decorators:
# from tests import conftest
# @conftest.TestServerFunctionalities('presens')  # class decorator
# def test_function_caller():
#     a = conftest.TestServerFunctionalities
#     method_list = [method for method in dir(conftest.TestServerFunctionalities) if method.startswith('__') is False]
#     for func in method_list:
#         exec('a.'+func)
#
# conftest.TestServerFunctionalities('presens')(test_function_caller)
# # do i need to implement __call__ and wrapper in conftest.py?
"""
# executes server tests centralized
import inspect
from tests.test_server import TestServerFunctionalities
# service_server_assignment(server)
server = 'Presens'
f = TestServerFunctionalities()
attrs = (getattr(f, name) for name in dir(f))
methods = filter(inspect.ismethod, attrs)
for j, method in enumerate(methods):
    if j < 1:  # pass a parameter to the __init__ (required)
        try:
            method(server)
        except TypeError as e:
            logger.error(f'Encountered exception {e.__class__.__name__}: {e}. Server tests not started')
    else:
        try:
            method()
        except TypeError as e:
            logger.error(f'Encountered exception {e.__class__.__name__}: {e}. Server tests not started')


@pytest.mark.parametrize('server', ['presens'])
@pytest.mark.usefixtures("setup_and_teardown_server")
class TestPresensSensorProviderGet:
    """ Test all SensorProvider Get functions"""
    sila_client = PresensServiceClient(server_ip=ip, server_port=port)

    # todo: sometimes random bug: Failed to pick subchannel, binascii.Error
    # caused with introduction of Channel param
    @pytest.mark.parametrize('GetSinglePH_value', (1, 2))
    def test_GetSinglePH(self, GetSinglePH_value):
        response = self.sila_client.sensorProvider_client.GetSinglePH(Channel=GetSinglePH_value)
        assert isinstance(response.CurrentChannelNumber.value, int)
        assert isinstance(response.CurrentSensorType.value, str)
        assert isinstance(response.CurrentAmplitude.value, int)
        assert isinstance(response.CurrentPhase.value, float)
        assert isinstance(response.CurrentTemperature.value, float)
        assert isinstance(response.CurrentErrorCode.value, str)
        assert isinstance(response.CurrentPH.value, float)

    @pytest.mark.parametrize('GetSingleO2_value', (1, 2))
    def test_GetSingleO2(self, GetSingleO2_value):
        response = self.sila_client.sensorProvider_client.GetSingleO2(Channel=GetSingleO2_value)
        assert isinstance(response.CurrentChannelNumber.value, int)
        assert isinstance(response.CurrentSensorType.value, str)
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
        # list comprehension needed due to type(list)
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
    sila_client = PresensServiceClient(server_ip=ip, server_port=port)

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
    """Test all Calibration Get functions"""
    sila_client = PresensServiceClient(server_ip=ip, server_port=port)

    def test_GetO2CalLow(self):
        response = self.sila_client.calibrationService_client.GetO2CalLow()
        assert all(type(i.value) is float for i in response.CurrentO2CalLow)
        # note: in case a single element is False, an AssertionError is risen

    def test_GetO2CalHigh(self):
        response = self.sila_client.calibrationService_client.GetO2CalHigh()
        assert all(type(i.value) is float for i in response.CurrentO2CalHigh)

    def test_GetO2CalTemp(self):
        response = self.sila_client.calibrationService_client.GetO2CalTemp()
        assert all(type(i.value) is float for i in response.CurrentO2CalTemp)

    def test_GetPHImax(self):
        response = self.sila_client.calibrationService_client.GetPHImax()
        assert all(type(i.value) is float for i in response.CurrentPHImax)

    def test_GetPHImin(self):
        response = self.sila_client.calibrationService_client.GetPHImin()
        assert all(type(i.value) is float for i in response.CurrentPHImin)

    def test_GetPHpH0(self):
        response = self.sila_client.calibrationService_client.GetPHpH0()
        assert all(type(i.value) is float for i in response.CurrentPHpH0)

    def test_GetPHdpH(self):
        response = self.sila_client.calibrationService_client.GetPHdpH()
        assert all(type(i.value) is float for i in response.CurrentPHdpH)

    def test_GetPHCalTemp(self):
        response = self.sila_client.calibrationService_client.GetPHCalTemp()
        assert all(type(i.value) is float for i in response.CurrentPHCalTemp)


@pytest.mark.parametrize('server', ['presens'])  # setup and teardown again for the setters
@pytest.mark.usefixtures("setup_and_teardown_server")
@pytest.mark.WIP  # functions not implemented in DeviceServicer yet
class TestPresensDeviceServiceSet:
    """Test all DeviceService Set functions"""
    sila_client = PresensServiceClient(server_ip=ip, server_port=port)

    @pytest.mark.WIP  # function is not implemented yet (real and simulation mode). Return value is the default 0.0
    @pytest.mark.parametrize('SetTComp_value', (total_channels * [0.01], random.sample(range(0, 60, 1), total_channels)))
    # accepted value range float 0 - 59 (inclusive)
    def test_SetTComp(self, SetTComp_value):
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
    # but a return value defined in the real or simulation function
    @pytest.mark.parametrize('SetDynAveraging_value', (total_bars * [0.01], random.sample(range(0, 9, 1), total_bars)))
    # accepted value range float 0 - 9 (inclusive)
    def test_SetDynAveraging(self, SetDynAveraging_value):
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
    sila_client = PresensServiceClient(server_ip=ip, server_port=port)

    @pytest.mark.parametrize('SetO2CalLow_value', (total_bars * [0.01], random.sample(range(0, 91, 1), total_bars)))
    # accepted value range float 0 - 90 (inclusive)
    def test_SetO2CalLow(self, SetO2CalLow_value):
        response = self.sila_client.calibrationService_client.SetO2CalLow(SetO2CalLow_value)
        return_val = response.CurrentO2CalLow
        assert len(return_val) == total_bars
        for count, elem in enumerate(return_val):
            assert isinstance(elem.value, float)
            assert elem.value == SetO2CalLow_value[count]

    @pytest.mark.parametrize('SetO2CalHigh_value', (total_bars * [0.01], random.sample(range(0, 91, 1), total_bars)))
    # accepted value range float 0 - 90 (inclusive)
    def test_SetO2CalHigh(self, SetO2CalHigh_value):
        response = self.sila_client.calibrationService_client.SetO2CalHigh(SetO2CalHigh_value)
        return_val = response.CurrentO2CalHigh
        assert len(return_val) == total_bars
        for count, elem in enumerate(return_val):
            assert isinstance(elem.value, float)
            assert elem.value == SetO2CalHigh_value[count]

    @pytest.mark.parametrize('SetO2CalTemp_value', (total_bars * [-9.65], random.sample(range(0, 61, 1), total_bars)))
    # accepted value range float -10 - 60 (inclusive)
    def test_SetO2CalTemp(self, SetO2CalTemp_value):
        response = self.sila_client.calibrationService_client.SetO2CalTemp(SetO2CalTemp_value)
        return_val = response.CurrentO2CalTemp
        assert len(return_val) == total_bars
        for count, elem in enumerate(return_val):
            assert isinstance(elem.value, float)
            assert elem.value == SetO2CalTemp_value[count]

    @pytest.mark.parametrize('SetPHImax_value', (total_bars * [0.01], random.sample(range(0, 91, 1), total_bars)))
    # accepted value range float 0 - 90 (inclusive)
    def test_SetPHImax(self, SetPHImax_value):
        response = self.sila_client.calibrationService_client.SetPHImax(SetPHImax_value)
        return_val = response.CurrentPHImax
        assert len(return_val) == total_bars
        for count, elem in enumerate(return_val):
            assert isinstance(elem.value, float)
            assert elem.value == SetPHImax_value[count]

    @pytest.mark.parametrize('SetPHImin_value', (total_bars * [0.01], random.sample(range(0, 91, 1), total_bars)))
    # accepted value range float 0 - 90 (inclusive)
    def test_SetPHImin(self, SetPHImin_value):
        response = self.sila_client.calibrationService_client.SetPHImin(SetPHImin_value)
        return_val = response.CurrentPHImin
        assert len(return_val) == total_bars
        for count, elem in enumerate(return_val):
            assert isinstance(elem.value, float)
            assert elem.value == SetPHImin_value[count]

    @pytest.mark.parametrize('SetPHpH0_value', (total_bars * [0.01], random.sample(range(0, 51, 1), total_bars)))
    # accepted value range float 0 - 50 (inclusive)
    def test_SetPHpH0(self, SetPHpH0_value):
        response = self.sila_client.calibrationService_client.SetPHpH0(SetPHpH0_value)
        return_val = response.CurrentPHpH0
        assert len(return_val) == total_bars
        for count, elem in enumerate(return_val):
            assert isinstance(elem.value, float)
            assert elem.value == SetPHpH0_value[count]

    @pytest.mark.parametrize('SetPHdpH_value', (total_bars * [0.01], random.sample(range(0, 11, 1), total_bars)))
    # accepted value range float 0 - 10 (inclusive)
    def test_SetPHdpH(self, SetPHdpH_value):
        response = self.sila_client.calibrationService_client.SetPHdpH(SetPHdpH_value)
        return_val = response.CurrentPHdpH
        assert len(return_val) == total_bars
        for count, elem in enumerate(return_val):
            assert isinstance(elem.value, float)
            assert elem.value == SetPHdpH_value[count]

    @pytest.mark.parametrize('SetPHCalTemp_value', (total_bars * [-9.65], random.sample(range(0, 61, 1), total_bars)))
    # accepted value range float -10 - 60 (inclusive)
    def test_SetPHCalTemp(self, SetPHCalTemp_value):
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
