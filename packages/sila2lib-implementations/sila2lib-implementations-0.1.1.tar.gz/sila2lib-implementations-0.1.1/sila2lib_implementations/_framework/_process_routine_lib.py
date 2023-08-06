from datetime import datetime
import csv
import os
import shutil
import persistent
from influxdb import InfluxDBClient
import numpy as np
import traceback

def read_schedule_from_csv(file_path = 'sampling_times.csv'):
    with open(file_path, newline='') as f:
        reader = csv.reader(f, delimiter=';')
        list_of_datestrings = list(reader)
    list_of_datetimes = [datetime.strptime(date[0], '%d.%m.%Y, %H:%M:%S') for date in list_of_datestrings]
    return list_of_datetimes

def read_schedule_from_list(list_of_datestrings):
    return [datetime.strptime(date, '%d.%m.%Y, %H:%M:%S') for date in list_of_datestrings]


class ExperimentDescriptionData(persistent.Persistent):

    default_description = 'Ante mare et terras et quod tegit omnia caelum unus erat toto naturae vultus in orbe quem ' \
                          'dixere chaos: rudis indigestaque moles nec quicquam nisi pondus iners congestaque eodem ' \
                          'non bene iunctarum discordia semina rerum.'

    def __init__(self, name='TestExperiment', operator='John Doe', description=default_description, path=os.getcwd(),
                 positions=48, active_positions=48, devices=[]):
        self.run_name = name
        self.operator = operator
        # Do NOT use any device names that are used as variables internally. The internal values of some tasks may be
        # overwritten!
        self.devices: list = devices
        self.datetime = datetime.now()
        self.datetime_as_str = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        self.description = description
        self.path = path
        # self.parent_path = f'{self.path}/{self.run_name}_{self.datetime_as_str}'
        self.parent_path = f'{self.path}/{self.run_name}_{self.datetime.strftime("%Y_%m_%d")}'
        self.log_path = f'{self.parent_path}/logs'
        self.zodb_path = f'{self.parent_path}/zodb_database'
        self.influx_path = f'{self.parent_path}/influx_database_export'
        self.figure_path = f'{self.parent_path}/figures'

        self.positions = positions
        self.initial_active_positions = active_positions
        self.active_positions = active_positions


    def create_folders(self):
        '''
        Create experiment folders for log files, figures and database
        '''
        # If the folder doesn't exist yet, create all directories
        if not os.path.exists(self.parent_path):
            # Create parent directory
            os.makedirs(self.parent_path)
            # Create sub-directories
            os.makedirs(self.log_path)
            os.makedirs(self.zodb_path)
            os.makedirs(self.influx_path)
            os.makedirs(self.figure_path)

        # If the folder already exists, check whether each sub-directory exists and create if necessary
        else:
            tmp = input(f'Project folder {self.parent_path} already exists. Should the folder be deleted (y/n)? ')
            if tmp == 'y':
                shutil.rmtree(self.parent_path, ignore_errors=True)
                # Create parent directory
                os.makedirs(self.parent_path)
                # Create sub-directories
                os.makedirs(self.log_path)
                os.makedirs(self.zodb_path)
                os.makedirs(self.influx_path)
                os.makedirs(self.figure_path)
            if tmp == 'n':
                tmp = input('Change run name. Type new run name (No spaces or special characters):')
                self.run_name = tmp
                self.__init__(name=self.run_name, operator=self.operator, description=self.description, path=self.path)
                if not os.path.exists(self.parent_path):
                    # Create parent directory
                    os.makedirs(self.parent_path)
                    # Create sub-directories
                    os.makedirs(self.log_path)
                    os.makedirs(self.zodb_path)
                    os.makedirs(self.influx_path)
                    os.makedirs(self.figure_path)

    def save_meta_data(self):
        if not os.path.isfile(f'{self.parent_path}/description.csv'):
            print('isfile', os.path.isfile(f'{self.parent_path}/description.csv'))
            with open(f'{self.parent_path}/description.csv', "w") as csv_file:
                writer = csv.writer(csv_file, delimiter=';')
                writer.writerow([f'Run name:\t{self.run_name}'])
                writer.writerow([f'Operator:\t{self.operator}'])
                writer.writerow([f'Start time:\t{self.datetime_as_str}'])
                writer.writerow([f'Description:\t{self.description}'])
                writer.writerow([f'Storage path: \t {self.parent_path}'])
                writer.writerow([f'Total number of available positions: \t {self.positions}'])
                writer.writerow([f'Number of active positions [Start]: \t {self.initial_active_positions}'])
                writer.writerow([f'Number of active positions [End]: \t {self.active_positions}'])
        else:
            with open(f'{self.parent_path}/description.csv', "a+") as csv_file:
                writer = csv.writer(csv_file, delimiter=';')
                writer.writerow([f'End time: \t {datetime.now().strftime("%Y_%m_%dT%H_%M_%SZ")}'])


class ExperimentProcessData:
    def __init__(self, positions=np.ones(48), active_positions=np.ones(48), logger=None):
        self.initial_positions = active_positions
        self.positions = active_positions.shape[0]
        self.active_positions = active_positions
        self.logger = logger

        self.measurements = ['initial', 'active']

    def add_active_reactor(self, positions_id):
        for position_id in positions_id:
            self.active_positions[position_id] = 1

    def exclude_reactor(self, positions_id):
        for position_id in positions_id:
            self.active_positions[position_id] = 0

    def write_db(self):
        # Should I make the DB call from here or from the parent file that's using this class?
        # If i make it from here, i must supply the class with the DB details on initialization
        pass

    def read_db(self):
        pass

    def update(self, client_object):
        for measurement in self.measurements:
            try:
                results = client_object.db_client.query(
                    'SELECT {} FROM "{}"."{}"."schedulerPositionData" GROUP BY position '
                    'ORDER BY DESC LIMIT 1'.format(measurement, client_object.db_name, client_object.db_policy))
                data_status = dict()
                for entry in results.items():
                    _status: int = 0
                    _position = entry[0][1]['position']
                    for value in entry[1]:
                        _status = value[measurement]
                    data_status[_position] = _status
                # Create an ordered list of the status of the reactor positions. List index corresponds to position.
                vars(self)[f'{measurement}_positions'] = np.array([data_status[str(k)] if str(k) in data_status.keys() else 0 for k in
                                                         range(len(data_status.keys()))])
                # print(f'UPDATED PROCESS DATA {measurement} ARRAY: ', vars(self)[f'{measurement}'])
            except:
                self.logger.error('Process data could not be read from DB!')
                vars(self)[f'{measurement}_positions'] = np.zeros(self.positions)


def initial_positions_to_db(experiment_name: str = "default_experiment_name", positions: np.array = np.ones(48)):
    data_points = list()
    for i in range(0, positions.shape[0], 1):
        data_point = {
            "measurement": "schedulerPositionData",
            "tags": {
                "experiment_name": experiment_name,
                "parameter": 'initial_positions',
                "position": i
            },
            "time": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "fields": {
                "initial": positions[i]
            }
        }
        data_points.append(data_point)
    return data_points


def active_positions_to_db(experiment_name: str = "default_experiment_name", positions: np.array = np.ones(48)):
    data_points = list()
    for i in range(0, positions.shape[0], 1):
        data_point = {
            "measurement": "schedulerPositionData",
            "tags": {
                "experiment_name": experiment_name,
                "parameter": 'active_positions',
                "position": i
            },
            "time": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "fields": {
                "active": positions[i]
            }
        }
        data_points.append(data_point)
    return data_points


def cum_malfunction_positions_to_db(experiment_name: str = "default_experiment_name", device_name:str = 'default device',
                                    positions: np.array = np.ones(48)):
    data_points = list()
    for i in range(0, positions.shape[0], 1):
        data_point = {
            "measurement": "schedulerBioREACTOR48Data",
            "tags": {
                "experiment_name": experiment_name,
                "device": device_name,
                "position": i
            },
            "time": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "fields": {
                "malfunctions": positions[i]
            }
        }
        data_points.append(data_point)
    return data_points

def exclude_positions_to_db(experiment_name: str = "default_experiment_name", device_name:str = 'default device',
                                    positions: np.array = np.ones(48)):
    data_points = list()
    for i in range(0, positions.shape[0], 1):
        data_point = {
            "measurement": "schedulerPositionData",
            "tags": {
                "experiment_name": experiment_name,
                "device": device_name,
                "position": i
            },
            "time": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "fields": {
                "exclusions": positions[i]
            }
        }
        data_points.append(data_point)
    return data_points


class ExperimentDeviceData:

    def __init__(self, device_name='default-name', server_ip='127.0.0.1', server_port='50001', logger=None):
        self.name = device_name
        self.server_ip = server_ip
        self.server_port = server_port
        self.UUID = 'default-UUID'
        self.restart_flag = 0

        self.logger = logger

    def update(self, client_object):
        """

        :param client_object:
        :return: A list is returned. The first object [0] is assigend to the self.restart flag. In the future, this
        class may be extended to accomodate for multiple elements to be updated.
        """
        attribute_name = 'restart_flag'
        try:
            results = client_object.db_client.query(
                'SELECT {} FROM "{}"."{}"."scheduler{}Data" GROUP BY device_name '
                'ORDER BY DESC LIMIT 1'.format(attribute_name, client_object.db_name, client_object.db_policy,
                                               self.name))
            _values = list()
            for entry in results.items():
                _value: int = False
                for i, value in enumerate(entry[1]):
                    _value = value[attribute_name]
                    _values.append(_value)
            vars(self)[f'{attribute_name}'] = _values[0]
                # [data_status[str(k)] if str(k) in data_status.keys() else 0 for k in
                #                                       range(len(data_status.keys()))][0]
        except:
            self.logger.error('Device data could not be read from DB!')
            vars(self)[f'{attribute_name}'] = [False]

    def restart_flag_positions_to_db(self, client_object, restart_flag, experiment_name: str = "default_experiment_name"
                                     ):
        data_points = list()
        data_point = {
            "measurement": f'scheduler{self.name}Data',
            "tags": {
                "experiment_name": experiment_name,
                "device_name": self.name,
                "position": '',
            },
            "time": datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ"),
            "fields": {
                "restart_flag": restart_flag
            }
        }
        data_points.append(data_point)
        client_object.db_client.write_points(data_points)
        return data_points


class InfluxDBClientClass:
    def __init__(self, db_host = 'localhost', db_port = 8086, db_name = 'schedulerDB', db_policy = 'schedulerPolicy',
                 db_username = 'schedulerApplication', db_password = 'DigInBio'):
        self.db_host = db_host
        self.db_port = db_port
        self.db_name = db_name
        self.db_policy: str = db_policy
        self.db_username = db_username
        self.db_password = db_password
        self.db_client = InfluxDBClient(host=self.db_host, port=self.db_port, username=self.db_username,
                                        password=self.db_password)

    def database_connect(self, logger):
        """
        Connect the scheduler to the InfluxDB for storing process specific data from scheduled tasks.
        :return: None
        """
        self.db_client = InfluxDBClient(host=self.db_host, port=self.db_port, username=self.db_username,
                                        password=self.db_password)
        # Select the right database and select the right retention policy
        if self.db_name in [database['name'] for database in self.db_client.get_list_database()]:
            logger.info(f'Connecting to existing database \"{self.db_name}\".')
            self.db_client.switch_database(self.db_name)
            self.db_client.create_retention_policy(self.db_policy, 'INF', replication="1", database=self.db_name,
                                                   default=True, shard_duration=u'0s')
        elif self.db_name not in [database['name'] for database in self.db_client.get_list_database()]:
            logger.info(f'Database with this name {self.db_name} could not be found. Creating new database.')
            self.db_client.create_database(self.db_name)
            logger.info(f'Connecting to new database {self.db_name}.')
            self.db_client.switch_database(self.db_name)
            self.db_client.create_retention_policy(self.db_policy, 'INF', replication="1", database=self.db_name,
                                                   default=True, shard_duration=u'0s')
        else:
            logger.error("Connection to database failed")
            logger.error(traceback.format_exc())
            raise ConnectionRefusedError

        logger.info(f'Checking connectivity. DB server version: {self.db_client.ping()}')
        logger.debug(f'Following users are registered on this database: {self.db_client.get_list_users()}')
