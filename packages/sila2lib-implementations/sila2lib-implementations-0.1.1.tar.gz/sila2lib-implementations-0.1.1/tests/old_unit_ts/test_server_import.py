from sila2lib_implementations.BioREACTOR48.BioREACTOR48Service import BioREACTOR48Service_server
from sila2lib_implementations.BlueVary.BlueVaryService import BlueVaryService_server
from sila2lib_implementations.DASGIP.DASGIP_Service import DASGIP_Service_server
from sila2lib_implementations.LAUDA.LAUDA_ThermostatService import LAUDA_ThermostatService_server
from sila2lib_implementations.Presens.PresensService import PresensService_server
from sila2lib_implementations.RegloICC.RegloICCService import RegloICCService_server

from sila2lib_implementations.BioREACTOR48.BioREACTOR48Service import BioREACTOR48Service_client
from sila2lib_implementations.BlueVary.BlueVaryService import BlueVaryService_client
from sila2lib_implementations.DASGIP.DASGIP_Service import DASGIP_Service_client
from sila2lib_implementations.LAUDA.LAUDA_ThermostatService import LAUDA_ThermostatService_client
from sila2lib_implementations.Presens.PresensService import PresensService_client
from sila2lib_implementations.RegloICC.RegloICCService import RegloICCService_client

import unittest
import os
import sys
import argparse
import threading
import time

__version__ = "1.0"


class TestPackage(unittest.TestCase):
    PYTHON_DIRECTORY = os.path.dirname(os.path.dirname(sys.executable))
    INSTALLATION_DIRECTORY = os.path.join(PYTHON_DIRECTORY, 'lib/site-packages/sila2lib_implementations')
    PROJECT_DIRECTORY = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    SERVER_NAMES: list = []
    CLIENT_NAMES: list = []

    # Test directories
    def test_environment_path(self):
        """
        Virtual environment has been set up using pipenv. Pipfile has been installed.
        """
        self.assertEqual(True if '.virtualenvs' in self.PYTHON_DIRECTORY else False, True, 'Pipenv virtual environment '
                                                                                           'not installed correctly')

    def test_installation_directory(self):
        """
        Tests whether the package installation directory in the used python environment is present.
        The package should be available in path-to-python/lib/site-packages/<my-package-name>
        """
        self.assertEqual(os.path.isdir(self.INSTALLATION_DIRECTORY), True,
                         'Package not installed in PYTHONPATH/lib/site-packages!')

    def test_project_directory(self):
        """
        Test for the existence of the project directory. Should be superfluous testing for this, but doing it anyway.
        """
        self.assertEqual(os.path.isdir(self.PROJECT_DIRECTORY), True,
                         'Project directory not found!')

    def test_python_directory_permissions(self):
        """
        Check whether the user running the tests and the script has the correct permissions for the python_directory
        """
        self.assertEqual(os.access(self.PYTHON_DIRECTORY, os.R_OK), True,
                         'No read permission for python interpreter directory')  # Check for read access
        self.assertEqual(os.access(self.PYTHON_DIRECTORY, os.W_OK), True,
                         'No write permission for python interpreter directory')  # Check for write access
        self.assertEqual(os.access(self.PYTHON_DIRECTORY, os.X_OK), True,
                         'No execution permission for python interpreter directory')  # Check for execution access
        self.assertEqual(os.access(self.PYTHON_DIRECTORY, os.F_OK), True,
                         'Directory does not exist')  # Check for existence of file

    def test_project_directory_permissions(self):
        """
        Check whether the user running the tests and the script has the correct permissions for the project_directory
        """
        self.assertEqual(os.access(self.PROJECT_DIRECTORY, os.R_OK), True,
                         'No read permission for project directory')  # Check for read access
        self.assertEqual(os.access(self.PROJECT_DIRECTORY, os.W_OK), True,
                         'No write permission for project directory')  # Check for write access
        self.assertEqual(os.access(self.PROJECT_DIRECTORY, os.X_OK), True,
                         'No execution permission for project directory')  # Check for execution access
        self.assertEqual(os.access(self.PROJECT_DIRECTORY, os.F_OK), True,
                         'Directory does not exist')  # Check for existence of file

    def test_installation_directory_content(self):
        _project_content = [element for element in os.listdir(
            os.path.join(self.PROJECT_DIRECTORY, 'sila2lib_implementations'))
                            if element[0:2] != '__' and element[0] != '.']
        _installation_content = [element for element in os.listdir(self.INSTALLATION_DIRECTORY) if element[0:2] != '__'] #
        self.assertEqual(_project_content == _installation_content, True,
                         'Content of installation and project directory do not match!')

    # Test server imports and version
    def test_server_import(self):
        _elements = os.listdir(self.INSTALLATION_DIRECTORY)
        for _element in _elements:
            if _element[0:1] != '_':
                _device_folder = os.path.join(self.INSTALLATION_DIRECTORY, _element)
                _service_name = [element for element in os.listdir(_device_folder) if 'Service' in element][0]
                _import_path = 'sila2lib_implementations' + '.' + _element + '.' + _service_name
                _server_name = _service_name + '_server'
                self.SERVER_NAMES.append(_server_name)
                _temp = __import__(_import_path, globals(), locals(), _server_name, 0)
                vars(self)[_server_name] = vars(_temp)[f'{_server_name}']
                print(f'Successfully imported module {_server_name}!')

    def test_server_version(self):
        _elements = os.listdir(self.INSTALLATION_DIRECTORY)
        for _element in _elements:
            if _element[0:1] != '_':
                _device_folder = os.path.join(self.INSTALLATION_DIRECTORY, _element)
                _service_name = [element for element in os.listdir(_device_folder) if 'Service' in element][0]
                _import_path = 'sila2lib_implementations' + '.' + _element + '.' + _service_name
                _server_name = _service_name + '_server'
                self.SERVER_NAMES.append(_server_name)
                _temp = __import__(_import_path, globals(), locals(), _server_name, 0)
                vars(self)[_server_name] = vars(_temp)[f'{_server_name}']
                self.assertEqual(vars(self)[_server_name].__version__, __version__,
                                 f'The version of the server {_server_name} is not supported. '
                                 f'Update the respective server to version {__version__}. Current version is: '
                                 f'{vars(self)[_server_name].__version__}')

    # Test client imports and version
    def test_client_import(self):
        _elements = os.listdir(self.INSTALLATION_DIRECTORY)
        for _element in _elements:
            if _element[0:1] != '_':
                _device_folder = os.path.join(self.INSTALLATION_DIRECTORY, _element)
                _service_name = [element for element in os.listdir(_device_folder) if 'Service' in element][0]
                _import_path = 'sila2lib_implementations' + '.' + _element + '.' + _service_name
                _client_name = _service_name + '_client'
                self.CLIENT_NAMES.append(_client_name)
                _temp = __import__(_import_path, globals(), locals(), _client_name, 0)
                vars(self)[_client_name] = vars(_temp)[f'{_client_name}']

    def test_client_version(self):
        _elements = os.listdir(self.INSTALLATION_DIRECTORY)
        for _element in _elements:
            if _element[0:1] != '_':
                _device_folder = os.path.join(self.INSTALLATION_DIRECTORY, _element)
                _service_name = [element for element in os.listdir(_device_folder) if 'Service' in element][0]
                _import_path = 'sila2lib_implementations' + '.' + _element + '.' + _service_name
                _client_name = _service_name + '_client'
                self.SERVER_NAMES.append(_client_name)
                _temp = __import__(_import_path, globals(), locals(), _client_name, 0)
                vars(self)[_client_name] = vars(_temp)[f'{_client_name}']
                self.assertEqual(vars(self)[_client_name].__version__, __version__,
                                 f'The version of the client {_client_name} is not supported. '
                                 f'Update the respective client to version {__version__}. Current version is: '
                                 f'{vars(self)[_client_name].__version__}')

    # Test server-client communication
    def test_server_client_communication(self):
        _elements = os.listdir(self.INSTALLATION_DIRECTORY)
        port = 50050
        for i, _element in enumerate(_elements):
            if _element[0:1] != '_':
                _device_folder = os.path.join(self.INSTALLATION_DIRECTORY, _element)
                _service_name = [element for element in os.listdir(_device_folder) if 'Service' in element][0]
                _import_path = 'sila2lib_implementations' + '.' + _element + '.' + _service_name
                _client_name = _service_name + '_client'
                _server_name = _service_name + '_server'
                self.SERVER_NAMES.append(_server_name)

                _temp = __import__(_import_path, globals(), locals(), _server_name, 0)
                vars(self)[_server_name] = vars(_temp)[f'{_server_name}']

                _temp = __import__(_import_path, globals(), locals(), _client_name, 0)
                vars(self)[_client_name] = vars(_temp)[f'{_client_name}']

                _port = port + i
                cmd_args = argparse.Namespace(description=f'This is a {_element} Service',
                                              encryption=None, encryption_cert=None, encryption_key=None, ip='127.0.0.1',
                                              port=_port, server_name=f'{_service_name}', server_type='Unknown Type')
                try:
                    server_thread = threading.Thread(target=vars(vars(self)[_server_name])[_service_name + 'Server'], name='server_thread',
                                                     args=(cmd_args, '127.0.0.1', _port, True), kwargs={}, daemon=True)
                    server_thread.start()
                    # print(server_thread.is_alive())
                    print('Server started')
                    time.sleep(2)
                    client = vars(vars(self)[_client_name])[_service_name + 'Client'](server_ip="127.0.0.1",
                                                                                      server_port=_port)
                    self.assertTrue(client.Get_ImplementedFeatures())
                    print(client.Get_ImplementedFeatures())
                    time.sleep(2)
                except RuntimeError:
                    assert True


if __name__ == "__main__":
    unittest.main()
