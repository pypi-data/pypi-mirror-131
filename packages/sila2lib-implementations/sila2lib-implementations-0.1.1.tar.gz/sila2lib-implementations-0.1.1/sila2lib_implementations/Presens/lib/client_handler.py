import os
import csv
import importlib

def InstantiateClient():

    #Load the communication configuration file
    com_config_path = "%s\\com_config.csv"%os.path.dirname(os.path.realpath(__file__))
    clients_info = list()
    # print('%s\\com_config.csv'%self.com_config_path)
    with open(com_config_path, mode='r') as infile:
        #next(infile)  # Skip the header file
        client_info = csv.DictReader(infile, delimiter=';')  # Write config_file to dict
        for row in client_info:
            clients_info.append(row)


    clients_list = list()
    #Import the client file and instantiate using the communication configuration
    for i, client_info in enumerate(clients_info):
        client_path = '%s.%s.%s' % (
        os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)),
        client_info['Device Name'], client_info['Client File Name'])
        client_path = 'interface.%s.%s.%s' % (client_info['Device'],client_info['Device Name'], client_info['Client File Name'])
        #client_path = 'interface'

        print(client_path)
        #def import_client(self, device: str, client_name: str):

        client = importlib.import_module(client_path)
        vars()["%s_%s" %(client_info['Client File Name'],i)] = vars(client)["%sClient" % client_info['Device Name']]()
        clients_list.append(vars()["%s_%s" %(client_info['Client File Name'],i)])

    return clients_info, clients_list