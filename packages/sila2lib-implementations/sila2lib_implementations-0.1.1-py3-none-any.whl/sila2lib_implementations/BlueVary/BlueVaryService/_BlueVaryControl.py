import os
import time
import datetime
import csv
import BlueVaryService_client as client

# TODO:Start servers automatically using a shell script
# os.system('sudo chmod 755 StartServer.sh')
# os.system('xterm -x ./ StartServer.sh')

Start_time = time.localtime(time.time())
# print(Start_time)

"""
### TODO: Find a better system for adressing the units. Get the UnitID as single source of truth
r1 = '/dev/ttyUSB1'
r2 = '/dev/ttyUSB0'
r3 = '/dev/ttyUSB3'
r4 = '/dev/ttyUSB2'
"""
units = (3, 4, 1, 2)
for i in units:
    print(i)
    vars()["client%s" % i] = client.BlueVaryServiceClient(server_ip='10.152.248.108', server_port=50000 + i)
    # print(vars()["client%s"%i].GetSensorID())
reactors = [client1, client2, client3, client4]

# TODO: get away from csv and us a DB. real-time plotting of the data should be possible.
# Constantly reading csv files is heavy on the processor and not very elegant


def create_csv(file_title):
    """
    This function generates the .csv file in which the BlueVary data will be stored.
    The function "append_data_csv" fills this file with information.
    """
    reactor = ['R1', 'R2', 'R3', 'R4']
    data_types = ['CO2 [%]', 'O2 [%]', 'Pressure [bar]', 'Humidity [%]', 'abs. Humidity [vol.-%]', 'Temperature [°C]']
    first_row = ['Time', 'Epoch time [s]', 'Time [h]']
    # create a list with the stuff to write in the first row
    for d_types in data_types:
        for r in reactor:
            first_row.append(r + ' ' + d_types)
    # actual writing of stuff
    with open(file_title, mode='w', newline='') as output_file:
        output_writer = csv.writer(output_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        output_writer.writerow(first_row)

def get_data(reactors, t_0):
    """
    A function that sends the respective data pull request via the SiLA2 clients to the SiLA2 servers of the respective modules.
    """
    ### TODO:Rearrange the outputfile to reduce the number of loops.
    ### TODO:Not fail-safe yet. Make sure that this function still works, once a module is excluded. The data must still be recorded if one unit fails.
    data = list()
    starttime = str(datetime.datetime.now())
    timestamp = time.time()
    t_0 = t_0
    curr_time = (timestamp - t_0) / (60 * 60)

    data.append(starttime)
    data.append(timestamp)
    data.append(curr_time)
    print(data)
    for i, unit in enumerate(reactors):
        data.append(unit.SensoorServicer_GetResults().CO2.value)
    print('CO2: ', data[-i-1:])
    for i, unit in enumerate(reactors):
        data.append(unit.SensoorServicer_GetResults().O2.value)
    print('O2: ', data[-i - 1:])
    for i, unit in enumerate(reactors):
        data.append(unit.SensoorServicer_GetResults().Pressure.value)
    print('P: ', data[-i - 1:])
    for i, unit in enumerate(reactors):
        data.append(unit.SensoorServicer_GetHumidity().Humidity.value)
    print('Hum.: ', data[-i - 1:])
    for i, unit in enumerate(reactors):
        data.append(unit.SensoorServicer_GetHumidity().Temperature.value)
    print('Temp.: ', data[-i - 1:])
    for i, unit in enumerate(reactors):
        data.append(unit.SensoorServicer_GetHumidity().AbsoluteHumidity.value)
    print('Abs. Hum.: ', data[-i - 1:])
    return data

def append_data_csv(file_title, data):
    """
    Appends the most current data from "get_data" to the .csv log-file
    """
    with open(file_title, mode='a', newline='') as output_file:
        output_writer = csv.writer(output_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        output_writer.writerow(data)


def get_file_size(file_title):
    """
    Calculates the file size of the log-file in bytes.
    """
    statinfo = os.stat(file_title)
    return statinfo.st_size
file_title = '/var/lib/cloud9/BlueVary/' + str(datetime.datetime.now()) + '.csv'
t_0 = time.time()
create_csv(file_title)

while True:
    data = get_data(reactors, t_0)
    append_data_csv(file_title=file_title, data=data)
    print('Measuring every 2 seconds. Current file size:%s KB' % (get_file_size(file_title) / 1024))
    print("Time:%.4s" % (time.time() - t_0))
    time.sleep(2 - (time.time() % 2))
