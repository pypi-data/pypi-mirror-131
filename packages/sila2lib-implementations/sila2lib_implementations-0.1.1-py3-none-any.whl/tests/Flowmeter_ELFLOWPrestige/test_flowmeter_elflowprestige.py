#!/usr/bin/env python3
"""
This file tests the simulation- or real mode of Bronkhorst, El-Flow Prestige (Flowmeter).
EL-FLOW Prestige is the next generation of Bronkhorst Mass Flow Meters/ Controllers using the latest, highly accurate, thermal by-pass sensor technology and featuring excellent control characteristics

REAL TESTS have to be executed with precaution. However, a secure mode is implemented by default that prevents breakdown
of the device due to overheating e.g.. For safe testing these steps have to be performed BEFORE test execution:
--Perform steps as usually to properly start up the device (here a cooling unit is needed)
--Connect the serial cable to device and PC (USB port favorably)

STRUCTURE:
Tests are organized in classes to logically separate the
services' features, as well as get- from set-functions. Return values are validated for data types, value range and whether
length of return values is as desired (e.g. as input values). All returns must assert "True", since the injected input
parameter range is only valid. For invalid parameter injection and error handling see:
'test_flowmeter_simulation_error.py'
Multiple executions of single test_functions are conducted via the "parametrize" functionality offered by pytest
(injection) to cover and test a wide input range.

Notes for real mode testing:
A Serial cable not attached to the PC (USB port) breaks down script execution completely.
A missing serial PC to device connection results in default return values and multiple assertion failures/test failures
since there is no handling of default values implemented.
"""

# Real vs. Sim issue: Real has no default values defined but sim_mode is not implemented so no assertion test possible at all :/
# todo: No simulation_mode implemented yet for the BlueVary?
# ERROR:root:gRPC Error: Simulation Mode not implemented ! -> the real mode doesnt want to start. How to do that?

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

from sila2lib_implementations.Flowmeter_ELFLOWPrestige.FlowmeterElflowPrestigeService.FlowmeterElflowPrestigeService_client import FlowmeterElflowPrestigeServiceClient
from sila2lib_implementations.Flowmeter_ELFLOWPrestige.FlowmeterElflowPrestigeService import FlowmeterElflowPrestigeService_server

from tests.config import settings


logger = logging.getLogger(__name__)
# logging.basicConfig(format  = '%(asctime)s - %(name)s - %(levelname)s- %(module)s - linenumber: %(lineno)d - %(message)s', level=logging.DEBUG)

# Set variables of Dotenv
ip = settings.FLOWMETER_IP
port = settings.FLOWMETER_PORT
simulation_mode = settings.FLOWMETER_SIMULATION_MODE

# test condition definition
sample_depth = 2
restore_default = dict()
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
# class FlowmeterTestServer(FlowmeterElflowPrestigeService_server.FlowmeterElflowPrestigeServiceServer):
#     """
#     Test server instance. Implementation of service until an abort event is sent
#     :param abort_event: Event that leads to the server stop
#     """
# 
#     ip = settings.FLOWMETER_IP
#     port = settings.FLOWMETER_PORT
#     simulation_mode = settings.FLOWMETER_SIMULATION_MODE
# 
#     def __init__(self, abort_event: Event):
#         self.abort_event = abort_event
#         super().__init__(cmd_args='Flowmeter', ip=self.ip, port=self.port, simulation_mode=self.simulation_mode)
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
# def setup_and_teardown_flowmeter_server():
#     """
#     Starts a server thread and tears it down automatically after the whole module is executed.
#     """
#     abort_event = Event()
#     server = FlowmeterTestServer(abort_event)
#     thread = Thread(target=server.serve, args=(), daemon=True)
#     thread.start()
#     wait_until_server_up(server)
#     logger.info('Started Flowmeter server')
#     yield thread
#     abort_event.set()
#     thread.join(timeout=10)
#     wait_until_port_closes(ip=FlowmeterTestServer.ip, port=FlowmeterTestServer.port, timeout=10)
#     if thread.is_alive:
#         logger.warning(f'Flowmeter server thread is still alive: {thread.is_alive()}')
#     logger.info('Stopped Flowmeter server')
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
#         cls.sila_client = FlowmeterElflowPrestigeServiceClient(server_ip=FlowmeterTestServer.ip, server_port=FlowmeterTestServer.port)
# 
#     def test_run_bluevary_test_server(self, setup_and_teardown_flowmeter_server):
#         logger.info(f'Flowmeter server running. Is alive: {setup_and_teardown_flowmeter_server.is_alive()}')
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
#         assert self.sila_client.server_port is FlowmeterTestServer.port
#         assert self.sila_client.server_hostname is FlowmeterTestServer.ip
#         assert self.sila_client.server_display_name == ''
#         assert self.sila_client.server_description == ''
#         assert self.sila_client.server_version == ''
# 
#     def test_client_values(self):
#         assert self.sila_client.vendor_url == ''
#         assert self.sila_client.name == 'FlowmeterElflowPrestigeServiceClient'
#         assert self.sila_client.version == '1.0'
#         assert self.sila_client.description == 'This is a Flowmeter MCR Service'
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


# todo: test the 'teardown' real mode without device is failing due to TypeError: object of type int/float has no len()
# backup real default data before in case my method fails
@pytest.fixture(scope='function')
def teardown_restore_default():
    """ Restores the default values to gain back the pre-test state. """
    if simulation_mode is False:
        sila_client = FlowmeterElflowPrestigeServiceClient(server_ip=ip, server_port=port)
        for key, value in restore_default.items():
            key = key.replace('Get', 'Set')  # convert get to set call
            exec('sila_client.' + key + '(' + str(value) + ')')
            # todo: Values are actually not set and still default are there??
            # try 'set' value = [i+2 for i in value] and 'get' to see that its just default values again
            # is there a separate/general set needed for real execution, like start?


class TestDeviceServiceGet:
    """ Test all DeviceService Get functions. Allows full control of the device features of the Flowmeter."""
    sila_client = FlowmeterElflowPrestigeServiceClient(server_ip=ip, server_port=port)

    def test_GetValveOutput(self):
        """ Represents the controller output signal for control valve operation. Range is from 0 to 300 mAdc.
                In reality it reaches until 250mAdc"""
        response = self.sila_client.GetValveOutput()
        assert response is not None
        assert isinstance(response.CurrentValveOutput.value, float)
        # assert int(response.CurrentValveOutput.value) in range(0, 300, 1)  # convert to integer and assert if in range

    def test_GetCapacity100(self):
        """ This parameter sets the maximum readout/control value (100%) for the current fluid in readout units corresponding to Capacity Unit."""
        response = self.sila_client.GetCapacity100()
        assert response is not None
        assert isinstance(response.CurrentCapacity100.value, float)
        # assert int(response.CurrentCapacity100.value) in range(-1E+10, 1E+10, 1)

    def test_GetCapacityUnit(self):
        """ This parameter defines the units in which is the measured value and set value are represented."""
        response = self.sila_client.GetCapacityUnit()
        assert response is not None
        assert isinstance(response.CurrentCapacityUnit.value, str)

    def test_GetSerialNumber(self):
        """ Gets the serial number of the device and software version"""
        response = self.sila_client.GetSerialNumber()
        assert response is not None
        assert isinstance(response.CurrentSerialNumber.value, str)

    def test_GetPrimaryNodeAddress(self):
        """ Primary node address: network parameter Flow-Bus"""
        response = self.sila_client.GetPrimaryNodeAddress()
        assert response is not None
        assert isinstance(response.CurrentPrimaryNodeAddress.value, str)

    def test_GetFirmwareVersion(self):
        response = self.sila_client.GetFirmwareVersion()
        assert response is not None
        assert isinstance(response.CurrentFirmwareVersion.value, str)

    def test_GetCommunicationProtocol(self):
        """ Current communication protocol between the program adn the device.
            2 possible options: "binary" and "ascii"
            Binary is the default protocol"""
        response = self.sila_client.GetCommunicationProtocol()
        assert response is not None
        assert isinstance(response.CurrentCommunicationProtocol.value, str)
        assert response.CurrentCommunicationProtocol.value in ["binary", "ascii"]

    def test_GetSerialPort(self):
        """ Current devices serial port. "50001" is the predefined value"""
        response = self.sila_client.GetSerialPort()
        assert response is not None
        assert isinstance(response.CurrentSerialPort.value, str)
        assert int(response.CurrentSerialPort.value) == port


class TestMeasurementServiceGet:
    """ Test all MeasurementService Get functions. Allows full control of the available fluid features of the Flowmeter."""
    sila_client = FlowmeterElflowPrestigeServiceClient(server_ip=ip, server_port=port)

    def test_GetMeasuredValue(self):
        """ Shows the measured value in the capacity unit for which the instrument is set."""
        response = self.sila_client.GetMeasuredValue()
        assert response is not None
        assert isinstance(response.CurrentMeasuredValue.value, float)
        # assert int(response.CurrentMeasuredValue.value) in range(-3.4E+38, +3.4E+38, 1)  # convert to integer and assert if in range

    def test_GetSetpointValue(self):
        """ Shows the current set point value in the capacity unit for which the instrument is set.
            Range in Percentage from 0.0 to 100.0 percent"""
        # todo: how can the range be 0,100 if  <MaximalInclusive>3.4E+38</MaximalInclusive>?!?!
        response = self.sila_client.GetSetpointValue()
        assert response is not None
        assert isinstance(response.GetSetpointValue.value, float)
        # assert int(response.GetSetpointValue.value) in range(0, +3.4E+38, 1)
        restore_default['GetSetpointValue'] = response.GetSetpointValue.value

    def test_GetFluidNumber(self):
        """ Current fluid ID-Nr. Preset of Fluid number is delimited up to 8 fluids."""
        response = self.sila_client.GetFluidNumber()
        assert response is not None
        assert isinstance(response.CurrentFluidNumber.value, int)
        # assert response.CurrentFluidNumber.value in range(1, 8, 1)
        restore_default['GetFluidNumber'] = response.CurrentFluidNumber.value

    def test_GetFluidName(self):
        response = self.sila_client.GetFluidName()
        assert response is not None
        assert isinstance(response.CurrentFluidName.value, str)
        assert response.CurrentFluidName.value == "error"


class TestDeviceServiceSet:
    """ Test all DeviceService Set functions. Allows full control of the device features of the Flowmeter."""
    sila_client = FlowmeterElflowPrestigeServiceClient(server_ip=ip, server_port=port)

    def test_SetCommunicationProtocolBinary(self):
        response = self.sila_client.SetCommunicationProtocolBinary()
        assert response is not None
        assert isinstance(response.CurrentCommunicationProtocolBinary.value, str)
        assert response.CurrentCommunicationProtocolBinary.value == "binary"

    def test_SetCommunicationProtocolAscii(self):
        response = self.sila_client.SetCommunicationProtocolAscii()
        assert response is not None
        assert isinstance(response.CurrentCommunicationProtocolAscii.value, str)
        assert response.CurrentCommunicationProtocolAscii.value == "ascii"

    # why no parameter passing necessary? -> default value is also different to the .xml
    def test_SetSerialPort(self):
        """ Sets devices new serial port. "50001" is the predefined value"""
        response = self.sila_client.SetSerialPort()
        assert response is not None
        assert isinstance(response.NewSerialPort.value, str)
        # value: "default string"


# todo: bug binascii.Error: Incorrect padding
class TestMeasurementServiceSet:
    """ Test all MeasurementService Set functions. Allows full control of the available fluid features of the Flowmeter."""
    sila_client = FlowmeterElflowPrestigeServiceClient(server_ip=ip, server_port=port)

    # @pytest.mark.parametrize('number', [random.uniform(0.01, 100)])
    # def test_SetSetpointValue(self, number):
    #     """ Sets the new set point value in the capacity unit for which the instrument is set.
    #             Range in Percentage from 0.0 to 100.0 percent"""
    #     response = self.sila_client.SetSetpointValue(number)
    #     assert response is not None
    #     assert isinstance(response.Status.value, str)
    #     assert isinstance(response.IndexPointing.value, str)
    #     # assert int(response.XXX.value) == number
    #
    # @pytest.mark.parametrize('number', random.sample(range(0, 8), 1))
    # def test_SetFluidNumber(self, number):
    #     """ The number of the fluid to work with"""
    #     response = self.sila_client.SetFluidNumber(number)
    #     assert response is not None
    #     assert isinstance(response.Status.value, str)
    #     assert isinstance(response.IndexPointing.value, str)
    #     # assert int(response.XXX.value) == number

    def test_restore_default(self, teardown_restore_default):
        """ This function calls the teardown to set all default values again to bring the device back to pre-test condition."""
        assert True


def test__init__():
    """ Starts the server in a mocked environment as defined in FlowmeterElflowPrestigeService_server.init()"""
    from sila2lib.sila_server import SiLA2Server
    with mock.patch.object(SiLA2Server, 'run', return_value=42):  # Syntax: .object(class, 'method', return)
        with mock.patch.object(FlowmeterElflowPrestigeService_server, '__name__', '__main__'):
            with mock.patch.object(FlowmeterElflowPrestigeService_server.sys, 'exit') as mock_exit:
                FlowmeterElflowPrestigeService_server.init()
                assert mock_exit.call_args[0][0] == 42
