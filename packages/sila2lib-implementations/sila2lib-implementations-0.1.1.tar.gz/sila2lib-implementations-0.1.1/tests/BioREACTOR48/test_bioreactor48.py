#!/usr/bin/env python3
"""
This file tests the simulation- or real mode of the BioREACTOR48.
REAL TESTS have to be executed with precaution. However, a secure mode is implemented by default that prevents breakdown
of the device due to overheating e.g.. For safe testing these steps have to be performed BEFORE test execution:
--Perform steps as usually to properly start up the device (here a cooling unit is needed)
--Connect the serial cable to device and PC (USB port favorably)

STRUCTURE:
Tests are organized in classes to logically separate the
services' features, as well as get- from set-functions. Return values are validated for data types, value range and whether
length of return values is as desired (e.g. as input values). All returns must assert "True", since the injected input
parameter range is only valid. For invalid parameter injection and error handling see:
'test_bioreactor48_simulation_error.py'
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
from threading import (
    Thread,
    Event
)
import time
from uuid import UUID
from unittest import mock

from sila2lib_implementations.BioREACTOR48.BioREACTOR48Service.BioREACTOR48Service_client import BioREACTOR48ServiceClient
from sila2lib_implementations.BioREACTOR48.BioREACTOR48Service import BioREACTOR48Service_server

from tests.config import settings


logger = logging.getLogger(__name__)

# Import PreSens device default configuration from BioREACTOR48Service_server.py:
total_bars = BioREACTOR48Service_server.Properties.TotalBars
bar_sensors = BioREACTOR48Service_server.Properties.BarSensors
total_channels = BioREACTOR48Service_server.Properties.TotalChannels
restore_default = dict()

# Set variables of Dotenv
ip = settings.BIOREACTOR48_IP
port = settings.BIOREACTOR48_PORT
simulation_mode = settings.BIOREACTOR48_SIMULATION_MODE
logger.info(f"Tests are executed in the {'simulation' if simulation_mode is True else 'real'} mode")


# real mode frequency and range of test executions
sample_depth = 2
# todo: ask Nikolas if values between [25, 50, 75, 100] can be covered +++ # is rpm_range a reasonable value? -> exception rpm too high
# power_ranger in sim. is only valid in 25 stepsize
power_ranger = range(0, 101, 25)  # int input needed in % # range (0-100) NOT implemented
power_sampling = random.sample(power_ranger, sample_depth)
rpm_range = range(0, 4000, 100)  # int input needed # NO range implemented # return type: list(int)
rpm_sampling = random.sample(rpm_range, sample_depth)


def wait_until_port_closes(ip: str, port: int, timeout: float = 10) -> bool:
    """ Try to bind the socket at {ip}:{port} to check if a socket resource is available

    :param ip: The ip of the host system.
    :param port: The port of the socket.
    :param timeout: The timeout until a connection attempt is aborted.
    :return: False if socket is available. True if unavailable.
    """
    a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    a_socket.settimeout(timeout)
    location = (ip, port)
    try:
        a_socket.connect_ex(location)
        while a_socket.connect_ex(location) == 0:
            return False
    except (TimeoutError, OSError, ValueError, OverflowError, InterruptedError) as e:
        logger.error(f'Encountered exception {e.__class__.__name__}: {e}')
    except Exception as e:
        logger.error(f'Encountered unknown exception {e.__class__.__name__}: {e}')
    finally:
        a_socket.close()
        return True


def wait_until_server_up(server, timeout: float = 10.0) -> bool:
    """ Waits until the server is started sanely. Currently unimplemented on server site (server.is_healthy not available)

    :param server: The server whose sanely up status has to be tested
    :param timeout: Defined timeout at which check is aborted and error is sent
    :return: 0 for server is up. 1 for timeout exceeded.
    """
    # t = 0
    # while server.healthy is False:
    #     if t > timeout:
    #         return True
    #     time.sleep(0.1)  # return error message
    #     t += 0.1
    # return False
    time.sleep(10)


# Test Server setup
class BioreactorTestServer(BioREACTOR48Service_server.BioREACTOR48ServiceServer):
    """
    Test server instance. Implementation of service until an abort event is sent
    :param abort_event: Event that leads to the server stop
    """

    ip = settings.BIOREACTOR48_IP
    port = settings.BIOREACTOR48_PORT
    simulation_mode = settings.BIOREACTOR48_SIMULATION_MODE

    def __init__(self, abort_event: Event):
        self.abort_event = abort_event
        super().__init__(ip=self.ip, port=self.port, simulation_mode=self.simulation_mode)

    def serve(self):
        self.run(block=False)
        while not self.abort_event.is_set():
            time.sleep(1)
        self.stop_grpc_server()


@pytest.fixture(autouse=True, scope='module')
def setup_and_teardown_bioreactor_server():
    """
    Starts a server thread and tears it down automatically after the whole module is executed.
    """
    abort_event = Event()
    server = BioreactorTestServer(abort_event)
    thread = Thread(target=server.serve, args=(), daemon=True)
    thread.start()
    wait_until_server_up(server)
    logger.info('Started Bioreactor server')
    yield thread
    abort_event.set()
    thread.join(timeout=10)
    wait_until_port_closes(ip=BioreactorTestServer.ip, port=BioreactorTestServer.port, timeout=10)
    if thread.is_alive:
        logger.warning(f'Bioreactor server thread is still alive: {thread.is_alive()}')
    logger.info('Stopped Bioreactor server')


@pytest.fixture(scope='function')
def setup_and_teardown_stirrer():
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


class TestPresensServerFunctionalities:
    """
    Basic connection test with the server. Also checks if the server was started with the correct parameters (port, ip, mode)
    """
    # Setup_class is meant to be used like __init__ but the latter is causing problems in pytest
    # (cannot collect test class because it has a __init__ constructor)
    def setup_class(cls):
        cls.sila_client = BioREACTOR48ServiceClient(server_ip=BioreactorTestServer.ip, server_port=BioreactorTestServer.port)

    def test_run_bioreactor_test_server(self, setup_and_teardown_bioreactor_server):
        logger.info(f'Bioreactor server running. Is alive: {setup_and_teardown_bioreactor_server.is_alive()}')
        assert True

    def test_connect_to_bioreactor_server(self):
        logger.info(f'Connected to client: {self.sila_client.run()}')
        assert self.sila_client.run() is True

    @pytest.mark.WIP  # .env and server start needs to be in same mode, else error
    def test_toggle_mode(self):
        # try:
        if simulation_mode is True:
            self.sila_client.toggleSimMode()
            assert self.sila_client.simulation_mode is False
        else:
            self.sila_client.toggleSimMode()
            time.sleep(4)
            assert self.sila_client.simulation_mode is True
        # except (AssertionError) as e:
          #   logger.info(f'Encountered exception {e.__class__.__name__}: {e}. BioREACTOR server is started differently as defined in .env')

    def test_mode_switch(self):
        self.sila_client.switchToSimMode()
        assert self.sila_client.simulation_mode is True
        self.sila_client.switchToRealMode()
        assert self.sila_client.simulation_mode is False
        # Re-assign the correct default value
        try:
            if simulation_mode is True:
                self.sila_client.switchToSimMode()
                assert self.sila_client.simulation_mode is True
            elif simulation_mode is False:
                self.sila_client.switchToRealMode()
                assert self.sila_client.simulation_mode is False
        except:
            logger.error('Fatal: server could not be re-assigned to correct mode.')
            self.sila_client.switchToSimMode()  # avoids risk for device

    def test_server_values(self):
        assert self.sila_client.server_port is BioreactorTestServer.port
        assert self.sila_client.server_hostname is BioreactorTestServer.ip
        assert self.sila_client.server_display_name == 'BioREACTOR48Service'
        assert self.sila_client.server_description == 'Unknown Type'
        assert self.sila_client.server_version == '1.0'

    def test_client_values(self):
        assert self.sila_client.vendor_url == ''
        assert self.sila_client.name == 'BioREACTOR48ServiceClient'
        assert self.sila_client.version == '1.0'
        assert self.sila_client.description == 'This is a BioREACTOR48 Service'
        assert isinstance(UUID(self.sila_client.client_uuid), UUID)

    def test_server_standard_features(self):
        assert hasattr(self.sila_client, 'SiLAService_stub')
        assert 'sila2lib.framework.std_features.SiLAService_pb2_grpc.SiLAServiceStub' in \
               str(type(self.sila_client.SiLAService_stub))
        assert hasattr(self.sila_client, 'SimulationController_stub')
        assert 'sila2lib.framework.std_features.SimulationController_pb2_grpc.SimulationControllerStub' in \
               str(type(self.sila_client.SimulationController_stub))

# todo: bug
    def test_server_custom_features(self):
        pass
        # assert hasattr(self.sila_client, 'deviceServicer_client')
        # assert hasattr(self.sila_client, 'motoService_client')
        # assert hasattr(self.sila_client, 'motorServicer_client')


class TestBioreactorDeviceServicerGet:
    """ Test all DeviceServicer Get functions. Used to acquire general device status and individual stirrer position status of the bioREACTOR48."""
    sila_client = BioREACTOR48ServiceClient(server_ip=BioreactorTestServer.ip, server_port=BioreactorTestServer.port)

# todo: ask why not all default values, instead different values
    def test_GetDeviceStatus(self):
        """ Get the current status of the device, software version, control mode, bar number and unit address."""
        response = self.sila_client.DeviceServicer_GetDeviceStatus()
        assert response is not None
        assert isinstance(response.Status.value, str)
        assert isinstance(response.Version.value, int)
        assert isinstance(response.Mode.value, str)
        assert isinstance(response.BarConnection.value, str)
        assert isinstance(response.Address.value, int)
        if simulation_mode is True:
        # todo: ask why not all default values, instead different values
            assert response.Status.value == 'OK'  # why not all defaults?
            assert response.Version.value == 8602
            assert response.Mode.value == 'REM'
            assert response.BarConnection.value == '101010'  # 1 = connected, 0 = not connected
            assert response.Address.value == 1
        else:  # default values for real mode are causing multiple tests to fail
            if response.Status.value == 'default string':
                logger.error('Serial cable probably not connected or detected. All tests will return the pre-defined default.'
                         'This is causing some tests to fail since string manipulation will fail. IndexError: list index out of range')
            else:
                assert response.Status.value == 'OK'
                assert response.Mode.value == 'REM' or response.Mode.value == 'OFF'

    # @pytest.mark.skip
    def test_DeviceServicer_GetReactorStatus(self):
        """ Get the current status of all 48 reactors. Check if stirrer is still running. 1 = stirring, 0 = not stirring.
        A random failure is implemented in the simulation and/or real implementation for DeviceServicer_GetReactorStatus().
        Therefore the assertion sometimes is false and the execution stopped. Uncomment '# @pytest.mark.skip' to skip this test."""
        response = self.sila_client.DeviceServicer_GetReactorStatus()
        assert response is not None
        return_val = response.ReactorStatus
        assert len(return_val) == total_channels
        for count, i in enumerate(return_val):
            if i.value is None:
                logger.info('reactor status unavailable for reactor number: ' + str(count + 1))
            else:
                assert i.value is True
        logger.info(return_val)
        # return_val is either true or none (false = none)
        # however in the .xml it is defined as 1 = stirring, 0 = not stirring?
        # except (AssertionError) as e:
        #     logger.info(f'Encountered exception {e.__class__.__name__}: {e}. BioREACTOR server is started differently as defined in .env')

    @pytest.mark.unimplemented  # real mode not tested yet in the lab
    def test_DeviceServicer_GetBarNumber(self):
        """ Number of stirrer bars available. Default = 6."""
        response = self.sila_client.Get_DeviceServicer_BarNumber()
        assert response is not None
        return_val = response.BarNumber.value
        assert response is not None
        assert isinstance(return_val, int)
        assert return_val == total_bars

    @pytest.mark.unimplemented  # real mode not tested yet in the lab
    def test_DeviceServicer_GetBarReactors(self):
        """ Number of reactors per bar. Default = 8."""
        response = self.sila_client.Get_DeviceServicer_BarReactors()
        assert response is not None
        return_val = response.BarReactors.value
        assert response is not None
        assert isinstance(return_val, int)
        assert return_val == bar_sensors

    @pytest.mark.unimplemented  # real mode not tested yet in the lab
    def test_DeviceServicer_GetTotalReactors(self):
        """ Number of total reactors. Default = 6*8 = 48."""
        response = self.sila_client.Get_DeviceServicer_TotalReactors()
        assert response is not None
        return_val = response.TotalReactors.value
        assert response is not None
        assert isinstance(return_val, int)
        assert return_val == total_channels
    # note: due to (partial) missing implementation these remaining features were not implemented for testing:
    # GetLog(), GetLog_Info(str(uuid4()), GetLog_Result(), grpc_error_handling(), Subscribe_CurrentStatus()


class TestBioREACTORMotorServicerGet:
    """Test all MotorServicer Get functions"""
    sila_client = BioREACTOR48ServiceClient(server_ip=BioreactorTestServer.ip, server_port=BioreactorTestServer.port)

    def test_GetPower(self):
        """ Get the current power input of the stirrer in %."""
        response = self.sila_client.MotorServicer_GetPower()
        assert response is not None
        return_val = response.CurrentPower.value
        assert isinstance(return_val, int)
        if simulation_mode is True:
            assert return_val == 100  # default value
            # no accepted value range implemented yet
        else:
            assert return_val in power_ranger
            restore_default['GetPower'] = return_val

    def test_GetRPM(self):
        """ Get the current rpm of the stirrer."""
        response = self.sila_client.MotorServicer_GetRPM()
        assert response is not None
        return_val = response.CurrentRPM.value
        assert isinstance(return_val, int)
        if simulation_mode is True:
            assert return_val == 3000  # default value
        # no accepted value range implemented yet
        else:
            assert return_val in rpm_range
            restore_default['GetRPM'] = return_val

class TestBioREACTORMotorServicerSet:
    """Test all MotorServicer Set functions"""
    sila_client = BioREACTOR48ServiceClient(server_ip=BioreactorTestServer.ip, server_port=BioreactorTestServer.port)

    @pytest.mark.parametrize("RPM_value",  rpm_sampling)
    def test_SetRPM(self, RPM_value):
        """ Set the current rpm of the stirrer. Value range not implemented. Accepted input: int, long"""
        response = self.sila_client.MotorServicer_SetRPM(RPM_value)
        assert response is not None
        curr_rpm = response.CurrentStatus.value.split('_')
        curr_rpm = curr_rpm[1][:-3]
        assert float(curr_rpm) == RPM_value

    @pytest.mark.parametrize("power_value", power_sampling)
    def test_SetPower(self, power_value):
        """ Set the current power input of the stirrer. Value range not implemented. Accepted input: int, long. No negative values"""
        response = self.sila_client.MotorServicer_SetPower(power_value)
        assert response is not None
        logging.debug(response)
        curr_power = response.CurrentStatus.value.split('_')
        curr_power = curr_power[-2][5:]
        assert float(curr_power) == power_value

    if simulation_mode is True:
        # todo: value bug
        def test_StirrerControl(self):
            self.sila_client.MotorServicer_SetPower(75)
            self.sila_client.MotorServicer_SetRPM(2800)
            response = self.sila_client.MotorServicer_StartStirrer()
            assert response is not None
            assert self.sila_client.MotorServicer_GetPower().CurrentPower.value == 100
            assert self.sila_client.MotorServicer_GetRPM().CurrentRPM.value == 3000  # why default value of 3000?
            self.sila_client.MotorServicer_StopStirrer()
            assert self.sila_client.MotorServicer_GetPower().CurrentPower.value == 100
            assert self.sila_client.MotorServicer_GetRPM().CurrentRPM.value == 3000
    else:
        # Note: In real mode stirrer is actually stirring, make sure the cooling is connected and switched 'on'
        @pytest.mark.real_unsafe
        def test_StirrerControl(self, setup_and_teardown_stirrer):
            feature_object = self.sila_client.MotorServicer_StartStirrer()
            time.sleep(5)
            assert feature_object is not None


# @pytest.mark.unimplemented
def test__init__():
    """Starts the server in a mocked environment as defined in BioREACTOR48Service_server.init()"""
    from sila2lib.sila_server import SiLA2Server
    with mock.patch.object(SiLA2Server, 'run', return_value=42):  # Syntax: .object(class, 'method', return)
        with mock.patch.object(BioREACTOR48Service_server, '__name__', '__main__'):
            with mock.patch.object(BioREACTOR48Service_server.sys, 'exit') as mock_exit:
                BioREACTOR48Service_server.init()
                assert mock_exit.call_args[0][0] == 42
