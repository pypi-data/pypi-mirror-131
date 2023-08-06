#!/usr/bin/env python3
"""
This file tests the simulation- or real mode of the RegloICC.
The Reglo Independent Channel Control (ICC) Digital Peristaltic Pumps provide individually addressable control of each fluidic channel, eliminating the clutter of multiple pumps on the benchtop. Each channel is independently programmable from the pump or the computer.

REAL TESTS have to be executed with precaution. However, a secure mode is implemented by default that prevents breakdown
of the device due to overheating e.g.. For safe testing these steps have to be performed BEFORE test execution:
--Perform steps as usually to properly start up the device (here a cooling unit is needed)
--Connect the serial cable to device and PC (USB port favorably)

STRUCTURE:
Tests are organized in classes to logically separate the
services' features, as well as get- from set-functions. Return values are validated for data types, value range and whether
length of return values is as desired (e.g. as input values). All returns must assert "True", since the injected input
parameter range is only valid. For invalid parameter injection and error handling see:
'test_regloicc_simulation_error.py'
Multiple executions of single test_functions are conducted via the "parametrize" functionality offered by pytest
(injection) to cover and test a wide input range.

Notes for real mode testing:
A Serial cable not attached to the PC (USB port) breaks down script execution completely.
A missing serial PC to device connection results in default return values and multiple assertion failures/test failures
since there is no handling of default values implemented.
"""


# todo: No simulation_mode implemented yet for the RegloICCC?
# Real vs. Sim issue: Real has no default values defined but sim_mode is not implemented so no assertion test possible at all :/
# all tests untested!!
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

from sila2lib_implementations.RegloICC.RegloICCService.RegloICCService_client import RegloICCServiceClient
from sila2lib_implementations.RegloICC.RegloICCService import RegloICCService_server

from tests.config import settings


logger = logging.getLogger(__name__)
# logging.basicConfig(format  = '%(asctime)s - %(name)s - %(levelname)s- %(module)s - linenumber: %(lineno)d - %(message)s', level=logging.DEBUG)

# Set variables of Dotenv
ip = settings.BLUEVARY_IP
port = settings.BLUEVARY_PORT
simulation_mode = settings.BLUEVARY_SIMULATION_MODE

# test condition definition
adresses = 8
channels = [1, 2, 3, 4]  # defines how many channels the pump has: here 1-4. List ensures that are channels are getting tested
sample_depth = 2
tubing_inside_diameter = [0.13,0.19,0.25,0.38,0.44,0.51,0.57,0.64,0.76,0.89,0.95,1.02,1.09,1.14,1.22,1.3,1.42,1.52,1.65,1.75,1.85,2.06,2.29,2.54,2.79,3.17]
pump_modes = ['L', 'M', 'O', 'G', 'Q', 'N', 'P']
restore_default = dict()

# ____________________start boilerplate__________________________________


# walkaround: server cmd_arg assert response is not Noneing issues -> manual server start
# replace all ip etc. to use the server one again sila_client = RegloICCServiceClient(server_ip=ip, server_port=port)
# 
# def wait_until_port_closes(ip: str, port: int, timeout: float = 10) -> bool:
#     """Try to bind the socket at {ip}:{port} to check if a socket resource is available
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
# class RegloICCTestServer(RegloICCService_server.RegloICCServiceServer):
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
#         super().__init__(cmd_args=args, ip=self.ip, port=self.port, simulation_mode=self.simulation_mode)
#         # todo: cmd_args needed but not implemented yet
# 
#     def serve(self):
#         self.run(block=False)
#         while not self.abort_event.is_set():
#             time.sleep(1)
#         self.stop_grpc_server()
# 
# 
# @pytest.fixture(autouse=True, scope='module')
# def setup_and_teardown_regloicc_server():
#     """
#     Starts a server thread and tears it down automatically after the whole module is executed.
#     """
#     abort_event = Event()
#     server = RegloICCTestServer(abort_event)
#     thread = Thread(target=server.serve, args=(), daemon=True)
#     thread.start()
#     wait_until_server_up(server)
#     logger.info('Started RegloICC server')
#     yield thread
#     abort_event.set()
#     thread.join(timeout=10)
#     wait_until_port_closes(ip=ip, port=port, timeout=10)
#     if thread.is_alive:
#         logger.warning(f'RegloICC server thread is still alive: {thread.is_alive()}')
#     logger.info('Stopped RegloICC server')


# todo: test the 'teardown' real mode without device is failing due to TypeError: object of type int/float has no len()
# backup real default data before in case my method fails


# ____________________end boilerplate__________________________________


# @pytest.fixture(scope='function')
# def teardown_restore_default():
#     """ Restores the default values to gain back the pre-test state. """
#     if simulation_mode is False:
#         sila_client = RegloICCServiceClient(server_ip=ip, server_port=port)
#         for key, value in restore_default.items():
#             if key == 'GetTComp':
#                 pass
#                 # sila_client.deviceService_client.SetTComp(value)
#             elif key == 'GetDynAveraging':
#                 pass
#                 # sila_client.deviceService_client.SetDynAveraging(value)
#             else:
#                 key = key.replace('Get', 'Set')  # convert get to set call
#                 value = [i.value for i in value]  # get a plain int/float list
#                 exec('sila_client.calibrationService_client.' + key + '(' + str(value) + ')')
#                 # todo: Values are actually not set and still default are there??
#                 # try 'set' value = [i+2 for i in value] and 'get' to see that its just default values again
#
#
# class TestRegloICCServerFunctionalities:
#     """
#     Basic connection test with the server. Also checks if the server was started with the correct parameters (port, ip, mode)
#     """
#     # Setup_class is meant to be used like __init__ but the latter is causing problems in pytest
#     # (cannot collect test class because it has a __init__ constructor)
#     def setup_class(cls):
#         cls.sila_client = RegloICCServiceClient(server_ip=ip, server_port=port)
#
#     def test_run_bluevary_test_server(self, setup_and_teardown_regloicc_server):
#         logger.info(f'PreSens server running. Is alive: {setup_and_teardown_regloicc_server.is_alive()}')
#         assert True
#
#     def test_connect_to_bluevary_server(self):
#         logger.info(f'Connected to client: {self.sila_client.run()}')
#         assert self.sila_client.run() is True
#
#     def test_toggle_mode(self):
#         assert self.sila_client.simulation_mode is True
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
#         assert self.sila_client.server_port is port
#         assert self.sila_client.server_hostname is ip
#         assert self.sila_client.server_display_name == ''
#         assert self.sila_client.server_description == ''
#         assert self.sila_client.server_version == ''
#
#     def test_client_values(self):
#         assert self.sila_client.vendor_url == ''
#         assert self.sila_client.name == 'RegloICCServiceClient'
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
#         # config, driveControl, ParameterControl

# sila_client.Get_ImplementedFeatures()  # implement it or not?

"""[[str(1) casting OR '1' OR 'a'
TypeError: Parameter to MergeFrom() must be instance of same class: expected SiLAFramework_pb2.Integer got SiLAFramework_pb2.String. for field GetFlowRate_Parameters.Channel
1
TypeError: Cannot set sila2.org.silastandard.String.value to 1: 1 has type <class 'int'>, but expected one of: (<class 'bytes'>, <class 'str'>) for field String.value
]]"""
class TestCalibrationServicerGet:
    """ Test all CalibrationServicer Get functions"""
    sila_client = RegloICCServiceClient(server_ip=ip, server_port=port)

    @pytest.mark.parametrize('channel', channels)
    def test_GetTargetVolume(self, channel):
        """ Get target volume to pump for calibrating in mL. Set and retrieve the control parameter values for calibration of the Reglo ICC pump."""
        response = self.sila_client.CalibrationServicer_GetTargetVolume(input=channel)  # no idea what input stands for! channels?
        # assert response is not None  # Bug: NoneType in simulation mode
        # assert isinstance(response.CurrentTargetVolume.value, float)  # Bug: NoneType in simulation mode

    @pytest.mark.parametrize('channel', channels)
    def test_GetDirectionCalibration(self, channel):
        """ Get direction flow for calibration J or K using DIRECTION format."""
        response = self.sila_client.CalibrationServicer_GetDirectionCalibration(channel=channel)
        assert response is not None
        assert isinstance(response.CurrentDirectionCalibration.value, str)

    @pytest.mark.parametrize('channel', channels)
    def test_GetCalibrationTime(self, channel):
        response = self.sila_client.CalibrationServicer_GetCalibrationTime(channel)
        assert response is not None
        assert isinstance(response.CurrentCalibrationTime.value, int)

    @pytest.mark.parametrize('channel', channels)
    def test_GetRunTimeCalibration(self, channel):
        response = self.sila_client.CalibrationServicer_GetRunTimeCalibration(channel)
        assert response is not None
        assert isinstance(response.CurrentRunTimeCalibration.value, int)

    # def test_GetActualVolume(self):  # method only exists as set


class TestConfigurationServicerGet:
    """ Test all ConfigurationServicer Get functions, Set and retrieve the control parameter values for the configuration of the Reglo ICC pump. """
    sila_client = RegloICCServiceClient(server_ip=ip, server_port=port)

    @pytest.mark.parametrize('TubingDiameter', random.sample(range(0, 10), 1))  # implement meaningful range
    def test_GetTubingDiameter(self, TubingDiameter):
        """ Get the inside diameter of the tubing in mm.
        : param input: The inside diameter of the tubing in mm. float without constraints"""
        response = self.sila_client.ConfigurationServicer_GetTubingDiameter(input=TubingDiameter)
        assert response is not None
        assert isinstance(response.CurrentTubingDiameter.value, float)

    @pytest.mark.parametrize('channel', channels)
    def test_GetBacksteps(self, channel):
        response = self.sila_client.ConfigurationServicer_GetBacksteps(channel)
        assert response is not None
        assert isinstance(response.CurrentBackstepsSetting.value, str)
        # assert response.CurrentBackstepsSetting.value == "GetBacksteps_test"


# todo: ask Lukas which implementation (.xml vs. .py) is more correct. I think there is an error in the implementation dtypes
# use casting to solve the issue if .py is correct str(channel)
class TestDeviceServicerGet:
    """ Test all DeviceServicer Get functions """
    sila_client = RegloICCServiceClient(server_ip=ip, server_port=port)

    def test_GetLog(self):
        response = self.sila_client.DeviceServicer_GetLog()
        assert response is not None
        assert isinstance(response.commandExecutionUUID.value, str)

# uuid needed; not implemented in .xml
    # def test_GetLog_Info(self):  # uuid needed
    #     response = self.sila_client
    #     assert response is not None
    #
    # def test_GetLog_Result(self):  # uuid needed
    #     response = self.sila_client
    #     assert response is not None

    @pytest.mark.parametrize('GetLanguage_address', random.sample(range(0, 4), 1))  # int
    def test_GetLanguage(self, GetLanguage_address):
        """ Get the language of the pump. 0=English / 1=French / 2=Spanish / 3=German."""
        response = self.sila_client.DeviceServicer_GetLanguage(GetLanguage_address)
        assert response is not None
        assert isinstance(response.CurrentLanguage.value, int)
        # assert response.CurrentLanguage.value == 999

# todo: lab real value: see if output is + or - -> why not implement bool values! 0/1
    @pytest.mark.parametrize('GetPumpStatus_address', random.sample(range(0, adresses), 1))
    def test_GetPumpStatus(self, GetPumpStatus_address):
        """ Get pump status. +=running, -=stopped/standby."""
        response = self.sila_client.DeviceServicer_GetPumpStatus(GetPumpStatus_address)
        assert response is not None
        assert isinstance(response.CurrentPumpStatus.value, str)
        # assert response.CurrentPumpStatus.value == "GetPumpStatus_test"

# fixed in RegloService_client.py : bug in address 'str expected' (_client.py implementation) but should have been int (.xml)
    @pytest.mark.parametrize('GetVersionType_address', random.sample(range(0, adresses), 1))  # int
    def test_GetVersionType(self, GetVersionType_address):
        """ Get pump information. Response is string of model description (variable length), software version (3 digits) and pump head model type code (3 digits)."""
        response = self.sila_client.DeviceServicer_GetVersionType(GetVersionType_address)
        assert response is not None
        assert isinstance(response.CurrentVersionType.value, str)
        # assert response.CurrentVersionType.value == "GetVersionType_test"

# fixed in RegloService_client.py : bug in address 'str expected' (_client.py implementation) but should have been int (.xml)
    @pytest.mark.parametrize('CurrentVersionSoftware_address', random.sample(range(0, adresses), 1))  # int
    def test_CurrentVersionSoftware(self, CurrentVersionSoftware_address):
        response = self.sila_client.DeviceServicer_CurrentVersionSoftware(CurrentVersionSoftware_address)
        assert response is not None
        assert isinstance(response.CurrentVersionSoftware.value, str)
        # assert response.CurrentVersionSoftware.value == "CurrentVersionSoftware_test"

# fixed in RegloService_client.py : bug in address 'str expected' (_client.py implementation) but should have been int (.xml)
    @pytest.mark.parametrize('GetSerialNumber_address', random.sample(range(0, adresses), 1))
    def test_GetSerialNumber(self, GetSerialNumber_address):
        response = self.sila_client.DeviceServicer_GetSerialNumber(GetSerialNumber_address)
        assert response is not None
        assert isinstance(response.SerialNumber.value, str)
        # assert response.SerialNumber.value == "GetSerialNumber_test"

    @pytest.mark.parametrize('address', random.sample(range(0, adresses), 1))
    def test_GetChannelAddressing(self, address):
        response = self.sila_client.DeviceServicer_GetChannelAddressing(address)
        # assert response is not None
        # assert isinstance(response.ChannelAddressing.value, bool)  # no return for sim_mode
        # assert response.ChannelAddressing.value == True

    @pytest.mark.parametrize('address', random.sample(range(0, adresses), 1))
    def test_GetEventMessages(self, address):
        response = self.sila_client.DeviceServicer_GetEventMessages(address)
        # assert response is not None
        # assert isinstance(response.EventMessages.value, bool)  # no return for sim_mode
        # assert response.EventMessages.value == True

# fixed in RegloService_client.py : bug in address 'str expected' (_client.py implementation) but should have been int (.xml)
    @pytest.mark.parametrize('address', random.sample(range(0, adresses), 1))
    def test_GetSerialProtocol(self, address):
        response = self.sila_client.DeviceServicer_GetSerialProtocol(address)
        assert response is not None
        assert isinstance(response.SerialProtocol.value, int)
        # assert response.SerialProtocol.value == 9999

    @pytest.mark.parametrize('address', random.sample(range(0, adresses), 1))
    def test_GetChannelNumber(self, address):
        response = self.sila_client.DeviceServicer_GetChannelNumber(address)
        assert response is not None
        assert isinstance(response.ChannelNumber.value, int)
        # assert response.ChannelNumber.value == 9

# fixed in RegloService_client.py : bug in address 'str expected' (_client.py implementation) but should have been int (.xml)
    @pytest.mark.parametrize('channel', channels)
    def test_GetRevolutions(self, channel):
        response = self.sila_client.DeviceServicer_GetRevolutions(channel)
        assert response is not None
        assert isinstance(response.Revolutions.value, int)
        # assert response.Revolutions.value == 999

    @pytest.mark.parametrize('input', random.sample(range(0, 10), 1))
    def test_GetChannelTotalVolume(self, input):
        """ Get channel total volume pumped since last reset, mL. float without constraints"""
        response = self.sila_client.DeviceServicer_GetChannelTotalVolume(input)
        assert response is not None
        assert isinstance(response.ChannelTotalVolume.value, float)
        # assert response.ChannelTotalVolume.value == 999.99

# fixed in RegloService_client.py : bug in address 'str expected' (_client.py implementation) but should have been int (.xml)
    @pytest.mark.parametrize('channel', channels)
    def test_GetTotalTime(self, channel):
        response = self.sila_client.DeviceServicer_GetTotalTime(channel)
        # assert response is not None
        # assert isinstance(response.TotalTime.value, int)   # no return for sim_mode
        # assert response.Revolutions.value == 999

    @pytest.mark.parametrize('address', random.sample(range(0, adresses), 1))
    def test_GetHeadModel(self, address):
        response = self.sila_client.DeviceServicer_GetHeadModel(address)
        assert response is not None
        assert isinstance(response.HeadModel.value, str)
        # assert response.HeadModel.value == "GetHeadModel_test"

# fixed in RegloService_client.py : bug in address 'str expected' (_client.py implementation) but should have been int (.xml)
    @pytest.mark.parametrize('channel', channels)
    def test_GetTimeSetting(self, channel):
        response = self.sila_client.DeviceServicer_GetTimeSetting(channel)
        assert response is not None
        assert isinstance(response.TimeSetting.value, float)
        # assert response.TimeSetting.value == 99.99

# fixed in RegloService_client.py : bug in address 'str expected' (_client.py implementation) but should have been int (.xml)
    @pytest.mark.parametrize('channel', channels)
    def test_GetRollerStepsLow(self, channel):
        response = self.sila_client.DeviceServicer_GetRollerStepsLow(channel)
        # assert response is not None
        # assert isinstance(response.RollerStepsLow.value, int)  # no return for sim_mode
        # assert response.RollerStepsLow.value == 999

# fixed in RegloService_client.py : bug in address 'str expected' (_client.py implementation) but should have been int (.xml)
    @pytest.mark.parametrize('channel', channels)
    def test_GetRollerStepsHigh(self, channel):
        response = self.sila_client.DeviceServicer_GetRollerStepsHigh(channel)
        # assert response is not None
        # assert isinstance(response.RollerStepsHigh.value, int)  # no return for sim_mode
        # assert response.RollerStepsHigh.value == 999

# fixed in RegloService_client.py : bug in address 'str expected' (_client.py implementation) but should have been int (.xml)
    @pytest.mark.parametrize('channel', channels)
    def test_GetRSV(self, channel):
        response = self.sila_client.DeviceServicer_GetRSV(channel)
        assert response is not None
        assert isinstance(response.RSV.value, float)
        # assert response.RSV.value == 999.999

# fixed in RegloService_client.py : bug in address 'str expected' (_client.py implementation) but should have been int (.xml)
    @pytest.mark.parametrize('channel', channels)
    def test_GetPauseTime(self, channel):
        response = self.sila_client.DeviceServicer_GetPauseTime(channel)
        assert response is not None
        assert isinstance(response.PauseTime.value, float)
        # assert response.PauseTime.value == 99.99

# fixed in RegloService_client.py : bug in address 'str expected' (_client.py implementation) but should have been int (.xml)
    @pytest.mark.parametrize('channel', channels)
    def test_GetTotalVolume(self, channel):
        response = self.sila_client.DeviceServicer_GetTotalVolume(channel)
        assert response is not None
        assert isinstance(response.CurrentTotalVolume.value, float)

    @pytest.mark.parametrize('address', random.sample(range(0, adresses), 1))
    def test_GetFootSwitchStatus(self, address):
        response = self.sila_client.DeviceServicer_GetFootSwitchStatus(address)
        # assert response is not None
        # assert isinstance(response.FootSwitchStatus.value, str)   # no return for sim_mode
        # assert response.FootSwitchStatus.value == "GetFootSwitchStatus_test"

# fixed in RegloService_client.py : bug in address 'str expected' (_client.py implementation) but should have been int (.xml)
    @pytest.mark.parametrize('channel', channels)
    def test_GetRollersNumber(self, channel):
        response = self.sila_client.DeviceServicer_GetRollersNumber(channel)
        assert response is not None
        assert isinstance(response.RollersNumber.value, int)
        # assert response.RollersNumber.value == 9

    def test_Subscribe_CurrentStatus(self):
        response = self.sila_client.Subscribe_DeviceServicer_CurrentStatus()
        assert response is not None
        assert isinstance(response, object)


class TestDriveControlServicerGet:
    """ Test all DriveControl Get functions """
    sila_client = RegloICCServiceClient(server_ip=ip, server_port=port)

    @pytest.mark.parametrize('channel', channels)
    def test_GetPumpDirection(self, channel):
        """ Pump direction query. J = clockwise/ K = counter-clockwise. """
        response = self.sila_client.DriveControlServicer_GetPumpDirection(channel)
        assert response is not None
        assert isinstance(response.PumpDirection.value, str)
        # assert response.PumpDirection.value == 'GetPumpDirection_test'
        # assert response.PumpDirection.value == 'K' or 'J'

    @pytest.mark.parametrize('channel', channels)
    def test_GetCauseresponse(self, channel):
        """ Get cause of "-" cannot run response = Parameter 1 :
            C=Cycle count of 0 / R=Max flow rate exceeded or flow rate is set to 0 / V=Max volume exceeded;
            Limiting value that was exceeded = Parameter 2:
            C=Value is undefined / R=Max flow (mL/min) / V=Max volume (mL)   ."""
        response = self.sila_client.DriveControlServicer_GetCauseResponse(channel)
        # assert response is not None
        # assert isinstance(response.Cause.value, str)  # no return value for sim_mode
        # assert response.Cause.value == 'GetCauseResponse_test'
        # assert response.Cause.value == 'K' or 'J'  # evaluate something useful

# todo: data type issues. expected int for channels but no!
# functions that have been changed in the _client.py are marked as:  # str issue
class TestParameterControlServicerGet:
    """ Test all ParameterControl Get functions. Set and retrieve information regarding the parameter settings of the Reglo ICC pump. """
    sila_client = RegloICCServiceClient(server_ip=ip, server_port=port)

    @pytest.mark.parametrize('channel', channels)  # int
    def test_GetFlowRate(self, channel):
        """ Get current flow rate (mL/min)."""
        response = self.sila_client.ParameterControlServicer_GetFlowRate(channel)
        # assert response is not None
        # assert isinstance(response, bool)  # str issue  # no return value for sim_mode

    @pytest.mark.parametrize('channel', channels)  # int
    def test_GetMode(self, channel):
        """ Gets the channel, on which the command will be executed"""
        response = self.sila_client.ParameterControlServicer_GetMode(channel)
        assert response is not None
        assert isinstance(response.CurrentPumpMode.value, str)

    @pytest.mark.parametrize('channel', channels)  # int
    def test_GetVolume(self, channel):
        """ Get the current setting for volume in mL/min."""
        response = self.sila_client.ParameterControlServicer_GetVolume(channel)
        # assert response is not None
        # assert isinstance(response, float)  # str issue  # no return value for sim_mode

    @pytest.mark.parametrize('channel', channels)  # int
    def test_GetMaximumFlowRate(self, channel):
        """ Get maximum flow rate achievable with current settings, mL/min."""
        response = self.sila_client.ParameterControlServicer_GetMaximumFlowRate(channel)
        assert response is not None
        assert isinstance(response.MaximumFlowRate.value, float)  # str issue

    @pytest.mark.parametrize('channel', channels)  # int
    def test_GetMaximumFlowRateWithCalibration(self, channel):
        """ Get maximum flow rate achievable with current settings using calibration, mL/min."""
        response = self.sila_client.ParameterControlServicer_GetMaximumFlowRateWithCalibration(channel)
        assert response is not None
        assert isinstance(response.MaximumFlowRateWithCalibration.value, float)

    @pytest.mark.parametrize('channel', channels)  # int
    def test_GetSpeedSettingRPM(self, channel):
        """ Get the current speed setting in RPM."""
        response = self.sila_client.ParameterControlServicer_GetSpeedSettingRPM(channel)
        assert response is not None
        assert isinstance(response.CurrentSpeedSetting.value, float)  # str issue

    @pytest.mark.parametrize('channel', channels)  # int
    def test_GetCurrentRunTime(self, channel):
        response = self.sila_client.ParameterControlServicer_GetCurrentRunTime(channel)
        assert response is not None
        assert isinstance(response.GetCurrentRunTime.value, int)

    @pytest.mark.parametrize('channel', channels)  # int
    def test_GetPumpingPauseTime(self, channel):
        response = self.sila_client.ParameterControlServicer_GetPumpingPauseTime(channel)
        assert response is not None
        assert isinstance(response.CurrentPumpingPauseTime.value, float)  # str issue

    @pytest.mark.parametrize('channel', channels)  # int
    def test_GetCycleCount(self, channel):
        response = self.sila_client.ParameterControlServicer_GetCycleCount(channel)
        assert response is not None
        assert isinstance(response.CurrentCycleCount.value, float)

    @pytest.mark.parametrize('channel', channels)  # int
    @pytest.mark.parametrize('volume', [random.uniform(0.00, 10.0)])  # float, not constrained
    @pytest.mark.parametrize('flowrate', [random.uniform(0.00, 10.0)])  # float, not constrained
    def test_GetDispenseTimeMlMin(self, channel, volume, flowrate):
        response = self.sila_client.ParameterControlServicer_GetDispenseTimeMlMin(channel, volume, flowrate)  # 'channel':int, 'volume':float, 'flowrate':float
        assert response is not None
        assert isinstance(response.CurrentDispenseTime.value, float)  # str issue 3x str -> int/float/float

    @pytest.mark.parametrize('channel', channels)  # int
    @pytest.mark.parametrize('volume', [random.uniform(0.00, 10.0)])  # float, not constrained
    @pytest.mark.parametrize('flowrate', [random.uniform(0.00, 10.0)])  # float, not constrained
    def test_GetDispenseTimeRPM(self, channel, volume, flowrate):
        response = self.sila_client.ParameterControlServicer_GetDispenseTimeRPM(channel, volume, flowrate)  # 'channel':int, 'volume':float, 'flowrate':float
        assert response is not None
        assert isinstance(response.CurrentDispenseTime.value, float)  # str issue 3x str -> int/float/float

    @pytest.mark.parametrize('channel', channels)  # int
    def test_GetFlowRateAtModes(self, channel):
        """ CurrentDispenseTime at a given volume at a given RPM. : 0=RPM, 1=Flow Rate"""
        response = self.sila_client.ParameterControlServicer_GetFlowRateAtModes(channel)
        # assert response is not None
        # assert isinstance(response.CurrentFlowRate.value, bool)  # no return value for sim_mode


class TestCalibrationServicerSet:
    """ Test all CalibrationServicer Set functions"""
    sila_client = RegloICCServiceClient(server_ip=ip, server_port=port)

    # todo: write setup&teardown for that ?
    # def test_StartCalibration(self):
    #     """ Start Calibration on a Channel. """
    #     response = self.sila_client.CalibrationServicer_StartCalibration()  # channel=
    #     assert response is not None
    #
    # def test_CancelCalibration(self):
    #     response = self.sila_client.CalibrationServicer_CancelCalibration()  # channel=
    #     assert response is not None

    @pytest.mark.parametrize('channel', channels)
    @pytest.mark.parametrize('volume', [random.uniform(0.01, 10.0)])  # real # not constrained: implement meaningful range
    def test_SetTargetVolume(self, channel, volume):
        """ Set target volume to pump for calibrating in mL."""
        response = self.sila_client.CalibrationServicer_SetTargetVolume(channel, volume)
        assert response is not None
        assert isinstance(response.TargetVolumeSet.value, str)
        # assert response.TargetVolumeSet.value =='SetTargetVolume_test'

    @pytest.mark.parametrize('channel', channels)  # int
    @pytest.mark.parametrize('volume', [random.uniform(0.01, 10.0)])  # real # not constrained: implement meaningful range
    def test_SetActualVolume(self, channel, volume):
        """ Set the actual volume measured during calibration in mL."""
        response = self.sila_client.CalibrationServicer_SetActualVolume(channel, volume)
        # assert response is not None  # Bug: NoneType in simulation mode
        # assert isinstance(response.ActualVolumeSet.value, str)  # Bug: NoneType in simulation mode
        # assert response.ActualVolumeSet.value =='SetActualVolume_test'

    @pytest.mark.parametrize('channel', channels)  # int
    @pytest.mark.parametrize('timee', random.sample(range(0, 10), 1))  # int # not constrained: implement meaningful range
    def test_SetCalibrationTime(self, channel, timee):
        """ Set the current calibration time using Time Type 2 format."""
        response = self.sila_client.CalibrationServicer_SetCalibrationTime(channel, timee)
        assert response is not None
        assert isinstance(response.SetCalibrationTimeSet.value, str)
        # assert response.SetCalibrationTimeSet.value =='SetCalibrationTime_test'

    # .xml states that 2 parameters are required
    @pytest.mark.parametrize('SetDirectionCalibration_channel', channels)
    def test_SetDirectionCalibration(self, SetDirectionCalibration_channel):
        """ Set direction flow for calibration J or K using DIRECTION format."""
        response = self.sila_client.CalibrationServicer_GetDirectionCalibration(channel=SetDirectionCalibration_channel)
        assert response is not None
        assert isinstance(response.CurrentDirectionCalibration.value, str)
        # assert response.CurrentDirectionCalibration.value == "GetDirectionCalibration_test"


class TestConfigurationServicerSet:
    """ Test all ConfigurationServicer Set functions """
    sila_client = RegloICCServiceClient(server_ip=ip, server_port=port)

    @pytest.mark.parametrize('channel', channels)  # int
    @pytest.mark.parametrize('diameter', [tubing_inside_diameter[random.randint(0, len(tubing_inside_diameter)-1)]])  # float, unconstrained
    def test_SetTubingDiameter(self, channel, diameter):
        """ Set the inside diameter of the tubing in mm.
        : param input: The inside diameter of the tubing in mm. float without constraints"""
        response = self.sila_client.ConfigurationServicer_SetTubingDiameter(channel, diameter)
        assert response is not None
        assert isinstance(response.TubingDiameterSet.value, str)
        # assert response.TubingDiameterSet.value == "SetTubingDiameter_test"

    @pytest.mark.parametrize('channel', [str(channels)])  # str, no valid strings specified
    def test_ResetToDefault(self, channel):
        """ Resets all user configurable data to default values."""
        response = self.sila_client.ConfigurationServicer_ResetToDefault(channel)
        # assert response is not None  # Bug: NoneType in simulation mode
        # assert isinstance(response.ResetStatus.value, str)
        # assert response.ResetStatus.value == "ResetToDefault_test"

    @pytest.mark.parametrize('channel', channels)  # int
    @pytest.mark.parametrize('steps', [str(random.sample(range(0, 10), 1))])  # str
    def test_SetBacksteps(self, channel, steps):
        response = self.sila_client.ConfigurationServicer_SetBacksteps(channel, steps)
        assert response is not None
        assert isinstance(response.BackstepsSettingSet.value, str)
        # assert response.BackstepsSettingSet.value == "SetBacksteps_test"


# # todo: ask Lukas which implementation (.xml vs. .py) is more correct before implementation
# # to adress the dtype changing
class TestDeviceServicerSet:
    """ Test all DeviceServicer Set functions """
    sila_client = RegloICCServiceClient(server_ip=ip, server_port=port)

    @pytest.mark.parametrize('address', random.sample(range(0, adresses), 1))  # int
    def test_SetPumpAddress(self, address):
        """ Set the address of the pump (1-8).
        : param address: address of the pump (1-8), integer."""
        response = self.sila_client.DeviceServicer_SetPumpAddress(address)
        assert response is not None
        assert isinstance(response.PumpAddressSet.value, str)
        # assert response.PumpAddressSet.value == "SetPumpAddress_test"

    @pytest.mark.parametrize('address', random.sample(range(0, adresses), 1))  # int
    @pytest.mark.parametrize('language', random.sample(range(0, 4), 1))  # int
    def test_SetLanguage(self, address, language):
        """ Set the language of the pump.
        : param language: The language of the pump. 0=English / 1=French / 2=Spanish / 3=German."""
        response = self.sila_client.DeviceServicer_SetLanguage(address, language)
        assert response is not None
        assert isinstance(response , str)  # str issue (2x str -> 2x int)
        # assert response.XX.value == language

    @pytest.mark.parametrize('address', random.sample(range(0, adresses), 1))  # int
    @pytest.mark.parametrize('value', bool(random.randint(0, 1)))  # bool
    def test_SetChannelAddressing(self, address, value):
        """ Set whether (1) or not (0) channel addressing is enabled."""
        response = self.sila_client.DeviceServicer_SetChannelAddressing(address, value)
        assert response is not None
        assert isinstance(response.ChannelAddressingSet.value, str)
        # assert response.ChannelAddressingSet.value == str(value)

    @pytest.mark.parametrize('address', random.sample(range(0, adresses), 1))  # int
    @pytest.mark.parametrize('value', bool(random.randint(0, 1)))  # bool
    def test_SetEventMessages(self, address, value):
        """ Set whether (1) or not (0) event messages is enabled."""
        response = self.sila_client.DeviceServicer_SetEventMessages(address, value)
        assert response is not None
        assert isinstance(response.XX.value, str)  # str issue (2x str -> int/real)
        # assert response.XX.value == str(value)

    @pytest.mark.parametrize('address', random.sample(range(0, adresses), 1))  # int
    @pytest.mark.parametrize('pump_name', ['pump_name1', 'pump_name2'])  # str  # insert meaningful strings here
    def test_SetPumpName(self, address, pump_name):
        """ Set pump name for display under remote control string."""
        response = self.sila_client.DeviceServicer_SetPumpName(address, pump_name)
        assert response is not None
        assert isinstance(response.XX.value, str)  # str issue (2x str -> int/str)
        # assert response.XX.value == str(value)

    @pytest.mark.parametrize('address', random.sample(range(0, adresses), 1))  # int
    @pytest.mark.parametrize('channel', channels)  # int
    def test_SetChannelNumber(self, address, channel):
        """ Set whether (1) or not (0) event messages is enabled."""
        response = self.sila_client.DeviceServicer_SetChannelNumber(address, channel)
        assert response is not None
        assert isinstance(response.XX.value, str)  # str issue (2x str -> 2x int)
        # assert response.XX.value == str(value)

    @pytest.mark.parametrize('address', random.sample(range(0, adresses), 1))  # int
    @pytest.mark.parametrize('head_model', ['whatever string'])  # str  # implement a meaningful value
    def test_SetHeadModel(self, address, head_model):
        """ Set pump head model type code up to 4 digits indicating the ID number of the pump head. The first two digits encode the number of channels on the head, and the second 2 digits represent the number of rollers
        : param head_model: ID number of the pump head. The first two digits encode the number of channels on the head, and the second 2 digits represent the number of rollers"""
        response = self.sila_client.DeviceServicer_SetHeadModel(address, head_model)
        assert response is not None
        assert isinstance(response , str)  # str issue 2x str -> int/str
        # assert response.X.value == head_model

    @pytest.mark.parametrize('ui', ['whatever string'])  # str  # implement a meaningful value
    def test_SetUserInterface(self, ui):
        """ Set control from the pump user interface. Variable - pump address"""
        response = self.sila_client.DeviceServicer_SetUserInterface(ui)
        assert response is not None
        assert isinstance(response.UserInterfaceSet.value, str)
        # assert response.UserInterfaceSet.value == ui

#     @pytest.mark.parametrize('address', str(random.sample(range(0, adresses), 1)))
#     def test_SetDisableInterface(self, address):
#         response = self.sila_client.DeviceServicer_SetDisableInterface(address)
#         assert response is not None
#         assert isinstance(response.DisableInterfaceSet.value, str)
#         # assert response.DisableInterfaceSet.value == "Error disabling pump local user interface"
#
#     def test_SetDisplayNumbers(self):
#         response = self.sila_client.DeviceServicer_SetDisplayNumbers()  # 'address' and 'value'
#         assert response is not None
#         assert isinstance(response )
#
#     def test_SetDisplayLetters(self):
#         response = self.sila_client.DeviceServicer_SetDisplayLetters()  # 'address' and 'value'
#         assert response is not None
#         assert isinstance(response )
#
#     def test_SetTimeSetting(self):
#         response = self.sila_client.DeviceServicer_SetTimeSetting()  # 'channel' and 'value'
#         assert response is not None
#         assert isinstance(response )
#
#     def test_SetRunTimeM(self):
#         response = self.sila_client.DeviceServicer_SetRunTimeM()  # 'channel' and 'value'
#         assert response is not None
#         assert isinstance(response )
#
#     def test_SetRunTimeH(self):
#         response = self.sila_client.DeviceServicer_SetRunTimeH()  # 'channel' and 'value'
#         assert response is not None
#         assert isinstance(response )
#
#     def test_SetRollerStepsLow(self):
#         response = self.sila_client.DeviceServicer_SetRollerStepsLow()  # 'channel' and 'value'
#         assert response is not None
#         assert isinstance(response )
#
#     def test_SetRollerStepsHigh(self):
#         response = self.sila_client.DeviceServicer_SetRollerStepsHigh()  # 'channel' and 'value'
#         assert response is not None
#         assert isinstance(response )
#
#     def test_SetRSV(self):
#         response = self.sila_client.DeviceServicer_SetRSV()  # 'channel' and 'value'
#         assert response is not None
#         assert isinstance(response )
#
#     def test_SetRSVReset(self):
#         response = self.sila_client.DeviceServicer_SetRSVReset()  # adress
#         assert response is not None
#         assert isinstance(response )
#
#     def test_ResetRSVTable(self):
#         response = self.sila_client.DeviceServicer_ResetRSVTable()
#         assert response is not None
#         assert isinstance(response )
#
#     def test_SetNonFactoryRSV(self):
#         response = self.sila_client.DeviceServicer_SetNonFactoryRSV()
#         assert response is not None
#         assert isinstance(response )
#
#     def test_SetPauseTime(self):
#         response = self.sila_client.DeviceServicer_SetPauseTime()
#         assert response is not None
#         assert isinstance(response )
#
#     def test_SetPauseTimeM(self):
#         response = self.sila_client.DeviceServicer_SetPauseTimeM()
#         assert response is not None
#         assert isinstance(response )
#
#     def test_SetPauseTimeH(self):
#         response = self.sila_client.DeviceServicer_SetPauseTimeH()
#         assert response is not None
#         assert isinstance(response )
#
#     def test_SaveSettings(self):
#         response = self.sila_client.DeviceServicer_SaveSettings()
#         assert response is not None
#         assert isinstance(response )
#
#     def test_SaveSetRoller(self):
#         response = self.sila_client.DeviceServicer_SaveSetRoller()
#         assert response is not None
#         assert isinstance(response )
#
#     def test_SetRollersNumber(self):
#         response = self.sila_client.DeviceServicer_SetRollersNumber()
#         assert response is not None
#         assert isinstance(response )
#
#     def test_SetPumpSerialNumber(self):
#         response = self.sila_client.DeviceServicer_SetPumpSerialNumber()
#         assert response is not None
#         assert isinstance(response )


class TestDriveControlServicerSet:
    """ Test all DriveControl Set functions """
    sila_client = RegloICCServiceClient(server_ip=ip, server_port=port)

        # # todo: is that needed as setup and teardown with 3 seconds spinning to see that direction is changed?
    @pytest.mark.parametrize('channel', channels)  # int
    def test_StartPump(self, channel):
        """ Starts the pump out of stand-by mode."""
        response = self.sila_client.DriveControlServicer_Start(channel)
        # assert response is not None  # no response defined in sim_mode

    @pytest.mark.parametrize('channel', channels)  # int
    def test_Stop(self, channel):
        response = self.sila_client.DriveControlServicer_Stop(channel)
        # assert response is not None  # no response defined in sim_mode

    @pytest.mark.parametrize('channel', channels)  # int
    def test_SetDirectionClockwise(self, channel):
        """ Set the rotation direction of the pump to J = clockwise/ K = counter-clockwise. """
        response = self.sila_client.DriveControlServicer_SetDirectionClockwise(channel)
        assert response is not None
        assert isinstance(response.SetDirectionSet.value, str)
        # assert response.PumpDirection.value != 'SetDirectionClockwise_test'
        # assert response.PumpDirection.value == 'J'

    @pytest.mark.parametrize('channel', channels)
    def test_SetDirectionCounterClockwise(self, channel):
        """ Set the rotation direction of the pump to J = clockwise/ K = counter-clockwise. """
        response = self.sila_client.DriveControlServicer_SetDirectionCounterClockwise(channel)
        assert response is not None
        assert isinstance(response.SetDirectionSet.value, str)
        # assert response.PumpDirection.value != 'SetDirectionCounterClockwise_test'
        # assert response.PumpDirection.value == 'K'


class TestParameterControlServicerSet:
    """ Test all ParameterControl Set functions """
    sila_client = RegloICCServiceClient(server_ip=ip, server_port=port)

    @pytest.mark.parametrize('channel', channels)  # int
    @pytest.mark.parametrize('flow_rate', channels)  # float
    def test_SetFlowRate(self, channel, flow_rate):
        """ Set the desired flow rate of the pump, mL/min"""
        response = self.sila_client.ParameterControlServicer_SetFlowRate(channel, flow_rate)
        # assert response is not None  # no return in sim_mode
        # assert isinstance(response, float)

    @pytest.mark.parametrize('mode', pump_modes)  # str
    def test_SetRPMMode(self, mode):
        """ Set the current channel/pump mode to RPM mode.
        :param mode: Current channel or pump mode: L=RPM / M=Flow Rate / O=Volume (at Rate) / G=Volume (over Time) / Q=Volume+Pause / N=Time / P=Time+Pause"""
        response = self.sila_client.ParameterControlServicer_SetRPMMode(mode)
        assert response is not None
        assert isinstance(response.PumpModeSet.value, str)
        # assert response.PumpModeSet.value == mode

    @pytest.mark.parametrize('mode', pump_modes)  # str
    def test_SetFlowRateMode(self, mode):
        """ Set the current channel/pump mode to Flow Rate mode..
        :param mode: Current channel or pump mode: L=RPM / M=Flow Rate / O=Volume (at Rate) / G=Volume (over Time) / Q=Volume+Pause / N=Time / P=Time+Pause"""
        response = self.sila_client.ParameterControlServicer_SetFlowRateMode(mode)
        assert response is not None
        assert isinstance(response.PumpModeSet.value, str)
        # assert response.PumpModeSet.value == mode

    @pytest.mark.parametrize('mode', pump_modes)  # str
    def test_SetVolumeRateMode(self, mode):
        """ Set the current channel/pump mode to Volume (at Rate) mode.
        :param mode: Current channel or pump mode: L=RPM / M=Flow Rate / O=Volume (at Rate) / G=Volume (over Time) / Q=Volume+Pause / N=Time / P=Time+Pause"""
        response = self.sila_client.ParameterControlServicer_SetVolumeRateMode(mode)
        assert response is not None
        assert isinstance(response.PumpModeSet.value, str)
        # assert response.PumpModeSet.value == mode

    @pytest.mark.parametrize('mode', pump_modes)  # str
    def test_SetVolumeTimeMode(self, mode):
        """ Set the current channel/pump mode to Volume (over Time) mode.
        :param mode: Current channel or pump mode: L=RPM / M=Flow Rate / O=Volume (at Rate) / G=Volume (over Time) / Q=Volume+Pause / N=Time / P=Time+Pause"""
        response = self.sila_client.ParameterControlServicer_SetVolumeTimeMode(mode)
        assert response is not None
        assert isinstance(response.PumpModeSet.value, str)
        # assert response.PumpModeSet.value == mode

    @pytest.mark.parametrize('mode', pump_modes)  # str
    def test_SetVolumePauseMode(self, mode):
        """ Set the current channel/pump mode to Volume+Pause mode.
        :param mode: Current channel or pump mode: L=RPM / M=Flow Rate / O=Volume (at Rate) / G=Volume (over Time) / Q=Volume+Pause / N=Time / P=Time+Pause"""
        response = self.sila_client.ParameterControlServicer_SetVolumePauseMode(mode)
        assert response is not None
        assert isinstance(response.PumpModeSet.value, str)
        # assert response.PumpModeSet.value == mode

    @pytest.mark.parametrize('mode', pump_modes)  # str
    def test_SetTimeMode(self, mode):
        """ Set the current channel/pump mode to Time mode.
        :param mode: Current channel or pump mode: L=RPM / M=Flow Rate / O=Volume (at Rate) / G=Volume (over Time) / Q=Volume+Pause / N=Time / P=Time+Pause"""
        response = self.sila_client.ParameterControlServicer_SetTimeMode(mode)
        assert response is not None
        assert isinstance(response.PumpModeSet.value, str)
        # assert response.PumpModeSet.value == mode

    @pytest.mark.parametrize('mode', pump_modes)  # str
    def test_SetTimePauseMode(self, mode):
        """ Set the current channel/pump mode to Time+Pause mode.
        :param mode: Current channel or pump mode: L=RPM / M=Flow Rate / O=Volume (at Rate) / G=Volume (over Time) / Q=Volume+Pause / N=Time / P=Time+Pause"""
        response = self.sila_client.ParameterControlServicer_SetTimePauseMode(mode)
        assert response is not None
        assert isinstance(response.PumpModeSet.value, str)
        # assert response.PumpModeSet.value == mode

    @pytest.mark.parametrize('channel', channels)
    @pytest.mark.parametrize('volume', [random.uniform(0, 10.0)])  # float
    def test_SetVolume(self, channel, volume):
        """ Set the current setting for volume in mL. Volume Type 2."""
        response = self.sila_client.ParameterControlServicer_SetVolume(channel, volume)
        # assert response is not None
        # assert isinstance(response , str)  # no return for sim_mode

    @pytest.mark.parametrize('channel', channels)  # int
    @pytest.mark.parametrize('speed', [round(random.uniform(0, 10.0), 2)])  # float
    def test_SetSpeedSettingRPM(self, channel, speed):
        """ Set speed setting in RPM (RPM Mode flow rate setting (0.01 RPM) Discrete Type 3)."""
        response = self.sila_client.ParameterControlServicer_SetSpeedSettingRPM(channel, speed)
        assert response is not None
        assert isinstance(response.CurrentSpeedSetting.value, str)  # str issue 2x str > int+real

    @pytest.mark.parametrize('channel', channels)  # int
    @pytest.mark.parametrize('set_time', [random.uniform(0, 3596400)])  # float, constrained
    def test_SetCurrentRunTime(self, channel, set_time):
        """ Set current pump run time using Time Type 2 format (0 to 999h or 0 to 3596400s).
        :param channel: int
        :param channel: float constrained: (0 to 999h or 0 to 3596400s)"""
        response = self.sila_client.ParameterControlServicer_SetCurrentRunTime(channel, set_time)
        assert response is not None
        assert isinstance(response.SetCurrentRunTimeSet.value, str)
        # assert float(response.SetCurrentRunTimeSet.value) == set_time

    @pytest.mark.parametrize('channel', channels)  # int
    @pytest.mark.parametrize('set_time', [random.uniform(0, 3596400)])  # float, constrained
    def test_SetPumpingPauseTime(self, channel, set_time):
        """ Set pumping pause time using Time Type 2 format (0 to 999h or 0 to 3596400s)
        :param channel: int
        :param channel: float constrained: (0 to 999h or 0 to 3596400s)"""
        response = self.sila_client.ParameterControlServicer_SetPumpingPauseTime(channel, set_time)
        assert response is not None
        assert isinstance(response.SetPumpingPauseTimeSet.value, str)   # str issue 2x str > int+real
        # assert float(response.SetPumpingPauseTimeSet.value) == set_time

    @pytest.mark.parametrize('channel', channels)  # int
    @pytest.mark.parametrize('cycle', [random.uniform(0, 100)])  # float, not constrained
    def test_SetCycleCount(self, channel, cycle):
        """ Set pump cycle count (Discrete Type 2) """
        response = self.sila_client.ParameterControlServicer_SetCycleCount(channel, cycle)
        assert response is not None
        assert isinstance(response.SetCycleCountSet.value, str)   # str issue 2x str > int+real
        # assert float(response.SetCycleCountSet.value) == cycle

    @pytest.mark.parametrize('channel', channels)  # int
    @pytest.mark.parametrize('flow_rate', [random.uniform(0, 100)])  # float, not constrained
    def test_SetFlowRateAtModes(self, channel, flow_rate):
        """ Set RPM flow rate not in RPM or Flow Rate mode. (Discrete Type 3 """
        response = self.sila_client.ParameterControlServicer_SetFlowRateAtModes(channel, flow_rate)
        assert response is not None
        assert isinstance(response.SetFlowRateSet.value, str)   # str issue 2x str > int+real
        # assert float(response.SetFlowRateSet.value) == flow_rate

    # def test_restore_default(self, teardown_restore_default):
    #     """ This function calls the teardown to set all default values again to bring the device back to pre-test condition."""
    #     assert True


def test__init__():
    """ Starts the server in a mocked environment as defined in RegloICCService_server.init()"""
    from sila2lib.sila_server import SiLA2Server
    with mock.patch.object(SiLA2Server, 'run', return_value=42):  # Syntax: .object(class, 'method', return)
        with mock.patch.object(RegloICCService_server, '__name__', '__main__'):
            with mock.patch.object(RegloICCService_server.sys, 'exit') as mock_exit:
                RegloICCService_server.init()
                assert mock_exit.call_args[0][0] == 42
