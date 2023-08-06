import argparse
import logging
from sila2lib_implementations.Presens.PresensService.PresensService_server import PresensServiceServer

cmd_args = argparse.Namespace(description=f'This is a Presens Service',
                              encryption=None, encryption_cert=None, encryption_key=None,
                              server_name=f'PresensService', server_type='Unknown Type')
logging.basicConfig(format='%(levelname)-8s| %(module)s.%(funcName)s: %(message)s', level=logging.DEBUG)

server = PresensServiceServer(cmd_args=cmd_args, ip='127.0.0.1', port=50002, simulation_mode=False)

