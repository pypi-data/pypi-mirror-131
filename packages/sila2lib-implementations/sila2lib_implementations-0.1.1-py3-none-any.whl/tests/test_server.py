import logging
import pytest
from uuid import UUID

from tests import conftest
from tests.config import settings  # optional

logger = logging.getLogger(__name__)


@pytest.mark.parametrize('server', ['presens'])
@pytest.mark.usefixtures("setup_and_teardown_server")
class TestServerFunctionalities:
    """
    Basic connection test with the server. Also checks if the server was started with the correct parameters (port, ip, mode)
    """
    # Setup_class is meant to be used like __init__ but the latter is causing problems in pytest
    # (cannot collect test class because it has a __init__ constructor)
    def setup_class(cls, server: str='Presens'):
        # todo: decide which implementation fits best!
        # cls.ip, cls.port, cls.simulation_mode = conftest.service_server_assignment(server)  # uncomment return statement in function
        # cls.ip = conftest.TestServer.server_ip
        # cls.ip = conftest.ServiceServer.server_ip  # conftest.TestServer.server_ip
        # way of not calling the server (but using same data as him)
        cls.server = server.upper()
        exec('cls.ip = '"settings." + cls.server + "_IP")  # fills variables of the .env respective of the server
        exec('cls.port = '"settings." + cls.server + "_PORT")
        exec('cls.simulation_mode = '"settings." + cls.server + "_SIMULATION_MODE")
        # ServiceServer, ServiceClient = conftest.XY.load_import_modules()
        # cls.sila_client = ServiceClient(server_ip=cls.ip, server_port=cls.port)
        cls.sila_client = conftest.ServiceClient(server_ip=cls.ip, server_port=cls.port)

    def test_run_presens_test_server(self, setup_and_teardown_server):
        logger.info(f'{self.server} server running. Is alive: {setup_and_teardown_server.is_alive()}')
        assert True

    def test_connect_to_presens_server(self):
        logger.info(f'Connected to {self.server} client: {self.sila_client.run()}')
        assert self.sila_client.run() is True

# todo: execution fails due to object has no attribute '_simulation_mode' -> same bug as in _real implementation
    # def test_toggle_mode(self):
    #     assert self.sila_client.simulation_mode is True  # ._simulation_mode also possible
    #     self.sila_client.toggleSimMode()
    #     assert self.sila_client.simulation_mode is False
    #
    # def test_mode_switch(self):
    #     self.sila_client.switchToSimMode()
    #     assert self.sila_client.simulation_mode is True
    #     self.sila_client.switchToRealMode()
    #     assert self.sila_client.simulation_mode is False
    #     self.sila_client.switchToSimMode()
    #     assert self.sila_client.simulation_mode is True

    def test_server_values(self):
        assert self.sila_client.server_port is self.port
        assert self.sila_client.server_hostname is self.ip
        assert self.sila_client.server_display_name == ''
        assert self.sila_client.server_description == ''
        assert self.sila_client.server_version == ''

    def test_client_values(self):
        assert self.sila_client.vendor_url == ''
        assert self.sila_client.name.lower() in (self.server + 'ServiceClient').lower()
        assert self.sila_client.version == '1.0'
        assert self.sila_client.description.lower() == ('This is a ' + self.server + ' MCR Service').lower()
        assert isinstance(UUID(self.sila_client.client_uuid), UUID)

    def test_server_standard_features(self):
        assert hasattr(self.sila_client, 'SiLAService_stub')
        assert 'sila2lib.framework.std_features.SiLAService_pb2_grpc.SiLAServiceStub' in \
               str(type(self.sila_client.SiLAService_stub))
        assert hasattr(self.sila_client, 'SimulationController_stub')
        assert 'sila2lib.framework.std_features.SimulationController_pb2_grpc.SimulationControllerStub' in \
               str(type(self.sila_client.SimulationController_stub))

    # WIP find source to parse data server specific
    def test_server_custom_features(self):
        assert hasattr(self.sila_client, 'deviceService_client')
        assert hasattr(self.sila_client, 'calibrationService_client')
        assert hasattr(self.sila_client, 'sensorProvider_client')
