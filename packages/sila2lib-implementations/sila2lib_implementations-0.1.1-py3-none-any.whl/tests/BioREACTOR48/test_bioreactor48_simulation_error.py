#!/usr/bin/env python3
"""
This file tests the error handling of the simulation for the BioREACTOR48.
Tests are intent to fail and the generated error is analyzed.
Tests are organized in classes to logically separate the services' features. Only SET functions are testet since get
errors are detected by the server itself on another level.
Return values are validated for data types, value range and whether length of return values is as desired
(e.g. as input values). All returns are expected to fail (assert "False"), since the injected input
parameter range is always invalid. For valid parameter injection see: 'test_bioreactor48_simulation.py'
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
from unittest import mock

from sila2lib_implementations.BioREACTOR48.BioREACTOR48Service.BioREACTOR48Service_client import BioREACTOR48ServiceClient
from sila2lib_implementations.BioREACTOR48.BioREACTOR48Service import BioREACTOR48Service_server

from tests.config import settings


logger = logging.getLogger(__name__)

# Import PreSens device default configuration from BioREACTOR48Service_server.py:
total_bars = BioREACTOR48Service_server.Properties.TotalBars
bar_sensors = BioREACTOR48Service_server.Properties.BarSensors
total_channels = BioREACTOR48Service_server.Properties.TotalChannels

# default test range definition
default_cases = [[-1], ['-1'], ['1'], [-0.01], ['aBc+!_'], [random.uniform(-100.01, 900.0)]]  # , 10, 'aBc+!']
default_cases = [total_bars*[item] for sublist in default_cases for item in sublist]  # not for [], 10, 'aBc+!'
default_cases.append([[], (), ['aBc+!_'], 10, 'aBc+!'])
default_cases.append([random.sample(range(100, 99999999, 1), total_bars)])
default_cases.append([random.sample(range(1000, 99999999, 1), total_channels)])


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

# no server errors implemented yet
# class TestPresensServerFunctionalities:
#     pass


def safe_exit():
    """ This function avoids accidental execution of this script if in REAL MODE.
    Note: passing out of range parameters to a device could potentially break it. """
    if BioreactorTestServer.simulation_mode is False:
        logger.error('Fatal: The error triggering mode is ONLY allowed to run in simulation mode. However it was started '
                     'in the real mode. Note that this could potentially break the device.')
        exit()
        # sys.exit(), exit(), quit(), and os._exit(0)
        # kill the Python interpreter: be carefull calling this from outside
safe_exit()


class TestBioREACTORMotorServicerSet:
    """Test all MotorServicer Set functions"""
    sila_client = BioREACTOR48ServiceClient(server_ip=BioreactorTestServer.ip, server_port=BioreactorTestServer.port)

    # @pytest.mark.parametrize('RPM_value', ([-1], [], (), # negative or empty lists/tuples
    #                                      total_bars * ['-1'],  # negative str list
    #                                      total_channels * ['1'],  # positive str list
    #                                      total_bars * [-0.01],
    #                                      random.sample(range(10000, 99999999, 1), total_bars),
    #                                      ['aBc']))
    @pytest.mark.parametrize('RPM_value', default_cases)
    def test_SetRPM(self, RPM_value):
        """value range not implemented. Accepted input: int, long"""
        try:
            response = self.sila_client.MotorServicer_SetRPM(RPM_value)
            curr_rpm = response.CurrentStatus.value.split('_')
            curr_rpm = curr_rpm[1][:-3]
            assert float(curr_rpm) == RPM_value
        except (AssertionError, AttributeError, TypeError) as e:
            logger.error(f'Encountered exception {e.__class__.__name__}: {e}')
            assert True
        except Exception as e:
            logger.error(f'Encountered unknown exception {e.__class__.__name__}: {e}')
            logger.info('Please include unknown exceptions into test framework')
            assert False

    # @pytest.mark.parametrize('power_value', ([-1], [], (), # negative or empty lists/tuples
    #                                          total_bars * ['-1'],  # negative str list
    #                                          total_channels * ['1'],  # positive str list
    #                                          total_bars * [-0.01],
    #                                          random.sample(range(100, 99999999, 1), total_bars),
    #                                          ['aBc']))
    @pytest.mark.parametrize('power_value', default_cases)
    def test_SetPower(self, power_value):
        """value range not implemented. Accepted input: int, long."""
        try:
            response = self.sila_client.MotorServicer_SetPower(power_value)
            logging.debug(response)
            curr_power = response.CurrentStatus.value.split('_')
            curr_power = curr_power[-2][5:]
            assert float(curr_power) == power_value
        except (AssertionError, AttributeError, TypeError) as e:
            logger.error(f'Encountered exception {e.__class__.__name__}: {e}')
            assert True
        except Exception as e:
            logger.error(f'Encountered unknown exception {e.__class__.__name__}: {e}')
            logger.info('Please include unknown exceptions into test framework')
            assert False

    @pytest.mark.unimplemented
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
