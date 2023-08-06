import argparse
import logging
from sila2lib_implementations.BioREACTOR48.BioREACTOR48Service.BioREACTOR48Service_server import BioREACTOR48ServiceServer

cmd_args = argparse.Namespace(description=f'This is a BioREACTOR48 Service',
                              encryption=None, encryption_cert=None, encryption_key=None,
                              server_name=f'BioREACTOR48Service', server_type='Unknown Type')
logging.basicConfig(format='%(levelname)-8s| %(module)s.%(funcName)s: %(message)s', level=logging.DEBUG)

server = BioREACTOR48ServiceServer(cmd_args=cmd_args, ip='127.0.0.1', port=50003, simulation_mode=False)
