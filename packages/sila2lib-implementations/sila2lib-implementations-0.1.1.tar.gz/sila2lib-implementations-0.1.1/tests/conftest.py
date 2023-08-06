# easier: import all and select with a dictionary the server/clients that should be started!!!

# """
# This file contains all the generalized fixtures that are used/needed for all tests. Fixtures are called by the respective
# method during their specific execution. Hence, this script is not intended to be executed.
# """
#
# import logging
# import pytest
# import socket
# from threading import (
#     Thread,
#     Event
# )
# import time
#
# from importlib import import_module  # dynamic imports
# # from sila2lib_implementations.Presens.PresensService.PresensService_server import PresensServiceServer as ServiceServer
# # from sila2lib_implementations.Presens.PresensService.PresensService_client import PresensServiceClient as ServiceClient
# from sila2lib import sila_server
#
# from tests.config import settings
#
#
# logger = logging.getLogger(__name__)
#
#
# from sila2lib_implementations.Presens.PresensService.PresensService_server import PresensServiceServer
# from sila2lib_implementations.BioREACTOR48.BioREACTOR48Service.BioREACTOR48Service_server import BioREACTOR48ServiceServer
#
# server_imports = {
#     'Presens': PresensServiceServer,
#     'BioREACTOR48': BioREACTOR48ServiceServer,
# }
#
#
# def load(my_server):
#     my_code = get_my_server_class(server_imports[my_server])
#     server = my_server.upper()
#     global ip; global port; global simulation_mode
#     exec('ip = '"settings." + server + "_IP")  # fills variables of the .env respective of the server
#     exec('port = '"settings." + server + "_PORT")
#     exec('simulation_mode = '"settings." + server + "_SIMULATION_MODE")
#     return my_code
#
#
# def get_my_server_class(base_class):
#
#     # Test Server setup
#     class TestServer(get_my_server_class(server_imports[my_server])):
#     # class TestServer(sila_server):  # or dynamic imports
#         """
#         Test server instance. Implementation of service until an abort event is sent
#         :param abort_event: Event that leads to the server stop
#         """
#
#         def __init__(self, abort_event: Event):
#             self.abort_event = abort_event
#             super().__init__(ip=ip, port=port, simulation_mode=simulation_mode)
#
#         def serve(self):
#             self.run(block=False)
#             while not self.abort_event.is_set():
#                 time.sleep(1)
#             self.stop_grpc_server()
#
#     return TestServer
#
#
#
#
# def service_server_assignment(server):
#     """dynamic import, inheritance and initialization function
#         :param server: Server that shall be started"""
#     server = server.upper()
#     global ip; global port; global simulation_mode
#     exec('ip = '"settings." + server + "_IP")  # fills variables of the .env respective of the server
#     exec('port = '"settings." + server + "_PORT")
#     exec('simulation_mode = '"settings." + server + "_SIMULATION_MODE")
#     # same could be done with the imports, right?
#
#     if server == 'PRESENS':
#         service_server = "sila2lib_implementations.Presens.PresensService.PresensService_server.PresensServiceServer"
#         service_client = "sila2lib_implementations.Presens.PresensService.PresensService_client.PresensServiceClient"
#         # ServiceClient = "sila2lib_implementations"
#         # from sila2lib_implementations.Presens.PresensService.PresensService_server import PresensServiceServer as ServiceServer
#         # from sila2lib_implementations.Presens.PresensService.PresensService_client import PresensServiceClient as ServiceClient
#         global ip; global port; global simulation_mode
#         ip = settings.PRESENS_IP
#         port = settings.PRESENS_PORT
#         simulation_mode = settings.PRESENS_SIMULATION_MODE
#     elif server == 'bioreactor':
#         pass
#     global ServiceServer; global ServiceClient
#     # ServiceServer = import_module(service_server)
#     # ServiceClient = import_module(service_client)
#     return ip, port, simulation_mode
#
# class XY:
#     # dependency injection, import hooks, (facade, config switch)
#     # todo: WIP dynamic import not working
#     def __init__(self, server):
#         self.server = server.upper()
#         global ip; global port; global simulation_mode
#         exec('ip = '"settings." + self.server + "_IP")  # fills variables of the .env respective of the server
#         exec('port = '"settings." + self.server + "_PORT")
#         exec('simulation_mode = '"settings." + self.server + "_SIMULATION_MODE")
#
#
#     def load_import_modules(self):
#         if self.server == 'PRESENS':
#             service_server = "sila2lib_implementations.Presens.PresensService.PresensService_server"
#             # service_client = "sila2lib_implementations.Presens.PresensService.PresensService_client.PresensServiceClient"
#         elif self.server == 'bioreactor':
#             pass
#         global ServiceServer; global ServiceClient
#         ServiceServer = import_module(service_server)  # , package=PresensServiceServer)
#         # ServiceClient = import_module(service_client)
#         return ServiceServer
#
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
# # @pytest.fixture(params=["chrome", "firefox"], scope='class')
# # def init_driver(request):
# #     if request.param == "chrome":
# @pytest.fixture  # (autouse=True, scope='class')
# def setup_and_teardown_server(server):
#     """
#     Starts a server thread and tears it down automatically after the whole module is executed.
#     """
#
#     abort_event = Event()
#     a = XY(server)
#     a.load_import_modules()
#     service_server_assignment(server)  # determines which (device-) server to start
#     server_instance = TestServer(abort_event)
#     thread = Thread(target=server_instance.serve, args=(), daemon=True)
#     thread.start()
#     wait_until_server_up(server)
#     logger.info('Started ' + server + ' server')
#     yield thread
#     abort_event.set()
#     thread.join(timeout=10)
#     wait_until_port_closes(ip=ip, port=port, timeout=10)  # ip and port became global variables
#     if thread.is_alive:
#         logger.warning(f'{server} server thread is still alive: {thread.is_alive()}')
#     logger.info('Stopped ' + server + ' server')
