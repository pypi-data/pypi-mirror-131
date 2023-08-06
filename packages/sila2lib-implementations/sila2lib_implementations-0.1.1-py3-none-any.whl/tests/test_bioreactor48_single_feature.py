import pytest
from threading import Thread, Event
import time
import socket

from tests.config import settings
from sila2lib_implementations.BioREACTOR48.BioREACTOR48Service.BioREACTOR48Service_client import BioREACTOR48ServiceClient
from sila2lib_implementations.BioREACTOR48.BioREACTOR48Service.BioREACTOR48Service_server import BioREACTOR48ServiceServer


# functions to control and enable server proper traffic
def wait_until_port_closes(ip: str, port: int, timeout: float = 10):
    a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    a_socket.settimeout(timeout)
    location = (ip, port)
    try:
        a_socket.connect_ex(location)
        while a_socket.connect_ex(location) == 0:
            return 0
    except Exception as e:
        print('timeout reached, exception: %s', e)
        return 1
    finally:
        a_socket.close()


def wait_until_server_up(server, timeout: float = 10.0):
    # # fork of sila_python is missing for health report -> comment bock for online CI pipeline
    # t = 0
    # while server.healthy is False:
    #     if t > timeout:
    #         return 1
    #     time.sleep(0.1)
    #     t += 0.1
    # return 0
    time.sleep(10)


# Test Server setup
class BioREACTOR48TestServer(BioREACTOR48ServiceServer):
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


@pytest.fixture(autouse=True, scope='class')
def setup_and_teardown_server():
    abort_event = Event()
    server = BioREACTOR48TestServer(abort_event)
    thread = Thread(target=server.serve, args=(), daemon=True)
    thread.start()
    wait_until_server_up(server)
    yield thread
    abort_event.set()
    thread.join(timeout=15)
    wait_until_port_closes(ip=BioREACTOR48TestServer.ip, port=BioREACTOR48TestServer.port, timeout=10.0)
    print(thread.is_alive())
    print('Stopped Presens server')


# basic connection test
class TestBioREACTOR48Connectivity:
    sila_client = BioREACTOR48ServiceClient(server_ip=BioREACTOR48TestServer.ip,
                                            server_port=BioREACTOR48TestServer.port)

    def test_run_BioREACTOR48_test_server(self, setup_and_teardown_server):
        print(f'BioREACTOR48 server running. Is alive: {setup_and_teardown_server.is_alive()}')
        assert True

    def test_connect_to_BioREACTOR48_server(self):
        print(f'Connected to client: {self.sila_client.run()}')
        assert self.sila_client.run() is True


# Single feature test of the MotoServicer GetRPM feature
class TestBioREACTOR48_MotoServicer_Single_Feature:
    sila_client = BioREACTOR48ServiceClient(server_ip=BioREACTOR48TestServer.ip,
                                            server_port=BioREACTOR48TestServer.port)

    def test_bioreactor48_MotoServicer_GETRPM(self):
        feature_object = self.sila_client.MotorServicer_GetRPM()
        res = feature_object.CurrentRPM.value
        assert isinstance(res, int)
        assert isinstance(feature_object.CurrentRPM.value, int)


if __name__ == '__main__':
    pass
