#!/usr/bin/env python3
"""
This file tests the real mode of the BioREACTOR48. Tests have to be executed with precaution however, a secure mode is
implemented by default that prevents breakdown of the device due to overheating e.g.. For safe testing these steps have to be
performed BEFORE test execution:
--Perform steps as usually to properly start up the device (here a cooling unit is needed)
--Connect the serial cable to device and PC (USB port favorably)
Tests are organized in classes to logically separate the services' features, as well as get from set functions.
Return values are validated for data types, value range and whether length of return values is as desired (e.g. as input
 values). All returns must assert "True", since the injected input parameter range is only valid.
Multiple executions of single test_functions are conducted via the "parametrize" functionality offered by pytest
(injection) to cover and test a wide input range.
notes:
A Serial cable not attached to the PC (USB port) breaks down script execution completely.
A missing serial PC to device connection results in default return values and multiple assertion failures/test failures
since there is no handling of default values implemented.
"""

import logging
import pytest
import random
import time
from unittest import mock

from sila2lib_implementations.BioREACTOR48.BioREACTOR48Service.BioREACTOR48Service_client import BioREACTOR48ServiceClient
from sila2lib_implementations.BioREACTOR48.BioREACTOR48Service import BioREACTOR48Service_server

from tests.config import settings


logger = logging.getLogger(__name__)

# Set variables of Dotenv
ip = settings.BIOREACTOR48_IP
port = settings.BIOREACTOR48_PORT

total_bars = BioREACTOR48Service_server.Properties.TotalBars
bar_sensors = BioREACTOR48Service_server.Properties.BarSensors
total_channels = BioREACTOR48Service_server.Properties.TotalChannels
restore_default = dict()


# Frequency and range of test executions
iterations = 2
# todo: ask Nikolas if values between [25, 50, 75, 100] can be covered +++ # is rpm_range a reasonable value? -> exception rpm too high
power_ranger = range(0, 101, 1)  # int input needed in % # range (0-100) NOT implemented
power_sampling = random.sample(power_ranger, iterations)
rpm_range = range(100, 4000, 100)  # int input needed # NO range implemented # return type: list(int)
rpm_sampling = random.sample(rpm_range, iterations)


@pytest.fixture(scope='function')
def setup_and_teardown():
    """
    Method to test the MotoServicer. Stirrer is actually turning, keep in mind to have the cooling unit connected.
    After the test, the stirrer is stopped and the default/previous values are loaded finally. This ensures impact less
    testing towards the device and their users
    """
    sila_client = BioREACTOR48ServiceClient(server_ip=ip, server_port=port)
    sila_client.MotorServicer_SetPower(100)
    sila_client.MotorServicer_SetRPM(2800)  # real stirrer motion is only conducted once at 2800 rpm
    yield
    sila_client.MotorServicer_StopStirrer()
    # restores the 'before test' settings
    sila_client.MotorServicer_SetPower(restore_default.get('GetPower'))
    sila_client.MotorServicer_SetRPM(restore_default.get('GetRPM'))


class TestBioREACTORServerFunctionalities:
    """
    Basic connection test with the server. Also checks if server was started with the correct parameters (ip, port, mode)
    """
    def setup_class(cls):
        cls.sila_client = BioREACTOR48ServiceClient(server_ip=ip, server_port=port)
        # all bugs if server is not started manually in the background

    def test_ensure_real_mode(self):
        sim_mode = self.sila_client.simulation_mode
        assert isinstance(sim_mode, bool)
        try:
            assert sim_mode is False
        except:
            logger.info('Fatal: server started in the wrong mode (simulation instead of real)')
            self.sila_client.switchToRealMode()

    def test_toggle_mode(self):
        sim_mode = self.sila_client.simulation_mode
        assert sim_mode is False
        self.sila_client.toggleSimMode()
        sim_mode = self.sila_client.simulation_mode
        assert sim_mode is True

    def test_mode_switch(self):
        self.sila_client.switchToRealMode()
        sim_mode = self.sila_client.simulation_mode
        assert sim_mode is False  # bug: none is false
        self.sila_client.switchToSimMode()
        sim_mode = self.sila_client.simulation_mode
        assert sim_mode is True
        self.sila_client.switchToRealMode()
        sim_mode = self.sila_client.simulation_mode
        try:
            assert sim_mode is False
        except:
            logger.info('Fatal: server is currently in the wrong simulation mode')

    def test_server_values(self):
        assert self.sila_client.server_port is port
        assert self.sila_client.server_hostname is ip


class TestBioREACTORDeviceServicerGet:
    """Test all DeviceServicer Get functions"""
    sila_client = BioREACTOR48ServiceClient(server_ip=ip, server_port=port)

    def test_GetDeviceStatus(self):
        response = self.sila_client.DeviceServicer_GetDeviceStatus()
        assert response is not None
        status = response.Status.value
        mode = response.Mode.value
        assert isinstance(status, str)
        assert isinstance(mode, str)
        if status == 'default string':
            logger.error('Serial cable probably not connected or detected. All tests will return the pre-defined default'
                         'values that are causing some tests to fail since string manipulation will fail e.g.')
        else:
            assert status == 'OK'
            assert mode == 'REM' or mode == 'OFF'

    # @pytest.mark.skip
    def test_DeviceServicer_GetReactorStatus(self):
        """A random failure is implemented in the simulation and/or real implementation for DeviceServicer_GetReactorStatus().
        Therefore the assertion sometimes is false and the execution stopped. Uncomment '@pytest.mark.skip' to skip this test."""
        response = self.sila_client.DeviceServicer_GetReactorStatus()
        assert response is not None
        return_val = response.ReactorStatus
        assert len(return_val) == total_channels  # return real_value and default
        for count, i in enumerate(return_val):
            if i.value is None:
                logger.info('reactor status unavailable for reactor number: ' + str(count + 1))
            else:
                assert i.value is True
        logger.info(return_val)
        # return_val is either true or none (false = none)

    @pytest.mark.unimplemented
    def test_DeviceServicer_GetBarNumber(self):
        response = self.sila_client.Get_DeviceServicer_BarNumber()
        assert response is not None
        return_val = response.BarNumber.value
        assert response is not None
        assert isinstance(return_val, int)
        assert return_val == total_bars

    @pytest.mark.unimplemented
    def test_DeviceServicer_GetBarReactors(self):
        response = self.sila_client.Get_DeviceServicer_BarReactors()
        assert response is not None
        return_val = response.BarReactors.value
        assert response is not None
        assert isinstance(return_val, int)
        assert return_val == bar_sensors

    @pytest.mark.unimplemented
    def test_DeviceServicer_GetTotalReactors(self):
        response = self.sila_client.Get_DeviceServicer_TotalReactors()
        assert response is not None
        return_val = response.TotalReactors.value
        assert response is not None
        assert isinstance(return_val, int)
        assert return_val == total_channels


class TestBioREACTORMotorServicerGet:
    """Test all MotorServicer Get functions"""
    sila_client = BioREACTOR48ServiceClient(server_ip=ip, server_port=port)

    def test_GetPower(self):
        response = self.sila_client.MotorServicer_GetPower()
        assert response is not None
        return_val = response.CurrentPower.value
        assert isinstance(return_val, int)
        assert return_val in power_ranger
        restore_default['GetPower'] = return_val

    def test_GetRPM(self):
        response = self.sila_client.MotorServicer_GetRPM()
        assert response is not None
        return_val = response.CurrentRPM.value
        assert isinstance(return_val, int)
        assert return_val in rpm_range
        restore_default['GetRPM'] = return_val


class TestBioREACTORMotorServicerSet:
    """Test all MotorServicer Set functions"""
    sila_client = BioREACTOR48ServiceClient(server_ip=ip, server_port=port)

    # Note: stirrer is not supposed to move
    @pytest.mark.parametrize("RPM_value", rpm_sampling)
    def test_SetRPM(self, RPM_value):
        response = self.sila_client.MotorServicer_SetRPM(RPM_value)
        assert response is not None
        # string manipulation to extract plain rpm value
        curr_rpm = response.CurrentStatus.value.split('_')
        curr_rpm = curr_rpm[1][:-3]
        assert float(curr_rpm) == RPM_value

    # Note: stirrer is not supposed to move
    @pytest.mark.parametrize("power_value", power_sampling)
    def test_SetPower(self, power_value):
        response = self.sila_client.MotorServicer_SetPower(power_value)
        assert response is not None
        logging.debug(response)
        curr_power = response.CurrentStatus.value.split('_')
        curr_power = curr_power[-2][5:]
        assert float(curr_power) == power_value

    # Note: stirrer is actually stirring here, make sure the cooling is connected and switched 'on'
    @pytest.mark.real_unsafe
    def test_StirrerControl(self, setup_and_teardown):
        response = self.sila_client.MotorServicer_StartStirrer()
        time.sleep(5)
        assert response is not None


def test__init__():
    """Starts the server in a mocked environment as defined in BioREACTOR48Service_server.init()"""
    from sila2lib.sila_server import SiLA2Server
    with mock.patch.object(SiLA2Server, 'run', return_value=42):  # Syntax: .object(class, 'method', return)
        with mock.patch.object(BioREACTOR48Service_server, '__name__', '__main__'):
            with mock.patch.object(BioREACTOR48Service_server.sys, 'exit') as mock_exit:
                BioREACTOR48Service_server.init()
                assert mock_exit.call_args[0][0] == 42
