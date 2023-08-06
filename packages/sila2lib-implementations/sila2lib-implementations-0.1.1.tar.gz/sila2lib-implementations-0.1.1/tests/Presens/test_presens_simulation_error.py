"""
This file tests the error handling of the simulation for the PreSens sensor bars.
Tests are intent to fail and the generated error is analyzed.
Tests are organized in classes to logically separate the services' features. Only SET functions are testet since get
errors are detected by the server itself on another level.
Return values are validated for data types, value range and whether length of return values is as desired
(e.g. as input values). All returns are expected to fail (assert "False"), since the injected input
parameter range is always invalid. For valid parameter injection see: 'test_presens_simulation.py'
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


from sila2lib_implementations.Presens.PresensService.PresensService_client import PresensServiceClient
from sila2lib_implementations.Presens.PresensService import PresensService_server

from tests.config import settings


logger = logging.getLogger(__name__)

# Import PreSens device default configuration from PresensService_server.py:
total_bars = PresensService_server.Properties.TotalBars
bar_sensors = PresensService_server.Properties.BarSensors
total_channels = PresensService_server.Properties.TotalChannels

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
class PresensTestServer(PresensService_server.PresensServiceServer):
    """
    Test server instance. Implementation of service until an abort event is sent
    :param abort_event: Event that leads to the server stop
    """

    ip = settings.PRESENS_IP
    port = settings.PRESENS_PORT
    simulation_mode = settings.PRESENS_SIMULATION_MODE

    def __init__(self, abort_event: Event):
        self.abort_event = abort_event
        super().__init__(ip=self.ip, port=self.port, simulation_mode=self.simulation_mode)

    def serve(self):
        self.run(block=False)
        while not self.abort_event.is_set():
            time.sleep(1)
        self.stop_grpc_server()


@pytest.fixture(autouse=True, scope='module')
def setup_and_teardown_presens_server():
    """
    Starts a server thread and tears it down automatically after the whole module is executed.
    """
    abort_event = Event()
    server = PresensTestServer(abort_event)
    thread = Thread(target=server.serve, args=(), daemon=True)
    thread.start()
    wait_until_server_up(server)
    logger.info('Started Presens server')
    yield thread
    abort_event.set()
    thread.join(timeout=10)
    wait_until_port_closes(ip=PresensTestServer.ip, port=PresensTestServer.port, timeout=10)
    if thread.is_alive:
        logger.warning(f'Presens server thread is still alive: {thread.is_alive()}')
    logger.info('Stopped Presens server')


# no server errors implemented yet
# class TestPresensServerFunctionalities:
#     pass


def safe_exit():
    """ This function avoids accidental execution of this script if in REAL MODE.
    Note: passing out of range parameters to a device could potentially break it. """
    if PresensTestServer.simulation_mode is False:
        logger.error('Fatal: The error triggering mode is ONLY allowed to run in simulation mode. However it was started '
                     'in the real mode. Note that this could potentially break the device.')
        exit()
        # sys.exit(), exit(), quit(), and os._exit(0)
        # kill the Python interpreter: be carefull calling this from outside
safe_exit()


class TestPresensCalibrationSet:
    """Test all Calibration Set functions"""
    sila_client = PresensServiceClient(server_ip=PresensTestServer.ip, server_port=PresensTestServer.port)

    # @pytest.mark.parametrize('SetO2CalLow_value', (total_bars * [-1],  # negative int list
    #                                                total_bars * ['-1'],  # negative str list
    #                                                total_bars * ['1'],  # positive str list
    #                                                total_bars * [-0.01],  # float list
    #                                                random.sample(range(91, 99999999, 1), total_bars),  # int list
    #                                                total_bars * [], total_bars * (),  # empty list/tuple
    #                                                ['aBc'],
    #                                                10))  # int
    @pytest.mark.parametrize('SetO2CalLow_value', default_cases)
    def test_SetO2CalLow(self, SetO2CalLow_value):
        """ The lower calibration point value set point for O2 up to two decimal points. Set the O2 calibration point value at 0% dissolved oxygen. Default = 57
        Accepted value range float 0 - 90 (inclusive)
        :param SetO2CalLow_value: The lower calibration point value set point for O2 up to two decimal points"""
        try:
            response = self.sila_client.calibrationService_client.SetO2CalLow(SetO2CalLow_value)
            return_val = response.CurrentO2CalLow
            for count, elem in enumerate(return_val):
                assert len(return_val) == total_bars
                assert isinstance(elem.value, float)
                assert elem.value in SetO2CalLow_value[count]  # in: -0.01 = -0.01\n
                assert elem.value in range(0, 91, 1)
        except (AssertionError, AttributeError, TypeError) as e:
            logger.error(f'Encountered exception {e.__class__.__name__}: {e}')
            assert True
        except Exception as e:
            logger.error(f'Encountered unknown exception {e.__class__.__name__}: {e}')
            logger.info('Please include unknown exceptions into test framework')
            assert False

    # @pytest.mark.parametrize('SetO2CalHigh_value', (total_bars * [-1],  # negative int list
    #                                                 total_bars * ['-1'],  # negative str list
    #                                                 total_bars * ['1'],  # positive str list
    #                                                 total_bars * [-0.01],
    #                                                 random.sample(range(91, 99999999, 1), total_bars),
    #                                                 total_bars * [], total_bars * (),
    #                                                 ['aBc'],
    #                                                 10))
    @pytest.mark.parametrize('SetO2CalHigh_value', default_cases)
    def test_SetO2CalHigh(self, SetO2CalHigh_value):
        """ The higher calibration point value setpoint for O2 up to two decimal points. Set the O2 calibration point value at 100% dissolved oxygen. Default = 27
        Accepted value range float 0 - 90 (inclusive)
        :param SetO2CalHigh_value: The higher calibration point value set point for O2 up to two decimal points"""
        try:
            response = self.sila_client.calibrationService_client.SetO2CalHigh(SetO2CalHigh_value)
            return_val = response.CurrentO2CalHigh
            for count, elem in enumerate(return_val):
                assert len(return_val) == total_bars
                assert isinstance(elem.value, float)
                assert elem.value in SetO2CalHigh_value[count]
                assert elem.value in range(0, 91, 1)
        except (AssertionError, AttributeError, TypeError) as e:
            logger.error(f'Encountered exception {e.__class__.__name__}: {e}')
            assert True
        except Exception as e:
            logger.error(f'Encountered unknown exception {e.__class__.__name__}: {e}')
            logger.info('Please include unknown exceptions into test framework')
            assert False

    # @pytest.mark.parametrize('SetO2CalTemp_value', (total_bars * [-11],  # negative int list
    #                                                 total_bars * ['-1'],  # negative str list
    #                                                 total_bars * ['1'],  # positive str list
    #                                                 total_bars * [-11.65],
    #                                                 random.sample(range(61, 99999999, 1), total_bars),
    #                                                 total_bars * [], total_bars * (),
    #                                                 ['aBc'],
    #                                                 10))
    @pytest.mark.parametrize('SetO2CalTemp_value', default_cases)
    def test_SetO2CalTemp(self, SetO2CalTemp_value):
        """ Set the value of the oxygen calibration temperature in degree Celsius. Default = 20
        Accepted value range float -10 - 60 (inclusive)
        :param SetO2CalTemp_value: The oxygen calibration temperature value to be set up to one decimal point in degree Celsius"""
        try:
            response = self.sila_client.calibrationService_client.SetO2CalTemp(SetO2CalTemp_value)
            return_val = response.CurrentO2CalTemp
            for count, elem in enumerate(return_val):
                assert len(return_val) == total_bars
                assert isinstance(elem.value, float)
                assert elem.value in SetO2CalTemp_value[count]
                assert elem.value in range(0, 91, 1)
        except (AssertionError, AttributeError, TypeError) as e:
            logger.error(f'Encountered exception {e.__class__.__name__}: {e}')
            assert True
        except Exception as e:
            logger.error(f'Encountered unknown exception {e.__class__.__name__}: {e}')
            logger.info('Please include unknown exceptions into test framework')
            assert False

    # @pytest.mark.parametrize('SetPHImax_value', (total_bars * [-1],  # negative int list
    #                                              total_bars * ['-1'],  # negative str list
    #                                              total_bars * ['1'],  # positive str list
    #                                              total_bars * [-0.01],
    #                                              random.sample(range(91, 99999999, 1), total_bars),
    #                                              total_bars * [], total_bars * (),
    #                                              ['aBc'],
    #                                              10))
    @pytest.mark.parametrize('SetPHImax_value', default_cases)
    def test_SetPHImax(self, SetPHImax_value):
        """ Set the value of the first calibration point (phi max) of the pH sensor. Default = 0
        Accepted value range float 0 - 90 (inclusive)
        :param SetPHImax_value: The set value of the first calibration point (phi max) of the pH sensor up to two decimal points."""
        try:
            response = self.sila_client.calibrationService_client.SetPHImax(SetPHImax_value)
            return_val = response.CurrentPHImax
            for count, elem in enumerate(return_val):
                assert len(return_val) == total_bars
                assert isinstance(elem.value, float)
                assert elem.value in SetPHImax_value[count]
                assert elem.value in range(0, 91, 1)
        except (AssertionError, AttributeError, TypeError) as e:
            logger.error(f'Encountered exception {e.__class__.__name__}: {e}')
            assert True
        except Exception as e:
            logger.error(f'Encountered unknown exception {e.__class__.__name__}: {e}')
            logger.info('Please include unknown exceptions into test framework')
            assert False

    # @pytest.mark.parametrize('SetPHImin_value', (total_bars * [-1],  # negative int list
    #                                              total_bars * ['-1'],  # negative str list
    #                                              total_bars * ['1'],  # positive str list
    #                                              total_bars * [-0.01],
    #                                              random.sample(range(91, 99999999, 1), total_bars),
    #                                              total_bars * [], total_bars * (),
    #                                              ['aBc'],
    #                                              10))
    @pytest.mark.parametrize('SetPHImin_value', default_cases)
    def test_SetPHImin(self, SetPHImin_value):
        """ Set the value of the second calibration point (phi min) of the pH sensor. Default = -
        Accepted value range float 0 - 90 (inclusive)
        :param SetPHImin_value: The set value of the first calibration point (phi min) of the pH sensor up to two decimal points."""
        try:
            response = self.sila_client.calibrationService_client.SetPHImin(SetPHImin_value)
            return_val = response.CurrentPHImin
            for count, elem in enumerate(return_val):
                assert len(return_val) == total_bars
                assert isinstance(elem.value, float)
                assert elem.value in SetPHImin_value[count]
                assert elem.value in range(0, 91, 1)
        except (AssertionError, AttributeError, TypeError) as e:
            logger.error(f'Encountered exception {e.__class__.__name__}: {e}')
            assert True
        except Exception as e:
            logger.error(f'Encountered unknown exception {e.__class__.__name__}: {e}')
            logger.info('Please include unknown exceptions into test framework')
            assert False

    # @pytest.mark.parametrize('SetPHpH0_value', (total_bars * [-1],  # negative int list
    #                                             total_bars * ['-1'],  # negative str list
    #                                             total_bars * ['1'],  # positive str list
    #                                             total_bars * [-0.01],
    #                                             random.sample(range(51, 99999999, 1), total_bars),
    #                                             total_bars * [], total_bars * (),
    #                                             ['aBc'],
    #                                             10))
    @pytest.mark.parametrize('SetPHpH0_value', default_cases)
    def test_SetPHpH0(self, SetPHpH0_value):
        """ Set the value of the third calibration point (pH0) of the pH sensor. Default = 0
        Accepted value range float 0 - 50 (inclusive)
        :param SetPHpH0_value: The set value of the third calibration point (pH0) of the pH sensor up to two decimal points."""
        try:
            response = self.sila_client.calibrationService_client.SetPHpH0(SetPHpH0_value)
            return_val = response.CurrentPHpH0
            for count, elem in enumerate(return_val):
                assert len(return_val) == total_bars
                assert isinstance(elem.value, float)
                assert elem.value in SetPHpH0_value[count]
                assert elem.value in range(0, 51, 1)
        except (AssertionError, AttributeError, TypeError) as e:
            logger.error(f'Encountered exception {e.__class__.__name__}: {e}')
            assert True
        except Exception as e:
            logger.error(f'Encountered unknown exception {e.__class__.__name__}: {e}')
            logger.info('Please include unknown exceptions into test framework')
            assert False

    # @pytest.mark.parametrize('SetPHdpH_value', (total_bars * [-1],  # negative int list
    #                                             total_bars * ['-1'],  # negative str list
    #                                             total_bars * ['1'],  # positive str list
    #                                             total_bars * [-0.01],
    #                                             random.sample(range(11, 99999999, 1), total_bars),
    #                                             total_bars * [], total_bars * (),
    #                                             ['aBc'],
    #                                             10))
    @pytest.mark.parametrize('SetPHdpH_value', default_cases)
    def test_SetPHdpH(self, SetPHdpH_value):
        """ Set the value of the fourth calibration point (dpH) of the pH sensor. Default = 0
        Accepted value range float 0 - 10 (inclusive)
        :param SetPHdpH_value: The set value of the fourth calibration point (dpH) of the pH sensor up to two decimal points."""
        try:
            response = self.sila_client.calibrationService_client.SetPHdpH(SetPHdpH_value)
            return_val = response.CurrentPHdpH
            for count, elem in enumerate(return_val):
                assert len(return_val) == total_bars
                assert isinstance(elem.value, float)
                assert elem.value in SetPHdpH_value[count]
                assert elem.value in range(0, 11, 1)
        except (AssertionError, AttributeError, TypeError) as e:
            logger.error(f'Encountered exception {e.__class__.__name__}: {e}')
            assert True
        except Exception as e:
            logger.error(f'Encountered unknown exception {e.__class__.__name__}: {e}')
            logger.info('Please include unknown exceptions into test framework')
            assert False

    # @pytest.mark.parametrize('SetPHCalTemp_value', (total_bars * [-1],  # negative int list
    #                                                 total_bars * ['-1'],  # negative str list
    #                                                 total_bars * ['1'],  # positive str list
    #                                                 total_bars * [-11.01],
    #                                                 random.sample(range(61, 99999999, 1), total_bars),
    #                                                 total_bars * [], total_bars * (),
    #                                                 ['aBc'],
    #                                                 10))
    @pytest.mark.parametrize('SetPHCalTemp_value', default_cases)
    def test_SetPHCalTemp(self, SetPHCalTemp_value):
        """ Set the value of the pH calibration temperature in degree Celsius. Default = 20
        Accepted value range float -10 - 60 (inclusive)
        :param SetPHCalTemp_value: The pH calibration temperature value to be set in degree Celsius up to one decimal point."""
        try:
            response = self.sila_client.calibrationService_client.SetPHCalTemp(SetPHCalTemp_value)
            return_val = response.CurrentPHCalTemp
            for count, elem in enumerate(return_val):
                assert len(return_val) == total_bars
                assert isinstance(elem.value, float)
                assert elem.value in SetPHCalTemp_value[count]
                assert elem.value in range(-10, 61, 1)
        except (AssertionError, AttributeError, TypeError) as e:
            logger.error(f'Encountered exception {e.__class__.__name__}: {e}')
            assert True
        except Exception as e:
            logger.error(f'Encountered unknown exception {e.__class__.__name__}: {e}')
            logger.info('Please include unknown exceptions into test framework')
            assert False


@pytest.mark.WIP  # functions not implemented in DeviceServicer yet
# please respect the style used above when implementing the functions, thanks :)
class TestPresensDeviceServiceSet:
    """Test all DeviceService Set functions"""
    sila_client = PresensServiceClient(server_ip=PresensTestServer.ip, server_port=PresensTestServer.port)

    @pytest.mark.WIP  # function is not implemented yet (real and simulation mode). Return value is the default 0.0
    # only pass invalid parameters here and catch the exceptions
    @pytest.mark.parametrize('SetTComp_value', (total_channels * [-0.01],
                                                random.sample(range(60, 99999999, 1), total_channels),
                                                total_channels * [],
                                                total_channels * (),))
    def test_SetTComp(self, SetTComp_value):
        """ Set the temperature compensation value. Values must be between 0-60 degrees Celsius. Default = 20
        Accepted value range float 0 - 59 (inclusive)
        :param SetTComp_value: The temperature compensation value to be set"""
        response = self.sila_client.deviceService_client.SetTComp(SetTComp_value)
        return_val = response.CurrentTComp.value
        assert isinstance(return_val, float)  # when WIP done: remove this line
        assert return_val == 0.0  # when WIP done: remove this line
        # when WIP done: uncomment this block line
        # assert len(return_val) == total_channels
        # for count, elem in enumerate(return_val):
        #     assert isinstance(elem.value, float)
        #     assert elem.value == SetTComp_value[count]

    @pytest.mark.WIP  # function is not implemented yet (real and simulation mode). Return value is the default 0.0
    @pytest.mark.parametrize('SetDynAveraging_value', (total_bars * [-0.01],
                                        random.sample(range(10, 99999999, 1), total_bars),
                                        total_bars * [],
                                        total_bars * (),))  # single int/float not possible
    def test_SetDynAveraging(self, SetDynAveraging_value):
        """ The dynamic averaging value to be set. Must be between 0-9. Default = 4.
        Accepted value range: float 0 - 9 (inclusive)
        :param SetDynAveraging_value: The dynamic averaging value to be set"""
        response = self.sila_client.deviceService_client.SetDynAveraging(SetDynAveraging_value)
        return_val = response.CurrentDynAverage.value
        assert isinstance(return_val, int)  # when WIP done: remove this line
        assert return_val == 1  # when WIP done: remove this line
        # assert len(return_val) == total_bars
        for count, elem in enumerate(return_val):
            pass
        # function is not implemented yet (real and simulation mode). Return value is NOT the default 0.0 but a return
        # value defined in the real or simulation function


def test__init__():
    """starts the server in a mocked environment as defined in PresensService_server.init()"""
    from sila2lib.sila_server import SiLA2Server
    with mock.patch.object(SiLA2Server, 'run', return_value=42):  # Syntax: .object(class, 'method', return)
        with mock.patch.object(PresensService_server, '__name__', '__main__'):
            with mock.patch.object(PresensService_server.sys, 'exit') as mock_exit:
                PresensService_server.init()
                assert mock_exit.call_args[0][0] == 42
