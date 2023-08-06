#!/usr/bin/env python3
"""
This file tests the simulation- or real mode of Eppendorf, DASGIP (4x Parallel Bioeactor System).

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

from sila2lib_implementations.DASGIP.DASGIPService.DASGIP_Service_client import DASGIP_ServiceClient
from sila2lib_implementations.DASGIP.DASGIPService import DASGIP_Service_server

from tests.config import settings


logger = logging.getLogger(__name__)
# logging.basicConfig(format  = '%(asctime)s - %(name)s - %(levelname)s- %(module)s - linenumber: %(lineno)d - %(message)s', level=logging.DEBUG)

# Set variables of Dotenv
ip = settings.DASGIP_IP
port = settings.DASGIP_PORT
simulation_mode = settings.DASGIP_SIMULATION_MODE

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
# class DasGipTestServer(DASGIP_Service_server.DASGIP_ServiceServer):
#     """
#     Test server instance. Implementation of service until an abort event is sent
#     :param abort_event: Event that leads to the server stop
#     """
#
#     ip = settings.DASGIP_IP
#     port = settings.DASGIP_PORT
#     simulation_mode = settings.DASGIP_SIMULATION_MODE
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
# def setup_and_teardown_dasgip_server():
#     """
#     Starts a server thread and tears it down automatically after the whole module is executed.
#     """
#     abort_event = Event()
#     server = DasGipTestServer(abort_event)
#     thread = Thread(target=server.serve, args=(), daemon=True)
#     thread.start()
#     wait_until_server_up(server)
#     logger.info('Started DasGip server')
#     yield thread
#     abort_event.set()
#     thread.join(timeout=10)
#     wait_until_port_closes(ip=DasGipTestServer.ip, port=DasGipTestServer.port, timeout=10)
#     if thread.is_alive:
#         logger.warning(f'DasGip server thread is still alive: {thread.is_alive()}')
#     logger.info('Stopped DasGip server')
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
#         cls.sila_client = DASGIP_ServiceClient(server_ip=DasGipTestServer.ip, server_port=DasGipTestServer.port)
#
#     def test_run_bluevary_test_server(self, setup_and_teardown_dasgip_server):
#         logger.info(f'DasGip server running. Is alive: {setup_and_teardown_dasgip_server.is_alive()}')
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
#         assert self.sila_client.server_port is DasGipTestServer.port
#         assert self.sila_client.server_hostname is DasGipTestServer.ip
#         assert self.sila_client.server_display_name == ''
#         assert self.sila_client.server_description == ''
#         assert self.sila_client.server_version == ''
#
#     def test_client_values(self):
#         assert self.sila_client.vendor_url == ''
#         assert self.sila_client.name == 'DASGIP_ServiceClient'
#         assert self.sila_client.version == '1.0'
#         assert self.sila_client.description == 'This is a DasGip MCR Service'
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



unit_ids = 48  # reasonable value?
val_range = 2  # reasonable value?

# Start of Get features - Pump A-D
class TestPumpAServicerGet:
    """ Test all PumpAServicer Get functions. Control a DASGIP PumpA module. Enables read and write operations for various parameters, including PumpA sensor, controller, and alarm.  """
    sila_client = DASGIP_ServiceClient(server_ip=ip, server_port=port)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetPVInt(self, UnitID):
        """ Get integrated present value
        :param UnitID: The UnitID of the addressed reactor"""
        response = self.sila_client.PumpAServicer_GetPVInt(UnitID)
        assert response is not None
        assert isinstance(response.CurrentPVInt.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetPV(self, UnitID):
        response = self.sila_client.PumpAServicer_GetPV(UnitID)
        assert response is not None
        assert isinstance(response.CurrentPV.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetSP(self, UnitID):
        response = self.sila_client.PumpAServicer_GetSP(UnitID)
        assert response is not None
        assert isinstance(response.CurrentSP.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetSPA(self, UnitID):
        response = self.sila_client.PumpAServicer_GetSPA(UnitID)
        assert response is not None
        assert isinstance(response.CurrentSPA.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetSPM(self, UnitID):
        response = self.sila_client.PumpAServicer_GetSPM(UnitID)
        assert response is not None
        assert isinstance(response.CurrentSPM.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetSPE(self, UnitID):
        response = self.sila_client.PumpAServicer_GetSPE(UnitID)
        assert response is not None
        assert isinstance(response.CurrentSPE.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetSPR(self, UnitID):
        response = self.sila_client.PumpAServicer_GetSPR(UnitID)
        assert response is not None
        assert isinstance(response.CurrentSPR.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetAccess(self, UnitID):
        response = self.sila_client.PumpAServicer_GetAccess(UnitID)
        assert response is not None
        assert isinstance(response.CurrentAccess.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetCmd(self, UnitID):
        response = self.sila_client.PumpAServicer_GetCmd(UnitID)
        assert response is not None
        assert isinstance(response.CurrentCmd.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetMode(self, UnitID):
        response = self.sila_client.PumpAServicer_GetMode(UnitID)
        assert response is not None
        assert isinstance(response.CurrentMode.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetSetpointSelect(self, UnitID):
        response = self.sila_client.PumpAServicer_GetSetpointSelect(UnitID)
        assert response is not None
        assert isinstance(response.CurrentSetpointSelect.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetState(self, UnitID):
        response = self.sila_client.PumpAServicer_GetState(UnitID)
        assert response is not None
        assert isinstance(response.CurrentState.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetType(self, UnitID):
        response = self.sila_client.PumpAServicer_GetType(UnitID)
        assert response is not None
        assert isinstance(response.CurrentType.value, str)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetAvailable(self, UnitID):
        response = self.sila_client.PumpAServicer_GetAvailable(UnitID)
        assert response is not None
        assert isinstance(response.CurrentAvailable.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetName(self, UnitID):
        response = self.sila_client.PumpAServicer_GetName(UnitID)
        assert response is not None
        assert isinstance(response.CurrentName.value, str)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetVersion(self, UnitID):
        response = self.sila_client.PumpAServicer_GetVersion(UnitID)
        assert response is not None
        assert isinstance(response.CurrentVersion.value, str)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetActuatorCalibration(self, UnitID):
        """ Get the actuator calibration value that is used. Calibration parameter (at 100% speed)."""
        response = self.sila_client.PumpAServicer_GetActuatorCalibration(UnitID)
        assert response is not None
        assert isinstance(response.CurrentActuatorCalibration.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetActuatorDirPV(self, UnitID):
        """ Get the actuator direction value. Actual pump direction (0=Clockwise, 1=Counterclockwise)."""
        response = self.sila_client.PumpAServicer_GetActuatorDirPV(UnitID)
        assert response is not None
        assert isinstance(response.CurrentActuatorDirPV.value, int)


class TestPumpBServicerGet:
    """ Test all PumpBServicer Get functions. Control a DASGIP PumpB module. Enables read and write operations for various parameters, including PumpB sensor, controller, and alarm.  """
    sila_client = DASGIP_ServiceClient(server_ip=ip, server_port=port)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetPVInt(self, UnitID):
        """ Get integrated present value
        :param UnitID: The UnitID of the addressed reactor"""
        response = self.sila_client.PumpBServicer_GetPVInt(UnitID)
        assert response is not None
        assert isinstance(response.CurrentPVInt.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetPV(self, UnitID):
        response = self.sila_client.PumpBServicer_GetPV(UnitID)
        assert response is not None
        assert isinstance(response.CurrentPV.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetSP(self, UnitID):
        response = self.sila_client.PumpBServicer_GetSP(UnitID)
        assert response is not None
        assert isinstance(response.CurrentSP.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetSPA(self, UnitID):
        response = self.sila_client.PumpBServicer_GetSPA(UnitID)
        assert response is not None
        assert isinstance(response.CurrentSPA.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetSPM(self, UnitID):
        response = self.sila_client.PumpBServicer_GetSPM(UnitID)
        assert response is not None
        assert isinstance(response.CurrentSPM.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetSPE(self, UnitID):
        response = self.sila_client.PumpBServicer_GetSPE(UnitID)
        assert response is not None
        assert isinstance(response.CurrentSPE.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetSPR(self, UnitID):
        response = self.sila_client.PumpBServicer_GetSPR(UnitID)
        assert response is not None
        assert isinstance(response.CurrentSPR.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetAccess(self, UnitID):
        response = self.sila_client.PumpBServicer_GetAccess(UnitID)
        assert response is not None
        assert isinstance(response.CurrentAccess.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetCmd(self, UnitID):
        response = self.sila_client.PumpBServicer_GetCmd(UnitID)
        assert response is not None
        assert isinstance(response.CurrentCmd.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetMode(self, UnitID):
        response = self.sila_client.PumpBServicer_GetMode(UnitID)
        assert response is not None
        assert isinstance(response.CurrentMode.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetSetpointSelect(self, UnitID):
        response = self.sila_client.PumpBServicer_GetSetpointSelect(UnitID)
        assert response is not None
        assert isinstance(response.CurrentSetpointSelect.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetState(self, UnitID):
        response = self.sila_client.PumpBServicer_GetState(UnitID)
        assert response is not None
        assert isinstance(response.CurrentState.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetType(self, UnitID):
        response = self.sila_client.PumpBServicer_GetType(UnitID)
        assert response is not None
        assert isinstance(response.CurrentType.value, str)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetAvailable(self, UnitID):
        response = self.sila_client.PumpBServicer_GetAvailable(UnitID)
        assert response is not None
        assert isinstance(response.CurrentAvailable.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetName(self, UnitID):
        response = self.sila_client.PumpBServicer_GetName(UnitID)
        assert response is not None
        assert isinstance(response.CurrentName.value, str)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetVersion(self, UnitID):
        response = self.sila_client.PumpBServicer_GetVersion(UnitID)
        assert response is not None
        assert isinstance(response.CurrentVersion.value, str)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetActuatorCalibration(self, UnitID):
        """ Get the actuator calibration value that is used. Calibration parameter (at 100% speed)."""
        response = self.sila_client.PumpBServicer_GetActuatorCalibration(UnitID)
        assert response is not None
        assert isinstance(response.CurrentActuatorCalibration.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetActuatorDirPV(self, UnitID):
        """ Get the actuator direction value. Actual pump direction (0=Clockwise, 1=Counterclockwise)."""
        response = self.sila_client.PumpBServicer_GetActuatorDirPV(UnitID)
        assert response is not None
        assert isinstance(response.CurrentActuatorDirPV.value, int)


class TestPumpCServicerGet:
    """ Test all PumpCServicer Get functions. Control a DASGIP PumpC module. Enables read and write operations for various parameters, including PumpC sensor, controller, and alarm.  """
    sila_client = DASGIP_ServiceClient(server_ip=ip, server_port=port)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetPVInt(self, UnitID):
        """ Get integrated present value
        :param UnitID: The UnitID of the addressed reactor"""
        response = self.sila_client.PumpCServicer_GetPVInt(UnitID)
        assert response is not None
        assert isinstance(response.CurrentPVInt.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetPV(self, UnitID):
        response = self.sila_client.PumpCServicer_GetPV(UnitID)
        assert response is not None
        assert isinstance(response.CurrentPV.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetSP(self, UnitID):
        response = self.sila_client.PumpCServicer_GetSP(UnitID)
        assert response is not None
        assert isinstance(response.CurrentSP.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetSPA(self, UnitID):
        response = self.sila_client.PumpCServicer_GetSPA(UnitID)
        assert response is not None
        assert isinstance(response.CurrentSPA.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetSPM(self, UnitID):
        response = self.sila_client.PumpCServicer_GetSPM(UnitID)
        assert response is not None
        assert isinstance(response.CurrentSPM.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetSPE(self, UnitID):
        response = self.sila_client.PumpCServicer_GetSPE(UnitID)
        assert response is not None
        assert isinstance(response.CurrentSPE.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetSPR(self, UnitID):
        response = self.sila_client.PumpCServicer_GetSPR(UnitID)
        assert response is not None
        assert isinstance(response.CurrentSPR.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetAccess(self, UnitID):
        response = self.sila_client.PumpCServicer_GetAccess(UnitID)
        assert response is not None
        assert isinstance(response.CurrentAccess.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetCmd(self, UnitID):
        response = self.sila_client.PumpCServicer_GetCmd(UnitID)
        assert response is not None
        assert isinstance(response.CurrentCmd.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetMode(self, UnitID):
        response = self.sila_client.PumpCServicer_GetMode(UnitID)
        assert response is not None
        assert isinstance(response.CurrentMode.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetSetpointSelect(self, UnitID):
        response = self.sila_client.PumpCServicer_GetSetpointSelect(UnitID)
        assert response is not None
        assert isinstance(response.CurrentSetpointSelect.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetState(self, UnitID):
        response = self.sila_client.PumpCServicer_GetState(UnitID)
        assert response is not None
        assert isinstance(response.CurrentState.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetType(self, UnitID):
        response = self.sila_client.PumpCServicer_GetType(UnitID)
        assert response is not None
        assert isinstance(response.CurrentType.value, str)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetAvailable(self, UnitID):
        response = self.sila_client.PumpCServicer_GetAvailable(UnitID)
        assert response is not None
        assert isinstance(response.CurrentAvailable.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetName(self, UnitID):
        response = self.sila_client.PumpCServicer_GetName(UnitID)
        assert response is not None
        assert isinstance(response.CurrentName.value, str)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetVersion(self, UnitID):
        response = self.sila_client.PumpCServicer_GetVersion(UnitID)
        assert response is not None
        assert isinstance(response.CurrentVersion.value, str)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetActuatorCalibration(self, UnitID):
        """ Get the actuator calibration value that is used. Calibration parameter (at 100% speed)."""
        response = self.sila_client.PumpCServicer_GetActuatorCalibration(UnitID)
        assert response is not None
        assert isinstance(response.CurrentActuatorCalibration.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetActuatorDirPV(self, UnitID):
        """ Get the actuator direction value. Actual pump direction (0=Clockwise, 1=Counterclockwise)."""
        response = self.sila_client.PumpCServicer_GetActuatorDirPV(UnitID)
        assert response is not None
        assert isinstance(response.CurrentActuatorDirPV.value, int)


class TestPumpDServicerGet:
    """ Test all PumpDServicer Get functions. Control a DASGIP PumpD module. Enables read and write operations for various parameters, including PumpD sensor, controller, and alarm.  """
    sila_client = DASGIP_ServiceClient(server_ip=ip, server_port=port)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetPVInt(self, UnitID):
        """ Get integrated present value
        :param UnitID: The UnitID of the addressed reactor"""
        response = self.sila_client.PumpDServicer_GetPVInt(UnitID)
        assert response is not None
        assert isinstance(response.CurrentPVInt.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetPV(self, UnitID):
        response = self.sila_client.PumpDServicer_GetPV(UnitID)
        assert response is not None
        assert isinstance(response.CurrentPV.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetSP(self, UnitID):
        response = self.sila_client.PumpDServicer_GetSP(UnitID)
        assert response is not None
        assert isinstance(response.CurrentSP.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetSPA(self, UnitID):
        response = self.sila_client.PumpDServicer_GetSPA(UnitID)
        assert response is not None
        assert isinstance(response.CurrentSPA.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetSPM(self, UnitID):
        response = self.sila_client.PumpDServicer_GetSPM(UnitID)
        assert response is not None
        assert isinstance(response.CurrentSPM.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetSPE(self, UnitID):
        response = self.sila_client.PumpDServicer_GetSPE(UnitID)
        assert response is not None
        assert isinstance(response.CurrentSPE.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetSPR(self, UnitID):
        response = self.sila_client.PumpDServicer_GetSPR(UnitID)
        assert response is not None
        assert isinstance(response.CurrentSPR.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetAccess(self, UnitID):
        response = self.sila_client.PumpDServicer_GetAccess(UnitID)
        assert response is not None
        assert isinstance(response.CurrentAccess.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetCmd(self, UnitID):
        response = self.sila_client.PumpDServicer_GetCmd(UnitID)
        assert response is not None
        assert isinstance(response.CurrentCmd.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetMode(self, UnitID):
        response = self.sila_client.PumpDServicer_GetMode(UnitID)
        assert response is not None
        assert isinstance(response.CurrentMode.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetSetpointSelect(self, UnitID):
        response = self.sila_client.PumpDServicer_GetSetpointSelect(UnitID)
        assert response is not None
        assert isinstance(response.CurrentSetpointSelect.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetState(self, UnitID):
        response = self.sila_client.PumpDServicer_GetState(UnitID)
        assert response is not None
        assert isinstance(response.CurrentState.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetType(self, UnitID):
        response = self.sila_client.PumpDServicer_GetType(UnitID)
        assert response is not None
        assert isinstance(response.CurrentType.value, str)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetAvailable(self, UnitID):
        response = self.sila_client.PumpDServicer_GetAvailable(UnitID)
        assert response is not None
        assert isinstance(response.CurrentAvailable.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetName(self, UnitID):
        response = self.sila_client.PumpDServicer_GetName(UnitID)
        assert response is not None
        assert isinstance(response.CurrentName.value, str)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetVersion(self, UnitID):
        response = self.sila_client.PumpDServicer_GetVersion(UnitID)
        assert response is not None
        assert isinstance(response.CurrentVersion.value, str)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetActuatorCalibration(self, UnitID):
        """ Get the actuator calibration value that is used. Calibration parameter (at 100% speed)."""
        response = self.sila_client.PumpDServicer_GetActuatorCalibration(UnitID)
        assert response is not None
        assert isinstance(response.CurrentActuatorCalibration.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetActuatorDirPV(self, UnitID):
        """ Get the actuator direction value. Actual pump direction (0=Clockwise, 1=Counterclockwise)."""
        response = self.sila_client.PumpDServicer_GetActuatorDirPV(UnitID)
        assert response is not None
        assert isinstance(response.CurrentActuatorDirPV.value, int)


# Start of Set features - Pump A-D
class TestPumpAServicerSet:
    """ Test all PumpAServicer Set functions. Control a DASGIP PumpA module. Enables read and write operations for various parameters, including PumpA sensor, controller, and alarm.  """
    sila_client = DASGIP_ServiceClient(server_ip=ip, server_port=port)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(0, val_range)])  # float
    def test_SetSPM(self, UnitID, val):
        """ Set the manual temperature setpoint.
        :param UnitID: The UnitID of the addressed reactor"""
        response = self.sila_client.PumpAServicer_SetSPM(UnitID, val)
        assert response is not None
        assert isinstance(response.SPMSet.value, float)
        # assert response.SPMSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(0, val_range)])  # float
    def test_SetSPE(self, UnitID, val):
        response = self.sila_client.PumpAServicer_SetSPE(UnitID, val)
        assert response is not None
        assert isinstance(response.SPESet.value, float)
        # assert response.SPESet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', random.sample(range(0, 3), 1))  # int
    def test_SetCmd(self, UnitID, val):
        response = self.sila_client.PumpAServicer_SetCmd(UnitID, val)
        assert response is not None
        assert isinstance(response.CmdSet.value, int)
        # assert response.CmdSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', random.sample(range(0, 2), 1))  # int
    def test_SetMode(self, UnitID, val):
        response = self.sila_client.PumpAServicer_SetMode(UnitID, val)
        assert response is not None
        assert isinstance(response.ModeSet.value, int)
        # assert response.ModeSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', random.sample(range(0, 6), 1))  # int
    def test_SetSetpointSelect(self, UnitID, val):
        response = self.sila_client.PumpAServicer_SetSetpointSelect(UnitID, val)
        assert response is not None
        assert isinstance(response.SetpointSelectSet.value, int)
        # assert response.SetpointSelectSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(0, val_range)])  # float
    def test_SetActuatorCalibration(self, UnitID, val):
        """ Set the actuator calibration value that should be used. Calibration parameter (at 100% speed)."""
        response = self.sila_client.PumpAServicer_SetActuatorCalibration(UnitID, val)
        assert response is not None
        assert isinstance(response.ActuatorCalibrationSet.value, float)
        # assert response.ActuatorCalibrationSet.value == val


class TestPumpBServicerSet:
    """ Test all PumpBServicer Set functions. Control a DASGIP PumpB module. Enables read and write operations for various parameters, including PumpB sensor, controller, and alarm.  """
    sila_client = DASGIP_ServiceClient(server_ip=ip, server_port=port)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(0, val_range)])  # float
    def test_SetSPM(self, UnitID, val):
        """ Set the manual temperature setpoint.
        :param UnitID: The UnitID of the addressed reactor"""
        response = self.sila_client.PumpBServicer_SetSPM(UnitID, val)
        assert response is not None
        assert isinstance(response.SPMSet.value, float)
        # assert response.SPMSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(0, val_range)])  # float
    def test_SetSPE(self, UnitID, val):
        response = self.sila_client.PumpBServicer_SetSPE(UnitID, val)
        assert response is not None
        assert isinstance(response.SPESet.value, float)
        # assert response.SPESet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', random.sample(range(0, 3), 1))  # int
    def test_SetCmd(self, UnitID, val):
        response = self.sila_client.PumpBServicer_SetCmd(UnitID, val)
        assert response is not None
        assert isinstance(response.CmdSet.value, int)
        # assert response.CmdSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', random.sample(range(0, 2), 1))  # int
    def test_SetMode(self, UnitID, val):
        response = self.sila_client.PumpBServicer_SetMode(UnitID, val)
        assert response is not None
        assert isinstance(response.ModeSet.value, int)
        # assert response.ModeSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', random.sample(range(0, 6), 1))  # int
    def test_SetSetpointSelect(self, UnitID, val):
        response = self.sila_client.PumpBServicer_SetSetpointSelect(UnitID, val)
        assert response is not None
        assert isinstance(response.SetpointSelectSet.value, int)
        # assert response.SetpointSelectSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(0, val_range)])  # float
    def test_SetActuatorCalibration(self, UnitID, val):
        """ Set the actuator calibration value that should be used. Calibration parameter (at 100% speed)."""
        response = self.sila_client.PumpBServicer_SetActuatorCalibration(UnitID, val)
        assert response is not None
        assert isinstance(response.ActuatorCalibrationSet.value, float)
        # assert response.ActuatorCalibrationSet.value == val


class TestPumpCServicerSet:
    """ Test all PumpCServicer Set functions. Control a DASGIP PumpC module. Enables read and write operations for various parameters, including PumpC sensor, controller, and alarm.  """
    sila_client = DASGIP_ServiceClient(server_ip=ip, server_port=port)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(0, val_range)])  # float
    def test_SetSPM(self, UnitID, val):
        """ Set the manual temperature setpoint.
        :param UnitID: The UnitID of the addressed reactor"""
        response = self.sila_client.PumpCServicer_SetSPM(UnitID, val)
        assert response is not None
        assert isinstance(response.SPMSet.value, float)
        # assert response.SPMSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(0, val_range)])  # float
    def test_SetSPE(self, UnitID, val):
        response = self.sila_client.PumpCServicer_SetSPE(UnitID, val)
        assert response is not None
        assert isinstance(response.SPESet.value, float)
        # assert response.SPESet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', random.sample(range(0, 3), 1))  # int
    def test_SetCmd(self, UnitID, val):
        response = self.sila_client.PumpCServicer_SetCmd(UnitID, val)
        assert response is not None
        assert isinstance(response.CmdSet.value, int)
        # assert response.CmdSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', random.sample(range(0, 2), 1))  # int
    def test_SetMode(self, UnitID, val):
        response = self.sila_client.PumpCServicer_SetMode(UnitID, val)
        assert response is not None
        assert isinstance(response.ModeSet.value, int)
        # assert response.ModeSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', random.sample(range(0, 6), 1))  # int
    def test_SetSetpointSelect(self, UnitID, val):
        response = self.sila_client.PumpCServicer_SetSetpointSelect(UnitID, val)
        assert response is not None
        assert isinstance(response.SetpointSelectSet.value, int)
        # assert response.SetpointSelectSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(0, val_range)])  # float
    def test_SetActuatorCalibration(self, UnitID, val):
        """ Set the actuator calibration value that should be used. Calibration parameter (at 100% speed)."""
        response = self.sila_client.PumpCServicer_SetActuatorCalibration(UnitID, val)
        assert response is not None
        assert isinstance(response.ActuatorCalibrationSet.value, float)
        # assert response.ActuatorCalibrationSet.value == val


class TestPumpDServicerSet:
    """ Test all PumpDServicer Set functions. Control a DASGIP PumpD module. Enables read and write operations for various parameters, including PumpD sensor, controller, and alarm.  """
    sila_client = DASGIP_ServiceClient(server_ip=ip, server_port=port)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(0, val_range)])  # float
    def test_SetSPM(self, UnitID, val):
        """ Set the manual temperature setpoint.
        :param UnitID: The UnitID of the addressed reactor"""
        response = self.sila_client.PumpDServicer_SetSPM(UnitID, val)
        assert response is not None
        assert isinstance(response.SPMSet.value, float)
        # assert response.SPMSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(0, val_range)])  # float
    def test_SetSPE(self, UnitID, val):
        response = self.sila_client.PumpDServicer_SetSPE(UnitID, val)
        assert response is not None
        assert isinstance(response.SPESet.value, float)
        # assert response.SPESet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', random.sample(range(0, 3), 1))  # int
    def test_SetCmd(self, UnitID, val):
        response = self.sila_client.PumpDServicer_SetCmd(UnitID, val)
        assert response is not None
        assert isinstance(response.CmdSet.value, int)
        # assert response.CmdSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', random.sample(range(0, 2), 1))  # int
    def test_SetMode(self, UnitID, val):
        response = self.sila_client.PumpDServicer_SetMode(UnitID, val)
        assert response is not None
        assert isinstance(response.ModeSet.value, int)
        # assert response.ModeSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', random.sample(range(0, 6), 1))  # int
    def test_SetSetpointSelect(self, UnitID, val):
        response = self.sila_client.PumpDServicer_SetSetpointSelect(UnitID, val)
        assert response is not None
        assert isinstance(response.SetpointSelectSet.value, int)
        # assert response.SetpointSelectSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(0, val_range)])  # float
    def test_SetActuatorCalibration(self, UnitID, val):
        """ Set the actuator calibration value that should be used. Calibration parameter (at 100% speed)."""
        response = self.sila_client.PumpDServicer_SetActuatorCalibration(UnitID, val)
        assert response is not None
        assert isinstance(response.ActuatorCalibrationSet.value, float)
        # assert response.ActuatorCalibrationSet.value == val


def test__init__():
    """ Starts the server in a mocked environment as defined in DASGIP_Service_server.init()"""
    from sila2lib.sila_server import SiLA2Server
    with mock.patch.object(SiLA2Server, 'run', return_value=42):  # Syntax: .object(class, 'method', return)
        with mock.patch.object(DASGIP_Service_server, '__name__', '__main__'):
            with mock.patch.object(DASGIP_Service_server.sys, 'exit') as mock_exit:
                DASGIP_Service_server.init()
                assert mock_exit.call_args[0][0] == 42
