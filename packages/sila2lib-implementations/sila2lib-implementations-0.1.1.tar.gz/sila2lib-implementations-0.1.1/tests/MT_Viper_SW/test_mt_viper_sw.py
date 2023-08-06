#!/usr/bin/env python3
"""
This file tests the simulation- or real mode of the Mettler-Toledo, MT Viper SW (Laboratory Balance).


REAL TESTS have to be executed with precaution. However, a secure mode is implemented by default that prevents breakdown
of the device due to overheating e.g.. For safe testing these steps have to be performed BEFORE test execution:
--Perform steps as usually to properly start up the device (here a cooling unit is needed)
--Connect the serial cable to device and PC (USB port favorably)

STRUCTURE:
Tests are organized in classes to logically separate the
services' features, as well as get- from set-functions. Return values are validated for data types, value range and whether
length of return values is as desired (e.g. as input values). All returns must assert "True", since the injected input
parameter range is only valid. For invalid parameter injection and error handling see:
'test_mt_viper_simulation_error.py'
Multiple executions of single test_functions are conducted via the "parametrize" functionality offered by pytest
(injection) to cover and test a wide input range.

Notes for real mode testing:
A Serial cable not attached to the PC (USB port) breaks down script execution completely.
A missing serial PC to device connection results in default return values and multiple assertion failures/test failures
since there is no handling of default values implemented.
"""

import logging
import pytest
import random
import socket
import string
from threading import (
    Thread,
    Event
)
import time
from uuid import UUID
from unittest import mock

from sila2lib_implementations.MT_Viper_SW.MT_Viper_SW_Balance_Service.MT_Viper_SW_Balance_Service_client import MT_Viper_SW_Balance_ServiceClient
from sila2lib_implementations.MT_Viper_SW.MT_Viper_SW_Balance_Service import MT_Viper_SW_Balance_Service_server

from tests.config import settings


logger = logging.getLogger(__name__)
# logging.basicConfig(format  = '%(asctime)s - %(name)s - %(levelname)s- %(module)s - linenumber: %(lineno)d - %(message)s', level=logging.DEBUG)

# Set variables of Dotenv
ip = settings.MTVIPERSW_IP
port = settings.MTVIPERSW_PORT
simulation_mode = settings.MTVIPERSW_SIMULATION_MODE


# ____________________start boilerplate__________________________________
# def wait_until_port_closes(ip: str, port: int, timeout: float = 10) -> bool:
#     """ Try to bind the socket at {ip}:{port} to check if a socket resource is available
#
#     :param ip: The ip of the host system.
#     :param port: The port of the socket.
#     :param timeout: The timeout until a connection attempt is aborted.
#     :return: False if socket is available. True if unavailable.
#     """
#
#     a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     a_socket.settimeout(timeout)
#     location = (ip, port)
#     try:
#         a_socket.connect_ex(location)
#         while a_socket.connect_ex(location) == 0:
#             return False
#     except (TimeoutError, OSError, ValueError, OverflowError, InterruptedError) as e:
#         logger.error(f'Encountered exception {e.__class__.__name__}: {e}')
#     except Exception as e:
#         logger.error(f'Encountered unknown exception {e.__class__.__name__}: {e}')
#     finally:
#         a_socket.close()
#         return True
#
#
# def wait_until_server_up(server, timeout: float = 10.0) -> bool:
#     """ Waits until the server is started sanely. Currently unimplemented on server site (server.is_healthy not available)
#
#     :param server: The server whose sanely up status has to be tested
#     :param timeout: Defined timeout at which check is aborted and error is sent
#     :return: 0 for server is up. 1 for timeout exceeded.
#     """
#     # t = 0
#     # while server.healthy is False:
#     #     if t > timeout:
#     #         return True
#     #     time.sleep(0.1)  # return error message
#     #     t += 0.1
#     # return False
#     time.sleep(10)
#
#
# # Test Server setup
# class BlueVaryTestServer(MT_Viper_SW_Balance_Service_server.MT_Viper_SW_Balance_ServiceServer):
#     """
#     Test server instance. Implementation of service until an abort event is sent
#     :param abort_event: Event that leads to the server stop
#     """
#
#     ip = settings.MTVIPERSW_IP
#     port = settings.MTVIPERSW_PORT
#     simulation_mode = settings.MTVIPERSW_SIMULATION_MODE
#
#     def __init__(self, abort_event: Event):
#         self.abort_event = abort_event
#         super().__init__(cmd_args='MT_Viper', simulation_mode=self.simulation_mode)  # why is there no , ip=self.ip, port=self.port needed?
#         # cmd_args not implemented yet
#
#     def serve(self):
#         self.run(block=False)
#         while not self.abort_event.is_set():
#             time.sleep(1)
#         self.stop_grpc_server()
#
#
# @pytest.fixture(autouse=True, scope='module')
# def setup_and_teardown_mt_viper_server():
#     """
#     Starts a server thread and tears it down automatically after the whole module is executed.
#     """
#     abort_event = Event()
#     server = BlueVaryTestServer(abort_event)
#     thread = Thread(target=server.serve, args=(), daemon=True)
#     thread.start()
#     wait_until_server_up(server)
#     logger.info('Started MT_Viper server')
#     yield thread
#     abort_event.set()
#     thread.join(timeout=10)
#     wait_until_port_closes(ip=BlueVaryTestServer.ip, port=BlueVaryTestServer.port, timeout=10)
#     if thread.is_alive:
#         logger.warning(f'MT_Viper server thread is still alive: {thread.is_alive()}')
#     logger.info('Stopped MT_Viper server')

# ____________________end boilerplate__________________________________

#
# class TestBlueVaryServerFunctionalities:
#     """
#     Basic connection test with the server. Also checks if the server was started with the correct parameters (port, ip, mode)
#     """
#     # Setup_class is meant to be used like __init__ but the latter is causing problems in pytest
#     # (cannot collect test class because it has a __init__ constructor)
#     def setup_class(cls):
#         cls.sila_client = MT_Viper_SW_Balance_ServiceClient(server_ip=BlueVaryTestServer.ip, server_port=BlueVaryTestServer.port)
#
#     def test_run_bluevary_test_server(self, setup_and_teardown_mt_viper_server):
#         logger.info(f'MT_Viper server running. Is alive: {setup_and_teardown_mt_viper_server.is_alive()}')
#         assert True
#
#     def test_connect_to_bluevary_server(self):
#         logger.info(f'Connected to client: {self.sila_client.run()}')
#         assert self.sila_client.run() is True
#
#     def test_toggle_mode(self):
#         assert self.sila_client.simulation_mode is True  # ._simulation_mode also possible
#         self.sila_client.toggleSimMode()
#         assert self.sila_client.simulation_mode is False
#
#     def test_mode_switch(self):
#         self.sila_client.switchToSimMode()
#         assert self.sila_client.simulation_mode is True
#         self.sila_client.switchToRealMode()
#         assert self.sila_client.simulation_mode is False
#         self.sila_client.switchToSimMode()
#         assert self.sila_client.simulation_mode is True
#
#     def test_server_values(self):
#         assert self.sila_client.server_port is BlueVaryTestServer.port
#         assert self.sila_client.server_hostname is BlueVaryTestServer.ip
#         assert self.sila_client.server_display_name == ''
#         assert self.sila_client.server_description == ''
#         assert self.sila_client.server_version == ''
#
#     def test_client_values(self):
#         assert self.sila_client.vendor_url == ''
#         assert self.sila_client.name == 'MT_Viper_SW_Balance_ServiceClient'
#         assert self.sila_client.version == '1.0'
#         assert self.sila_client.description == 'This is a BlueVary MCR Service'
#         assert isinstance(UUID(self.sila_client.client_uuid), UUID)
#
#     def test_server_standard_features(self):
#         assert hasattr(self.sila_client, 'SiLAService_stub')
#         assert 'sila2lib.framework.std_features.SiLAService_pb2_grpc.SiLAServiceStub' in \
#                str(type(self.sila_client.SiLAService_stub))
#         assert hasattr(self.sila_client, 'SimulationController_stub')
#         assert 'sila2lib.framework.std_features.SimulationController_pb2_grpc.SimulationControllerStub' in \
#                str(type(self.sila_client.SimulationController_stub))
#
#     def test_server_custom_features(self):
#         assert hasattr(self.sila_client, 'deviceService_client')
#         assert hasattr(self.sila_client, 'calibrationService_client')
#         assert hasattr(self.sila_client, 'sensorService_client')
""""""

# random failures are implemented (for the simulation mode at least) that are causing randomly choosen errors like
# UnderloadErrorError, InternalError etc.. These errors are not handled and result in a failure of the respective test
# function, unfortunately
class TestBalanceServiceGet:
    """ Test all BalanceService Get functions """
    sila_client = MT_Viper_SW_Balance_ServiceClient()

    def test_Get_StableWeightValue(self):
        """ Get the current stable weight value in g."""
        response = self.sila_client.balanceService_client.Get_StableWeightValue()
        assert response is not None
        assert isinstance(response.StableWeightValue.value, float)

    def test_Get_ImmediateWeightValue(self):
        response = self.sila_client.balanceService_client.Get_ImmediateWeightValue()
        assert response is not None
        assert isinstance(response.ImmediateWeightValue.StableWeightResponse.WeightValue.value, float)
        assert isinstance(response.ImmediateWeightValue.StableWeightResponse.IsStable.value, bool)

    def test_Get_TareWeightValue(self):
        """ Get the current tare weight value in g."""
        response = self.sila_client.balanceService_client.Get_TareWeightValue()
        assert response is not None
        assert isinstance(response.TareWeightValue.value, float)


class TestDeviceInformationProviderGet:
    """ Test all DeviceInformationProvider Get functions. General device information regarding firmware and hardware can be retrieved and changed within this feature. """
    sila_client = MT_Viper_SW_Balance_ServiceClient()

    def test_Get_ImplementedCommands(self):
        """ Lists all commands implemented in the present software version. All commands (MT-SICS) ordered according to level in alphabetical order."""
        response = self.sila_client.deviceInformationProvider_client.Get_ImplementedCommands()
        assert response is not None
        assert isinstance(response.ImplementedCommands.value, str)
        # 5 commands are implemented that are all named the same ImplementedCommands

    def test_Get_DeviceType(self):
        """ Lists all commands implemented in the present software version. All commands (MT-SICS) ordered according to level in alphabetical order."""
        response = self.sila_client.deviceInformationProvider_client.Get_DeviceType()
        assert response is not None
        assert isinstance(response.DeviceType.value, str)

    def test_Get_WeighingCapacity(self):
        """ Query weighing capacity. The maximum allowed balance capacity in g."""
        response = self.sila_client.deviceInformationProvider_client.Get_WeighingCapacity()
        assert response is not None
        assert isinstance(response.WeighingCapacity.value, float)

    def test_Get_FirmwareVersion(self):
        response = self.sila_client.deviceInformationProvider_client.Get_FirmwareVersion()
        assert response is not None
        assert isinstance(response.FirmwareVersion.value, str)

    def test_Get_TypeDefinitionNumber(self):
        response = self.sila_client.deviceInformationProvider_client.Get_TypeDefinitionNumber()
        assert response is not None
        assert isinstance(response.TypeDefinitionNumber.value, str)

    def test_Get_SerialNumber(self):
        response = self.sila_client.deviceInformationProvider_client.Get_SerialNumber()
        assert response is not None
        assert isinstance(response.SerialNumber.value, str)


class TestDisplayController:
    """ Test all DisplayController Get functions """
    sila_client = MT_Viper_SW_Balance_ServiceClient()

    def test_WriteToDisplay(self):
        response = self.sila_client.displayController_client.WriteToDisplay()
        assert response is not None
        assert isinstance(response, bool)

    def test_ShowWeight(self):
        """ Resets the display after using the WriteToDisplay command. The device display will show the current weight value and unit."""
        response = self.sila_client.displayController_client.ShowWeight()
        assert response is not None
        assert isinstance(response, bool)


class TestBalanceServiceSet:
    """ Test all BalanceService Set functions """
    sila_client = MT_Viper_SW_Balance_ServiceClient()

    def test_Zero(self):
        """ Set a new zero; all weight values (including tare weight) will be measured relative to this zero. After zeroing has taken place, the following values applky: tare weight = 0; net weight = (=gross weight) = 0."""
        response = self.sila_client.balanceService_client.Zero()
        assert response is not None
        assert isinstance(response.Success.value, bool)
        # 3 defined execution errors listed

    def test_ZeroImmediate(self):
        """ Set a new zero immediately, regardless of balance stability. All weight values (including tare weight) will be measured relative to this zero. After zeroing has taken place, the following values applky: tare weight = 0; net weight = (=gross weight) = 0."""
        response = self.sila_client.balanceService_client.ZeroImmediate()
        assert response is not None
        assert isinstance(response.Success.value, bool)
        assert isinstance(response.IsStable.value, bool)

    def test_Tare(self):
        """ The tare value if taring has been successfully performed. The tare weight value returned corresponds to the weight change on the balance in the unit actually set under display unit since the last zero setting."""
        response = self.sila_client.balanceService_client.Tare()
        assert response is not None
        assert isinstance(response.TareValue.value, float)
        # constraints and Units exist. what to do with them?
        # 3 defined execution errors listed

    def test_WeightValueOnChange(self):
        """ Request the current stable weight value in display unit followed by weight values after predefined minimum weight changes until the command is stopped, i.e. sends the current stable weight value followed by every load change of predefined amount of g."""
        response = self.sila_client.balanceService_client.WeightValueOnChange()
        assert response is not None
        assert isinstance(response.commandExecutionUUID.value, str)  # default
        assert isinstance(response.commandExecutionUUID.value, float)  # real

# required positional argument: 'uuid'
#     def test_WeightValueOnChange_Info(self):
#         """ Request the current stable weight value in display unit followed by weight values after predefined minimum weight changes until the command is stopped, i.e. sends the current stable weight value followed by every load change of predefined amount of g. Predefined minimum weight change in g. If no value is entered, the weight change must be at least 12.5% of the last stable weight value."""
#         response = self.sila_client.balanceService_client.WeightValueOnChange_Info()
#         assert response is not None
#         assert isinstance(response, float)

    def test_WeightValueOnChange_Result(self):
        response = self.sila_client.balanceService_client.WeightValueOnChange_Result('1')  # implement valid uuid (range)
        assert response is not None
        assert isinstance(response.WeightValue.value, float)
        assert isinstance(response.IsStable.value, bool)

    def test_PresetTareWeight(self):
        """ Preset a known tare weight value in g."""
        response = self.sila_client.balanceService_client.PresetTareWeight()
        assert response is not None
        assert isinstance(response.TareWeightValue.value, float)
        # 2 defined execution errors listed

    def test_ClearTareValue(self):
        """ The reset tare weight value in g. Is always 0."""
        response = self.sila_client.balanceService_client.ClearTareValue()
        assert response is not None
        # assert isinstance(response.TareWeightValue.value, float)

    def test_TareImmediately(self):
        """ Taring performed successfully with the stable or non-stable taring weight value  in g. The new tare value corresponds to the weight change on the balance since the last zero setting."""
        response = self.sila_client.balanceService_client.TareImmediately()
        assert response is not None
        assert isinstance(response.TareWeightValue.value, float)
        assert isinstance(response.IsStable.value, bool)
        # 4 defined execution errors listed

    def test_Subscribe_CurrentWeightValue(self):
        response = self.sila_client.balanceService_client.Subscribe_CurrentWeightValue()
        assert response is not None
        assert isinstance(response, object)


class TestDeviceInformationProviderSet:
    """ Test all DeviceInformationProvider Set functions. General device information regarding firmware and hardware can be retrieved and changed within this feature. """
    sila_client = MT_Viper_SW_Balance_ServiceClient()

    def test_Reset(self):
        """ Query the serial number of the balance terminal. The serial number agrees with that on the model plate and is different for every MT balance. If no terminal is present, the SN of the bridge is issued instead."""
        # .xml states 'confirmation has to be sent' -> implementation: no - not really
        response = self.sila_client.deviceInformationProvider_client.Reset()
        assert response is not None
        assert isinstance(response.SerialNumber.value, str)


def test__init__():
    """ Starts the server in a mocked environment as defined in MT_Viper_SW_Balance_Service_server.init()"""
    from sila2lib.sila_server import SiLA2Server
    with mock.patch.object(SiLA2Server, 'run', return_value=42):  # Syntax: .object(class, 'method', return)
        with mock.patch.object(MT_Viper_SW_Balance_Service_server, '__name__', '__main__'):
            with mock.patch.object(MT_Viper_SW_Balance_Service_server.sys, 'exit') as mock_exit:
                MT_Viper_SW_Balance_Service_server.init()
                assert mock_exit.call_args[0][0] == 42
