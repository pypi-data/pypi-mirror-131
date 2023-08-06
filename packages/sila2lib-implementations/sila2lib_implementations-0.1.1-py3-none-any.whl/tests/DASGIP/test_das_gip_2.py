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



class TestTemperatureServicerGet:
    """ Test all TemperatureServicer Get functions. Control a DASGIP temperature module. Enables read and write operations for various parameters, including temperature sensor, controller, and alarm. """
    sila_client = DASGIP_ServiceClient(server_ip=ip, server_port=port)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetPV(self, UnitID):
        """ Get present value in absorption unit. Turbidity signal in absorption units.
        :param UnitID: The UnitID of the addressed reactor"""
        response = self.sila_client.TemperatureServicer_GetPV(UnitID)
        assert response is not None
        assert isinstance(response.CurrentPV.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetSP(self, UnitID):
        response = self.sila_client.TemperatureServicer_GetSP(UnitID)
        assert response is not None
        assert isinstance(response.CurrentSP.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetSPA(self, UnitID):
        response = self.sila_client.TemperatureServicer_GetSPA(UnitID)
        assert response is not None
        assert isinstance(response.CurrentSPA.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetSPM(self, UnitID):
        response = self.sila_client.TemperatureServicer_GetSPM(UnitID)
        assert response is not None
        assert isinstance(response.CurrentSPM.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetSPE(self, UnitID):
        response = self.sila_client.TemperatureServicer_GetSPE(UnitID)
        assert response is not None
        assert isinstance(response.CurrentSPE.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetSPR(self, UnitID):
        response = self.sila_client.TemperatureServicer_GetSPR(UnitID)
        assert response is not None
        assert isinstance(response.CurrentSPR.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetAccess(self, UnitID):
        response = self.sila_client.TemperatureServicer_GetAccess(UnitID)
        assert response is not None
        assert isinstance(response.CurrentAccess.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetCmd(self, UnitID):
        response = self.sila_client.TemperatureServicer_GetCmd(UnitID)
        assert response is not None
        assert isinstance(response.CurrentCmd.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetMode(self, UnitID):
        response = self.sila_client.TemperatureServicer_GetMode(UnitID)
        assert response is not None
        assert isinstance(response.CurrentMode.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetSetpointSelect(self, UnitID):
        response = self.sila_client.TemperatureServicer_GetSetpointSelect(UnitID)
        assert response is not None
        assert isinstance(response.CurrentSetpointSelect.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetState(self, UnitID):
        response = self.sila_client.TemperatureServicer_GetState(UnitID)
        assert response is not None
        assert isinstance(response.CurrentState.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetType(self, UnitID):
        response = self.sila_client.TemperatureServicer_GetType(UnitID)
        assert response is not None
        assert isinstance(response.CurrentType.value, str)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetAvailable(self, UnitID):
        response = self.sila_client.TemperatureServicer_GetAvailable(UnitID)
        assert response is not None
        assert isinstance(response.CurrentAvailable.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetName(self, UnitID):
        response = self.sila_client.TemperatureServicer_GetName(UnitID)
        assert response is not None
        assert isinstance(response.CurrentName.value, str)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetVersion(self, UnitID):
        response = self.sila_client.TemperatureServicer_GetVersion(UnitID)
        assert response is not None
        assert isinstance(response.CurrentVersion.value, str)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetSensorOffset(self, UnitID):
        response = self.sila_client.TemperatureServicer_GetSensorOffset(UnitID)
        assert response is not None
        assert isinstance(response.CurrentSensorOffset.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetSensorPVRaw(self, UnitID):
        response = self.sila_client.TemperatureServicer_GetSensorPVRaw(UnitID)
        assert response is not None
        assert isinstance(response.CurrentSensorPVRaw.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetSensorSlope(self, UnitID):
        response = self.sila_client.TemperatureServicer_GetSensorSlope(UnitID)
        assert response is not None
        assert isinstance(response.CurrentSensorSlope.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetSensorCompensation(self, UnitID):
        response = self.sila_client.TemperatureServicer_GetSensorCompensation(UnitID)
        assert response is not None
        assert isinstance(response.CurrentSensorCompensation.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetControllerDB(self, UnitID):
        response = self.sila_client.TemperatureServicer_GetControllerDB(UnitID)
        assert response is not None
        assert isinstance(response.CurrentControllerDB.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetControllerOut(self, UnitID):
        response = self.sila_client.TemperatureServicer_GetControllerOut(UnitID)
        assert response is not None
        assert isinstance(response.CurrentControllerOut.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetControllerP(self, UnitID):
        response = self.sila_client.TemperatureServicer_GetControllerP(UnitID)
        assert response is not None
        assert isinstance(response.CurrentControllerP.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetControllerTd(self, UnitID):
        response = self.sila_client.TemperatureServicer_GetControllerTd(UnitID)
        assert response is not None
        assert isinstance(response.CurrentControllerTd.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetControllerTi(self, UnitID):
        response = self.sila_client.TemperatureServicer_GetControllerTi(UnitID)
        assert response is not None
        assert isinstance(response.CurrentControllerTi.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetControllerMin(self, UnitID):
        response = self.sila_client.TemperatureServicer_GetControllerMin(UnitID)
        assert response is not None
        assert isinstance(response.CurrentControllerMin.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetControllerMax(self, UnitID):
        response = self.sila_client.TemperatureServicer_GetControllerMax(UnitID)
        assert response is not None
        assert isinstance(response.CurrentControllerMax.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetAlarmEnabled(self, UnitID):
        response = self.sila_client.TemperatureServicer_GetAlarmEnabled(UnitID)
        assert response is not None
        assert isinstance(response.CurrentAlarmEnabled.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetAlarmAlarmHigh(self, UnitID):
        response = self.sila_client.TemperatureServicer_GetAlarmAlarmHigh(UnitID)
        assert response is not None
        assert isinstance(response.CurrentAlarmAlarmHigh.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetAlarmAlarmLow(self, UnitID):
        response = self.sila_client.TemperatureServicer_GetAlarmAlarmLow(UnitID)
        assert response is not None
        assert isinstance(response.CurrentAlarmAlarmLow.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetAlarmMode(self, UnitID):
        response = self.sila_client.TemperatureServicer_GetAlarmMode(UnitID)
        assert response is not None
        assert isinstance(response.CurrentAlarmMode.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetAlarmState(self, UnitID):
        response = self.sila_client.TemperatureServicer_GetAlarmState(UnitID)
        assert response is not None
        assert isinstance(response.CurrentAlarmState.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetAlarmDelay(self, UnitID):
        response = self.sila_client.TemperatureServicer_GetAlarmDelay(UnitID)
        assert response is not None
        assert isinstance(response.CurrentAlarmDelay.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetAlarmWarnHigh(self, UnitID):
        response = self.sila_client.TemperatureServicer_GetAlarmWarnHigh(UnitID)
        assert response is not None
        assert isinstance(response.CurrentAlarmWarnHigh.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetAlarmWarnLow(self, UnitID):
        response = self.sila_client.TemperatureServicer_GetAlarmWarnLow(UnitID)
        assert response is not None
        assert isinstance(response.CurrentAlarmWarnLow.value, float)


class TestTemperatureServicerSet:
    """ Test all TemperatureServicer Set functions. Control a DASGIP temperature module. Enables read and write operations for various parameters, including temperature sensor, controller, and alarm. """
    sila_client = DASGIP_ServiceClient(server_ip=ip, server_port=port)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(0, val_range)])  # float
    def test_SetSPM(self, UnitID, val):
        """ Set the manual temperature setpoint.
        :param UnitID: The UnitID of the addressed reactor"""
        response = self.sila_client.TemperatureServicer_SetSPM(UnitID, val)
        assert response is not None
        assert isinstance(response.SPMSet.value, float)
        # assert response.SPMSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(0, val_range)])  # float
    def test_SetSPE(self, UnitID, val):
        response = self.sila_client.TemperatureServicer_SetSPE(UnitID, val)
        assert response is not None
        assert isinstance(response.SPESet.value, float)
        # assert response.SPESet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', random.sample(range(0, 3), 1))  # int
    def test_SetCmd(self, UnitID, val):
        response = self.sila_client.TemperatureServicer_SetCmd(UnitID, val)
        assert response is not None
        assert isinstance(response.CmdSet.value, int)
        # assert response.CmdSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', random.sample(range(0, 3), 1))  # int
    def test_SetMode(self, UnitID, val):
        response = self.sila_client.TemperatureServicer_SetMode(UnitID, val)
        assert response is not None
        assert isinstance(response.ModeSet.value, int)
        # assert response.ModeSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', random.sample(range(0, 6), 1))  # int
    def test_SetSetpointSelect(self, UnitID, val):
        response = self.sila_client.TemperatureServicer_SetSetpointSelect(UnitID, val)
        assert response is not None
        assert isinstance(response.SetpointSelectSet.value, int)
        # assert response.SetpointSelectSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(0, val_range)])  # float, implement more meaningful range
    def test_SetSensorOffset(self, UnitID, val):
        response = self.sila_client.TemperatureServicer_SetSensorOffset(UnitID, val)
        assert response is not None
        assert isinstance(response.SensorOffsetSet.value, float)
        # assert response.SensorOffsetSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(0, val_range)])  # float, implement more meaningful range
    def test_SetSensorSlope(self, UnitID, val):
        response = self.sila_client.TemperatureServicer_SetSensorSlope(UnitID, val)
        assert response is not None
        assert isinstance(response.SensorSlopeSet.value, float)
        # assert response.SensorSlopeSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(0, val_range)])  # float, implement more meaningful range
    def test_SetSensorCompensation(self, UnitID, val):
        response = self.sila_client.TemperatureServicer_SetSensorCompensation(UnitID, val)
        assert response is not None
        assert isinstance(response.SensorCompensationSet.value, float)
        # assert response.SensorCompensationSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(0, val_range)])  # float, implement more meaningful range
    def test_SetControllerDB(self, UnitID, val):
        """ Set the controller deadband value. PID controller: deadband (set to zero to disable). """
        response = self.sila_client.TemperatureServicer_SetControllerDB(UnitID, val)
        assert response is not None
        assert isinstance(response.ControllerDBSet.value, float)
        # assert response.ControllerDBSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(0, val_range)])  # float, implement more meaningful range
    def test_SetControllerP(self, UnitID, val):
        """ Set the controller deadband value. PID controller: deadband (set to zero to disable). """
        response = self.sila_client.TemperatureServicer_SetControllerP(UnitID, val)
        assert response is not None
        assert isinstance(response.ControllerPSet.value, float)
        # assert response.ControllerPSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(0, val_range)])  # float, implement more meaningful range
    def test_SetControllerTd(self, UnitID, val):
        """ Set the controller differentiator time constant. PID controller: differentiator time constant (set to zero to disable). """
        response = self.sila_client.TemperatureServicer_SetControllerTd(UnitID, val)
        assert response is not None
        assert isinstance(response.ControllerTdSet.value, float)
        # assert response.ControllerTdSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(0, val_range)])  # float, implement more meaningful range
    def test_SetControllerTi(self, UnitID, val):
        """ Set the controller integrator time constant. PID controller: integrator time constant (set to zero to disable). """
        response = self.sila_client.TemperatureServicer_SetControllerTi(UnitID, val)
        assert response is not None
        assert isinstance(response.ControllerTiSet.value, float)
        # assert response.ControllerTiSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(0, val_range)])  # float, implement more meaningful range
    def test_SetControllerMin(self, UnitID, val):
        """ Set the controller minimal output value. PID controller: minimal output value. """
        response = self.sila_client.TemperatureServicer_SetControllerMin(UnitID, val)
        assert response is not None
        assert isinstance(response.ControllerMinSet.value, float)
        # assert response.ControllerMinSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(0, val_range)])  # float, implement more meaningful range
    def test_SetControllerMax(self, UnitID, val):
        """ Set the controller maximal output value. PID controller: maximal output value. """
        response = self.sila_client.TemperatureServicer_SetControllerMax(UnitID, val)
        assert response is not None
        assert isinstance(response.ControllerMaxSet.value, float)
        # assert response.ControllerMaxSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', random.sample(range(0, 2), 1)) # int [0, 1]
    def test_SetAlarmEnabled(self, UnitID, val):
        """ Set the alarm enabled value. Enables alarm function. """
        response = self.sila_client.TemperatureServicer_SetAlarmEnabled(UnitID, val)
        assert response is not None
        assert isinstance(response.AlarmEnabledSet.value, int)
        # assert response.AlarmEnabledSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(0, val_range)])  # float, implement more meaningful range
    def test_SetAlarmAlarmHigh(self, UnitID, val):
        """ The alarm alarmhigh value. Higher alarm limit. """
        response = self.sila_client.TemperatureServicer_SetAlarmAlarmHigh(UnitID, val)
        assert response is not None
        assert isinstance(response.AlarmAlarmHighSet.value, float)
        # assert response.AlarmAlarmHighSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(0, val_range)])  # float, implement more meaningful range
    def test_SetAlarmAlarmLow(self, UnitID, val):
        """ The alarm alarmLow value. Lower alarm limit. """
        response = self.sila_client.TemperatureServicer_SetAlarmAlarmLow(UnitID, val)
        assert response is not None
        assert isinstance(response.AlarmAlarmLowSet.value, float)
        # assert response.AlarmAlarmLowSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', random.sample(range(0, 2), 1)) # int [0, 1]
    def test_SetAlarmMode(self, UnitID, val):
        """ The alarm mode value. Alarm mode. """
        response = self.sila_client.TemperatureServicer_SetAlarmMode(UnitID, val)
        assert response is not None
        assert isinstance(response.AlarmModeSet.value, int)
        # assert response.AlarmModeSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(0, val_range)])  # float, implement more meaningful range
    def test_SetAlarmDelay(self, UnitID, val):
        """ Set the alarm delay value. Alarm hysteresis time. """
        response = self.sila_client.TemperatureServicer_SetAlarmDelay(UnitID, val)
        assert response is not None
        assert isinstance(response.AlarmDelaySet.value, float)
        # assert response.AlarmDelaySet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(0, val_range)])  # float, implement more meaningful range
    def test_SetAlarmWarnHigh(self, UnitID, val):
        response = self.sila_client.TemperatureServicer_SetAlarmWarnHigh(UnitID, val)
        assert response is not None
        assert isinstance(response.AlarmWarnHighSet.value, float)
        # assert response.AlarmWarnHighSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(0, val_range)])  # float, implement more meaningful range
    def test_SetAlarmWarnLow(self, UnitID, val):
        response = self.sila_client.TemperatureServicer_SetAlarmWarnLow(UnitID, val)
        assert response is not None
        assert isinstance(response.AlarmWarnLowSet.value, float)
        # assert response.AlarmWarnLowSet.value == val


class TestDOServicerGet:
    """ Test all DOServicer Get functions. Control a DASGIP DO module. Enables read and write operations for various parameters, including DO sensor, controller, and alarm. """
    sila_client = DASGIP_ServiceClient(server_ip=ip, server_port=port)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetPV(self, UnitID):
        """ :param UnitID: The UnitID of the addressed reactor"""
        response = self.sila_client.DOServicer_GetPV(UnitID)
        assert response is not None
        assert isinstance(response.CurrentPV.value, float)
        # assert response.CurrentPV.value == UnitID  # this makes no sence i guess

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetSP(self, UnitID):
        response = self.sila_client.DOServicer_GetSP(UnitID)
        assert response is not None
        assert isinstance(response.CurrentSP.value, float)
        # assert response.CurrentSP.value == UnitID  # this makes no sence i guess

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetSPA(self, UnitID):
        response = self.sila_client.DOServicer_GetSPA(UnitID)
        assert response is not None
        assert isinstance(response.CurrentSPA.value, float)
        # assert response.CurrentSPA.value == UnitID  # this makes no sence i guess

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetSPM(self, UnitID):
        response = self.sila_client.DOServicer_GetSPM(UnitID)
        assert response is not None
        assert isinstance(response.CurrentSPM.value, float)
        # assert response.CurrentSPM.value == UnitID  # this makes no sence i guess

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetSPE(self, UnitID):
        response = self.sila_client.DOServicer_GetSPE(UnitID)
        assert response is not None
        assert isinstance(response.CurrentSPE.value, float)
        # assert response.CurrentSPE.value == UnitID  # this makes no sence i guess

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetSPR(self, UnitID):
        response = self.sila_client.DOServicer_GetSPR(UnitID)
        assert response is not None
        assert isinstance(response.CurrentSPR.value, float)
        # assert response.CurrentSPR.value == UnitID  # this makes no sence i guess

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetAccess(self, UnitID):
        response = self.sila_client.DOServicer_GetAccess(UnitID)
        assert response is not None
        assert isinstance(response.CurrentAccess.value, int)
        # assert response.CurrentAccess.value == UnitID  # this makes no sence i guess

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetCmd(self, UnitID):
        response = self.sila_client.DOServicer_GetCmd(UnitID)
        assert response is not None
        assert isinstance(response.CurrentCmd.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetMode(self, UnitID):
        response = self.sila_client.DOServicer_GetMode(UnitID)
        assert response is not None
        assert isinstance(response.CurrentMode.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetSetpointSelect(self, UnitID):
        response = self.sila_client.DOServicer_GetSetpointSelect(UnitID)
        assert response is not None
        assert isinstance(response.CurrentSetpointSelect.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetState(self, UnitID):
        response = self.sila_client.DOServicer_GetState(UnitID)
        assert response is not None
        assert isinstance(response.CurrentState.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetType(self, UnitID):
        response = self.sila_client.DOServicer_GetType(UnitID)
        assert response is not None
        assert isinstance(response.CurrentType.value, str)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetAvailable(self, UnitID):
        response = self.sila_client.DOServicer_GetAvailable(UnitID)
        assert response is not None
        assert isinstance(response.CurrentAvailable.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetName(self, UnitID):
        response = self.sila_client.DOServicer_GetName(UnitID)
        assert response is not None
        assert isinstance(response.CurrentName.value, str)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetVersion(self, UnitID):
        response = self.sila_client.DOServicer_GetVersion(UnitID)
        assert response is not None
        assert isinstance(response.CurrentVersion.value, str)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetSensorOffset(self, UnitID):
        response = self.sila_client.DOServicer_GetSensorOffset(UnitID)
        assert response is not None
        assert isinstance(response.CurrentSensorOffset.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetSensorPVRaw(self, UnitID):
        response = self.sila_client.DOServicer_GetSensorPVRaw(UnitID)
        assert response is not None
        assert isinstance(response.CurrentSensorPVRaw.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetSensorSlope(self, UnitID):
        response = self.sila_client.DOServicer_GetSensorSlope(UnitID)
        assert response is not None
        assert isinstance(response.CurrentSensorSlope.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetSensorCompensation(self, UnitID):
        response = self.sila_client.DOServicer_GetSensorCompensation(UnitID)
        assert response is not None
        assert isinstance(response.CurrentSensorCompensation.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetControllerDB(self, UnitID):
        response = self.sila_client.DOServicer_GetControllerDB(UnitID)
        assert response is not None
        assert isinstance(response.CurrentControllerDB.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetControllerOut(self, UnitID):
        response = self.sila_client.DOServicer_GetControllerOut(UnitID)
        assert response is not None
        assert isinstance(response.CurrentControllerOut.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetControllerP(self, UnitID):
        response = self.sila_client.DOServicer_GetControllerP(UnitID)
        assert response is not None
        assert isinstance(response.CurrentControllerP.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetControllerTd(self, UnitID):
        response = self.sila_client.DOServicer_GetControllerTd(UnitID)
        assert response is not None
        assert isinstance(response.CurrentControllerTd.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetControllerTi(self, UnitID):
        response = self.sila_client.DOServicer_GetControllerTi(UnitID)
        assert response is not None
        assert isinstance(response.CurrentControllerTi.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetControllerMin(self, UnitID):
        response = self.sila_client.DOServicer_GetControllerMin(UnitID)
        assert response is not None
        assert isinstance(response.CurrentControllerMin.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetControllerMax(self, UnitID):
        response = self.sila_client.DOServicer_GetControllerMax(UnitID)
        assert response is not None
        assert isinstance(response.CurrentControllerMax.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetAlarmEnabled(self, UnitID):
        response = self.sila_client.DOServicer_GetAlarmEnabled(UnitID)
        assert response is not None
        assert isinstance(response.CurrentAlarmEnabled.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetAlarmAlarmHigh(self, UnitID):
        response = self.sila_client.DOServicer_GetAlarmAlarmHigh(UnitID)
        assert response is not None
        assert isinstance(response.CurrentAlarmAlarmHigh.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetAlarmAlarmLow(self, UnitID):
        response = self.sila_client.DOServicer_GetAlarmAlarmLow(UnitID)
        assert response is not None
        assert isinstance(response.CurrentAlarmAlarmLow.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetAlarmMode(self, UnitID):
        response = self.sila_client.DOServicer_GetAlarmMode(UnitID)
        assert response is not None
        assert isinstance(response.CurrentAlarmMode.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetAlarmState(self, UnitID):
        response = self.sila_client.DOServicer_GetAlarmState(UnitID)
        assert response is not None
        assert isinstance(response.CurrentAlarmState.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetAlarmDelay(self, UnitID):
        response = self.sila_client.DOServicer_GetAlarmDelay(UnitID)
        assert response is not None
        assert isinstance(response.CurrentAlarmDelay.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetAlarmWarnHigh(self, UnitID):
        response = self.sila_client.DOServicer_GetAlarmWarnHigh(UnitID)
        assert response is not None
        assert isinstance(response.CurrentAlarmWarnHigh.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetAlarmWarnLow(self, UnitID):
        response = self.sila_client.DOServicer_GetAlarmWarnLow(UnitID)
        assert response is not None
        assert isinstance(response.CurrentAlarmWarnLow.value, float)


class TestDOServicerSet:
    """ Test all DOServicer Set functions. Control a DASGIP DO module. Enables read and write operations for various parameters, including DO sensor, controller, and alarm. """
    sila_client = DASGIP_ServiceClient(server_ip=ip, server_port=port)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(0, val_range)])  # float
    def test_SetSPM(self, UnitID, val):
        """ Set the manual temperature setpoint.
        :param UnitID: The UnitID of the addressed reactor"""
        response = self.sila_client.DOServicer_SetSPM(UnitID, val)
        assert response is not None
        assert isinstance(response.SPMSet.value, float)
        # assert response.SPMSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(0, val_range)])  # float
    def test_SetSPE(self, UnitID, val):
        response = self.sila_client.DOServicer_SetSPE(UnitID, val)
        assert response is not None
        assert isinstance(response.SPESet.value, float)
        # assert response.SPESet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', random.sample(range(0, 3), 1))  # int
    def test_SetCmd(self, UnitID, val):
        response = self.sila_client.DOServicer_SetCmd(UnitID, val)
        assert response is not None
        assert isinstance(response.CmdSet.value, int)
        # assert response.CmdSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', random.sample(range(0, 3), 1))  # int
    def test_SetMode(self, UnitID, val):
        response = self.sila_client.DOServicer_SetMode(UnitID, val)
        assert response is not None
        assert isinstance(response.ModeSet.value, int)
        # assert response.ModeSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', random.sample(range(0, 6), 1))  # int
    def test_SetSetpointSelect(self, UnitID, val):
        response = self.sila_client.DOServicer_SetSetpointSelect(UnitID, val)
        assert response is not None
        assert isinstance(response.SetpointSelectSet.value, int)
        # assert response.SetpointSelectSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(0, val_range)])  # float, implement more meaningful range
    def test_SetSensorOffset(self, UnitID, val):
        response = self.sila_client.DOServicer_SetSensorOffset(UnitID, val)
        assert response is not None
        assert isinstance(response.SensorOffsetSet.value, float)
        # assert response.SensorOffsetSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(0, val_range)])  # float, implement more meaningful range
    def test_SetSensorSlope(self, UnitID, val):
        response = self.sila_client.DOServicer_SetSensorSlope(UnitID, val)
        assert response is not None
        assert isinstance(response.SensorSlopeSet.value, float)
        # assert response.SensorSlopeSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(0, val_range)])  # float, implement more meaningful range
    def test_SetSensorCompensation(self, UnitID, val):
        response = self.sila_client.DOServicer_SetSensorCompensation(UnitID, val)
        assert response is not None
        assert isinstance(response.SensorCompensationSet.value, float)
        # assert response.SensorCompensationSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(0, val_range)])  # float, implement more meaningful range
    def test_SetControllerDB(self, UnitID, val):
        """ Set the controller deadband value. PID controller: deadband (set to zero to disable). """
        response = self.sila_client.DOServicer_SetControllerDB(UnitID, val)
        assert response is not None
        assert isinstance(response.ControllerDBSet.value, float)
        # assert response.ControllerDBSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(0, val_range)])  # float, implement more meaningful range
    def test_SetControllerP(self, UnitID, val):
        """ Set the controller deadband value. PID controller: deadband (set to zero to disable). """
        response = self.sila_client.DOServicer_SetControllerP(UnitID, val)
        assert response is not None
        assert isinstance(response.ControllerPSet.value, float)
        # assert response.ControllerPSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(0, val_range)])  # float, implement more meaningful range
    def test_SetControllerTd(self, UnitID, val):
        """ Set the controller differentiator time constant. PID controller: differentiator time constant (set to zero to disable). """
        response = self.sila_client.DOServicer_SetControllerTd(UnitID, val)
        assert response is not None
        assert isinstance(response.ControllerTdSet.value, float)
        # assert response.ControllerTdSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(0, val_range)])  # float, implement more meaningful range
    def test_SetControllerTi(self, UnitID, val):
        """ Set the controller integrator time constant. PID controller: integrator time constant (set to zero to disable). """
        response = self.sila_client.DOServicer_SetControllerTi(UnitID, val)
        assert response is not None
        assert isinstance(response.ControllerTiSet.value, float)
        # assert response.ControllerTiSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(0, val_range)])  # float, implement more meaningful range
    def test_SetControllerMin(self, UnitID, val):
        """ Set the controller minimal output value. PID controller: minimal output value. """
        response = self.sila_client.DOServicer_SetControllerMin(UnitID, val)
        assert response is not None
        assert isinstance(response.ControllerMinSet.value, float)
        # assert response.ControllerMinSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(0, val_range)])  # float, implement more meaningful range
    def test_SetControllerMax(self, UnitID, val):
        """ Set the controller maximal output value. PID controller: maximal output value. """
        response = self.sila_client.DOServicer_SetControllerMax(UnitID, val)
        assert response is not None
        assert isinstance(response.ControllerMaxSet.value, float)
        # assert response.ControllerMaxSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', random.sample(range(0, 2), 1)) # int [0, 1]
    def test_SetAlarmEnabled(self, UnitID, val):
        """ Set the alarm enabled value. Enables alarm function. """
        response = self.sila_client.DOServicer_SetAlarmEnabled(UnitID, val)
        assert response is not None
        assert isinstance(response.AlarmEnabledSet.value, int)
        # assert response.AlarmEnabledSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(0, val_range)])  # float, implement more meaningful range
    def test_SetAlarmAlarmHigh(self, UnitID, val):
        """ The alarm alarmhigh value. Higher alarm limit. """
        response = self.sila_client.DOServicer_SetAlarmAlarmHigh(UnitID, val)
        assert response is not None
        assert isinstance(response.AlarmAlarmHighSet.value, float)
        # assert response.AlarmAlarmHighSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(0, val_range)])  # float, implement more meaningful range
    def test_SetAlarmAlarmLow(self, UnitID, val):
        """ The alarm alarmLow value. Lower alarm limit. """
        response = self.sila_client.DOServicer_SetAlarmAlarmLow(UnitID, val)
        assert response is not None
        assert isinstance(response.AlarmAlarmLowSet.value, float)
        # assert response.AlarmAlarmLowSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', random.sample(range(0, 2), 1)) # int [0, 1]
    def test_SetAlarmMode(self, UnitID, val):
        """ The alarm mode value. Alarm mode. """
        response = self.sila_client.DOServicer_SetAlarmMode(UnitID, val)
        assert response is not None
        assert isinstance(response.AlarmModeSet.value, int)
        # assert response.AlarmModeSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(0, val_range)])  # float, implement more meaningful range
    def test_SetAlarmDelay(self, UnitID, val):
        """ Set the alarm delay value. Alarm hysteresis time. """
        response = self.sila_client.DOServicer_SetAlarmDelay(UnitID, val)
        assert response is not None
        assert isinstance(response.AlarmDelaySet.value, float)
        # assert response.AlarmDelaySet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(0, val_range)])  # float, implement more meaningful range
    def test_SetAlarmWarnHigh(self, UnitID, val):
        response = self.sila_client.DOServicer_SetAlarmWarnHigh(UnitID, val)
        assert response is not None
        assert isinstance(response.AlarmWarnHighSet.value, float)
        # assert response.AlarmWarnHighSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(0, val_range)])  # float, implement more meaningful range
    def test_SetAlarmWarnLow(self, UnitID, val):
        response = self.sila_client.DOServicer_SetAlarmWarnLow(UnitID, val)
        assert response is not None
        assert isinstance(response.AlarmWarnLowSet.value, float)
        # assert response.AlarmWarnLowSet.value == val


class TestLevelServicerGet:
    """ Test all LevelServicer Get functions. Control a DASGIP level module. Enables read and write operations for various parameters, including level sensor and alarm. """
    sila_client = DASGIP_ServiceClient(server_ip=ip, server_port=port)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetPV(self, UnitID):
        """ :param UnitID: The UnitID of the addressed reactor"""
        response = self.sila_client.LevelServicer_GetPV(UnitID)
        assert response is not None
        assert isinstance(response.CurrentPV.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetType(self, UnitID):
        response = self.sila_client.LevelServicer_GetType(UnitID)
        assert response is not None
        assert isinstance(response.CurrentType.value, str)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetAvailable(self, UnitID):
        response = self.sila_client.LevelServicer_GetAvailable(UnitID)
        assert response is not None
        assert isinstance(response.CurrentAvailable.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetName(self, UnitID):
        response = self.sila_client.LevelServicer_GetName(UnitID)
        assert response is not None
        assert isinstance(response.CurrentName.value, str)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetVersion(self, UnitID):
        response = self.sila_client.LevelServicer_GetVersion(UnitID)
        assert response is not None
        assert isinstance(response.CurrentVersion.value, str)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetSensorPVRaw(self, UnitID):
        response = self.sila_client.LevelServicer_GetSensorPVRaw(UnitID)
        assert response is not None
        assert isinstance(response.CurrentSensorPVRaw.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetSensorSlope(self, UnitID):
        response = self.sila_client.LevelServicer_GetSensorSlope(UnitID)
        assert response is not None
        assert isinstance(response.CurrentSensorSlope.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetAlarmEnabled(self, UnitID):
        response = self.sila_client.LevelServicer_GetAlarmEnabled(UnitID)
        assert response is not None
        assert isinstance(response.CurrentAlarmEnabled.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetAlarmAlarmHigh(self, UnitID):
        response = self.sila_client.LevelServicer_GetAlarmAlarmHigh(UnitID)
        assert response is not None
        assert isinstance(response.CurrentAlarmAlarmHigh.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetAlarmAlarmLow(self, UnitID):
        response = self.sila_client.LevelServicer_GetAlarmAlarmLow(UnitID)
        assert response is not None
        assert isinstance(response.CurrentAlarmAlarmLow.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetAlarmMode(self, UnitID):
        response = self.sila_client.LevelServicer_GetAlarmMode(UnitID)
        assert response is not None
        assert isinstance(response.CurrentAlarmMode.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetAlarmState(self, UnitID):
        response = self.sila_client.LevelServicer_GetAlarmState(UnitID)
        assert response is not None
        assert isinstance(response.CurrentAlarmState.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetAlarmDelay(self, UnitID):
        response = self.sila_client.LevelServicer_GetAlarmDelay(UnitID)
        assert response is not None
        assert isinstance(response.CurrentAlarmDelay.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetAlarmWarnHigh(self, UnitID):
        response = self.sila_client.LevelServicer_GetAlarmWarnHigh(UnitID)
        assert response is not None
        assert isinstance(response.CurrentAlarmWarnHigh.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetAlarmWarnLow(self, UnitID):
        response = self.sila_client.LevelServicer_GetAlarmWarnLow(UnitID)
        assert response is not None
        assert isinstance(response.CurrentAlarmWarnLow.value, float)


class TestLevelServicerSet:
    """ Test all LevelServicer Set functions. Control a DASGIP level module. Enables read and write operations for various parameters, including level sensor and alarm. """
    sila_client = DASGIP_ServiceClient(server_ip=ip, server_port=port)

# level servicer has no SetSensorSlope, right?
#     @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
#     @pytest.mark.parametrize('val', [random.uniform(0, val_range)])  # float, implement more meaningful range
#     def test_SetSensorSlope(self, UnitID, val):
#         response = self.sila_client.LevelServicer_SetSensorSlope(UnitID, val)
#         assert response is not None
#         assert isinstance(response.SensorSlopeSet.value, float)
#         # assert response.SensorSlopeSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', random.sample(range(0, 2), 1)) # int [0, 1]
    def test_SetAlarmEnabled(self, UnitID, val):
        """ Set the alarm enabled value. Enables alarm function. """
        response = self.sila_client.LevelServicer_SetAlarmEnabled(UnitID, val)
        assert response is not None
        assert isinstance(response.AlarmEnabledSet.value, int)
        # assert response.AlarmEnabledSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(0, val_range)])  # float, implement more meaningful range
    def test_SetAlarmAlarmHigh(self, UnitID, val):
        """ The alarm alarmhigh value. Higher alarm limit. """
        response = self.sila_client.LevelServicer_SetAlarmAlarmHigh(UnitID, val)
        assert response is not None
        assert isinstance(response.AlarmAlarmHighSet.value, float)
        # assert response.AlarmAlarmHighSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(0, val_range)])  # float, implement more meaningful range
    def test_SetAlarmAlarmLow(self, UnitID, val):
        """ The alarm alarmLow value. Lower alarm limit. """
        response = self.sila_client.LevelServicer_SetAlarmAlarmLow(UnitID, val)
        assert response is not None
        assert isinstance(response.AlarmAlarmLowSet.value, float)
        # assert response.AlarmAlarmLowSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', random.sample(range(0, 2), 1)) # int [0, 1]
    def test_SetAlarmMode(self, UnitID, val):
        """ The alarm mode value. Alarm mode. """
        response = self.sila_client.LevelServicer_SetAlarmMode(UnitID, val)
        assert response is not None
        assert isinstance(response.AlarmModeSet.value, int)
        # assert response.AlarmModeSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(0, val_range)])  # float, implement more meaningful range
    def test_SetAlarmDelay(self, UnitID, val):
        """ Set the alarm delay value. Alarm hysteresis time. """
        response = self.sila_client.LevelServicer_SetAlarmDelay(UnitID, val)
        assert response is not None
        assert isinstance(response.AlarmDelaySet.value, float)
        # assert response.AlarmDelaySet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(0, val_range)])  # float, implement more meaningful range
    def test_SetAlarmWarnHigh(self, UnitID, val):
        response = self.sila_client.LevelServicer_SetAlarmWarnHigh(UnitID, val)
        assert response is not None
        assert isinstance(response.AlarmWarnHighSet.value, float)
        # assert response.AlarmWarnHighSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(0, val_range)])  # float, implement more meaningful range
    def test_SetAlarmWarnLow(self, UnitID, val):
        response = self.sila_client.LevelServicer_SetAlarmWarnLow(UnitID, val)
        assert response is not None
        assert isinstance(response.AlarmWarnLowSet.value, float)
        # assert response.AlarmWarnLowSet.value == val


class TestPHServicerGet:
    """ Test all PHServicer Get functions. Control a DASGIP Redox module. Enables read and write operations for various parameters, including Redox sensor, controller, and alarm.  """
    sila_client = DASGIP_ServiceClient(server_ip=ip, server_port=port)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetPV(self, UnitID):
        """ :param UnitID: The UnitID of the addressed reactor"""
        response = self.sila_client.PHServicer_GetPV(UnitID)
        assert response is not None
        assert isinstance(response.CurrentPV.value, float)
        # assert response.CurrentPV.value == UnitID  # this makes no sence i guess

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetSP(self, UnitID):
        response = self.sila_client.PHServicer_GetSP(UnitID)
        assert response is not None
        assert isinstance(response.CurrentSP.value, float)
        # assert response.CurrentSP.value == UnitID  # this makes no sence i guess

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetSPA(self, UnitID):
        response = self.sila_client.PHServicer_GetSPA(UnitID)
        assert response is not None
        assert isinstance(response.CurrentSPA.value, float)
        # assert response.CurrentSPA.value == UnitID  # this makes no sence i guess

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetSPM(self, UnitID):
        response = self.sila_client.PHServicer_GetSPM(UnitID)
        assert response is not None
        assert isinstance(response.CurrentSPM.value, float)
        # assert response.CurrentSPM.value == UnitID  # this makes no sence i guess

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetSPE(self, UnitID):
        response = self.sila_client.PHServicer_GetSPE(UnitID)
        assert response is not None
        assert isinstance(response.CurrentSPE.value, float)
        # assert response.CurrentSPE.value == UnitID  # this makes no sence i guess

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetSPR(self, UnitID):
        response = self.sila_client.PHServicer_GetSPR(UnitID)
        assert response is not None
        assert isinstance(response.CurrentSPR.value, float)
        # assert response.CurrentSPR.value == UnitID  # this makes no sence i guess

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetAccess(self, UnitID):
        response = self.sila_client.PHServicer_GetAccess(UnitID)
        assert response is not None
        assert isinstance(response.CurrentAccess.value, int)
        # assert response.CurrentAccess.value == UnitID  # this makes no sence i guess

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetCmd(self, UnitID):
        response = self.sila_client.PHServicer_GetCmd(UnitID)
        assert response is not None
        assert isinstance(response.CurrentCmd.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetMode(self, UnitID):
        response = self.sila_client.PHServicer_GetMode(UnitID)
        assert response is not None
        assert isinstance(response.CurrentMode.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetSetpointSelect(self, UnitID):
        response = self.sila_client.PHServicer_GetSetpointSelect(UnitID)
        assert response is not None
        assert isinstance(response.CurrentSetpointSelect.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetState(self, UnitID):
        response = self.sila_client.PHServicer_GetState(UnitID)
        assert response is not None
        assert isinstance(response.CurrentState.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetType(self, UnitID):
        response = self.sila_client.PHServicer_GetType(UnitID)
        assert response is not None
        assert isinstance(response.CurrentType.value, str)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetAvailable(self, UnitID):
        response = self.sila_client.PHServicer_GetAvailable(UnitID)
        assert response is not None
        assert isinstance(response.CurrentAvailable.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetName(self, UnitID):
        response = self.sila_client.PHServicer_GetName(UnitID)
        assert response is not None
        assert isinstance(response.CurrentName.value, str)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetVersion(self, UnitID):
        response = self.sila_client.PHServicer_GetVersion(UnitID)
        assert response is not None
        assert isinstance(response.CurrentVersion.value, str)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetSensorOffset(self, UnitID):
        response = self.sila_client.PHServicer_GetSensorOffset(UnitID)
        assert response is not None
        assert isinstance(response.CurrentSensorOffset.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetSensorPVRaw(self, UnitID):
        response = self.sila_client.PHServicer_GetSensorPVRaw(UnitID)
        assert response is not None
        assert isinstance(response.CurrentSensorPVRaw.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetSensorCompensation(self, UnitID):
        response = self.sila_client.PHServicer_GetSensorCompensation(UnitID)
        assert response is not None
        assert isinstance(response.CurrentSensorCompensation.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetControllerDB(self, UnitID):
        response = self.sila_client.PHServicer_GetControllerDB(UnitID)
        assert response is not None
        assert isinstance(response.CurrentControllerDB.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetControllerOut(self, UnitID):
        response = self.sila_client.PHServicer_GetControllerOut(UnitID)
        assert response is not None
        assert isinstance(response.CurrentControllerOut.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetControllerP(self, UnitID):
        response = self.sila_client.PHServicer_GetControllerP(UnitID)
        assert response is not None
        assert isinstance(response.CurrentControllerP.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetControllerTd(self, UnitID):
        response = self.sila_client.PHServicer_GetControllerTd(UnitID)
        assert response is not None
        assert isinstance(response.CurrentControllerTd.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetControllerTi(self, UnitID):
        response = self.sila_client.PHServicer_GetControllerTi(UnitID)
        assert response is not None
        assert isinstance(response.CurrentControllerTi.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetControllerMin(self, UnitID):
        response = self.sila_client.PHServicer_GetControllerMin(UnitID)
        assert response is not None
        assert isinstance(response.CurrentControllerMin.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetControllerMax(self, UnitID):
        response = self.sila_client.PHServicer_GetControllerMax(UnitID)
        assert response is not None
        assert isinstance(response.CurrentControllerMax.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetAlarmEnabled(self, UnitID):
        response = self.sila_client.PHServicer_GetAlarmEnabled(UnitID)
        assert response is not None
        assert isinstance(response.CurrentAlarmEnabled.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetAlarmAlarmHigh(self, UnitID):
        response = self.sila_client.PHServicer_GetAlarmAlarmHigh(UnitID)
        assert response is not None
        assert isinstance(response.CurrentAlarmAlarmHigh.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetAlarmAlarmLow(self, UnitID):
        response = self.sila_client.PHServicer_GetAlarmAlarmLow(UnitID)
        assert response is not None
        assert isinstance(response.CurrentAlarmAlarmLow.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetAlarmMode(self, UnitID):
        response = self.sila_client.PHServicer_GetAlarmMode(UnitID)
        assert response is not None
        assert isinstance(response.CurrentAlarmMode.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetAlarmState(self, UnitID):
        response = self.sila_client.PHServicer_GetAlarmState(UnitID)
        assert response is not None
        assert isinstance(response.CurrentAlarmState.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetAlarmDelay(self, UnitID):
        response = self.sila_client.PHServicer_GetAlarmDelay(UnitID)
        assert response is not None
        assert isinstance(response.CurrentAlarmDelay.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetAlarmWarnHigh(self, UnitID):
        response = self.sila_client.PHServicer_GetAlarmWarnHigh(UnitID)
        assert response is not None
        assert isinstance(response.CurrentAlarmWarnHigh.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetAlarmWarnLow(self, UnitID):
        response = self.sila_client.PHServicer_GetAlarmWarnLow(UnitID)
        assert response is not None
        assert isinstance(response.CurrentAlarmWarnLow.value, float)


class TestPHServicerSet:
    """ Test all PHServicer Set functions. Control a DASGIP Redox module. Enables read and write operations for various parameters, including Redox sensor, controller, and alarm.  """
    sila_client = DASGIP_ServiceClient(server_ip=ip, server_port=port)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(0, val_range)])  # float
    def test_SetSPM(self, UnitID, val):
        """ Set the manual temperature setpoint.
        :param UnitID: The UnitID of the addressed reactor"""
        response = self.sila_client.PHServicer_SetSPM(UnitID, val)
        assert response is not None
        assert isinstance(response.SPMSet.value, float)
        # assert response.SPMSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(0, val_range)])  # float
    def test_SetSPE(self, UnitID, val):
        response = self.sila_client.PHServicer_SetSPE(UnitID, val)
        assert response is not None
        assert isinstance(response.SPESet.value, float)
        # assert response.SPESet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', random.sample(range(0, 3), 1))  # int
    def test_SetCmd(self, UnitID, val):
        response = self.sila_client.PHServicer_SetCmd(UnitID, val)
        assert response is not None
        assert isinstance(response.CmdSet.value, int)
        # assert response.CmdSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', random.sample(range(0, 3), 1))  # int
    def test_SetMode(self, UnitID, val):
        response = self.sila_client.PHServicer_SetMode(UnitID, val)
        assert response is not None
        assert isinstance(response.ModeSet.value, int)
        # assert response.ModeSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', random.sample(range(0, 6), 1))  # int
    def test_SetSetpointSelect(self, UnitID, val):
        response = self.sila_client.PHServicer_SetSetpointSelect(UnitID, val)
        assert response is not None
        assert isinstance(response.SetpointSelectSet.value, int)
        # assert response.SetpointSelectSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(0, val_range)])  # float, implement more meaningful range
    def test_SetSensorOffset(self, UnitID, val):
        response = self.sila_client.PHServicer_SetSensorOffset(UnitID, val)
        assert response is not None
        assert isinstance(response.SensorOffsetSet.value, float)
        # assert response.SensorOffsetSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(0, val_range)])  # float, implement more meaningful range
    def test_SetSensorCompensation(self, UnitID, val):
        response = self.sila_client.PHServicer_SetSensorCompensation(UnitID, val)
        assert response is not None
        assert isinstance(response.SensorCompensationSet.value, float)
        # assert response.SensorCompensationSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(0, val_range)])  # float, implement more meaningful range
    def test_SetControllerDB(self, UnitID, val):
        """ Set the controller deadband value. PID controller: deadband (set to zero to disable). """
        response = self.sila_client.PHServicer_SetControllerDB(UnitID, val)
        assert response is not None
        assert isinstance(response.ControllerDBSet.value, float)
        # assert response.ControllerDBSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(0, val_range)])  # float, implement more meaningful range
    def test_SetControllerP(self, UnitID, val):
        """ Set the controller deadband value. PID controller: deadband (set to zero to disable). """
        response = self.sila_client.PHServicer_SetControllerP(UnitID, val)
        assert response is not None
        assert isinstance(response.ControllerPSet.value, float)
        # assert response.ControllerPSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(0, val_range)])  # float, implement more meaningful range
    def test_SetControllerTd(self, UnitID, val):
        """ Set the controller differentiator time constant. PID controller: differentiator time constant (set to zero to disable). """
        response = self.sila_client.PHServicer_SetControllerTd(UnitID, val)
        assert response is not None
        assert isinstance(response.ControllerTdSet.value, float)
        # assert response.ControllerTdSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(0, val_range)])  # float, implement more meaningful range
    def test_SetControllerTi(self, UnitID, val):
        """ Set the controller integrator time constant. PID controller: integrator time constant (set to zero to disable). """
        response = self.sila_client.PHServicer_SetControllerTi(UnitID, val)
        assert response is not None
        assert isinstance(response.ControllerTiSet.value, float)
        # assert response.ControllerTiSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(0, val_range)])  # float, implement more meaningful range
    def test_SetControllerMin(self, UnitID, val):
        """ Set the controller minimal output value. PID controller: minimal output value. """
        response = self.sila_client.PHServicer_SetControllerMin(UnitID, val)
        assert response is not None
        assert isinstance(response.ControllerMinSet.value, float)
        # assert response.ControllerMinSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(0, val_range)])  # float, implement more meaningful range
    def test_SetControllerMax(self, UnitID, val):
        """ Set the controller maximal output value. PID controller: maximal output value. """
        response = self.sila_client.PHServicer_SetControllerMax(UnitID, val)
        assert response is not None
        assert isinstance(response.ControllerMaxSet.value, float)
        # assert response.ControllerMaxSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', random.sample(range(0, 2), 1)) # int [0, 1]
    def test_SetAlarmEnabled(self, UnitID, val):
        """ Set the alarm enabled value. Enables alarm function. """
        response = self.sila_client.PHServicer_SetAlarmEnabled(UnitID, val)
        assert response is not None
        assert isinstance(response.AlarmEnabledSet.value, int)
        # assert response.AlarmEnabledSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(0, val_range)])  # float, implement more meaningful range
    def test_SetAlarmAlarmHigh(self, UnitID, val):
        """ The alarm alarmhigh value. Higher alarm limit. """
        response = self.sila_client.PHServicer_SetAlarmAlarmHigh(UnitID, val)
        assert response is not None
        assert isinstance(response.AlarmAlarmHighSet.value, float)
        # assert response.AlarmAlarmHighSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(0, val_range)])  # float, implement more meaningful range
    def test_SetAlarmAlarmLow(self, UnitID, val):
        """ The alarm alarmLow value. Lower alarm limit. """
        response = self.sila_client.PHServicer_SetAlarmAlarmLow(UnitID, val)
        assert response is not None
        assert isinstance(response.AlarmAlarmLowSet.value, float)
        # assert response.AlarmAlarmLowSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', random.sample(range(0, 2), 1)) # int [0, 1]
    def test_SetAlarmMode(self, UnitID, val):
        """ The alarm mode value. Alarm mode. """
        response = self.sila_client.PHServicer_SetAlarmMode(UnitID, val)
        assert response is not None
        assert isinstance(response.AlarmModeSet.value, int)
        # assert response.AlarmModeSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(0, val_range)])  # float, implement more meaningful range
    def test_SetAlarmDelay(self, UnitID, val):
        """ Set the alarm delay value. Alarm hysteresis time. """
        response = self.sila_client.PHServicer_SetAlarmDelay(UnitID, val)
        assert response is not None
        assert isinstance(response.AlarmDelaySet.value, float)
        # assert response.AlarmDelaySet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(0, val_range)])  # float, implement more meaningful range
    def test_SetAlarmWarnHigh(self, UnitID, val):
        response = self.sila_client.PHServicer_SetAlarmWarnHigh(UnitID, val)
        assert response is not None
        assert isinstance(response.AlarmWarnHighSet.value, float)
        # assert response.AlarmWarnHighSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(0, val_range)])  # float, implement more meaningful range
    def test_SetAlarmWarnLow(self, UnitID, val):
        response = self.sila_client.PHServicer_SetAlarmWarnLow(UnitID, val)
        assert response is not None
        assert isinstance(response.AlarmWarnLowSet.value, float)
        # assert response.AlarmWarnLowSet.value == val


class TestPressureServicerGet:
    """ Test all PressureServicer Get functions. Control a DASGIP pressure module. Enables read and write operations for various parameters, including pressure sensor and controller.  """
    sila_client = DASGIP_ServiceClient(server_ip=ip, server_port=port)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetPV(self, UnitID):
        """ :param UnitID: The UnitID of the addressed reactor"""
        response = self.sila_client.PressureServicer_GetPV(UnitID)
        assert response is not None
        assert isinstance(response.CurrentPV.value, float)
        # assert response.CurrentPV.value == UnitID  # this makes no sence i guess

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetSP(self, UnitID):
        response = self.sila_client.PressureServicer_GetSP(UnitID)
        assert response is not None
        assert isinstance(response.CurrentSP.value, float)
        # assert response.CurrentSP.value == UnitID  # this makes no sence i guess

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetSPA(self, UnitID):
        response = self.sila_client.PressureServicer_GetSPA(UnitID)
        assert response is not None
        assert isinstance(response.CurrentSPA.value, float)
        # assert response.CurrentSPA.value == UnitID  # this makes no sence i guess

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetSPM(self, UnitID):
        response = self.sila_client.PressureServicer_GetSPM(UnitID)
        assert response is not None
        assert isinstance(response.CurrentSPM.value, float)
        # assert response.CurrentSPM.value == UnitID  # this makes no sence i guess

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetSPE(self, UnitID):
        response = self.sila_client.PressureServicer_GetSPE(UnitID)
        assert response is not None
        assert isinstance(response.CurrentSPE.value, float)
        # assert response.CurrentSPE.value == UnitID  # this makes no sence i guess

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetSPR(self, UnitID):
        response = self.sila_client.PressureServicer_GetSPR(UnitID)
        assert response is not None
        assert isinstance(response.CurrentSPR.value, float)
        # assert response.CurrentSPR.value == UnitID  # this makes no sence i guess

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetAccess(self, UnitID):
        response = self.sila_client.PressureServicer_GetAccess(UnitID)
        assert response is not None
        assert isinstance(response.CurrentAccess.value, int)
        # assert response.CurrentAccess.value == UnitID  # this makes no sence i guess

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetCmd(self, UnitID):
        response = self.sila_client.PressureServicer_GetCmd(UnitID)
        assert response is not None
        assert isinstance(response.CurrentCmd.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetMode(self, UnitID):
        response = self.sila_client.PressureServicer_GetMode(UnitID)
        assert response is not None
        assert isinstance(response.CurrentMode.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetSetpointSelect(self, UnitID):
        response = self.sila_client.PressureServicer_GetSetpointSelect(UnitID)
        assert response is not None
        assert isinstance(response.CurrentSetpointSelect.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetState(self, UnitID):
        response = self.sila_client.PressureServicer_GetState(UnitID)
        assert response is not None
        assert isinstance(response.CurrentState.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetType(self, UnitID):
        response = self.sila_client.PressureServicer_GetType(UnitID)
        assert response is not None
        assert isinstance(response.CurrentType.value, str)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetAvailable(self, UnitID):
        response = self.sila_client.PressureServicer_GetAvailable(UnitID)
        assert response is not None
        assert isinstance(response.CurrentAvailable.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetName(self, UnitID):
        response = self.sila_client.PressureServicer_GetName(UnitID)
        assert response is not None
        assert isinstance(response.CurrentName.value, str)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetVersion(self, UnitID):
        response = self.sila_client.PressureServicer_GetVersion(UnitID)
        assert response is not None
        assert isinstance(response.CurrentVersion.value, str)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetSensorOffset(self, UnitID):
        response = self.sila_client.PressureServicer_GetSensorOffset(UnitID)
        assert response is not None
        assert isinstance(response.CurrentSensorOffset.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetSensorPVRaw(self, UnitID):
        response = self.sila_client.PressureServicer_GetSensorPVRaw(UnitID)
        assert response is not None
        assert isinstance(response.CurrentSensorPVRaw.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetSensorCompensation(self, UnitID):
        response = self.sila_client.PressureServicer_GetSensorCompensation(UnitID)
        assert response is not None
        assert isinstance(response.CurrentSensorCompensation.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetControllerDB(self, UnitID):
        response = self.sila_client.PressureServicer_GetControllerDB(UnitID)
        assert response is not None
        assert isinstance(response.CurrentControllerDB.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetControllerOut(self, UnitID):
        response = self.sila_client.PressureServicer_GetControllerOut(UnitID)
        assert response is not None
        assert isinstance(response.CurrentControllerOut.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetControllerP(self, UnitID):
        response = self.sila_client.PressureServicer_GetControllerP(UnitID)
        assert response is not None
        assert isinstance(response.CurrentControllerP.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetControllerTd(self, UnitID):
        response = self.sila_client.PressureServicer_GetControllerTd(UnitID)
        assert response is not None
        assert isinstance(response.CurrentControllerTd.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetControllerTi(self, UnitID):
        response = self.sila_client.PressureServicer_GetControllerTi(UnitID)
        assert response is not None
        assert isinstance(response.CurrentControllerTi.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetControllerMin(self, UnitID):
        response = self.sila_client.PressureServicer_GetControllerMin(UnitID)
        assert response is not None
        assert isinstance(response.CurrentControllerMin.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetControllerMax(self, UnitID):
        response = self.sila_client.PressureServicer_GetControllerMax(UnitID)
        assert response is not None
        assert isinstance(response.CurrentControllerMax.value, float)


class TestPressureServicerSet:
    """ Test all PressureServicer Set functions. Control a DASGIP pressure module. Enables read and write operations for various parameters, including pressure sensor and controller.  """
    sila_client = DASGIP_ServiceClient(server_ip=ip, server_port=port)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(0, val_range)])  # float
    def test_SetSPM(self, UnitID, val):
        """ Set the manual temperature setpoint.
        :param UnitID: The UnitID of the addressed reactor"""
        response = self.sila_client.PressureServicer_SetSPM(UnitID, val)
        assert response is not None
        assert isinstance(response.SPMSet.value, float)
        # assert response.SPMSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(0, val_range)])  # float
    def test_SetSPE(self, UnitID, val):
        response = self.sila_client.PressureServicer_SetSPE(UnitID, val)
        assert response is not None
        assert isinstance(response.SPESet.value, float)
        # assert response.SPESet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', random.sample(range(0, 3), 1))  # int
    def test_SetCmd(self, UnitID, val):
        response = self.sila_client.PressureServicer_SetCmd(UnitID, val)
        assert response is not None
        assert isinstance(response.CmdSet.value, int)
        # assert response.CmdSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', random.sample(range(0, 3), 1))  # int
    def test_SetMode(self, UnitID, val):
        response = self.sila_client.PressureServicer_SetMode(UnitID, val)
        assert response is not None
        assert isinstance(response.ModeSet.value, int)
        # assert response.ModeSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', random.sample(range(0, 6), 1))  # int
    def test_SetSetpointSelect(self, UnitID, val):
        response = self.sila_client.PressureServicer_SetSetpointSelect(UnitID, val)
        assert response is not None
        assert isinstance(response.SetpointSelectSet.value, int)
        # assert response.SetpointSelectSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(0, val_range)])  # float, implement more meaningful range
    def test_SetSensorOffset(self, UnitID, val):
        response = self.sila_client.PressureServicer_SetSensorOffset(UnitID, val)
        assert response is not None
        assert isinstance(response.SensorOffsetSet.value, float)
        # assert response.SensorOffsetSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(0, val_range)])  # float, implement more meaningful range
    def test_SetSensorCompensation(self, UnitID, val):
        response = self.sila_client.PressureServicer_SetSensorCompensation(UnitID, val)
        assert response is not None
        assert isinstance(response.SensorCompensationSet.value, float)
        # assert response.SensorCompensationSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(0, val_range)])  # float, implement more meaningful range
    def test_SetControllerDB(self, UnitID, val):
        """ Set the controller deadband value. PID controller: deadband (set to zero to disable). """
        response = self.sila_client.PressureServicer_SetControllerDB(UnitID, val)
        assert response is not None
        assert isinstance(response.ControllerDBSet.value, float)
        # assert response.ControllerDBSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(0, val_range)])  # float, implement more meaningful range
    def test_SetControllerP(self, UnitID, val):
        """ Set the controller deadband value. PID controller: deadband (set to zero to disable). """
        response = self.sila_client.PressureServicer_SetControllerP(UnitID, val)
        assert response is not None
        assert isinstance(response.ControllerPSet.value, float)
        # assert response.ControllerPSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(0, val_range)])  # float, implement more meaningful range
    def test_SetControllerTd(self, UnitID, val):
        """ Set the controller differentiator time constant. PID controller: differentiator time constant (set to zero to disable). """
        response = self.sila_client.PressureServicer_SetControllerTd(UnitID, val)
        assert response is not None
        assert isinstance(response.ControllerTdSet.value, float)
        # assert response.ControllerTdSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(0, val_range)])  # float, implement more meaningful range
    def test_SetControllerTi(self, UnitID, val):
        """ Set the controller integrator time constant. PID controller: integrator time constant (set to zero to disable). """
        response = self.sila_client.PressureServicer_SetControllerTi(UnitID, val)
        assert response is not None
        assert isinstance(response.ControllerTiSet.value, float)
        # assert response.ControllerTiSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(0, val_range)])  # float, implement more meaningful range
    def test_SetControllerMin(self, UnitID, val):
        """ Set the controller minimal output value. PID controller: minimal output value. """
        response = self.sila_client.PressureServicer_SetControllerMin(UnitID, val)
        assert response is not None
        assert isinstance(response.ControllerMinSet.value, float)
        # assert response.ControllerMinSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(0, val_range)])  # float, implement more meaningful range
    def test_SetControllerMax(self, UnitID, val):
        """ Set the controller maximal output value. PID controller: maximal output value. """
        response = self.sila_client.PressureServicer_SetControllerMax(UnitID, val)
        assert response is not None
        assert isinstance(response.ControllerMaxSet.value, float)
        # assert response.ControllerMaxSet.value == val


class TestRedoxServicerGet:
    """ Test all RedoxServicer Get functions. Control a DASGIP Redox module. Enables read and write operations for various parameters, including Redox sensor, controller, and alarm.  """
    sila_client = DASGIP_ServiceClient(server_ip=ip, server_port=port)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetPV(self, UnitID):
        """ :param UnitID: The UnitID of the addressed reactor"""
        response = self.sila_client.RedoxServicer_GetPV(UnitID)
        assert response is not None
        assert isinstance(response.CurrentPV.value, float)
        # assert response.CurrentPV.value == UnitID  # this makes no sence i guess

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetSP(self, UnitID):
        response = self.sila_client.RedoxServicer_GetSP(UnitID)
        assert response is not None
        assert isinstance(response.CurrentSP.value, float)
        # assert response.CurrentSP.value == UnitID  # this makes no sence i guess

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetSPA(self, UnitID):
        response = self.sila_client.RedoxServicer_GetSPA(UnitID)
        assert response is not None
        assert isinstance(response.CurrentSPA.value, float)
        # assert response.CurrentSPA.value == UnitID  # this makes no sence i guess

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetSPM(self, UnitID):
        response = self.sila_client.RedoxServicer_GetSPM(UnitID)
        assert response is not None
        assert isinstance(response.CurrentSPM.value, float)
        # assert response.CurrentSPM.value == UnitID  # this makes no sence i guess

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetSPE(self, UnitID):
        response = self.sila_client.RedoxServicer_GetSPE(UnitID)
        assert response is not None
        assert isinstance(response.CurrentSPE.value, float)
        # assert response.CurrentSPE.value == UnitID  # this makes no sence i guess

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetSPR(self, UnitID):
        response = self.sila_client.RedoxServicer_GetSPR(UnitID)
        assert response is not None
        assert isinstance(response.CurrentSPR.value, float)
        # assert response.CurrentSPR.value == UnitID  # this makes no sence i guess

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetAccess(self, UnitID):
        response = self.sila_client.RedoxServicer_GetAccess(UnitID)
        assert response is not None
        assert isinstance(response.CurrentAccess.value, int)
        # assert response.CurrentAccess.value == UnitID  # this makes no sence i guess

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetCmd(self, UnitID):
        response = self.sila_client.RedoxServicer_GetCmd(UnitID)
        assert response is not None
        assert isinstance(response.CurrentCmd.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetMode(self, UnitID):
        response = self.sila_client.RedoxServicer_GetMode(UnitID)
        assert response is not None
        assert isinstance(response.CurrentMode.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetSetpointSelect(self, UnitID):
        response = self.sila_client.RedoxServicer_GetSetpointSelect(UnitID)
        assert response is not None
        assert isinstance(response.CurrentSetpointSelect.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetState(self, UnitID):
        response = self.sila_client.RedoxServicer_GetState(UnitID)
        assert response is not None
        assert isinstance(response.CurrentState.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetType(self, UnitID):
        response = self.sila_client.RedoxServicer_GetType(UnitID)
        assert response is not None
        assert isinstance(response.CurrentType.value, str)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetAvailable(self, UnitID):
        response = self.sila_client.RedoxServicer_GetAvailable(UnitID)
        assert response is not None
        assert isinstance(response.CurrentAvailable.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetName(self, UnitID):
        response = self.sila_client.RedoxServicer_GetName(UnitID)
        assert response is not None
        assert isinstance(response.CurrentName.value, str)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetVersion(self, UnitID):
        response = self.sila_client.RedoxServicer_GetVersion(UnitID)
        assert response is not None
        assert isinstance(response.CurrentVersion.value, str)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetSensorOffset(self, UnitID):
        response = self.sila_client.RedoxServicer_GetSensorOffset(UnitID)
        assert response is not None
        assert isinstance(response.CurrentSensorOffset.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetSensorPVRaw(self, UnitID):
        response = self.sila_client.RedoxServicer_GetSensorPVRaw(UnitID)
        assert response is not None
        assert isinstance(response.CurrentSensorPVRaw.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetSensorCompensation(self, UnitID):
        response = self.sila_client.RedoxServicer_GetSensorCompensation(UnitID)
        assert response is not None
        assert isinstance(response.CurrentSensorCompensation.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetControllerDB(self, UnitID):
        response = self.sila_client.RedoxServicer_GetControllerDB(UnitID)
        assert response is not None
        assert isinstance(response.CurrentControllerDB.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetControllerOut(self, UnitID):
        response = self.sila_client.RedoxServicer_GetControllerOut(UnitID)
        assert response is not None
        assert isinstance(response.CurrentControllerOut.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetControllerP(self, UnitID):
        response = self.sila_client.RedoxServicer_GetControllerP(UnitID)
        assert response is not None
        assert isinstance(response.CurrentControllerP.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetControllerTd(self, UnitID):
        response = self.sila_client.RedoxServicer_GetControllerTd(UnitID)
        assert response is not None
        assert isinstance(response.CurrentControllerTd.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetControllerTi(self, UnitID):
        response = self.sila_client.RedoxServicer_GetControllerTi(UnitID)
        assert response is not None
        assert isinstance(response.CurrentControllerTi.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetControllerMin(self, UnitID):
        response = self.sila_client.RedoxServicer_GetControllerMin(UnitID)
        assert response is not None
        assert isinstance(response.CurrentControllerMin.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetControllerMax(self, UnitID):
        response = self.sila_client.RedoxServicer_GetControllerMax(UnitID)
        assert response is not None
        assert isinstance(response.CurrentControllerMax.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetAlarmEnabled(self, UnitID):
        response = self.sila_client.RedoxServicer_GetAlarmEnabled(UnitID)
        assert response is not None
        assert isinstance(response.CurrentAlarmEnabled.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetAlarmAlarmHigh(self, UnitID):
        response = self.sila_client.RedoxServicer_GetAlarmAlarmHigh(UnitID)
        assert response is not None
        assert isinstance(response.CurrentAlarmAlarmHigh.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetAlarmAlarmLow(self, UnitID):
        response = self.sila_client.RedoxServicer_GetAlarmAlarmLow(UnitID)
        assert response is not None
        assert isinstance(response.CurrentAlarmAlarmLow.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetAlarmMode(self, UnitID):
        response = self.sila_client.RedoxServicer_GetAlarmMode(UnitID)
        assert response is not None
        assert isinstance(response.CurrentAlarmMode.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetAlarmState(self, UnitID):
        response = self.sila_client.RedoxServicer_GetAlarmState(UnitID)
        assert response is not None
        assert isinstance(response.CurrentAlarmState.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetAlarmDelay(self, UnitID):
        response = self.sila_client.RedoxServicer_GetAlarmDelay(UnitID)
        assert response is not None
        assert isinstance(response.CurrentAlarmDelay.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetAlarmWarnHigh(self, UnitID):
        response = self.sila_client.RedoxServicer_GetAlarmWarnHigh(UnitID)
        assert response is not None
        assert isinstance(response.CurrentAlarmWarnHigh.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetAlarmWarnLow(self, UnitID):
        response = self.sila_client.RedoxServicer_GetAlarmWarnLow(UnitID)
        assert response is not None
        assert isinstance(response.CurrentAlarmWarnLow.value, float)


class TestRedoxServicerSet:
    """ Test all RedoxServicer Set functions. Control a DASGIP Redox module. Enables read and write operations for various parameters, including Redox sensor, controller, and alarm.  """
    sila_client = DASGIP_ServiceClient(server_ip=ip, server_port=port)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(0, val_range)])  # float
    def test_SetSPM(self, UnitID, val):
        """ Set the manual temperature setpoint.
        :param UnitID: The UnitID of the addressed reactor"""
        response = self.sila_client.RedoxServicer_SetSPM(UnitID, val)
        assert response is not None
        assert isinstance(response.SPMSet.value, float)
        # assert response.SPMSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(0, val_range)])  # float
    def test_SetSPE(self, UnitID, val):
        response = self.sila_client.RedoxServicer_SetSPE(UnitID, val)
        assert response is not None
        assert isinstance(response.SPESet.value, float)
        # assert response.SPESet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', random.sample(range(0, 3), 1))  # int
    def test_SetCmd(self, UnitID, val):
        response = self.sila_client.RedoxServicer_SetCmd(UnitID, val)
        assert response is not None
        assert isinstance(response.CmdSet.value, int)
        # assert response.CmdSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', random.sample(range(0, 3), 1))  # int
    def test_SetMode(self, UnitID, val):
        response = self.sila_client.RedoxServicer_SetMode(UnitID, val)
        assert response is not None
        assert isinstance(response.ModeSet.value, int)
        # assert response.ModeSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', random.sample(range(0, 6), 1))  # int
    def test_SetSetpointSelect(self, UnitID, val):
        response = self.sila_client.RedoxServicer_SetSetpointSelect(UnitID, val)
        assert response is not None
        assert isinstance(response.SetpointSelectSet.value, int)
        # assert response.SetpointSelectSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(0, val_range)])  # float, implement more meaningful range
    def test_SetSensorOffset(self, UnitID, val):
        response = self.sila_client.RedoxServicer_SetSensorOffset(UnitID, val)
        assert response is not None
        assert isinstance(response.SensorOffsetSet.value, float)
        # assert response.SensorOffsetSet.value == val 

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(0, val_range)])  # float, implement more meaningful range
    def test_SetSensorCompensation(self, UnitID, val):
        response = self.sila_client.RedoxServicer_SetSensorCompensation(UnitID, val)
        assert response is not None
        assert isinstance(response.SensorCompensationSet.value, float)
        # assert response.SensorCompensationSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(0, val_range)])  # float, implement more meaningful range
    def test_SetControllerDB(self, UnitID, val):
        """ Set the controller deadband value. PID controller: deadband (set to zero to disable). """
        response = self.sila_client.RedoxServicer_SetControllerDB(UnitID, val)
        assert response is not None
        assert isinstance(response.ControllerDBSet.value, float)
        # assert response.ControllerDBSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(0, val_range)])  # float, implement more meaningful range
    def test_SetControllerP(self, UnitID, val):
        """ Set the controller deadband value. PID controller: deadband (set to zero to disable). """
        response = self.sila_client.RedoxServicer_SetControllerP(UnitID, val)
        assert response is not None
        assert isinstance(response.ControllerPSet.value, float)
        # assert response.ControllerPSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(0, val_range)])  # float, implement more meaningful range
    def test_SetControllerTd(self, UnitID, val):
        """ Set the controller differentiator time constant. PID controller: differentiator time constant (set to zero to disable). """
        response = self.sila_client.RedoxServicer_SetControllerTd(UnitID, val)
        assert response is not None
        assert isinstance(response.ControllerTdSet.value, float)
        # assert response.ControllerTdSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(0, val_range)])  # float, implement more meaningful range
    def test_SetControllerTi(self, UnitID, val):
        """ Set the controller integrator time constant. PID controller: integrator time constant (set to zero to disable). """
        response = self.sila_client.RedoxServicer_SetControllerTi(UnitID, val)
        assert response is not None
        assert isinstance(response.ControllerTiSet.value, float)
        # assert response.ControllerTiSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(0, val_range)])  # float, implement more meaningful range
    def test_SetControllerMin(self, UnitID, val):
        """ Set the controller minimal output value. PID controller: minimal output value. """
        response = self.sila_client.RedoxServicer_SetControllerMin(UnitID, val)
        assert response is not None
        assert isinstance(response.ControllerMinSet.value, float)
        # assert response.ControllerMinSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(0, val_range)])  # float, implement more meaningful range
    def test_SetControllerMax(self, UnitID, val):
        """ Set the controller maximal output value. PID controller: maximal output value. """
        response = self.sila_client.RedoxServicer_SetControllerMax(UnitID, val)
        assert response is not None
        assert isinstance(response.ControllerMaxSet.value, float)
        # assert response.ControllerMaxSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', random.sample(range(0, 2), 1)) # int [0, 1]
    def test_SetAlarmEnabled(self, UnitID, val):
        """ Set the alarm enabled value. Enables alarm function. """
        response = self.sila_client.RedoxServicer_SetAlarmEnabled(UnitID, val)
        assert response is not None
        assert isinstance(response.AlarmEnabledSet.value, int)
        # assert response.AlarmEnabledSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(0, val_range)])  # float, implement more meaningful range
    def test_SetAlarmAlarmHigh(self, UnitID, val):
        """ The alarm alarmhigh value. Higher alarm limit. """
        response = self.sila_client.RedoxServicer_SetAlarmAlarmHigh(UnitID, val)
        assert response is not None
        assert isinstance(response.AlarmAlarmHighSet.value, float)
        # assert response.AlarmAlarmHighSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(0, val_range)])  # float, implement more meaningful range
    def test_SetAlarmAlarmLow(self, UnitID, val):
        """ The alarm alarmLow value. Lower alarm limit. """
        response = self.sila_client.RedoxServicer_SetAlarmAlarmLow(UnitID, val)
        assert response is not None
        assert isinstance(response.AlarmAlarmLowSet.value, float)
        # assert response.AlarmAlarmLowSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', random.sample(range(0, 2), 1)) # int [0, 1]
    def test_SetAlarmMode(self, UnitID, val):
        """ The alarm mode value. Alarm mode. """
        response = self.sila_client.RedoxServicer_SetAlarmMode(UnitID, val)
        assert response is not None
        assert isinstance(response.AlarmModeSet.value, int)
        # assert response.AlarmModeSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(0, val_range)])  # float, implement more meaningful range
    def test_SetAlarmDelay(self, UnitID, val):
        """ Set the alarm delay value. Alarm hysteresis time. """
        response = self.sila_client.RedoxServicer_SetAlarmDelay(UnitID, val)
        assert response is not None
        assert isinstance(response.AlarmDelaySet.value, float)
        # assert response.AlarmDelaySet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(0, val_range)])  # float, implement more meaningful range
    def test_SetAlarmWarnHigh(self, UnitID, val):
        response = self.sila_client.RedoxServicer_SetAlarmWarnHigh(UnitID, val)
        assert response is not None
        assert isinstance(response.AlarmWarnHighSet.value, float)
        # assert response.AlarmWarnHighSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(0, val_range)])  # float, implement more meaningful range
    def test_SetAlarmWarnLow(self, UnitID, val):
        response = self.sila_client.RedoxServicer_SetAlarmWarnLow(UnitID, val)
        assert response is not None
        assert isinstance(response.AlarmWarnLowSet.value, float)
        # assert response.AlarmWarnLowSet.value == val


def test__init__():
    """ Starts the server in a mocked environment as defined in DASGIP_Service_server.init()"""
    from sila2lib.sila_server import SiLA2Server
    with mock.patch.object(SiLA2Server, 'run', return_value=42):  # Syntax: .object(class, 'method', return)
        with mock.patch.object(DASGIP_Service_server, '__name__', '__main__'):
            with mock.patch.object(DASGIP_Service_server.sys, 'exit') as mock_exit:
                DASGIP_Service_server.init()
                assert mock_exit.call_args[0][0] == 42
