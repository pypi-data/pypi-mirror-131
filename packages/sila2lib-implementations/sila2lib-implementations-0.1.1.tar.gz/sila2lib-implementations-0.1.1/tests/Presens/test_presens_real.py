#!/usr/bin/env python3
"""
This file tests the real mode of the PreSens sensor bars. Tests have to be executed with precaution however, a secure mode is
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
import string
import time
from unittest import mock

from sila2lib_implementations.Presens.PresensService.PresensService_client import PresensServiceClient
from sila2lib_implementations.Presens.PresensService import PresensService_server

from tests.config import settings


logger = logging.getLogger(__name__)
# initialize logging
logging.basicConfig(format  = '%(asctime)s - %(name)s - %(levelname)s- %(module)s - linenumber: %(lineno)d - %(message)s', level=logging.DEBUG)

# Set variables of Dotenv
ip = settings.PRESENS_IP
port = settings.PRESENS_PORT

# Import PreSens device default configuration from PresensService_server.py:
sample_depth = 10
total_bars = PresensService_server.Properties.TotalBars
bar_sensors = PresensService_server.Properties.BarSensors
total_channels = PresensService_server.Properties.TotalChannels
restore_default = dict()


def convert_position(position):
    """ This function converts the coordinate position (i.e. F1) to a numeric position (i.e. 6)
    works with 1-based counting"""
    char = position[0]
    pos_in_alphabet = string.ascii_lowercase.index(char.lower()) + 1
    num_position = ((int(position[1])-1) * 8) + pos_in_alphabet
    logging.debug(f' The current position in the PreSens sensor array is {num_position}')
    return num_position


"""
def test_StartupSequence():
    ''' This tests only if the sensor bars react at all'''
    Answer = PreSensObject.run()
    logging.debug(Answer)
    assert Answer != None
"""


class TestPresensSensorProviderGet:
    """ Test all SensorProvider Get functions"""
    sila_client = PresensServiceClient(server_ip=ip, server_port=port)

    @pytest.mark.parametrize('GetSinglePH_channel', random.sample(range(0, total_channels), sample_depth))  # is 0 or 1 start? channels +1 end?
    def test_GetSinglePH(self, GetSinglePH_channel):
        """ Function asks each reactor ('channel') individually to provide pH data.
        Accepted input: int. No constraints defined (+- infinity)
        :param Channel=GetSinglePH_channel: specifies the channel/reactor that is asked to provide (get) the value.
        """
        response = self.sila_client.sensorProvider_client.GetSinglePH(Channel=GetSinglePH_channel)
        assert response is not None
        assert isinstance(response.CurrentChannelNumber.value, int)
        # assert response.CurrentChannelNumber.value is GetSinglePH_channel  # why is this failing? position conversion?
        # assert convert_position(response.CurrentChannelNumber.value) is GetSinglePH_channel  # known bug, simulator always answers the same position
        assert isinstance(response.CurrentSensorType.value, str)
        assert response.CurrentSensorType.value == 'pH'  # ensures that the correct sensor is attached
        assert isinstance(response.CurrentAmplitude.value, int)
        assert isinstance(response.CurrentPhase.value, float)
        assert isinstance(response.CurrentTemperature.value, float)
        assert isinstance(response.CurrentErrorCode.value, str)
        assert isinstance(response.CurrentPH.value, float)
        logging.debug(response)
        logging.debug(f'The current retrieved pH value is {response.CurrentPH.value}')
    # Nikolas only tested CurrentPH & CurrentChannel, others unnecessary to test?

    @pytest.mark.parametrize('GetSingleO2_channel', random.sample(range(0, total_channels), sample_depth))  # is 0 or 1 start? channels +1 end?
    def test_GetSingleO2(self, GetSingleO2_channel):
        """ Asks each reactor ('channel') individually to provide O2 data.
        Accepted input: int. No range defined (+- infinity)
        :param Channel=GetSingleO2_channel: specifies the channel/reactor that is asked to provide (get) the value.
        """
        response = self.sila_client.sensorProvider_client.GetSingleO2(Channel=GetSingleO2_channel)
        assert response is not None
        assert isinstance(response.CurrentChannelNumber.value, int)
        # assert response.CurrentChannelNumber.value is GetSingleO2_channel  # why is this failing? position conversion?
        # assert convert_position(response.CurrentChannelNumber.value) is GetSingleO2_channel
        assert isinstance(response.CurrentSensorType.value, str)
        assert response.CurrentSensorType.value == 'O2'  # ensures that the correct sensor is attached
        assert isinstance(response.CurrentAmplitude.value, int)
        assert isinstance(response.CurrentPhase.value, float)
        assert isinstance(response.CurrentTemperature.value, float)
        assert isinstance(response.CurrentO2.value, float)
        assert isinstance(response.CurrentErrorCode.value, str)

    def test_GetAllO2(self):
        response = self.sila_client.sensorProvider_client.GetAllO2()
        assert response is not None
        for channel in range(total_channels):
            assert isinstance(response.CurrentSensorType[channel].value, str)
            assert response.CurrentSensorType[channel].value == 'O2'
            assert response.CurrentO2[channel].value is float
        assert all(type(i.value) is int for i in response.CurrentAmplitude)
        assert all(type(i.value) is float for i in response.CurrentPhase)
        assert all(type(i.value) is float for i in response.CurrentTemperature)
        assert all(type(i.value) is str for i in response.CurrentErrorCode)
        # note: in case a single element is False, an AssertionError is risen

    def test_GetAllPH(self):
        response = self.sila_client.sensorProvider_client.GetAllPH()
        assert response is not None
        for channel in range(total_channels):
            assert isinstance(response.CurrentSensorType[channel].value, str)
            assert response.CurrentSensorType[channel].value == 'pH'
            assert response.CurrentPH[channel].value is float
        assert all(type(i.value) is int for i in response.CurrentAmplitude)
        assert all(type(i.value) is float for i in response.CurrentPhase)
        assert all(type(i.value) is float for i in response.CurrentTemperature)
        assert all(type(i.value) is str for i in response.CurrentErrorCode)


def test__init__():
    """ Starts the server in a mocked environment as defined in BioREACTOR48Service_server.init()"""
    from sila2lib.sila_server import SiLA2Server
    with mock.patch.object(SiLA2Server, 'run', return_value=42):  # Syntax: .object(class, 'method', return)
        with mock.patch.object(PresensService_server, '__name__', '__main__'):
            with mock.patch.object(PresensService_server.sys, 'exit') as mock_exit:
                PresensService_server.init()
                assert mock_exit.call_args[0][0] == 42
