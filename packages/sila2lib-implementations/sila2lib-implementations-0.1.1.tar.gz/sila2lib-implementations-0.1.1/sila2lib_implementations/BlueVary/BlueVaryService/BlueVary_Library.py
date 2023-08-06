import os
import csv
import time
import datetime
import subprocess
from subprocess import Popen

if os.name == "nt": #only available on windows
    from subprocess import CREATE_NEW_CONSOLE
else:
    pass

from . import BlueVaryService_client as client

def timestamp():
    t = time.localtime()
    timestamp = "%s_%s_%s-%s_%s_%s"%(t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec)
    print(timestamp)
    return timestamp

no_units = 4    #number of total implemented units
dict_address_mapping = {
    '1': ("127.0.0.1", 50001),
    '2': ("127.0.0.1", 50002),
    '3': ("127.0.0.1", 50003),
    '4': ("127.0.0.1", 50004)
}
def InputUnits():
    units = list()
    while True:
        try:
            user_input = input("Add reactor positions. Enter the reactor position/s used [1-%s], exit with [c]: " % no_units)
            if "," in user_input:
                entries = user_input.split(",")
                for entry in entries:
                    if int(entry) in range(1, (no_units+1), 1):
                        units.append(int(entry))
                    else:
                        print("Enter integer numbers!")
                units.sort()    
                print("The following reactors position/s will be observed: ", units)
                
                add_another = input("Do you want to add another reactor position? [y,n]")
                if add_another == "y":
                    pass
                elif add_another == "n":
                    print("The following reactor position/s will be observed: ", units)
                    break
                else:
                    pass
            elif len(user_input) <= 1 and user_input in ["1", "2", "3", "4"]:
                units.append(int(user_input))
                units.sort() 
                print("The following reactor position/s will be observed: ", units)
                add_another = input("Do you want to add another reactor position? [y,n]")
                if add_another == "y":
                    pass
                elif add_another == "n":
                    print("The following reactor position/s will be observed: ", units)
                    break
                else:
                    pass
            elif (user_input == "c") == True:
                break
            else:
                print("Enter reactor positions as integers [1-%s]! Use a comma to separate reactors positions, if multiple reactors are used!" % no_units)
                pass
        except:
            print("Exception")
            print("Enter reactors as integers [1-%s]! Use a comma to separate reactors, if multiple reactors are used!" % no_units)
    print("Eliminating duplicates...")
    units = list(dict.fromkeys(units))
    print(units)
    return units

def InputInterval():
    while True:
        try:
            user_input = input("Define a measurement interval [in seconds]. Max interval is 3600:")
            try:
                user_input = int(user_input)
                if user_input in range(1, 3601, 1):
                    interval = user_input
                    print("Measurements are taken every %s seconds" % interval)
                    break
                else:
                    pass
            except:
                if user_input =='':
                    tmp = input("Would you like to use the default 60s Dominik? [y/enter,n]")
                    if tmp in ["y",""]:
                        interval = 60
                        break
                    else:
                        pass
                else:
                    print("Enter an integer number in the range of [1,3600]. @Dominik: default is 60!")
        except:
            print("Wrong format. Enter an integer!")
    return interval

def InputCalibration():
    while True:
        calibration = input("Do you want to calibrate the system? [y/n]:")
        if calibration == "y":
            calibration = True
            print("System is being calibrated")
            break
        elif calibration == "n":
            calibration = False
            print("No calibration")
            break
        else:
            print("Incorrect input. Retry!")
    return calibration

def calibrate(units):
    """
    Initiates the calibration sequence of the BlueVary device.
    """
    for i, unit in enumerate(units):
        unit.CalibrationServicer_StartCalibration()
    time.sleep(10)
    print("Systeme kalibriert")

def StartServers(units):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    servers = list()
    ### Todo minimize spawned server windows using STARTUPINFO
    # info = subprocess.STARTUPINFO()
    # info.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    for i, unit in enumerate(units):
        print("UNIT %s and i %s" % (unit, i))
        print("Starting %s\Server_Unit%s.py...." % (dir_path, unit))
        try:
            if os.name == "nt": #only available on windows
                print(os.name)
                vars()["SubprocessServer%s" % (unit)] = subprocess.Popen(
                    ["python", "%s\Server_Unit%s.py" % (dir_path, unit)], creationflags=CREATE_NEW_CONSOLE) #, startupinfo = info

            elif os.name == "posix":
                print(os.name)
                vars()["SubprocessServer%s" % (unit)] = subprocess.Popen(
                    ["python3.7", "%s/Server_Unit%s.py" % (dir_path, unit)])
                    # shell=True)#, start_new_session = True)  # stdout=subprocess.PIPE)  # close_fds=True, start_new_session = true, shell=False)
            else:
                print("OS not supported: %s" % os.name)
            print("Server %s started in SubprocessServer%s" % (unit, unit))

        except:
            print("Error starting server %s" % unit)
        finally:
            pass
            # print("finally")
        servers.append(vars()["SubprocessServer%s" % unit])
        time.sleep(5)
    print("Servers started")
    print(servers)
    return servers

def ServerStatus(servers):
    status_list = list()
    inactive_list = list()
    for i,server in enumerate(servers):
        status = server.poll()  # None means active, 1 means dead
        status_list.append(status)
        print(status)

    if status_list.count(None) == len(status_list):
        pass
    else:
        inactive_list = [i for i in range(0, len(status_list)) if status_list[i] == 1]
        for i, unit in enumerate(inactive_list):
            inactive_list[i] = int(unit)+1
        print("Error: The following servers of reactor positions are offline/ Can't be started. Check the serial connection!")
        print(inactive_list)
        for i, unit in enumerate(inactive_list):
            print(inactive_list[i])
            print("%s DEAD" % servers[i-1])
        if len(inactive_list) == 0:
            print("All servers offline")
            pass
        while True:
            tmp = input("Continue without, restart dead server and continue, abort? [y,r,n]")
            if tmp == "y":
                break
            elif tmp == "r":
                print("Restarting Server/s %s..." % inactive_list)
                StartServers(inactive_list)
                break
            elif tmp == "n":
                print("Abort")
                KillServers(servers)
                exit()
            else:
                print("Incorrect input. Retry!")
    return inactive_list

def KillServers(servers):
    print("Shutting down servers")
    for i, server in enumerate(servers):
        subprocess.Popen.kill(server)

def LoadClients(units, server_list):
    #dir_path = os.path.dirname(os.path.realpath(__file__))
    clients = list()
    for i, unit in enumerate(units):
        print(i, unit)
        ip = dict_address_mapping[str(unit)][0]
        port = dict_address_mapping[str(unit)][1]
        print(ip, port)
        vars()["Client%s" % unit] = client.BlueVaryServiceClient(server_ip=ip, server_port=port)
        clients.append(vars()["Client%s" % unit])
    return clients

def get_data(client_list, t_0):
    """
    A function that sends the respective data pull request via the SiLA2 clients to the SiLA2 servers of the respective modules. 
    """

    # To-do: Rearrange the outputfile to reduce the number of loops.
    # To-do: Not fail-safe yet. Make sure that this function still works, once a module is excluded. The data must still be recorded if one unit fails.
    data = list()
    starttime = str(datetime.datetime.now())
    timestamp=time.time()
    t_0 = t_0
    curr_time = (timestamp - t_0)/(60*60)

    data.append(starttime)
    data.append(timestamp)
    data.append(curr_time)
    print(data)
    for i, unit in enumerate(reactors):
        data.append(unit.SensorServicer_GetResults().CO2.value)
    print('CO2: ', data[-i-1:])
    for i, unit in enumerate(reactors):
        data.append(unit.SensorServicer_GetResults().O2.value)
    print('O2: ', data[-i - 1:])
    for i, unit in enumerate(reactors):
        data.append(unit.SensorServicer_GetResults().Pressure.value)
    print('P: ', data[-i - 1:])
    for i, unit in enumerate(reactors):
        data.append(unit.SensorServicer_GetHumidity().Humidity.value)
    print('Hum.: ', data[-i - 1:])
    for i, unit in enumerate(reactors):
        data.append(unit.SensorServicer_GetHumidity().Temperature.value)
    print('Temp.: ', data[-i - 1:])
    for i, unit in enumerate(reactors):
        data.append(unit.SensorServicer_GetHumidity().AbsoluteHumidity.value)
    print('Abs. Hum.: ', data[-i - 1:])
    return data


# TODO: get away from csv and us a DB. real-time plotting of the data should be possible.
# Constantly reading csv files is heavy on the processor and not very elegant
def create_csv(units):
    """
    This function generates the .csv file in which the BlueVary data will be stored.
    The function "append_data_csv" fills this file with information.
    """
    file_title = "Data/%s.csv" % timestamp()

    first_row = ['Time', 'Epoch time [s]', 'Time [h]']
    reactors = list()
    for i, unit in enumerate(units):
        print(i+1)
        reactors.append("R{}".format(unit))
    #reactors = [ 'R1', 'R2', 'R3', 'R4']
    data_types = ['CO2 [%]', 'O2 [%]', 'Pressure [bar]', 'Humidity [%]', 'abs. Humidity [vol.-%]', 'Temperature [°C]']

    # create a list with the stuff to write in the first row
    for d_types in data_types:
        for r in reactors:
            first_row.append(r+' '+ d_types)

    # actual writing of stuff
    with open(file_title, mode='w', newline='') as output_file:
        output_writer = csv.writer(output_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        output_writer.writerow(first_row)
    print("File created in: %s\\Data\\%s" % (os.path.dirname(os.path.realpath(__file__)), file_title))
    return file_title

def append_data_csv(file_title, data):
    """
    Appends the most current data from "get_data" to the .csv log-file
    """
    with open((file_title), mode='a', newline='') as output_file:
        output_writer = csv.writer(output_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        output_writer.writerow(data)
        
def get_file_size(file_title):        
    """
    Calculates the file size of the log-file in bytes.
    """
    statinfo = os.stat(file_title)
    return statinfo.st_size
