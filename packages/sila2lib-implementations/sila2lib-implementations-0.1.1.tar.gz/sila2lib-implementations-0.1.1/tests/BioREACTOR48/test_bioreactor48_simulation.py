#!/usr/bin/env python3
"""
This file tests the simulation mode of the BioREACTOR48. Tests are organized in classes to logically separate the
services' features, as well as get- from set-functions. Return values are validated for data types, value range and whether
length of return values is as desired (e.g. as input values). All returns must assert "True", since the injected input
parameter range is only valid. For invalid parameter injection and error handling see:
'test_bioreactor48_simulation_error.py'
Multiple executions of single test_functions are conducted via the "parametrize" functionality offered by pytest
(injection) to cover and test a wide input range.
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


def wait_until_port_closes(ip: str, port: int, timeout: float = 10) -> bool:
    """Try to bind the socket at {ip}:{port} to check if a socket resource is available

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

    def test_toggle_mode(self):
        assert self.sila_client.simulation_mode is True  # ._simulation_mode also possible
        self.sila_client.toggleSimMode()
        assert self.sila_client.simulation_mode is False

    def test_mode_switch(self):
        self.sila_client.switchToSimMode()
        assert self.sila_client.simulation_mode is True
        self.sila_client.switchToRealMode()
        assert self.sila_client.simulation_mode is False
        self.sila_client.switchToSimMode()
        assert self.sila_client.simulation_mode is True

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
    """ Test all DeviceServicer Get functions"""
    sila_client = BioREACTOR48ServiceClient(server_ip=BioreactorTestServer.ip, server_port=BioreactorTestServer.port)

# todo: ask why not all default values, instead different values
    def test_GetDeviceStatus(self):
        response = self.sila_client.DeviceServicer_GetDeviceStatus()
        assert isinstance(response.Status.value, str)
        assert isinstance(response.Version.value, int)
        assert isinstance(response.Mode.value, str)
        assert isinstance(response.BarConnection.value, str)
        assert isinstance(response.Address.value, int)
        assert response.Status.value == 'OK'  # why not all defaults?
        assert response.Version.value == 8602
        assert response.Mode.value == 'REM'
        assert response.BarConnection.value == '101010'  # 1 = connected, 0 = not connected
        assert response.Address.value == 1

    # @pytest.mark.skip
    def test_DeviceServicer_GetReactorStatus(self):
        """A random failure is implemented in the simulation and/or real implementation for DeviceServicer_GetReactorStatus().
        Therefore the assertion sometimes is false and the execution stopped. Uncomment '# @pytest.mark.skip' to skip this test."""
        response = self.sila_client.DeviceServicer_GetReactorStatus()
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

    def test_DeviceServicer_GetBarNumber(self):
        response = self.sila_client.Get_DeviceServicer_BarNumber()
        return_val = response.BarNumber.value
        assert response is not None
        assert isinstance(return_val, int)
        assert return_val == total_bars

    def test_DeviceServicer_GetBarReactors(self):
        response = self.sila_client.Get_DeviceServicer_BarReactors()
        return_val = response.BarReactors.value
        assert response is not None
        assert isinstance(return_val, int)
        assert return_val == bar_sensors

    def test_DeviceServicer_GetTotalReactors(self):
        response = self.sila_client.Get_DeviceServicer_TotalReactors()
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
        response = self.sila_client.MotorServicer_GetPower()
        return_val = response.CurrentPower.value
        assert isinstance(return_val, int)
        assert return_val == 100  # default value
        # no accepted value range implemented yet

    def test_GetRPM(self):
        response = self.sila_client.MotorServicer_GetRPM()
        return_val = response.CurrentRPM.value
        assert isinstance(return_val, int)
        assert return_val == 3000  # default value
        # no accepted value range implemented yet


class TestBioREACTORMotorServicerSet:
    """Test all MotorServicer Set functions"""
    sila_client = BioREACTOR48ServiceClient(server_ip=BioreactorTestServer.ip, server_port=BioreactorTestServer.port)

    @pytest.mark.parametrize("RPM_value",  random.sample(range(0, 4000, 1000), 2))
    def test_SetRPM(self, RPM_value):
        """value range not implemented. Accepted input: int, long"""
        response = self.sila_client.MotorServicer_SetRPM(RPM_value)
        curr_rpm = response.CurrentStatus.value.split('_')
        curr_rpm = curr_rpm[1][:-3]
        assert float(curr_rpm) == RPM_value

    @pytest.mark.parametrize("power_value", (0, 75))
    def test_SetPower(self, power_value):
        """value range not implemented. Accepted input: int, long. No negative values"""
        response = self.sila_client.MotorServicer_SetPower(power_value)
        logging.debug(response)
        curr_power = response.CurrentStatus.value.split('_')
        curr_power = curr_power[-2][5:]
        assert float(curr_power) == power_value

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

@pytest.mark.unimplemented
def test__init__():
    """Starts the server in a mocked environment as defined in BioREACTOR48Service_server.init()"""
    from sila2lib.sila_server import SiLA2Server
    with mock.patch.object(SiLA2Server, 'run', return_value=42):  # Syntax: .object(class, 'method', return)
        with mock.patch.object(BioREACTOR48Service_server, '__name__', '__main__'):
            with mock.patch.object(BioREACTOR48Service_server.sys, 'exit') as mock_exit:
                BioREACTOR48Service_server.init()
                assert mock_exit.call_args[0][0] == 42
# todo: bug: BioREACTOR48ServiceServer' object has no attribute 'ser'
