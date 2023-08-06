#!/usr/bin/env python3
"""
This file tests the simulation- or real mode of Blue Vary.
Blue Vary is a device to read out off-gas analytics sensor data for gas1 and gas2.
Gas concentrations [vol.-%], pressure [mbar], humidity [%], temperature[C] and absolute humidity [vol.-%] are provided.

REAL TESTS have to be executed with precaution. However, a secure mode is implemented by default that prevents breakdown
of the device due to overheating e.g.. For safe testing these steps have to be performed BEFORE test execution:
--Perform steps as usually to properly start up the device (here a cooling unit is needed)
--Connect the serial cable to device and PC (USB port favorably)

STRUCTURE:
Tests are organized in classes to logically separate the
services' features, as well as get- from set-functions. Return values are validated for data types, value range and whether
length of return values is as desired (e.g. as input values). All returns must assert "True", since the injected input
parameter range is only valid. For invalid parameter injection and error handling see:
'test_blue_vary_simulation_error.py'
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

from sila2lib_implementations.BlueVary.BlueVaryService.BlueVaryService_client import BlueVaryServiceClient
from sila2lib_implementations.BlueVary.BlueVaryService import BlueVaryService_server

from tests.config import settings


logger = logging.getLogger(__name__)
# logging.basicConfig(format  = '%(asctime)s - %(name)s - %(levelname)s- %(module)s - linenumber: %(lineno)d - %(message)s', level=logging.DEBUG)

# Set variables of Dotenv
ip = settings.BLUEVARY_IP
port = settings.BLUEVARY_PORT
simulation_mode = settings.BLUEVARY_SIMULATION_MODE


#
# # ____________________start boilerplate__________________________________
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
# class BlueVaryTestServer(BlueVaryService_server.BlueVaryServiceServer):
#     """
#     Test server instance. Implementation of service until an abort event is sent
#     :param abort_event: Event that leads to the server stop
#     """
#
#     ip = settings.BLUEVARY_IP
#     port = settings.BLUEVARY_PORT
#     simulation_mode = settings.BLUEVARY_SIMULATION_MODE
#
#     def __init__(self, abort_event: Event):
#         self.abort_event = abort_event
#         super().__init__(cmd_args='BlueVaryServiceDasgip2', ip=self.ip, port=self.port, simulation_mode=self.simulation_mode)
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
# def setup_and_teardown_bluevary_server():
#     """
#     Starts a server thread and tears it down automatically after the whole module is executed.
#     """
#     abort_event = Event()
#     server = BlueVaryTestServer(abort_event)
#     thread = Thread(target=server.serve, args=(), daemon=True)
#     thread.start()
#     wait_until_server_up(server)
#     logger.info('Started BlueVary server')
#     yield thread
#     abort_event.set()
#     thread.join(timeout=10)
#     wait_until_port_closes(ip=BlueVaryTestServer.ip, port=BlueVaryTestServer.port, timeout=10)
#     if thread.is_alive:
#         logger.warning(f'BlueVary server thread is still alive: {thread.is_alive()}')
#     logger.info('Stopped BlueVary server')
#
# # ____________________end boilerplate__________________________________
#
#
# class TestBlueVaryServerFunctionalities:
#     """
#     Basic connection test with the server. Also checks if the server was started with the correct parameters (port, ip, mode)
#     """
#     # Setup_class is meant to be used like __init__ but the latter is causing problems in pytest
#     # (cannot collect test class because it has a __init__ constructor)
#     def setup_class(cls):
#         cls.sila_client = BlueVaryServiceClient(server_ip=BlueVaryTestServer.ip, server_port=BlueVaryTestServer.port)
#
#     def test_run_bluevary_test_server(self, setup_and_teardown_bluevary_server):
#         logger.info(f'PreSens server running. Is alive: {setup_and_teardown_bluevary_server.is_alive()}')
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
#         assert self.sila_client.name == 'BlueVaryServiceClient'
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




# sila_client.Get_ImplementedFeatures()  # implement it or not?

# sometimes the implementation is missing in particular for simulation


class TestCalibrationServicer:
    """ Test all CalibrationServicer Get functions """
    sila_client = BlueVaryServiceClient(server_ip=ip, server_port=port)

    # For a good calibration ensure that device has been flushed with air 'recently')
    def test_StartCalibration(self):
        """ Used to initiate device 1-pt calibration of the off-gas sensors. Start the 1-pt calibration of the sensors """
        response = self.sila_client.CalibrationServicer_StartCalibration()
        assert response is not None
    # no test implemeted: _get_command_state?

class TestDeviceServicerGet:  # no constraints defined at all
    """ Test all DeviceServicer Get functions. General device settings of the BlueVary Off-Gas analysis device can be retrieved within this feature. """
    sila_client = BlueVaryServiceClient(server_ip=ip, server_port=port)

    def test_GetLog(self):
        """ Get the current status of the device from the state machine of the SiLA server."""
        response = self.sila_client.DeviceServicer_GetLog()
        assert response is not None
        assert isinstance(response.commandExecutionUUID.value, str)
        # .xml outdated?
        # assert isinstance(response.CurrentLogLevel, int)
        # assert isinstance(response.CurrentLogTimestamp, str)  # timestamp
        # assert isinstance(response.CurrentLogMessage, str)

    # not in .xml definition
    def test_GetLog_Info(self):
        response = self.sila_client.DeviceServicer_GetSensorInfo()
        assert response is not None
        assert isinstance(response.SensorInfo.value, str)

    # not in .xml definition
    # def test_GetLog_Result(self):
    #     response = self.sila_client.DeviceServicer_GetLog_Result(uuid=)  # what to insert for uuid?
    #     assert response is not None

    def test_GetSensorID(self):
        """ Get the sensor IDs of the gas1, gas2, pressure and humidity sensor."""
        response = self.sila_client.DeviceServicer_GetSensorID()
        assert response is not None
        assert isinstance(response.UnitID.value, int)
        assert isinstance(response.CO2ID.value, int)
        assert isinstance(response.O2ID.value, int)
        assert isinstance(response.HUMID.value, int)
        assert isinstance(response.PRESID.value, int)

    def test_GetSensorInfo(self):
        """ Get all relevant sensor information of the device."""
        response = self.sila_client.DeviceServicer_GetSensorInfo()
        assert response is not None
        # assert isinstance(response.SensorInfo.value, str)

    def test_Subscribe_CurrentStatus(self):
        response = self.sila_client.Subscribe_DeviceServicer_CurrentStatus()
        assert response is not None

# bug: implementation: default values somehow not accessible
class TestSensorServicerGet:
    """ Test all SensorServicer Get functions. Read out the off-gas analytics sensor data for gas1 and gas2.Gas concentrations [vol.-%], pressure [mbar], humidity [%], temperature[C] and absolute humidity [vol.-%] are provided.  """
    sila_client = BlueVaryServiceClient(server_ip=ip, server_port=port)

    def test_GetResults(self):
        """ Get the current gas concentrations for CO2 and O2 in [vol.-%] and the pressure readings in [mbar]. """
        response = self.sila_client.SensorServicer_GetResults()
        assert response is not None
        # assert isinstance(response.CO2.value, float)
        # assert isinstance(response.O2.value, float)
        # assert isinstance(response.Pressure.value, float)
        # DefinedExecutionErrors><Identifier>SensorInHeatUpPhase
        # Nikolas asserted here if values are in the range(0, 100) [pressure 0.5, 1.5]

    def test_GetHumidity(self):
        """ Get the current humidity [%], temperature [C] and absolute humidity [vol.-%]."""
        response = self.sila_client.SensorServicer_GetHumidity()
        assert response is not None
        # assert isinstance(response.Humidity.value, float)
        # assert isinstance(response.Temperature.value, float)
        # assert isinstance(response.AbsoluteHumidity.value, float)
        # DefinedExecutionErrors><Identifier>SensorInHeatUpPhase
        # Nikolas asserted here if values are in the range(0, 100) [pressure 0.5, 1.5]


def test__init__():
    """ Starts the server in a mocked environment as defined in BlueVaryService_server.init()"""
    from sila2lib.sila_server import SiLA2Server
    with mock.patch.object(SiLA2Server, 'run', return_value=42):  # Syntax: .object(class, 'method', return)
        with mock.patch.object(BlueVaryService_server, '__name__', '__main__'):
            with mock.patch.object(BlueVaryService_server.sys, 'exit') as mock_exit:
                BlueVaryService_server.init()
                assert mock_exit.call_args[0][0] == 42
