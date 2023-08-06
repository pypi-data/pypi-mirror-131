#!/usr/bin/env python3
"""
This file tests the simulation- or real mode of LOOP Thermoelectric Heating and Cooling Unit, LAUDA-Brinkmann.
LAUDA LOOP provides rapid and precise temperature control with a working range of 4 to 80 °C

REAL TESTS have to be executed with precaution. However, a secure mode is implemented by default that prevents breakdown
of the device due to overheating e.g.. For safe testing these steps have to be performed BEFORE test execution:
--Perform steps as usually to properly start up the device (here a cooling unit is needed)
--Connect the serial cable to device and PC (USB port favorably)

STRUCTURE:
Tests are organized in classes to logically separate the
services' features, as well as get- from set-functions. Return values are validated for data types, value range and whether
length of return values is as desired (e.g. as input values). All returns must assert "True", since the injected input
parameter range is only valid. For invalid parameter injection and error handling see:
'test_lauda_simulation_error.py'
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

from sila2lib_implementations.LAUDA.LAUDA_ThermostatService.LAUDA_ThermostatService_client import \
    LAUDA_ThermostatServiceClient
from sila2lib_implementations.LAUDA.LAUDA_ThermostatService import LAUDA_ThermostatService_server

from tests.config import settings

logger = logging.getLogger(__name__)
# logging.basicConfig(format  = '%(asctime)s - %(name)s - %(levelname)s- %(module)s - linenumber: %(lineno)d - %(message)s', level=logging.DEBUG)

# Set variables of Dotenv
ip = settings.LAUDA_IP
port = settings.LAUDA_PORT
simulation_mode = settings.LAUDA_SIMULATION_MODE

# test condition definition
sample_depth = 2
restore_default = dict()


# ____________________start boilerplate__________________________________

#
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
# class LaudaTestServer(LAUDA_ThermostatService_server.LAUDA_ThermostatServiceServer):
#     """
#     Test server instance. Implementation of service until an abort event is sent
#     :param abort_event: Event that leads to the server stop
#     """
#
#     ip = settings.LAUDA_IP
#     port = settings.LAUDA_PORT
#     simulation_mode = settings.LAUDA_SIMULATION_MODE
#
#     def __init__(self, abort_event: Event):
#         self.abort_event = abort_event
#         super().__init__(cmd_args='lauda', ip=self.ip, port=self.port, simulation_mode=self.simulation_mode)
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
# def setup_and_teardown_lauda_server():
#     """
#     Starts a server thread and tears it down automatically after the whole module is executed.
#     """
#     abort_event = Event()
#     server = LaudaTestServer(abort_event)
#     thread = Thread(target=server.serve, args=(), daemon=True)
#     thread.start()
#     wait_until_server_up(server)
#     logger.info('Started Lauda server')
#     yield thread
#     abort_event.set()
#     thread.join(timeout=10)
#     wait_until_port_closes(ip=LaudaTestServer.ip, port=LaudaTestServer.port, timeout=10)
#     if thread.is_alive:
#         logger.warning(f'Lauda server thread is still alive: {thread.is_alive()}')
#     logger.info('Stopped Lauda server')

# ____________________end boilerplate__________________________________

#
# class TestBlueVaryServerFunctionalities:
#     """
#     Basic connection test with the server. Also checks if the server was started with the correct parameters (port, ip, mode)
#     """
#     # Setup_class is meant to be used like __init__ but the latter is causing problems in pytest
#     # (cannot collect test class because it has a __init__ constructor)
#     def setup_class(cls):
#         cls.sila_client = LAUDA_ThermostatServiceClient(server_ip=LaudaTestServer.ip, server_port=LaudaTestServer.port)
#
#     def test_run_bluevary_test_server(self, setup_and_teardown_lauda_server):
#         logger.info(f'PreSens server running. Is alive: {setup_and_teardown_lauda_server.is_alive()}')
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
#         assert self.sila_client.server_port is LaudaTestServer.port
#         assert self.sila_client.server_hostname is LaudaTestServer.ip
#         assert self.sila_client.server_display_name == ''
#         assert self.sila_client.server_description == ''
#         assert self.sila_client.server_version == ''
#
#     def test_client_values(self):
#         assert self.sila_client.vendor_url == ''
#         assert self.sila_client.name == 'LAUDA_ThermostatServiceClient'
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


# todo: test the 'teardown' real mode without device is failing due to TypeError: object of type int/float has no len()
# backup real default data before in case my method fails

# todo: think about frequency for reseting to defaults. In case something fails that independend of execution stops,
# default values are Set in the end
@pytest.fixture(scope='function')
def teardown_restore_default():
    """ Restores the default values to gain back the pre-test state. """
    if simulation_mode is False:
        sila_client = LAUDA_ThermostatServiceClient(server_ip=ip, server_port=port)
        for key, value in restore_default.items():
            key = key.replace('Get', 'Set')  # convert get to set call
            exec('sila_client.' + key + '(' + str(value) + ')')
            # todo: Values are actually not set and still default are there??
            # try 'set' value = [i+2 for i in value] and 'get' to see that its just default values again
            # is there a separate/general set needed for real execution, like start?


class TestControlParameterServicerGet:
    """ Test all ControlParameterServicer Get functions. Set and retrieve the control parameter values of the in-built PID-controller of the LAUDA L250 Thermostat."""
    sila_client = LAUDA_ThermostatServiceClient(server_ip=ip, server_port=port)

    def test_GetControlParamXp(self):
        response = self.sila_client.ControlParameterServicer_GetControlParamXp()
        assert response is not None
        assert isinstance(response.CurrentControlParamXp.value, str)
        restore_default['ControlParameterServicer_GetControlParamXp'] = response.CurrentControlParamXp.value

    def test_GetControlParamTn(self):
        """ Current control parameter of the integral factor, Tn, of the PID-controller in s.
        A value of Tn=181 is equivalent to "off"."""
        response = self.sila_client.ControlParameterServicer_GetControlParamTn()
        assert response is not None
        assert isinstance(response.CurrentControlParamTn.value, str)
        restore_default['ControlParameterServicer_GetControlParamTn'] = response.CurrentControlParamTn.value

    def test_GetControlParamTv(self):
        """ Current control parameter of the derivative factor, Tv, of the PID-controller in s."""
        response = self.sila_client.ControlParameterServicer_GetControlParamTv()
        assert response is not None
        assert isinstance(response.CurrentControlParamTv.value, str)
        restore_default['ControlParameterServicer_GetControlParamTv'] = response.CurrentControlParamTv.value

    def test_GetControlParamTd(self):
        """ Get control parameter dampening factor, Td, of the derivative factor, Tv, of the PID-controller in s."""
        response = self.sila_client.ControlParameterServicer_GetControlParamTd()
        assert response is not None
        assert isinstance(response.CurrentControlParamTd.value, str)
        restore_default['ControlParameterServicer_GetControlParamTd'] = response.CurrentControlParamTd.value


class TestDeviceServicerGet:
    """ Test all DeviceServicer Get functions. General device settings can be retrieved and changed within this function. """
    sila_client = LAUDA_ThermostatServiceClient(server_ip=ip, server_port=port)

    def test_GetLog(self):
        response = self.sila_client.DeviceServicer_GetLog()
        assert response is not None
        assert isinstance(response.commandExecutionUUID.value, str)
        # assert response.commandExecutionUUID.value == "bc83a553-0869-4589-8261-28a93eea7708"
        # .xml is more detailed in return identifier. not all implemented?

# uuid needed
    # def test_GetLog_Info(self):
    #     response = self.sila_client.DeviceServicer_GetLog_Info()
    #     assert response is not None
    #     assert isinstance(response.)
    #
    # def test_GetLog_Result(self):
    #     response = self.sila_client.DeviceServicer_GetLog_Result()
    #     assert response is not None
    #     assert isinstance(response.)

    def test_GetKeyLockMode(self):
        """ Get mode of the keyboard lock feature. 0=unlocked, 1=locked."""
        response = self.sila_client.DeviceServicer_GetKeyLockMode()
        assert response is not None
        assert isinstance(response.CurrentKeyLockMode.value, str)
        # assert int(response.CurrentKeyLockMode.value) in range(0, 2, 1)
        restore_default['DeviceServicer_GetKeyLockMode'] = response.CurrentKeyLockMode.value

    def test_GetDeviceStatus(self):
        """ Get the device status. 0 = status ok/ 1 = malfunction"""
        response = self.sila_client.DeviceServicer_GetDeviceStatus()
        assert response is not None
        assert isinstance(response.CurrentDeviceStatus.value, str)
        # assert int(response.CurrentDeviceStatus.value) in range(0, 2, 1)

    def test_GetDeviceStatusDiagnosis(self):
        """ Get the device status malfunction diagnosis. String of form XXXXXXX; 0=no malfunction,1=malfunction.
		For X1 = Error, X2-X4 = unassigned, X5 = sublevel, X6-X7 = unassigned."""
        response = self.sila_client.DeviceServicer_GetDeviceStatusDiagnosis()
        assert response is not None
        assert isinstance(response.CurrentDeviceStatusDiagnosis.value, str)
        # assert response.CurrentDeviceStatusDiagnosis.value in ['X1', 'X2', 'X3', 'X4', 'X5', 'X6', 'X7']

    def test_GetPowerStatus(self):
        """ Get power/standby mode. 0=On, 1=Off/Standby."""
        response = self.sila_client.DeviceServicer_GetPowerStatus()
        assert response is not None
        assert isinstance(response.CurrentPowerStatus.value, str)
        # assert int(response.CurrentPowerStatus.value) in range(0, 2, 1)

    def test_Get_CurrentSoftwareVersion(self):
        """ Get thermostat software version. Response is string."""
        response = self.sila_client.Get_DeviceServicer_CurrentSoftwareVersion()
        assert response is not None
        assert isinstance(response.CurrentSoftwareVersion.value, str)

    def test_Subscribe_CurrentStatus(self):
        response = self.sila_client.Subscribe_DeviceServicer_CurrentStatus()
        assert response is not None


class TestTemperatureControlServicerGet:
    """ Test all TemperatureControlServicer Get functions. Set and retrieve information regarding the temperature setpoints and current temperature readings of the LAUDA LOOP 250 thermostat. Setpoint thresholds may be defined within the range of the upper and lower temperature limits THi and TLo. """
    sila_client = LAUDA_ThermostatServiceClient(server_ip=ip, server_port=port)

    def test_GetFeedLineTemperature(self):
        """ Get Feed Line Temperature of the Thermostat."""
        response = self.sila_client.TemperatureControlServicer_GetFeedLineTemperature()
        assert response is not None
        assert isinstance(response.CurrentFeedLineTemperature.value, str)

    def test_GetSetpointTemperature(self):
        """ Get the desired setpoint temperature of the thermostat"""
        response = self.sila_client.TemperatureControlServicer_GetSetpointTemperature()
        assert response is not None
        assert isinstance(response.CurrentTemperatureSetpoint.value, str)
        restore_default['TemperatureControlServicer_GetSetpointTemperature'] = response.CurrentTemperatureSetpoint.value

    def test_GetUpperLimTemperature(self):
        response = self.sila_client.TemperatureControlServicer_GetUpperLimTemperature()
        assert response is not None
        assert isinstance(response.CurrentUpperLimTemperature.value, str)
        restore_default['TemperatureControlServicer_GetUpperLimTemperature'] = response.CurrentUpperLimTemperature.value

    def test_GetLowerLimTemperature(self):
        response = self.sila_client.TemperatureControlServicer_GetLowerLimTemperature()
        assert response is not None
        assert isinstance(response.CurrentLowerLimTemperature.value, str)
        restore_default['TemperatureControlServicer_GetLowerLimTemperature'] = response.CurrentLowerLimTemperature.value

class TestControlParameterServicerSet:
    """ Test all ControlParameterServicer Set functions. Set and retrieve the control parameter values of the in-built PID-controller of the LAUDA L250 Thermostat."""
    sila_client = LAUDA_ThermostatServiceClient(server_ip=ip, server_port=port)

    @pytest.mark.parametrize('k_control_param', [random.uniform(273.15, 373.15)])  # constrained with float 273.15 - 373.15
    def test_SetControlParamXp(self, k_control_param):
        """ Set the control parameter Xp of the PID controller in Kelvin, K."""
        response = self.sila_client.ControlParameterServicer_SetControlParamXp(k_control_param)
        assert response is not None
        assert isinstance(response.ControlParamXpSet.value, str)
        # assert int(response.ControlParamXpSet.value) == k_control_param
        # defined exec. error implemented

    @pytest.mark.parametrize('control_param', [random.uniform(6, 181)])  # constrained with float 5 - 181
    def test_SetControlParamTn(self, control_param):
        """ The control parameter Tn for the integral part of the PID-controller in s.
                The length of the interval to be integrated to calculate the control deviation.
                A value of 181s deactivates the I-part of the PID-controller."""
        response = self.sila_client.ControlParameterServicer_SetControlParamTn(control_param)
        assert response is not None
        assert isinstance(response.ControlParamTnSet.value, str)
        # assert int(response.ControlParamTnSet.value) == control_param
        # defined exec. error implemented

    @pytest.mark.parametrize('control_param', [random.uniform(0, 10000)])  # constrained with float 10000
    def test_SetControlParamTv(self, control_param):
        """ The control parameter Tv for the derivative part of the PID-controller in s.
                The derivative time dampens the effect of the proportional and the integral part."""
        response = self.sila_client.ControlParameterServicer_SetControlParamTv(control_param)
        assert response is not None
        assert isinstance(response.ControlParamTvSet.value, str)
        # assert int(response.ControlParamTvSet.value) == control_param
        # defined exec. error implemented?

    @pytest.mark.parametrize('control_param', [random.uniform(0, 10000)])  # constrained with float 10000
    def test_SetControlParamTd(self, control_param):
        """ The control parameter Td introduces a dampening effect on the derivative part Tv of the PID-controller in s. """
        response = self.sila_client.ControlParameterServicer_SetControlParamTd(control_param)
        assert response is not None
        assert isinstance(response.ControlParamTdSet.value, str)
        # assert int(response.ControlParamTdSet.value) == control_param
        # defined exec. error implemented

# todo ask: Do i need the thermostat to be started to assert if all Set were actually performed and values are set?
class TestDeviceServicerSet:
    """ Test all DeviceServicer Set functions """
    sila_client = LAUDA_ThermostatServiceClient(server_ip=ip, server_port=port)

    @pytest.mark.parametrize('input', ['0', '1'])  # constrained as: str:[0, 1]
    def test_StartThermostat(self, input):
        """ Starts the thermostat out of stand-by mode.
        :param: input: Boolean that defines wether system is started or not. User input 0 = no start, 1 = start up."""
        response = self.sila_client.DeviceServicer_StartThermostat(input)
        assert response is not None
        assert isinstance(response.StartStatus.value, str)

    @pytest.mark.parametrize('input', ['0', '1'])  # constrained as: str:[0, 1]
    def test_StopThermostat(self, input):
        """ Stops the thermostat and puts it into stand-by mode.
        :param: input: Boolean that defines wether system is started or not. User input 0 = no shut-down, 1 = shut-down."""
        response = self.sila_client.DeviceServicer_StopThermostat(input)
        assert response is not None
        assert isinstance(response.StopStatus.value, str)

    @pytest.mark.real_unsafe  # can device lock itself and get un-accessible?
    @pytest.mark.parametrize('key_lock', str(random.randint(0, 1)))
    def test_SetKeyLockMode(self, key_lock):
        """ Mode of the keyboard lock succeeded to Set. The lock mode of the keyboard lock. 0=free/1=locked."""
        response = self.sila_client.DeviceServicer_SetKeyLockMode(key_lock)
        assert response is not None
        assert isinstance(response.KeyLockModeSet.value, str)  # why str and not bool!?!?
        # assert response.SetTemperatureSet.value == key_lock
        # defined exec. error implemented


class TestTemperatureControlServicerSet:
    """ Test all TemperatureControlServicer Set functions. Set and retrieve information regarding the temperature setpoints and current temperature readings of the LAUDA LOOP 250 thermostat. Setpoint thresholds may be defined within the range of the upper and lower temperature limits THi and TLo. """
    sila_client = LAUDA_ThermostatServiceClient(server_ip=ip, server_port=port)

    @pytest.mark.parametrize('k_control_param', [random.uniform(273.15, 373.15)])  # constrained with float 273.15 - 373.15
    def test_SetPointTemperature(self, k_control_param):
        """ The target temperature that the thermostat will try to reach. Depending on the control mechanism
				and the selected correcting values, the temperature might oscillate around or not reach the set
				temperature at all. More on the control mechanism can be found in the user manual, p29."""
        response = self.sila_client.TemperatureControlServicer_SetPointTemperature(k_control_param)
        assert response is not None
        assert isinstance(response.SetTemperatureSet.value, str)
        # assert int(response.SetTemperatureSet.value) == k_control_param
        # defined exec. error implemented

    @pytest.mark.parametrize('k_control_param', [random.uniform(273.15, 373.15)])  # constrained with float 273.15 - 373.15
    def test_SetUpperLimTemperature(self, k_control_param):
        """ Set the upper limit of the feed line temperature of the thermostat, Tih.
        The temperature limits restrict the input range of the temperature setpoint, Tset."""
        response = self.sila_client.TemperatureControlServicer_SetUpperLimTemperature(k_control_param)
        assert response is not None
        assert isinstance(response.UpperLimTemperatureSet.value, str)
        # assert int(response.UpperLimTemperatureSet.value) == k_control_param
        # 3 defined exec. error implemented

    @pytest.mark.parametrize('k_control_param', [random.uniform(273.15, 373.15)])  # constrained with float 273.15 - 373.15
    def test_SetLowerLimTemperature(self,k_control_param):
        """ Set the lower limit of the feed line temperature of the thermostat, Til.
        The temperature limits restrict the input range of the temperature setpoint, Tset."""
        response = self.sila_client.TemperatureControlServicer_SetLowerLimTemperature(k_control_param)
        assert response is not None
        assert isinstance(response.LowerLimTemperatureSet.value, str)
        # assert int(response.LowerLimTemperatureSet.value) == k_control_param
        # 3 defined exec. error implemented

    def test_restore_default(self, teardown_restore_default):
        """ This function calls the teardown to set all default values again to bring the device back to pre-test condition."""
        assert True


def test__init__():
    """ Starts the server in a mocked environment as defined in LAUDA_ThermostatService_server.init()"""
    from sila2lib.sila_server import SiLA2Server
    with mock.patch.object(SiLA2Server, 'run', return_value=42):  # Syntax: .object(class, 'method', return)
        with mock.patch.object(LAUDA_ThermostatService_server, '__name__', '__main__'):
            with mock.patch.object(LAUDA_ThermostatService_server.sys, 'exit') as mock_exit:
                LAUDA_ThermostatService_server.init()
                assert mock_exit.call_args[0][0] == 42
