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

"""
Complexity of services. Note: Since functions are identical between some Servicers it is mostly sufficient to only implement
each Class Servicer once to make a scaffold for: Base, Alarm, Sensor, Controller, Actuator, and some spepcial implementations
Grouping:

test_das_gip_pumpsA-D.py   (97 tests)
Pumps A-D = basic

test_das_gip.py   (>303 tests)
AgitationServicer = basic + little Actuator stuff
DeviceServicer = only get
ReactorServicer = only minimal Volume stuff
OffgasServicer = basic + minimal new features
TurbidityServicer = basic + minimal new features

IlluminationServicer = basic + (a lot of Actuator)
OverlayServicer = basic + lots of gas specific stuff
GassingServicer = basic + lots of gas specific stuff
'OverlayServicer = GassingServicer'

test_das_gip_2.py   (277 tests)
pressure servicer (basic + controller -Alarms
LevelServicer = basic + Alarm + slope etc
pH servicer = Redox servicer = DOServicer = (basic + Controler + Alarms)
TemperatureServicer = basic + Sensor + COntroller + Alarm
'pH servicer = Redox servicer = DOServicer'
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


# no setters at all
class TestOffgasServicerGet:
    """ Test all OffgasServicer Get functions. Control a DASGIP offgas module. Enables read and write operations for various parameters.  """
    sila_client = DASGIP_ServiceClient(server_ip=ip, server_port=port)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetCTRPV(self, UnitID):
        """ Get offgas carbondioxide transfer rate process value. """
        response = self.sila_client.OffgasServicer_GetCTRPV(UnitID)
        assert response is not None
        assert isinstance(response.CurrentCTRPV.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetFPV(self, UnitID):
        """ Get offgas total flow process value """
        response = self.sila_client.OffgasServicer_GetFPV(UnitID)
        assert response is not None
        assert isinstance(response.CurrentFPV.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetOTRPV(self, UnitID):
        """ Get offgas oxygen transfer rate process value """
        response = self.sila_client.OffgasServicer_GetOTRPV(UnitID)
        assert response is not None
        assert isinstance(response.CurrentOTRPV.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetRQPV(self, UnitID):
        """ Get offgas RQ process value """
        response = self.sila_client.OffgasServicer_GetRQPV(UnitID)
        assert response is not None
        assert isinstance(response.CurrentRQPV.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetXCO2PV(self, UnitID):
        """ Get offgas CO2 concentration process value"""
        response = self.sila_client.OffgasServicer_GetXCO2PV(UnitID)
        assert response is not None
        assert isinstance(response.CurrentXCO2PV.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetVCTPV(self, UnitID):
        """ Get offgas cumulated CO2 transfer rate """
        response = self.sila_client.OffgasServicer_GetVCTPV(UnitID)
        assert response is not None
        assert isinstance(response.CurrentVCTPV.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetVOTPV(self, UnitID):
        """ Get offgas cumulated O2 transfer rate """
        response = self.sila_client.OffgasServicer_GetVOTPV(UnitID)
        assert response is not None
        assert isinstance(response.CurrentVOTPV.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetState(self, UnitID):
        response = self.sila_client.OffgasServicer_GetState(UnitID)
        assert response is not None
        assert isinstance(response.CurrentState.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetType(self, UnitID):
        response = self.sila_client.OffgasServicer_GetType(UnitID)
        assert response is not None
        assert isinstance(response.CurrentType.value, str)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetAvailable(self, UnitID):
        response = self.sila_client.OffgasServicer_GetAvailable(UnitID)
        assert response is not None
        assert isinstance(response.CurrentAvailable.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetName(self, UnitID):
        response = self.sila_client.OffgasServicer_GetName(UnitID)
        assert response is not None
        assert isinstance(response.CurrentName.value, str)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetVersion(self, UnitID):
        response = self.sila_client.OffgasServicer_GetVersion(UnitID)
        assert response is not None
        assert isinstance(response.CurrentVersion.value, str)


class TestAgitationServicerGet:
    """ Test all AgitationServicer Get functions. Control a DASGIP agitation module. Enables read and write operations for various parameters, including the agitation actuator.  """
    sila_client = DASGIP_ServiceClient(server_ip=ip, server_port=port)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetPV(self, UnitID):
        """ :param UnitID: The UnitID of the addressed reactor"""
        response = self.sila_client.AgitationServicer_GetPV(UnitID)
        assert response is not None
        assert isinstance(response.CurrentPV.value, float)
        # assert response.CurrentPV.value == UnitID  # this makes no sence i guess

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetSP(self, UnitID):
        response = self.sila_client.AgitationServicer_GetSP(UnitID)
        assert response is not None
        assert isinstance(response.CurrentSP.value, float)
        # assert response.CurrentSP.value == UnitID  # this makes no sence i guess

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetSPA(self, UnitID):
        response = self.sila_client.AgitationServicer_GetSPA(UnitID)
        assert response is not None
        assert isinstance(response.CurrentSPA.value, float)
        # assert response.CurrentSPA.value == UnitID  # this makes no sence i guess

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetSPM(self, UnitID):
        response = self.sila_client.AgitationServicer_GetSPM(UnitID)
        assert response is not None
        assert isinstance(response.CurrentSPM.value, float)
        # assert response.CurrentSPM.value == UnitID  # this makes no sence i guess

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetSPE(self, UnitID):
        response = self.sila_client.AgitationServicer_GetSPE(UnitID)
        assert response is not None
        assert isinstance(response.CurrentSPE.value, float)
        # assert response.CurrentSPE.value == UnitID  # this makes no sence i guess

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetSPR(self, UnitID):
        response = self.sila_client.AgitationServicer_GetSPR(UnitID)
        assert response is not None
        assert isinstance(response.CurrentSPR.value, float)
        # assert response.CurrentSPR.value == UnitID  # this makes no sence i guess

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetAccess(self, UnitID):
        response = self.sila_client.AgitationServicer_GetAccess(UnitID)
        assert response is not None
        assert isinstance(response.CurrentAccess.value, int)
        # assert response.CurrentAccess.value == UnitID  # this makes no sence i guess

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetCmd(self, UnitID):
        response = self.sila_client.AgitationServicer_GetCmd(UnitID)
        assert response is not None
        assert isinstance(response.CurrentCmd.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetMode(self, UnitID):
        response = self.sila_client.AgitationServicer_GetMode(UnitID)
        assert response is not None
        assert isinstance(response.CurrentMode.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetSetpointSelect(self, UnitID):
        response = self.sila_client.AgitationServicer_GetSetpointSelect(UnitID)
        assert response is not None
        assert isinstance(response.CurrentSetpointSelect.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetState(self, UnitID):
        response = self.sila_client.AgitationServicer_GetState(UnitID)
        assert response is not None
        assert isinstance(response.CurrentState.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetType(self, UnitID):
        response = self.sila_client.AgitationServicer_GetType(UnitID)
        assert response is not None
        assert isinstance(response.CurrentType.value, str)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetAvailable(self, UnitID):
        response = self.sila_client.AgitationServicer_GetAvailable(UnitID)
        assert response is not None
        assert isinstance(response.CurrentAvailable.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetName(self, UnitID):
        response = self.sila_client.AgitationServicer_GetName(UnitID)
        assert response is not None
        assert isinstance(response.CurrentName.value, str)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetVersion(self, UnitID):
        response = self.sila_client.AgitationServicer_GetVersion(UnitID)
        assert response is not None
        assert isinstance(response.CurrentVersion.value, str)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetActuatorDirPV(self, UnitID):
        response = self.sila_client.AgitationServicer_GetActuatorDirPV(UnitID)
        assert response is not None
        assert isinstance(response.CurrentActuatorDirPV.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetActuatorPwrPV(self, UnitID):
        response = self.sila_client.AgitationServicer_GetActuatorPwrPV(UnitID)
        assert response is not None
        assert isinstance(response.CurrentActuatorPwrPV.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetActuatorTStirPV(self, UnitID):
        response = self.sila_client.AgitationServicer_GetActuatorTStirPV(UnitID)
        assert response is not None
        assert isinstance(response.CurrentActuatorTStirPV.value, float)


class TestAgitationServicerSet:
    """ Test all AgitationServicer Set functions. Control a DASGIP agitation module. Enables read and write operations for various parameters, including the agitation actuator.  """
    sila_client = DASGIP_ServiceClient(server_ip=ip, server_port=port)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(0, unit_ids)])  # float
    def test_SetSPM(self, UnitID, val):
        """ Set the manual pH setpoint."""
        response = self.sila_client.AgitationServicer_SetSPM(UnitID, val)
        assert response is not None
        assert isinstance(response.SPMSet.value, float)
        # assert response.SPMSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(0, unit_ids)])  # float
    def test_SetSPE(self, UnitID, val):
        """ Set the external pH setpoint."""
        response = self.sila_client.AgitationServicer_SetSPE(UnitID, val)
        assert response is not None
        assert isinstance(response.SPESet.value, float)
        # assert response.SPESet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', random.sample(range(0, 3), 1))  # int
    def test_SetCmd(self, UnitID, val):
        """ Set the controller command. Controller command (Nothing, Stop, Start)."""
        response = self.sila_client.AgitationServicer_SetCmd(UnitID, val)
        assert response is not None
        assert isinstance(response.CmdSet.value, int)
        # assert response.CmdSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', random.sample(range(0, 5), 1))  # int
    def test_SetSetpointSelect(self, UnitID, val):
        """ Set the selected setpoint that should be used. Setpoint selection (Local, Manual, Internal, Script, External).
        I assume they are sorted 1-5 since val needs int input. However no mapping specified. """
        response = self.sila_client.AgitationServicer_SetSetpointSelect(UnitID, val)
        assert response is not None
        assert isinstance(response.SetpointSelectSet.value, int)
        # assert response.SetpointSelectSet.value == val


# no setters at all
class TestDeviceServicerGet:
    """ Test all DeviceServicer Get functions. General device settings of the DASGIP reactor system can be retrieved and changed within this function.  """
    sila_client = DASGIP_ServiceClient(server_ip=ip, server_port=port)

    def test_GetLog(self):
        response = self.sila_client.DeviceServicer_GetLog()
        assert response is not None
        assert isinstance(response.commandExecutionUUID.value, str)
# uuid needed
    # def test_GetLog_Info(self):
    #     response = self.sila_client.DeviceServicer_GetLog_Info()
    #     assert response is not None
    #     assert isinstance(response )
    #
    # def test_GetLog_Result(self):
    #     response = self.sila_client.DeviceServicer_GetLog_Result()
    #     assert response is not None
    #     assert isinstance(response )

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetRuntimeClock(self, UnitID):
        response = self.sila_client.DeviceServicer_GetRuntimeClock(UnitID)
        assert response is not None
        assert isinstance(response.CurrentRuntime.value, str)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetStartedUTC(self, UnitID):
        response = self.sila_client.DeviceServicer_GetStartedUTC(UnitID)
        assert response is not None
        assert isinstance(response.CurrentStartedUTC.second, int)
        assert isinstance(response.CurrentStartedUTC.minute, int)
        assert isinstance(response.CurrentStartedUTC.hour, int)
        assert isinstance(response.CurrentStartedUTC.day, int)
        assert isinstance(response.CurrentStartedUTC.month, int)
        assert isinstance(response.CurrentStartedUTC.year, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetStarted(self, UnitID):
        response = self.sila_client.DeviceServicer_GetStarted(UnitID)
        assert response is not None
        assert isinstance(response.CurrentStarted.second, int)
        assert isinstance(response.CurrentStarted.minute, int)
        assert isinstance(response.CurrentStarted.hour, int)
        assert isinstance(response.CurrentStarted.day, int)
        assert isinstance(response.CurrentStarted.month, int)
        assert isinstance(response.CurrentStarted.year, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetStoppedUTC(self, UnitID):
        response = self.sila_client.DeviceServicer_GetStoppedUTC(UnitID)
        assert response is not None
        assert isinstance(response.CurrentStoppedUTC.second, int)
        assert isinstance(response.CurrentStoppedUTC.minute, int)
        assert isinstance(response.CurrentStoppedUTC.hour, int)
        assert isinstance(response.CurrentStoppedUTC.day, int)
        assert isinstance(response.CurrentStoppedUTC.month, int)
        assert isinstance(response.CurrentStoppedUTC.year, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetStopped(self, UnitID):
        response = self.sila_client.DeviceServicer_GetStopped(UnitID)
        assert response is not None
        assert isinstance(response.CurrentStopped.second, int)
        assert isinstance(response.CurrentStopped.minute, int)
        assert isinstance(response.CurrentStopped.hour, int)
        assert isinstance(response.CurrentStopped.day, int)
        assert isinstance(response.CurrentStopped.month, int)
        assert isinstance(response.CurrentStopped.year, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetUserId(self, UnitID):
        response = self.sila_client.DeviceServicer_GetUserId(UnitID)
        assert response is not None
        assert isinstance(response.CurrentUserId.value, str)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetBatchId(self, UnitID):
        response = self.sila_client.DeviceServicer_GetBatchId(UnitID)
        assert response is not None
        assert isinstance(response.CurrentBatchId.value, str)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetInoculatedUTC(self, UnitID):
        response = self.sila_client.DeviceServicer_GetInoculatedUTC(UnitID)
        assert response is not None
        assert isinstance(response.CurrentInoculationUTC.second, int)
        assert isinstance(response.CurrentInoculationUTC.minute, int)
        assert isinstance(response.CurrentInoculationUTC.hour, int)
        assert isinstance(response.CurrentInoculationUTC.day, int)
        assert isinstance(response.CurrentInoculationUTC.month, int)
        assert isinstance(response.CurrentInoculationUTC.year, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetInoculated(self, UnitID):
        response = self.sila_client.DeviceServicer_GetInoculated(UnitID)
        assert response is not None
        assert isinstance(response.CurrentInoculation.second, int)
        assert isinstance(response.CurrentInoculation.minute, int)
        assert isinstance(response.CurrentInoculation.hour, int)
        assert isinstance(response.CurrentInoculation.day, int)
        assert isinstance(response.CurrentInoculation.month, int)
        assert isinstance(response.CurrentInoculation.year, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetAvailable(self, UnitID):
        response = self.sila_client.DeviceServicer_GetAvailable(UnitID)
        assert response is not None
        assert isinstance(response.CurrentAvailable.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetName(self, UnitID):
        response = self.sila_client.DeviceServicer_GetName(UnitID)
        assert response is not None
        assert isinstance(response.CurrentName.value, str)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetVersion(self, UnitID):
        response = self.sila_client.DeviceServicer_GetVersion(UnitID)
        assert response is not None
        assert isinstance(response.CurrentVersion.value, str)

    def test_Subscribe_CurrentStatus(self):
        response = self.sila_client.Subscribe_DeviceServicer_CurrentStatus()
        assert response is not None
        assert isinstance(response, object)


class TestReactorServicerGet:
    """ Test all ReactorServicer Get functions.Control a DASGIP reactor module. Enables read and write operations for various parameters, including reactor sensor, controller, and alarm.  """
    sila_client = DASGIP_ServiceClient(server_ip=ip, server_port=port)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetVInitial(self, UnitID):
        """ Get initial liquid volume value. Initial liquid volume (initial working volume).
        :param UnitID: The UnitID of the addressed reactor"""
        response = self.sila_client.ReactorServicer_GetVInitial(UnitID)
        assert response is not None
        assert isinstance(response.CurrentVInitial.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetVLiquid(self, UnitID):
        """ Get actual liquid volume value. Actual liquid volume (working volume).
        :param UnitID: The UnitID of the addressed reactor"""
        response = self.sila_client.ReactorServicer_GetVLiquid(UnitID)
        assert response is not None
        assert isinstance(response.CurrentVLiquid.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetVMax(self, UnitID):
        response = self.sila_client.ReactorServicer_GetVMax(UnitID)
        assert response is not None
        assert isinstance(response.CurrentVMax.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetVMin(self, UnitID):
        response = self.sila_client.ReactorServicer_GetVMin(UnitID)
        assert response is not None
        assert isinstance(response.CurrentVMin.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetVTotal(self, UnitID):
        response = self.sila_client.ReactorServicer_GetVTotal(UnitID)
        assert response is not None
        assert isinstance(response.CurrentVTotal.value, float)


# Set functions not provided by the client
class TestReactorServicerSet:
    """ Test all ReactorServicer Set functions. Control a DASGIP reactor module. Enables read and write operations for various parameters, including reactor sensor, controller, and alarm.  """
    # sila_client = DASGIP_ServiceClient(server_ip=ip, server_port=port)
    #
    # def test_SetVLiquid(self):
    #     response = self.sila_client.ReactorServicer_SetVLiquid()
    #     assert response is not None
    #     assert isinstance(response )
    #
    # def test_SetVMax(self):
    #     response = self.sila_client.ReactorServicer_SetVMax()
    #     assert response is not None
    #     assert isinstance(response )
    #
    # def test_SetVMin(self):
    #     response = self.sila_client.ReactorServicer_SetVMin()
    #     assert response is not None
    #     assert isinstance(response )
    #
    # def test_SetVTotal(self):
    #     response = self.sila_client.ReactorServicer_SetVTotal()
    #     assert response is not None
    #     assert isinstance(response )


# no setters at all
class TestTurbidityServicerGet:
    """ Test all TurbidityServicer Get functions. Control a DASGIP turbidity module. Enables read and write operations for various parameters, including turbidity sensor, controller, and alarm.  """
    sila_client = DASGIP_ServiceClient(server_ip=ip, server_port=port)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetAUPV(self, UnitID):
        """ Get present value in absorption unit. Turbidity signal in absorption units.
        :param UnitID: The UnitID of the addressed reactor"""
        response = self.sila_client.TurbidityServicer_GetAUPV(UnitID)
        assert response is not None
        assert isinstance(response.CurrentAUPV.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetCXPV(self, UnitID):
        """ Get calculated turbidity present value. Calculated turbidity signal, i.e. OD600, CDW or others.
        :param UnitID: The UnitID of the addressed reactor"""
        response = self.sila_client.TurbidityServicer_GetCXPV(UnitID)
        assert response is not None
        assert isinstance(response.CurrentCXPV.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetType(self, UnitID):
        response = self.sila_client.TurbidityServicer_GetType(UnitID)
        assert response is not None
        assert isinstance(response.CurrentType.value, str)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetAvailable(self, UnitID):
        response = self.sila_client.TurbidityServicer_GetAvailable(UnitID)
        assert response is not None
        assert isinstance(response.CurrentAvailable.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetName(self, UnitID):
        response = self.sila_client.TurbidityServicer_GetName(UnitID)
        assert response is not None
        assert isinstance(response.CurrentName.value, str)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetVersion(self, UnitID):
        response = self.sila_client.TurbidityServicer_GetVersion(UnitID)
        assert response is not None
        assert isinstance(response.CurrentVersion.value, str)
        # assert response.CurrentVersion.value == "SimTurbidityVersion_1.0"


class TestIlluminationServicerGet:
    """ Test all IlluminationServicer Get functions. Control a DASGIP illumination module. Enables read and write operations for various parameters, including the illumination actuators. """
    sila_client = DASGIP_ServiceClient(server_ip=ip, server_port=port)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetAccess(self, UnitID):
        response = self.sila_client.IlluminationServicer_GetAccess(UnitID)
        assert response is not None
        assert isinstance(response.CurrentAccess.value, int)
        # assert response.CurrentAccess.value == UnitID  # this makes no sence i guess

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetCmd(self, UnitID):
        response = self.sila_client.IlluminationServicer_GetCmd(UnitID)
        assert response is not None
        assert isinstance(response.CurrentCmd.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetMode(self, UnitID):
        response = self.sila_client.IlluminationServicer_GetMode(UnitID)
        assert response is not None
        assert isinstance(response.CurrentMode.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetState(self, UnitID):
        response = self.sila_client.IlluminationServicer_GetState(UnitID)
        assert response is not None
        assert isinstance(response.CurrentState.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetType(self, UnitID):
        response = self.sila_client.IlluminationServicer_GetType(UnitID)
        assert response is not None
        assert isinstance(response.CurrentType.value, str)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetAvailable(self, UnitID):
        response = self.sila_client.IlluminationServicer_GetAvailable(UnitID)
        assert response is not None
        assert isinstance(response.CurrentAvailable.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetName(self, UnitID):
        response = self.sila_client.IlluminationServicer_GetName(UnitID)
        assert response is not None
        assert isinstance(response.CurrentName.value, str)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetVersion(self, UnitID):
        response = self.sila_client.IlluminationServicer_GetVersion(UnitID)
        assert response is not None
        assert isinstance(response.CurrentVersion.value, str)

# start of ActuatorA
    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetActuatorAPV(self, UnitID):
        """ Get ActuatorA controller process value."""
        response = self.sila_client.IlluminationServicer_GetActuatorAPV(UnitID)
        assert response is not None
        assert isinstance(response.CurrentActuatorAPV.value, float)

# # binascii.Error: Incorrect padding
#     @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
#     def test_GetActuatorAPVInt(self, UnitID):
#         """ Get ActuatorA controller process value."""
#         response = self.sila_client.IlluminationServicer_GetActuatorAPVInt(UnitID)
#         assert response is not None
#         assert isinstance(response.XXX.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetActuatorASource(self, UnitID):
        response = self.sila_client.IlluminationServicer_GetActuatorASource(UnitID)
        assert response is not None
        assert isinstance(response.CurrentActuatorASource.value, str)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetActuatorASP(self, UnitID):
        response = self.sila_client.IlluminationServicer_GetActuatorASP(UnitID)
        assert response is not None
        assert isinstance(response.CurrentActuatorASP.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetActuatorASPA(self, UnitID):
        response = self.sila_client.IlluminationServicer_GetActuatorASPA(UnitID)
        assert response is not None
        assert isinstance(response.CurrentActuatorASPA.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetActuatorASPM(self, UnitID):
        response = self.sila_client.IlluminationServicer_GetActuatorASPM(UnitID)
        assert response is not None
        assert isinstance(response.CurrentActuatorASPM.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetActuatorASPE(self, UnitID):
        response = self.sila_client.IlluminationServicer_GetActuatorASPE(UnitID)
        assert response is not None
        assert isinstance(response.CurrentActuatorASPE.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetActuatorASPR(self, UnitID):
        response = self.sila_client.IlluminationServicer_GetActuatorASPR(UnitID)
        assert response is not None
        assert isinstance(response.CurrentActuatorASPR.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetActuatorAMode(self, UnitID):
        """ Get the ActuatorA controller mode. Controller mode (Manual, Automatic)."""
        response = self.sila_client.IlluminationServicer_GetActuatorAMode(UnitID)
        assert response is not None
        assert isinstance(response.CurrentActuatorAMode.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetActuatorASetpointSelect(self, UnitID):
        """ Get the ActuatorA setpoint selection. Controller state (Off, On, Error)"""
        response = self.sila_client.IlluminationServicer_GetActuatorASetpointSelect(UnitID)
        assert response is not None
        assert isinstance(response.CurrentActuatorASetpointSelect.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetActuatorAAvailable(self, UnitID):
        response = self.sila_client.IlluminationServicer_GetActuatorAAvailable(UnitID)
        assert response is not None
        assert isinstance(response.CurrentActuatorAAvailable.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetActuatorAName(self, UnitID):
        response = self.sila_client.IlluminationServicer_GetActuatorAName(UnitID)
        assert response is not None
        assert isinstance(response.CurrentActuatorAName.value, str)

# start of ActuatorB
    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetActuatorBPV(self, UnitID):
        response = self.sila_client.IlluminationServicer_GetActuatorBPV(UnitID)
        assert response is not None
        assert isinstance(response.CurrentActuatorBPV.value, float)

# binascii.Error: Incorrect padding
#     @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
#     def test_GetActuatorBPVInt(self, UnitID):
#         response = self.sila_client.IlluminationServicer_GetActuatorBPVInt(UnitID)
#         assert response is not None
#         assert isinstance(response.CurrentActuatorBPVInt.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetActuatorBSource(self, UnitID):
        response = self.sila_client.IlluminationServicer_GetActuatorBSource(UnitID)
        assert response is not None
        assert isinstance(response.CurrentActuatorBSource.value, str)

    def test_GetActuatorBSP(self):
        response = self.sila_client.IlluminationServicer_GetActuatorBSP()
        assert response is not None
        assert isinstance(response.CurrentActuatorBSP.value, float)

    def test_GetActuatorBSPA(self):
        response = self.sila_client.IlluminationServicer_GetActuatorBSPA()
        assert response is not None
        assert isinstance(response.CurrentActuatorBSPA.value, float)

    def test_GetActuatorBSPM(self):
        response = self.sila_client.IlluminationServicer_GetActuatorBSPM()
        assert response is not None
        assert isinstance(response.CurrentActuatorBSPM.value, float)

    def test_GetActuatorBSPE(self):
        response = self.sila_client.IlluminationServicer_GetActuatorBSPE()
        assert response is not None
        assert isinstance(response.CurrentActuatorBSPE.value, float)

    def test_GetActuatorBSPR(self):
        response = self.sila_client.IlluminationServicer_GetActuatorBSPR()
        assert response is not None
        assert isinstance(response.CurrentActuatorBSPR.value, float)

    def test_GetActuatorBMode(self):
        response = self.sila_client.IlluminationServicer_GetActuatorBMode()
        assert response is not None
        assert isinstance(response.CurrentActuatorBMode.value, int)

    def test_GetActuatorBSetpointSelect(self):
        response = self.sila_client.IlluminationServicer_GetActuatorBSetpointSelect()
        assert response is not None
        assert isinstance(response.CurrentActuatorBSetpointSelect.value, int)

    def test_GetActuatorBAvailable(self):
        response = self.sila_client.IlluminationServicer_GetActuatorBAvailable()
        assert response is not None
        assert isinstance(response.CurrentActuatorBAvailable.value, int)

    def test_GetActuatorBName(self):
        response = self.sila_client.IlluminationServicer_GetActuatorBName()
        assert response is not None
        assert isinstance(response.CurrentActuatorBName.value, str)

# start of ActuatorA
    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetActuatorCPV(self, UnitID):
        response = self.sila_client.IlluminationServicer_GetActuatorCPV(UnitID)
        assert response is not None
        assert isinstance(response.CurrentActuatorCPV.value, float)

# binascii.Error: Incorrect padding
#     @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
#     def test_GetActuatorCPVInt(self, UnitID):
#         response = self.sila_client.IlluminationServicer_GetActuatorCPVInt(UnitID)
#         assert response is not None
#         assert isinstance(response.XXX.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetActuatorCSource(self, UnitID):
        response = self.sila_client.IlluminationServicer_GetActuatorCSource(UnitID)
        assert response is not None
        assert isinstance(response.CurrentActuatorCSource.value, str)

    def test_GetActuatorCSP(self):
        response = self.sila_client.IlluminationServicer_GetActuatorCSP()
        assert response is not None
        assert isinstance(response.CurrentActuatorCSP.value, float)

    def test_GetActuatorCSPA(self):
        response = self.sila_client.IlluminationServicer_GetActuatorCSPA()
        assert response is not None
        assert isinstance(response.CurrentActuatorCSPA.value, float)

    def test_GetActuatorCSPM(self):
        response = self.sila_client.IlluminationServicer_GetActuatorCSPM()
        assert response is not None
        assert isinstance(response.CurrentActuatorCSPM.value, float)

    def test_GetActuatorCSPE(self):
        response = self.sila_client.IlluminationServicer_GetActuatorCSPE()
        assert response is not None
        assert isinstance(response.CurrentActuatorCSPE.value, float)

    def test_GetActuatorCSPR(self):
        response = self.sila_client.IlluminationServicer_GetActuatorCSPR()
        assert response is not None
        assert isinstance(response.CurrentActuatorCSPR.value, float)

    def test_GetActuatorCMode(self):
        response = self.sila_client.IlluminationServicer_GetActuatorCMode()
        assert response is not None
        assert isinstance(response.CurrentActuatorCMode.value, int)

    def test_GetActuatorCSetpointSelect(self):
        response = self.sila_client.IlluminationServicer_GetActuatorCSetpointSelect()
        assert response is not None
        assert isinstance(response.CurrentActuatorCSetpointSelect.value, int)

    def test_GetActuatorCAvailable(self):
        response = self.sila_client.IlluminationServicer_GetActuatorCAvailable()
        assert response is not None
        assert isinstance(response.CurrentActuatorCAvailable.value, int)

    def test_GetActuatorCName(self):
        response = self.sila_client.IlluminationServicer_GetActuatorCName()
        assert response is not None
        assert isinstance(response.CurrentActuatorCName.value, str)


class TestIlluminationServicerSet:
    """ Test all IlluminationServicer Set functions. Control a DASGIP illumination module. Enables read and write operations for various parameters, including the illumination actuators. """
    sila_client = DASGIP_ServiceClient(server_ip=ip, server_port=port)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', random.sample(range(0, 3), 1))  # int
    def test_SetCmd(self, UnitID, val):
        """ Set the controller command. Controller command (Nothing, Stop, Start)."""
        response = self.sila_client.IlluminationServicer_SetCmd(UnitID, val)
        assert response is not None
        assert isinstance(response.CmdSet.value, int)
        # assert response.CmdSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', random.sample(range(0, 2), 1))  # int [0, 1]
    def test_SetMode(self, UnitID, val):
        """ Set the controller mode. Controller mode (Manual, Automatic)."""
        response = self.sila_client.IlluminationServicer_SetMode(UnitID, val)
        assert response is not None
        assert isinstance(response.ModeSet.value, int)
        # assert response.ModeSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(-10.00, 60.0)])  # float
    def test_SetActuatorASPM(self, UnitID, val):
        """ The set ActuatorA manual setpoint."""
        response = self.sila_client.IlluminationServicer_SetActuatorASPM(UnitID, val)
        assert response is not None
        assert isinstance(response.ActuatorASPMSet.value, float)
        # assert response.ActuatorASPMSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(-10.00, 60.0)])  # float
    def test_SetActuatorASPE(self, UnitID, val):
        """ The set ActuatorA manual setpoint."""
        response = self.sila_client.IlluminationServicer_SetActuatorASPE(UnitID, val)
        assert response is not None
        assert isinstance(response.ActuatorASPESet.value, float)
        # assert response.ActuatorASPESet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', random.sample(range(0, 2), 1))  # int [0, 1]
    def test_SetActuatorAMode(self, UnitID, val):
        """ The set ActuatorA manual setpoint."""
        response = self.sila_client.IlluminationServicer_SetActuatorAMode(UnitID, val)
        assert response is not None
        assert isinstance(response.ActuatorAModeSet.value, int)
        # assert response.ActuatorAModeSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', random.sample(range(0, 6), 1))
    def test_SetActuatorASetpointSelect(self, UnitID, val):
        """ Set the selected ActuatorA setpoint that should be used. Setpoint selection (Local, Manual, Internal, Script, External)."""
        response = self.sila_client.IlluminationServicer_SetActuatorASetpointSelect(UnitID, val)
        assert response is not None
        assert isinstance(response.ActuatorASetpointSelectSet.value, int)
        # assert response.ActuatorASetpointSelectSet.value == val

    def test_SetActuatorBSPE(self):
        response = self.sila_client.IlluminationServicer_SetActuatorBSPE()
        assert response is not None
        assert isinstance(response.ActuatorBSPESet.value, float)

    def test_SetActuatorBSPM(self):
        response = self.sila_client.IlluminationServicer_SetActuatorBSPM()
        assert response is not None
        assert isinstance(response.ActuatorBSPMSet.value, float)

    def test_SetActuatorBMode(self):
        response = self.sila_client.IlluminationServicer_SetActuatorBMode()
        assert response is not None
        assert isinstance(response.ActuatorBModeSet.value, int)

    def test_SetActuatorBSetpointSelect(self):
        response = self.sila_client.IlluminationServicer_SetActuatorBSetpointSelect()
        assert response is not None
        assert isinstance(response.ActuatorBSetpointSelectSet.value, int)

    def test_SetActuatorCSPM(self):
        response = self.sila_client.IlluminationServicer_SetActuatorCSPM()
        assert response is not None
        assert isinstance(response.ActuatorCSPMSet.value, float)

    def test_SetActuatorCSPE(self):
        response = self.sila_client.IlluminationServicer_SetActuatorCSPE()
        assert response is not None
        assert isinstance(response.ActuatorCSPESet.value, float)

    def test_SetActuatorCMode(self):
        response = self.sila_client.IlluminationServicer_SetActuatorCMode()
        assert response is not None
        assert isinstance(response.ActuatorCModeSet.value, int)
        assert response.ActuatorCModeSet.value in [0, 1]

    def test_SetActuatorCSetpointSelect(self):
        response = self.sila_client.IlluminationServicer_SetActuatorCSetpointSelect()
        assert response is not None
        assert isinstance(response.ActuatorCSetpointSelectSet.value, int)
        assert response.ActuatorCSetpointSelectSet.value in range(0, 6)


class TestGassingServicerGet:
    """ Test all GassingServicer Get functions. Control a DASGIP gassing module. Enables read and write operations for various parameters. """
    sila_client = DASGIP_ServiceClient(server_ip=ip, server_port=port)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetPV(self, UnitID):
        response = self.sila_client.GassingServicer_GetPV(UnitID)
        assert response is not None
        assert isinstance(response.CurrentPV.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetSP(self, UnitID):
        response = self.sila_client.GassingServicer_GetSP(UnitID)
        assert response is not None
        assert isinstance(response.CurrentSP.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetFPV(self, UnitID):
        response = self.sila_client.GassingServicer_GetFPV(UnitID)
        assert response is not None
        assert isinstance(response.CurrentFPV.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetVPV(self, UnitID):
        response = self.sila_client.GassingServicer_GetVPV(UnitID)
        assert response is not None
        assert isinstance(response.CurrentVPV.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetFSP(self, UnitID):
        response = self.sila_client.GassingServicer_GetFSP(UnitID)
        assert response is not None
        assert isinstance(response.CurrentFSP.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetFSPM(self, UnitID):
        response = self.sila_client.GassingServicer_GetFSPM(UnitID)
        assert response is not None
        assert isinstance(response.CurrentFSPM.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetFSPE(self, UnitID):
        response = self.sila_client.GassingServicer_GetFSPE(UnitID)
        assert response is not None
        assert isinstance(response.CurrentFSPE.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetFSPA(self, UnitID):
        response = self.sila_client.GassingServicer_GetFSPA(UnitID)
        assert response is not None
        assert isinstance(response.CurrentFSPA.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetFSPR(self, UnitID):
        response = self.sila_client.GassingServicer_GetFSPR(UnitID)
        assert response is not None
        assert isinstance(response.CurrentFSPR.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetFSPL(self, UnitID):
        response = self.sila_client.GassingServicer_GetFSPL(UnitID)
        assert response is not None
        assert isinstance(response.CurrentFSPL.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetFMode(self, UnitID):
        """ Get gas total flow operation mode. Controller mode (Manual, Automatic)"""
        response = self.sila_client.GassingServicer_GetFMode(UnitID)
        assert response is not None
        assert isinstance(response.CurrentFMode.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetFSetpointSelect(self, UnitID):
        """ Get gas total flow setpoint selection (Local, Manual, Internal, Script, External)."""
        response = self.sila_client.GassingServicer_GetFSetpointSelect(UnitID)
        assert response is not None
        assert isinstance(response.CurrentFSetpointSelect.value, int)
# Start CO2
    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetXCO2PV(self, UnitID):
        """ Current gas total flow setpoint selection (Local, Manual, Internal, Script, External)."""
        response = self.sila_client.GassingServicer_GetXCO2PV(UnitID)
        assert response is not None
        assert isinstance(response.CurrentXCO2PV.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetXCO2SP(self, UnitID):
        response = self.sila_client.GassingServicer_GetXCO2SP(UnitID)
        assert response is not None
        assert isinstance(response.CurrentXCO2SP.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetXCO2SPM(self, UnitID):
        response = self.sila_client.GassingServicer_GetXCO2SPM(UnitID)
        assert response is not None
        assert isinstance(response.CurrentXCO2SPM.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetXCO2SPE(self, UnitID):
        response = self.sila_client.GassingServicer_GetXCO2SPE(UnitID)
        assert response is not None
        assert isinstance(response.CurrentXCO2SPE.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetXCO2SPA(self, UnitID):
        response = self.sila_client.GassingServicer_GetXCO2SPA(UnitID)
        assert response is not None
        assert isinstance(response.CurrentXCO2SPA.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetXCO2SPR(self, UnitID):
        response = self.sila_client.GassingServicer_GetXCO2SPR(UnitID)
        assert response is not None
        assert isinstance(response.CurrentXCO2SPR.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetXCO2SPL(self, UnitID):
        response = self.sila_client.GassingServicer_GetXCO2SPL(UnitID)
        assert response is not None
        assert isinstance(response.CurrentXCO2SPL.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetXCO2Mode(self, UnitID):
        response = self.sila_client.GassingServicer_GetXCO2Mode(UnitID)
        assert response is not None
        assert isinstance(response.CurrentXCO2Mode.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetXCO2SetpointSelect(self, UnitID):
        response = self.sila_client.GassingServicer_GetXCO2SetpointSelect(UnitID)
        assert response is not None
        assert isinstance(response.CurrentXCO2SetpointSelect.value, int)

# Start O2
    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetXO2PV(self, UnitID):
        response = self.sila_client.GassingServicer_GetXO2PV(UnitID)
        assert response is not None
        assert isinstance(response.CurrentXO2PV.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetXO2SP(self, UnitID):
        response = self.sila_client.GassingServicer_GetXO2SP(UnitID)
        assert response is not None
        assert isinstance(response.CurrentXO2SP.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetXO2SPM(self, UnitID):
        response = self.sila_client.GassingServicer_GetXO2SPM(UnitID)
        assert response is not None
        assert isinstance(response.CurrentXO2SPM.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetXO2SPE(self, UnitID):
        response = self.sila_client.GassingServicer_GetXO2SPE(UnitID)
        assert response is not None
        assert isinstance(response.CurrentXO2SPE.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetXO2SPA(self, UnitID):
        response = self.sila_client.GassingServicer_GetXO2SPA(UnitID)
        assert response is not None
        assert isinstance(response.CurrentXO2SPA.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetXO2SPR(self, UnitID):
        response = self.sila_client.GassingServicer_GetXO2SPR(UnitID)
        assert response is not None
        assert isinstance(response.CurrentXO2SPR.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetXO2SPL(self, UnitID):
        response = self.sila_client.GassingServicer_GetXO2SPL(UnitID)
        assert response is not None
        assert isinstance(response.CurrentXO2SPL.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetXO2Mode(self, UnitID):
        response = self.sila_client.GassingServicer_GetXO2Mode(UnitID)
        assert response is not None
        assert isinstance(response.CurrentXO2Mode.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetXO2SetpointSelect(self, UnitID):
        response = self.sila_client.GassingServicer_GetXO2SetpointSelect(UnitID)
        assert response is not None
        assert isinstance(response.CurrentXO2SetpointSelect.value, int)

# Start Air
    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetFAirPV(self, UnitID):
        response = self.sila_client.GassingServicer_GetFAirPV(UnitID)
        assert response is not None
        assert isinstance(response.CurrentFAirPV.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetVAirPV(self, UnitID):
        response = self.sila_client.GassingServicer_GetVAirPV(UnitID)
        assert response is not None
        assert isinstance(response.CurrentVAirPV.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetFAirSP(self, UnitID):
        response = self.sila_client.GassingServicer_GetFAirSP(UnitID)
        assert response is not None
        assert isinstance(response.CurrentFAirSP.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetFAirSPM(self, UnitID):
        response = self.sila_client.GassingServicer_GetFAirSPM(UnitID)
        assert response is not None
        assert isinstance(response.CurrentFAirSPM.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetFAirSPE(self, UnitID):
        response = self.sila_client.GassingServicer_GetFAirSPE(UnitID)
        assert response is not None
        assert isinstance(response.CurrentFAirSPE.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetFAirSPA(self, UnitID):
        response = self.sila_client.GassingServicer_GetFAirSPA(UnitID)
        assert response is not None
        assert isinstance(response.CurrentFAirSPA.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetFAirSPR(self, UnitID):
        response = self.sila_client.GassingServicer_GetFAirSPR(UnitID)
        assert response is not None
        assert isinstance(response.CurrentFAirSPR.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetFAirMode(self, UnitID):
        response = self.sila_client.GassingServicer_GetFAirMode(UnitID)
        assert response is not None
        assert isinstance(response.CurrentFAirMode.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetFAirSetpointSelect(self, UnitID):
        response = self.sila_client.GassingServicer_GetFAirSetpointSelect(UnitID)
        assert response is not None
        assert isinstance(response.CurrentFAirSetpointSelect.value, int)

# Start FO2
    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetFO2PV(self, UnitID):
        response = self.sila_client.GassingServicer_GetFO2PV(UnitID)
        assert response is not None
        assert isinstance(response.CurrentFO2PV.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetVO2PV(self, UnitID):
        response = self.sila_client.GassingServicer_GetVO2PV(UnitID)
        assert response is not None
        assert isinstance(response.CurrentVO2PV.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetFO2SP(self, UnitID):
        response = self.sila_client.GassingServicer_GetFO2SP(UnitID)
        assert response is not None
        assert isinstance(response.CurrentFO2SP.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetFO2SPM(self, UnitID):
        response = self.sila_client.GassingServicer_GetFO2SPM(UnitID)
        assert response is not None
        assert isinstance(response.CurrentFO2SPM.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetFO2SPE(self, UnitID):
        response = self.sila_client.GassingServicer_GetFO2SPE(UnitID)
        assert response is not None
        assert isinstance(response.CurrentFO2SPE.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetFO2SPA(self, UnitID):
        response = self.sila_client.GassingServicer_GetFO2SPA(UnitID)
        assert response is not None
        assert isinstance(response.CurrentFO2SPA.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetFO2SPR(self, UnitID):
        response = self.sila_client.GassingServicer_GetFO2SPR(UnitID)
        assert response is not None
        assert isinstance(response.CurrentFO2SPR.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetFO2Mode(self, UnitID):
        response = self.sila_client.GassingServicer_GetFO2Mode(UnitID)
        assert response is not None
        assert isinstance(response.CurrentFO2Mode.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetFO2SetpointSelect(self, UnitID):
        response = self.sila_client.GassingServicer_GetFO2SetpointSelect(UnitID)
        assert response is not None
        assert isinstance(response.CurrentFO2SetpointSelect.value, int)

# Start FCO2
    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetFCO2PV(self, UnitID):
        response = self.sila_client.GassingServicer_GetFCO2PV(UnitID)
        assert response is not None
        assert isinstance(response.CurrentFCO2PV.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetVCO2PV(self, UnitID):
        response = self.sila_client.GassingServicer_GetVCO2PV(UnitID)
        assert response is not None
        assert isinstance(response.CurrentVCO2PV.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetFCO2SP(self, UnitID):
        response = self.sila_client.GassingServicer_GetFCO2SP(UnitID)
        assert response is not None
        assert isinstance(response.CurrentFCO2SP.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetFCO2SPM(self, UnitID):
        response = self.sila_client.GassingServicer_GetFCO2SPM(UnitID)
        assert response is not None
        assert isinstance(response.CurrentFCO2SPM.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetFCO2SPE(self, UnitID):
        response = self.sila_client.GassingServicer_GetFCO2SPE(UnitID)
        assert response is not None
        assert isinstance(response.CurrentFCO2SPE.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetFCO2SPA(self, UnitID):
        response = self.sila_client.GassingServicer_GetFCO2SPA(UnitID)
        assert response is not None
        assert isinstance(response.CurrentFCO2SPA.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetFCO2SPR(self, UnitID):
        response = self.sila_client.GassingServicer_GetFCO2SPR(UnitID)
        assert response is not None
        assert isinstance(response.CurrentFCO2SPR.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetFCO2Mode(self, UnitID):
        response = self.sila_client.GassingServicer_GetFCO2Mode(UnitID)
        assert response is not None
        assert isinstance(response.CurrentFCO2Mode.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetFCO2SetpointSelect(self, UnitID):
        response = self.sila_client.GassingServicer_GetFCO2SetpointSelect(UnitID)
        assert response is not None
        assert isinstance(response.CurrentFCO2SetpointSelect.value, int)

# Start FN2
    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetFCO2PV(self, UnitID):
        response = self.sila_client.GassingServicer_GetFCO2PV(UnitID)
        assert response is not None
        assert isinstance(response.CurrentFCO2PV.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetVCO2PV(self, UnitID):
        response = self.sila_client.GassingServicer_GetVCO2PV(UnitID)
        assert response is not None
        assert isinstance(response.CurrentVCO2PV.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetFCO2SP(self, UnitID):
        response = self.sila_client.GassingServicer_GetFCO2SP(UnitID)
        assert response is not None
        assert isinstance(response.CurrentFCO2SP.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetFCO2SPM(self, UnitID):
        response = self.sila_client.GassingServicer_GetFCO2SPM(UnitID)
        assert response is not None
        assert isinstance(response.CurrentFCO2SPM.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetFCO2SPE(self, UnitID):
        response = self.sila_client.GassingServicer_GetFCO2SPE(UnitID)
        assert response is not None
        assert isinstance(response.CurrentFCO2SPE.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetFCO2SPA(self, UnitID):
        response = self.sila_client.GassingServicer_GetFCO2SPA(UnitID)
        assert response is not None
        assert isinstance(response.CurrentFCO2SPA.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetFCO2SPR(self, UnitID):
        response = self.sila_client.GassingServicer_GetFCO2SPR(UnitID)
        assert response is not None
        assert isinstance(response.CurrentFCO2SPR.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetFCO2Mode(self, UnitID):
        response = self.sila_client.GassingServicer_GetFCO2Mode(UnitID)
        assert response is not None
        assert isinstance(response.CurrentFCO2Mode.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetFCO2SetpointSelect(self, UnitID):
        response = self.sila_client.GassingServicer_GetFCO2SetpointSelect(UnitID)
        assert response is not None
        assert isinstance(response.CurrentFCO2SetpointSelect.value, int)

# Start Basic
    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetAccess(self, UnitID):
        response = self.sila_client.GassingServicer_GetAccess(UnitID)
        assert response is not None
        assert isinstance(response.CurrentAccess.value, int)
        # assert response.CurrentAccess.value == UnitID  # this makes no sence i guess

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetCmd(self, UnitID):
        response = self.sila_client.GassingServicer_GetCmd(UnitID)
        assert response is not None
        assert isinstance(response.CurrentCmd.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetState(self, UnitID):
        response = self.sila_client.GassingServicer_GetState(UnitID)
        assert response is not None
        assert isinstance(response.CurrentState.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetType(self, UnitID):
        response = self.sila_client.GassingServicer_GetType(UnitID)
        assert response is not None
        assert isinstance(response.CurrentType.value, str)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetAvailable(self, UnitID):
        response = self.sila_client.GassingServicer_GetAvailable(UnitID)
        assert response is not None
        assert isinstance(response.CurrentAvailable.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetName(self, UnitID):
        response = self.sila_client.GassingServicer_GetName(UnitID)
        assert response is not None
        assert isinstance(response.CurrentName.value, str)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetVersion(self, UnitID):
        response = self.sila_client.GassingServicer_GetVersion(UnitID)
        assert response is not None
        assert isinstance(response.CurrentVersion.value, str)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetGassingMode(self, UnitID):
        response = self.sila_client.GassingServicer_GetGassingMode(UnitID)
        assert response is not None
        assert isinstance(response.CurrentGassingMode.value, int)


class TestGassingServicerSet:
    """ Test all GassingServicer Set functions. Control a DASGIP gassing module. Enables read and write operations for various parameters. """
    sila_client = DASGIP_ServiceClient(server_ip=ip, server_port=port)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(-10.00, 60.0)])  # float  # find more reasonable value
    def test_SetFSPM(self, UnitID, val):
        """ Set gassing total flow setpoint manual."""
        response = self.sila_client.GassingServicer_SetFSPM(UnitID, val)
        assert response is not None
        assert isinstance(response.FSPMSet.value, float)
        # assert response.FSPMSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(-10.00, 60.0)])  # float  # find more reasonable value
    def test_SetFSPE(self, UnitID, val):
        response = self.sila_client.GassingServicer_SetFSPE(UnitID, val)
        assert response is not None
        assert isinstance(response.FSPESet.value, float)
        # assert response.FSPESet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', random.sample(range(0, 103), 1))  # int  # find more reasonable value
    def test_SetFMode(self, UnitID, val):
        """ Set gas total flow operation mode. Controller mode (Manual, Automatic)."""
        response = self.sila_client.GassingServicer_SetFMode(UnitID, val)
        assert response is not None
        assert isinstance(response.FModeSet.value, int)
        # assert response.FModeSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', random.sample(range(0, 103), 1))  # int  # find more reasonable value
    def test_SetFSetpointSelect(self, UnitID, val):
        """ Set gas total flow setpoint selection (Local, Manual, Internal, Script, External)."""
        response = self.sila_client.GassingServicer_SetFSetpointSelect(UnitID, val)
        assert response is not None
        assert isinstance(response.FSetpointSelectSet.value, int)
        # assert response.FSetpointSelectSet.value == val

# Start Set XCO2
    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(-10.00, 60.0)])  # float  # find more reasonable value
    def test_SetXCO2SPM(self, UnitID, val):
        """ Set gassing XCO2 concentration setpoint manual."""
        response = self.sila_client.GassingServicer_SetXCO2SPM(UnitID, val)
        assert response is not None
        assert isinstance(response.XCO2SPMSet.value, float)
        # assert response.XCO2SPMSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(-10.00, 60.0)])  # float  # find more reasonable value
    def test_SetXCO2SPE(self, UnitID, val):
        """ Set gassing XCO2 concentration setpoint external."""
        response = self.sila_client.GassingServicer_SetXCO2SPE(UnitID, val)
        assert response is not None
        assert isinstance(response.XCO2SPESet.value, float)
        # assert response.XCO2SPESet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', random.sample(range(0, 103), 1))  # int  # find more reasonable value
    def test_SetXCO2Mode(self, UnitID, val):
        """ Set gas XCO2 concentration operation mode. Controller mode (Manual, Automatic)."""
        response = self.sila_client.GassingServicer_SetXCO2Mode(UnitID, val)
        assert response is not None
        assert isinstance(response.XCO2ModeSet.value, int)
        # assert response.XCO2ModeSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', random.sample(range(0, 103), 1))  # int  # find more reasonable value
    def test_SetXCO2SetpointSelect(self, UnitID, val):
        """ Set gas XCO2 concentration operation mode. Controller mode (Manual, Automatic)."""
        response = self.sila_client.GassingServicer_SetXCO2SetpointSelect(UnitID, val)
        assert response is not None
        assert isinstance(response.XCO2SetpointSelectSet.value, int)
        # assert response.XCO2SetpointSelectSet.value == val

# Start Set XO2
    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(-10.00, 60.0)])  # float  # find more reasonable value
    def test_SetXO2SPM(self, UnitID, val):
        """ Set gassing XO2 concentration setpoint manual."""
        response = self.sila_client.GassingServicer_SetXO2SPM(UnitID, val)
        assert response is not None
        assert isinstance(response.XO2SPMSet.value, float)
        # assert response.XO2SPMSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(-10.00, 60.0)])  # float  # find more reasonable value
    def test_SetXO2SPE(self, UnitID, val):
        """ Set gassing XO2 concentration setpoint external."""
        response = self.sila_client.GassingServicer_SetXO2SPE(UnitID, val)
        assert response is not None
        assert isinstance(response.XO2SPESet.value, float)
        # assert response.XO2SPESet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', random.sample(range(0, 103), 1))  # int  # find more reasonable value
    def test_SetXO2Mode(self, UnitID, val):
        """ Set gas XO2 concentration operation mode. Controller mode (Manual, Automatic)."""
        response = self.sila_client.GassingServicer_SetXO2Mode(UnitID, val)
        assert response is not None
        assert isinstance(response.XO2ModeSet.value, int)
        # assert response.XO2ModeSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', random.sample(range(0, 103), 1))  # int  # find more reasonable value
    def test_SetXO2SetpointSelect(self, UnitID, val):
        """ Set gas XO2 concentration operation mode. Controller mode (Manual, Automatic)."""
        response = self.sila_client.GassingServicer_SetXO2SetpointSelect(UnitID, val)
        assert response is not None
        assert isinstance(response.XO2SetpointSelectSet.value, int)
        # assert response.XO2SetpointSelectSet.value == val

# Start Set FAir
    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(-10.00, 60.0)])  # float  # find more reasonable value
    def test_SetFAirSPM(self, UnitID, val):
        """ Set gassing FAir concentration setpoint manual."""
        response = self.sila_client.GassingServicer_SetFAirSPM(UnitID, val)
        assert response is not None
        assert isinstance(response.FAirSPMSet.value, float)
        # assert response.FAirSPMSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(-10.00, 60.0)])  # float  # find more reasonable value
    def test_SetFAirSPE(self, UnitID, val):
        """ Set gassing FAir concentration setpoint external."""
        response = self.sila_client.GassingServicer_SetFAirSPE(UnitID, val)
        assert response is not None
        assert isinstance(response.FAirSPESet.value, float)
        # assert response.FAirSPESet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', random.sample(range(0, 103), 1))  # int  # find more reasonable value
    def test_SetFAirMode(self, UnitID, val):
        """ Set gas FAir concentration operation mode. Controller mode (Manual, Automatic)."""
        response = self.sila_client.GassingServicer_SetFAirMode(UnitID, val)
        assert response is not None
        assert isinstance(response.FAirModeSet.value, int)
        # assert response.FAirModeSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', random.sample(range(0, 103), 1))  # int  # find more reasonable value
    def test_SetFAirSetpointSelect(self, UnitID, val):
        """ Set gas FAir concentration operation mode. Controller mode (Manual, Automatic)."""
        response = self.sila_client.GassingServicer_SetFAirSetpointSelect(UnitID, val)
        assert response is not None
        assert isinstance(response.FAirSetpointSelectSet.value, int)
        # assert response.FAirSetpointSelectSet.value == val

# Start Set FO2
    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(-10.00, 60.0)])  # float  # find more reasonable value
    def test_SetFO2SPM(self, UnitID, val):
        """ Set gassing FO2 concentration setpoint manual."""
        response = self.sila_client.GassingServicer_SetFO2SPM(UnitID, val)
        assert response is not None
        assert isinstance(response.FO2SPMSet.value, float)
        # assert response.FO2SPMSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(-10.00, 60.0)])  # float  # find more reasonable value
    def test_SetFO2SPE(self, UnitID, val):
        """ Set gassing FO2 concentration setpoint external."""
        response = self.sila_client.GassingServicer_SetFO2SPE(UnitID, val)
        assert response is not None
        assert isinstance(response.FO2SPESet.value, float)
        # assert response.FO2SPESet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', random.sample(range(0, 103), 1))  # int  # find more reasonable value
    def test_SetFO2Mode(self, UnitID, val):
        """ Set gas FO2 concentration operation mode. Controller mode (Manual, Automatic)."""
        response = self.sila_client.GassingServicer_SetFO2Mode(UnitID, val)
        assert response is not None
        assert isinstance(response.FO2ModeSet.value, int)
        # assert response.FO2ModeSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', random.sample(range(0, 103), 1))  # int  # find more reasonable value
    def test_SetFO2SetpointSelect(self, UnitID, val):
        """ Set gas FO2 concentration operation mode. Controller mode (Manual, Automatic)."""
        response = self.sila_client.GassingServicer_SetFO2SetpointSelect(UnitID, val)
        assert response is not None
        assert isinstance(response.FO2SetpointSelectSet.value, int)
        # assert response.FO2SetpointSelectSet.value == val

# Start Set FCO2
    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(-10.00, 60.0)])  # float  # find more reasonable value
    def test_SetFCO2SPM(self, UnitID, val):
        """ Set gassing FCO2 concentration setpoint manual."""
        response = self.sila_client.GassingServicer_SetFCO2SPM(UnitID, val)
        assert response is not None
        assert isinstance(response.FCO2SPMSet.value, float)
        # assert response.FCO2SPMSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(-10.00, 60.0)])  # float  # find more reasonable value
    def test_SetFCO2SPE(self, UnitID, val):
        """ Set gassing FCO2 concentration setpoint external."""
        response = self.sila_client.GassingServicer_SetFCO2SPE(UnitID, val)
        assert response is not None
        assert isinstance(response.FCO2SPESet.value, float)
        # assert response.FCO2SPESet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', random.sample(range(0, 103), 1))  # int  # find more reasonable value
    def test_SetFCO2Mode(self, UnitID, val):
        """ Set gas FCO2 concentration operation mode. Controller mode (Manual, Automatic)."""
        response = self.sila_client.GassingServicer_SetFCO2Mode(UnitID, val)
        assert response is not None
        assert isinstance(response.FCO2ModeSet.value, int)
        # assert response.FCO2ModeSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', random.sample(range(0, 103), 1))  # int  # find more reasonable value
    def test_SetFCO2SetpointSelect(self, UnitID, val):
        """ Set gas FCO2 concentration operation mode. Controller mode (Manual, Automatic)."""
        response = self.sila_client.GassingServicer_SetFCO2SetpointSelect(UnitID, val)
        assert response is not None
        assert isinstance(response.FCO2SetpointSelectSet.value, int)
        # assert response.FCO2SetpointSelectSet.value == val

# Start Set F2
    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(-10.00, 60.0)])  # float  # find more reasonable value
    def test_SetFN2SPM(self, UnitID, val):
        """ Set gassing FN2 concentration setpoint manual."""
        response = self.sila_client.GassingServicer_SetFN2SPM(UnitID, val)
        assert response is not None
        assert isinstance(response.FN2SPMSet.value, float)
        # assert response.FN2SPMSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(-10.00, 60.0)])  # float  # find more reasonable value
    def test_SetFN2SPE(self, UnitID, val):
        """ Set gassing FN2 concentration setpoint external."""
        response = self.sila_client.GassingServicer_SetFN2SPE(UnitID, val)
        assert response is not None
        assert isinstance(response.FN2SPESet.value, float)
        # assert response.FN2SPESet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', random.sample(range(0, 103), 1))  # int  # find more reasonable value
    def test_SetFN2Mode(self, UnitID, val):
        """ Set gas FN2 concentration operation mode. Controller mode (Manual, Automatic)."""
        response = self.sila_client.GassingServicer_SetFN2Mode(UnitID, val)
        assert response is not None
        assert isinstance(response.FN2ModeSet.value, int)
        # assert response.FN2ModeSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', random.sample(range(0, 103), 1))  # int  # find more reasonable value
    def test_SetFN2SetpointSelect(self, UnitID, val):
        """ Set gas FN2 concentration operation mode. Controller mode (Manual, Automatic)."""
        response = self.sila_client.GassingServicer_SetFN2SetpointSelect(UnitID, val)
        assert response is not None
        assert isinstance(response.FN2SetpointSelectSet.value, int)
        # assert response.FN2SetpointSelectSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', random.sample(range(0, 3), 1))  # int
    def test_SetCmd(self, UnitID, val):
        """ Set the controller command. Controller command (Nothing, Stop, Start)."""
        response = self.sila_client.GassingServicer_SetCmd(UnitID, val)
        assert response is not None
        assert isinstance(response.CmdSet.value, int)
        # assert response.CmdSet.value == val


class TestOverlayServicerGet:
    """ Test all OverlayServicer Get functions. Control a DASGIP gassing module. Enables read and write operations for various parameters. """
    sila_client = DASGIP_ServiceClient(server_ip=ip, server_port=port)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetPV(self, UnitID):
        response = self.sila_client.OverlayServicer_GetPV(UnitID)
        assert response is not None
        assert isinstance(response.CurrentPV.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetSP(self, UnitID):
        response = self.sila_client.OverlayServicer_GetSP(UnitID)
        assert response is not None
        assert isinstance(response.CurrentSP.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetFPV(self, UnitID):
        response = self.sila_client.OverlayServicer_GetFPV(UnitID)
        assert response is not None
        assert isinstance(response.CurrentFPV.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetVPV(self, UnitID):
        response = self.sila_client.OverlayServicer_GetVPV(UnitID)
        assert response is not None
        assert isinstance(response.CurrentVPV.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetFSP(self, UnitID):
        response = self.sila_client.OverlayServicer_GetFSP(UnitID)
        assert response is not None
        assert isinstance(response.CurrentFSP.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetFSPM(self, UnitID):
        response = self.sila_client.OverlayServicer_GetFSPM(UnitID)
        assert response is not None
        assert isinstance(response.CurrentFSPM.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetFSPE(self, UnitID):
        response = self.sila_client.OverlayServicer_GetFSPE(UnitID)
        assert response is not None
        assert isinstance(response.CurrentFSPE.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetFSPA(self, UnitID):
        response = self.sila_client.OverlayServicer_GetFSPA(UnitID)
        assert response is not None
        assert isinstance(response.CurrentFSPA.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetFSPR(self, UnitID):
        response = self.sila_client.OverlayServicer_GetFSPR(UnitID)
        assert response is not None
        assert isinstance(response.CurrentFSPR.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetFSPL(self, UnitID):
        response = self.sila_client.OverlayServicer_GetFSPL(UnitID)
        assert response is not None
        assert isinstance(response.CurrentFSPL.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetFMode(self, UnitID):
        """ Get gas total flow operation mode. Controller mode (Manual, Automatic)"""
        response = self.sila_client.OverlayServicer_GetFMode(UnitID)
        assert response is not None
        assert isinstance(response.CurrentFMode.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetFSetpointSelect(self, UnitID):
        """ Get gas total flow setpoint selection (Local, Manual, Internal, Script, External)."""
        response = self.sila_client.OverlayServicer_GetFSetpointSelect(UnitID)
        assert response is not None
        assert isinstance(response.CurrentFSetpointSelect.value, int)
# Start CO2
    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetXCO2PV(self, UnitID):
        """ Current gas total flow setpoint selection (Local, Manual, Internal, Script, External)."""
        response = self.sila_client.OverlayServicer_GetXCO2PV(UnitID)
        assert response is not None
        assert isinstance(response.CurrentXCO2PV.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetXCO2SP(self, UnitID):
        response = self.sila_client.OverlayServicer_GetXCO2SP(UnitID)
        assert response is not None
        assert isinstance(response.CurrentXCO2SP.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetXCO2SPM(self, UnitID):
        response = self.sila_client.OverlayServicer_GetXCO2SPM(UnitID)
        assert response is not None
        assert isinstance(response.CurrentXCO2SPM.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetXCO2SPE(self, UnitID):
        response = self.sila_client.OverlayServicer_GetXCO2SPE(UnitID)
        assert response is not None
        assert isinstance(response.CurrentXCO2SPE.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetXCO2SPA(self, UnitID):
        response = self.sila_client.OverlayServicer_GetXCO2SPA(UnitID)
        assert response is not None
        assert isinstance(response.CurrentXCO2SPA.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetXCO2SPR(self, UnitID):
        response = self.sila_client.OverlayServicer_GetXCO2SPR(UnitID)
        assert response is not None
        assert isinstance(response.CurrentXCO2SPR.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetXCO2SPL(self, UnitID):
        response = self.sila_client.OverlayServicer_GetXCO2SPL(UnitID)
        assert response is not None
        assert isinstance(response.CurrentXCO2SPL.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetXCO2Mode(self, UnitID):
        response = self.sila_client.OverlayServicer_GetXCO2Mode(UnitID)
        assert response is not None
        assert isinstance(response.CurrentXCO2Mode.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetXCO2SetpointSelect(self, UnitID):
        response = self.sila_client.OverlayServicer_GetXCO2SetpointSelect(UnitID)
        assert response is not None
        assert isinstance(response.CurrentXCO2SetpointSelect.value, int)

# Start O2
    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetXO2PV(self, UnitID):
        response = self.sila_client.OverlayServicer_GetXO2PV(UnitID)
        assert response is not None
        assert isinstance(response.CurrentXO2PV.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetXO2SP(self, UnitID):
        response = self.sila_client.OverlayServicer_GetXO2SP(UnitID)
        assert response is not None
        assert isinstance(response.CurrentXO2SP.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetXO2SPM(self, UnitID):
        response = self.sila_client.OverlayServicer_GetXO2SPM(UnitID)
        assert response is not None
        assert isinstance(response.CurrentXO2SPM.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetXO2SPE(self, UnitID):
        response = self.sila_client.OverlayServicer_GetXO2SPE(UnitID)
        assert response is not None
        assert isinstance(response.CurrentXO2SPE.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetXO2SPA(self, UnitID):
        response = self.sila_client.OverlayServicer_GetXO2SPA(UnitID)
        assert response is not None
        assert isinstance(response.CurrentXO2SPA.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetXO2SPR(self, UnitID):
        response = self.sila_client.OverlayServicer_GetXO2SPR(UnitID)
        assert response is not None
        assert isinstance(response.CurrentXO2SPR.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetXO2SPL(self, UnitID):
        response = self.sila_client.OverlayServicer_GetXO2SPL(UnitID)
        assert response is not None
        assert isinstance(response.CurrentXO2SPL.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetXO2Mode(self, UnitID):
        response = self.sila_client.OverlayServicer_GetXO2Mode(UnitID)
        assert response is not None
        assert isinstance(response.CurrentXO2Mode.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetXO2SetpointSelect(self, UnitID):
        response = self.sila_client.OverlayServicer_GetXO2SetpointSelect(UnitID)
        assert response is not None
        assert isinstance(response.CurrentXO2SetpointSelect.value, int)

# Start Air
    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetFAirPV(self, UnitID):
        response = self.sila_client.OverlayServicer_GetFAirPV(UnitID)
        assert response is not None
        assert isinstance(response.CurrentFAirPV.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetVAirPV(self, UnitID):
        response = self.sila_client.OverlayServicer_GetVAirPV(UnitID)
        assert response is not None
        assert isinstance(response.CurrentVAirPV.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetFAirSP(self, UnitID):
        response = self.sila_client.OverlayServicer_GetFAirSP(UnitID)
        assert response is not None
        assert isinstance(response.CurrentFAirSP.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetFAirSPM(self, UnitID):
        response = self.sila_client.OverlayServicer_GetFAirSPM(UnitID)
        assert response is not None
        assert isinstance(response.CurrentFAirSPM.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetFAirSPE(self, UnitID):
        response = self.sila_client.OverlayServicer_GetFAirSPE(UnitID)
        assert response is not None
        assert isinstance(response.CurrentFAirSPE.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetFAirSPA(self, UnitID):
        response = self.sila_client.OverlayServicer_GetFAirSPA(UnitID)
        assert response is not None
        assert isinstance(response.CurrentFAirSPA.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetFAirSPR(self, UnitID):
        response = self.sila_client.OverlayServicer_GetFAirSPR(UnitID)
        assert response is not None
        assert isinstance(response.CurrentFAirSPR.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetFAirMode(self, UnitID):
        response = self.sila_client.OverlayServicer_GetFAirMode(UnitID)
        assert response is not None
        assert isinstance(response.CurrentFAirMode.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetFAirSetpointSelect(self, UnitID):
        response = self.sila_client.OverlayServicer_GetFAirSetpointSelect(UnitID)
        assert response is not None
        assert isinstance(response.CurrentFAirSetpointSelect.value, int)

# Start FO2
    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetFO2PV(self, UnitID):
        response = self.sila_client.OverlayServicer_GetFO2PV(UnitID)
        assert response is not None
        assert isinstance(response.CurrentFO2PV.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetVO2PV(self, UnitID):
        response = self.sila_client.OverlayServicer_GetVO2PV(UnitID)
        assert response is not None
        assert isinstance(response.CurrentVO2PV.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetFO2SP(self, UnitID):
        response = self.sila_client.OverlayServicer_GetFO2SP(UnitID)
        assert response is not None
        assert isinstance(response.CurrentFO2SP.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetFO2SPM(self, UnitID):
        response = self.sila_client.OverlayServicer_GetFO2SPM(UnitID)
        assert response is not None
        assert isinstance(response.CurrentFO2SPM.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetFO2SPE(self, UnitID):
        response = self.sila_client.OverlayServicer_GetFO2SPE(UnitID)
        assert response is not None
        assert isinstance(response.CurrentFO2SPE.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetFO2SPA(self, UnitID):
        response = self.sila_client.OverlayServicer_GetFO2SPA(UnitID)
        assert response is not None
        assert isinstance(response.CurrentFO2SPA.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetFO2SPR(self, UnitID):
        response = self.sila_client.OverlayServicer_GetFO2SPR(UnitID)
        assert response is not None
        assert isinstance(response.CurrentFO2SPR.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetFO2Mode(self, UnitID):
        response = self.sila_client.OverlayServicer_GetFO2Mode(UnitID)
        assert response is not None
        assert isinstance(response.CurrentFO2Mode.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetFO2SetpointSelect(self, UnitID):
        response = self.sila_client.OverlayServicer_GetFO2SetpointSelect(UnitID)
        assert response is not None
        assert isinstance(response.CurrentFO2SetpointSelect.value, int)

# Start FCO2
    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetFCO2PV(self, UnitID):
        response = self.sila_client.OverlayServicer_GetFCO2PV(UnitID)
        assert response is not None
        assert isinstance(response.CurrentFCO2PV.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetVCO2PV(self, UnitID):
        response = self.sila_client.OverlayServicer_GetVCO2PV(UnitID)
        assert response is not None
        assert isinstance(response.CurrentVCO2PV.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetFCO2SP(self, UnitID):
        response = self.sila_client.OverlayServicer_GetFCO2SP(UnitID)
        assert response is not None
        assert isinstance(response.CurrentFCO2SP.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetFCO2SPM(self, UnitID):
        response = self.sila_client.OverlayServicer_GetFCO2SPM(UnitID)
        assert response is not None
        assert isinstance(response.CurrentFCO2SPM.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetFCO2SPE(self, UnitID):
        response = self.sila_client.OverlayServicer_GetFCO2SPE(UnitID)
        assert response is not None
        assert isinstance(response.CurrentFCO2SPE.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetFCO2SPA(self, UnitID):
        response = self.sila_client.OverlayServicer_GetFCO2SPA(UnitID)
        assert response is not None
        assert isinstance(response.CurrentFCO2SPA.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetFCO2SPR(self, UnitID):
        response = self.sila_client.OverlayServicer_GetFCO2SPR(UnitID)
        assert response is not None
        assert isinstance(response.CurrentFCO2SPR.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetFCO2Mode(self, UnitID):
        response = self.sila_client.OverlayServicer_GetFCO2Mode(UnitID)
        assert response is not None
        assert isinstance(response.CurrentFCO2Mode.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetFCO2SetpointSelect(self, UnitID):
        response = self.sila_client.OverlayServicer_GetFCO2SetpointSelect(UnitID)
        assert response is not None
        assert isinstance(response.CurrentFCO2SetpointSelect.value, int)

# Start FN2
    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetFCO2PV(self, UnitID):
        response = self.sila_client.OverlayServicer_GetFCO2PV(UnitID)
        assert response is not None
        assert isinstance(response.CurrentFCO2PV.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetVCO2PV(self, UnitID):
        response = self.sila_client.OverlayServicer_GetVCO2PV(UnitID)
        assert response is not None
        assert isinstance(response.CurrentVCO2PV.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetFCO2SP(self, UnitID):
        response = self.sila_client.OverlayServicer_GetFCO2SP(UnitID)
        assert response is not None
        assert isinstance(response.CurrentFCO2SP.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetFCO2SPM(self, UnitID):
        response = self.sila_client.OverlayServicer_GetFCO2SPM(UnitID)
        assert response is not None
        assert isinstance(response.CurrentFCO2SPM.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetFCO2SPE(self, UnitID):
        response = self.sila_client.OverlayServicer_GetFCO2SPE(UnitID)
        assert response is not None
        assert isinstance(response.CurrentFCO2SPE.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetFCO2SPA(self, UnitID):
        response = self.sila_client.OverlayServicer_GetFCO2SPA(UnitID)
        assert response is not None
        assert isinstance(response.CurrentFCO2SPA.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetFCO2SPR(self, UnitID):
        response = self.sila_client.OverlayServicer_GetFCO2SPR(UnitID)
        assert response is not None
        assert isinstance(response.CurrentFCO2SPR.value, float)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetFCO2Mode(self, UnitID):
        response = self.sila_client.OverlayServicer_GetFCO2Mode(UnitID)
        assert response is not None
        assert isinstance(response.CurrentFCO2Mode.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetFCO2SetpointSelect(self, UnitID):
        response = self.sila_client.OverlayServicer_GetFCO2SetpointSelect(UnitID)
        assert response is not None
        assert isinstance(response.CurrentFCO2SetpointSelect.value, int)

# Start Basic
    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetAccess(self, UnitID):
        response = self.sila_client.OverlayServicer_GetAccess(UnitID)
        assert response is not None
        assert isinstance(response.CurrentAccess.value, int)
        # assert response.CurrentAccess.value == UnitID  # this makes no sence i guess

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetCmd(self, UnitID):
        response = self.sila_client.OverlayServicer_GetCmd(UnitID)
        assert response is not None
        assert isinstance(response.CurrentCmd.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetState(self, UnitID):
        response = self.sila_client.OverlayServicer_GetState(UnitID)
        assert response is not None
        assert isinstance(response.CurrentState.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetType(self, UnitID):
        response = self.sila_client.OverlayServicer_GetType(UnitID)
        assert response is not None
        assert isinstance(response.CurrentType.value, str)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetAvailable(self, UnitID):
        response = self.sila_client.OverlayServicer_GetAvailable(UnitID)
        assert response is not None
        assert isinstance(response.CurrentAvailable.value, int)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetName(self, UnitID):
        response = self.sila_client.OverlayServicer_GetName(UnitID)
        assert response is not None
        assert isinstance(response.CurrentName.value, str)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetVersion(self, UnitID):
        response = self.sila_client.OverlayServicer_GetVersion(UnitID)
        assert response is not None
        assert isinstance(response.CurrentVersion.value, str)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    def test_GetGassingMode(self, UnitID):
        response = self.sila_client.OverlayServicer_GetGassingMode(UnitID)
        assert response is not None
        assert isinstance(response.CurrentGassingMode.value, int)


class TestOverlayServicerSet:
    """ Test all OverlayServicer Set functions. Control a DASGIP Overlay module. Enables read and write operations for various parameters. """
    sila_client = DASGIP_ServiceClient(server_ip=ip, server_port=port)

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(-10.00, 60.0)])  # float  # find more reasonable value
    def test_SetFSPM(self, UnitID, val):
        """ Set gassing total flow setpoint manual."""
        response = self.sila_client.OverlayServicer_SetFSPM(UnitID, val)
        assert response is not None
        assert isinstance(response.FSPMSet.value, float)
        # assert response.FSPMSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(-10.00, 60.0)])  # float  # find more reasonable value
    def test_SetFSPE(self, UnitID, val):
        response = self.sila_client.OverlayServicer_SetFSPE(UnitID, val)
        assert response is not None
        assert isinstance(response.FSPESet.value, float)
        # assert response.FSPESet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', random.sample(range(0, 103), 1))  # int  # find more reasonable value
    def test_SetFMode(self, UnitID, val):
        """ Set gas total flow operation mode. Controller mode (Manual, Automatic)."""
        response = self.sila_client.OverlayServicer_SetFMode(UnitID, val)
        assert response is not None
        assert isinstance(response.FModeSet.value, int)
        # assert response.FModeSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', random.sample(range(0, 103), 1))  # int  # find more reasonable value
    def test_SetFSetpointSelect(self, UnitID, val):
        """ Set gas total flow setpoint selection (Local, Manual, Internal, Script, External)."""
        response = self.sila_client.OverlayServicer_SetFSetpointSelect(UnitID, val)
        assert response is not None
        assert isinstance(response.FSetpointSelectSet.value, int)
        # assert response.FSetpointSelectSet.value == val

# Start Set XCO2
    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(-10.00, 60.0)])  # float  # find more reasonable value
    def test_SetXCO2SPM(self, UnitID, val):
        """ Set gassing XCO2 concentration setpoint manual."""
        response = self.sila_client.OverlayServicer_SetXCO2SPM(UnitID, val)
        assert response is not None
        assert isinstance(response.XCO2SPMSet.value, float)
        # assert response.XCO2SPMSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(-10.00, 60.0)])  # float  # find more reasonable value
    def test_SetXCO2SPE(self, UnitID, val):
        """ Set gassing XCO2 concentration setpoint external."""
        response = self.sila_client.OverlayServicer_SetXCO2SPE(UnitID, val)
        assert response is not None
        assert isinstance(response.XCO2SPESet.value, float)
        # assert response.XCO2SPESet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', random.sample(range(0, 103), 1))  # int  # find more reasonable value
    def test_SetXCO2Mode(self, UnitID, val):
        """ Set gas XCO2 concentration operation mode. Controller mode (Manual, Automatic)."""
        response = self.sila_client.OverlayServicer_SetXCO2Mode(UnitID, val)
        assert response is not None
        assert isinstance(response.XCO2ModeSet.value, int)
        # assert response.XCO2ModeSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', random.sample(range(0, 103), 1))  # int  # find more reasonable value
    def test_SetXCO2SetpointSelect(self, UnitID, val):
        """ Set gas XCO2 concentration operation mode. Controller mode (Manual, Automatic)."""
        response = self.sila_client.OverlayServicer_SetXCO2SetpointSelect(UnitID, val)
        assert response is not None
        assert isinstance(response.XCO2SetpointSelectSet.value, int)
        # assert response.XCO2SetpointSelectSet.value == val

# Start Set XO2
    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(-10.00, 60.0)])  # float  # find more reasonable value
    def test_SetXO2SPM(self, UnitID, val):
        """ Set gassing XO2 concentration setpoint manual."""
        response = self.sila_client.OverlayServicer_SetXO2SPM(UnitID, val)
        assert response is not None
        assert isinstance(response.XO2SPMSet.value, float)
        # assert response.XO2SPMSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(-10.00, 60.0)])  # float  # find more reasonable value
    def test_SetXO2SPE(self, UnitID, val):
        """ Set gassing XO2 concentration setpoint external."""
        response = self.sila_client.OverlayServicer_SetXO2SPE(UnitID, val)
        assert response is not None
        assert isinstance(response.XO2SPESet.value, float)
        # assert response.XO2SPESet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', random.sample(range(0, 103), 1))  # int  # find more reasonable value
    def test_SetXO2Mode(self, UnitID, val):
        """ Set gas XO2 concentration operation mode. Controller mode (Manual, Automatic)."""
        response = self.sila_client.OverlayServicer_SetXO2Mode(UnitID, val)
        assert response is not None
        assert isinstance(response.XO2ModeSet.value, int)
        # assert response.XO2ModeSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', random.sample(range(0, 103), 1))  # int  # find more reasonable value
    def test_SetXO2SetpointSelect(self, UnitID, val):
        """ Set gas XO2 concentration operation mode. Controller mode (Manual, Automatic)."""
        response = self.sila_client.OverlayServicer_SetXO2SetpointSelect(UnitID, val)
        assert response is not None
        assert isinstance(response.XO2SetpointSelectSet.value, int)
        # assert response.XO2SetpointSelectSet.value == val

# Start Set FAir
    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(-10.00, 60.0)])  # float  # find more reasonable value
    def test_SetFAirSPM(self, UnitID, val):
        """ Set gassing FAir concentration setpoint manual."""
        response = self.sila_client.OverlayServicer_SetFAirSPM(UnitID, val)
        assert response is not None
        assert isinstance(response.FAirSPMSet.value, float)
        # assert response.FAirSPMSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(-10.00, 60.0)])  # float  # find more reasonable value
    def test_SetFAirSPE(self, UnitID, val):
        """ Set gassing FAir concentration setpoint external."""
        response = self.sila_client.OverlayServicer_SetFAirSPE(UnitID, val)
        assert response is not None
        assert isinstance(response.FAirSPESet.value, float)
        # assert response.FAirSPESet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', random.sample(range(0, 103), 1))  # int  # find more reasonable value
    def test_SetFAirMode(self, UnitID, val):
        """ Set gas FAir concentration operation mode. Controller mode (Manual, Automatic)."""
        response = self.sila_client.OverlayServicer_SetFAirMode(UnitID, val)
        assert response is not None
        assert isinstance(response.FAirModeSet.value, int)
        # assert response.FAirModeSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', random.sample(range(0, 103), 1))  # int  # find more reasonable value
    def test_SetFAirSetpointSelect(self, UnitID, val):
        """ Set gas FAir concentration operation mode. Controller mode (Manual, Automatic)."""
        response = self.sila_client.OverlayServicer_SetFAirSetpointSelect(UnitID, val)
        assert response is not None
        assert isinstance(response.FAirSetpointSelectSet.value, int)
        # assert response.FAirSetpointSelectSet.value == val

# Start Set FO2
    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(-10.00, 60.0)])  # float  # find more reasonable value
    def test_SetFO2SPM(self, UnitID, val):
        """ Set gassing FO2 concentration setpoint manual."""
        response = self.sila_client.OverlayServicer_SetFO2SPM(UnitID, val)
        assert response is not None
        assert isinstance(response.FO2SPMSet.value, float)
        # assert response.FO2SPMSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(-10.00, 60.0)])  # float  # find more reasonable value
    def test_SetFO2SPE(self, UnitID, val):
        """ Set gassing FO2 concentration setpoint external."""
        response = self.sila_client.OverlayServicer_SetFO2SPE(UnitID, val)
        assert response is not None
        assert isinstance(response.FO2SPESet.value, float)
        # assert response.FO2SPESet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', random.sample(range(0, 103), 1))  # int  # find more reasonable value
    def test_SetFO2Mode(self, UnitID, val):
        """ Set gas FO2 concentration operation mode. Controller mode (Manual, Automatic)."""
        response = self.sila_client.OverlayServicer_SetFO2Mode(UnitID, val)
        assert response is not None
        assert isinstance(response.FO2ModeSet.value, int)
        # assert response.FO2ModeSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', random.sample(range(0, 103), 1))  # int  # find more reasonable value
    def test_SetFO2SetpointSelect(self, UnitID, val):
        """ Set gas FO2 concentration operation mode. Controller mode (Manual, Automatic)."""
        response = self.sila_client.OverlayServicer_SetFO2SetpointSelect(UnitID, val)
        assert response is not None
        assert isinstance(response.FO2SetpointSelectSet.value, int)
        # assert response.FO2SetpointSelectSet.value == val

# Start Set FCO2
    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(-10.00, 60.0)])  # float  # find more reasonable value
    def test_SetFCO2SPM(self, UnitID, val):
        """ Set gassing FCO2 concentration setpoint manual."""
        response = self.sila_client.OverlayServicer_SetFCO2SPM(UnitID, val)
        assert response is not None
        assert isinstance(response.FCO2SPMSet.value, float)
        # assert response.FCO2SPMSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(-10.00, 60.0)])  # float  # find more reasonable value
    def test_SetFCO2SPE(self, UnitID, val):
        """ Set gassing FCO2 concentration setpoint external."""
        response = self.sila_client.OverlayServicer_SetFCO2SPE(UnitID, val)
        assert response is not None
        assert isinstance(response.FCO2SPESet.value, float)
        # assert response.FCO2SPESet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', random.sample(range(0, 103), 1))  # int  # find more reasonable value
    def test_SetFCO2Mode(self, UnitID, val):
        """ Set gas FCO2 concentration operation mode. Controller mode (Manual, Automatic)."""
        response = self.sila_client.OverlayServicer_SetFCO2Mode(UnitID, val)
        assert response is not None
        assert isinstance(response.FCO2ModeSet.value, int)
        # assert response.FCO2ModeSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', random.sample(range(0, 103), 1))  # int  # find more reasonable value
    def test_SetFCO2SetpointSelect(self, UnitID, val):
        """ Set gas FCO2 concentration operation mode. Controller mode (Manual, Automatic)."""
        response = self.sila_client.OverlayServicer_SetFCO2SetpointSelect(UnitID, val)
        assert response is not None
        assert isinstance(response.FCO2SetpointSelectSet.value, int)
        # assert response.FCO2SetpointSelectSet.value == val

# Start Set F2
    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(-10.00, 60.0)])  # float  # find more reasonable value
    def test_SetFN2SPM(self, UnitID, val):
        """ Set gassing FN2 concentration setpoint manual."""
        response = self.sila_client.OverlayServicer_SetFN2SPM(UnitID, val)
        assert response is not None
        assert isinstance(response.FN2SPMSet.value, float)
        # assert response.FN2SPMSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', [random.uniform(-10.00, 60.0)])  # float  # find more reasonable value
    def test_SetFN2SPE(self, UnitID, val):
        """ Set gassing FN2 concentration setpoint external."""
        response = self.sila_client.OverlayServicer_SetFN2SPE(UnitID, val)
        assert response is not None
        assert isinstance(response.FN2SPESet.value, float)
        # assert response.FN2SPESet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', random.sample(range(0, 103), 1))  # int  # find more reasonable value
    def test_SetFN2Mode(self, UnitID, val):
        """ Set gas FN2 concentration operation mode. Controller mode (Manual, Automatic)."""
        response = self.sila_client.OverlayServicer_SetFN2Mode(UnitID, val)
        assert response is not None
        assert isinstance(response.FN2ModeSet.value, int)
        # assert response.FN2ModeSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', random.sample(range(0, 103), 1))  # int  # find more reasonable value
    def test_SetFN2SetpointSelect(self, UnitID, val):
        """ Set gas FN2 concentration operation mode. Controller mode (Manual, Automatic)."""
        response = self.sila_client.OverlayServicer_SetFN2SetpointSelect(UnitID, val)
        assert response is not None
        assert isinstance(response.FN2SetpointSelectSet.value, int)
        # assert response.FN2SetpointSelectSet.value == val

    @pytest.mark.parametrize('UnitID', random.sample(range(0, unit_ids), 1))  # int
    @pytest.mark.parametrize('val', random.sample(range(0, 3), 1))  # int
    def test_SetCmd(self, UnitID, val):
        """ Set the controller command. Controller command (Nothing, Stop, Start)."""
        response = self.sila_client.OverlayServicer_SetCmd(UnitID, val)
        assert response is not None
        assert isinstance(response.CmdSet.value, int)
        # assert response.CmdSet.value == val


def test__init__():
    """ Starts the server in a mocked environment as defined in DASGIP_Service_server.init()"""
    from sila2lib.sila_server import SiLA2Server
    with mock.patch.object(SiLA2Server, 'run', return_value=42):  # Syntax: .object(class, 'method', return)
        with mock.patch.object(DASGIP_Service_server, '__name__', '__main__'):
            with mock.patch.object(DASGIP_Service_server.sys, 'exit') as mock_exit:
                DASGIP_Service_server.init()
                assert mock_exit.call_args[0][0] == 42
