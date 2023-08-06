import os
import sys
sys.path.append('./BlueVaryService')
import time
import BlueVaryService.BlueVary_Library as lib

Start_time = time.localtime(time.time())
t_0 = time.time()
dir_path = os.path.dirname(os.path.realpath(__file__))
lib.timestamp()

units = lib.InputUnits()
calibration = lib.InputCalibration()
interval = lib.InputInterval()
file_title = lib.create_csv(units)

#Start servers
server_list = lib.StartServers(units)
time.sleep(2)
inactive_list = lib.ServerStatus(server_list)
print("Servers on server_list: %s" %server_list)
print("Servers on inactive_list: %s" %inactive_list)
print("Servers on units: %s" %units)

#def del element:
#TODO: Implement del function
for i in inactive_list:
    del(units[units.index(i)])
print(units)
#def restart(inactive_list, units):
### TODO: ask indefinetly wether servers should be restarted
### keep returning the inactive_list
###TODO: Invoke del function and delete if user choses to continue


### TODO: Delete inactive servers from server list or/AND implement try:/except: statements in GetResults!
client_list = lib.LoadClients(units, server_list)
time.sleep(5)

try:
    # TODO: Implement a request to the respective servers,
    # wether they are all warmed up and ready to use. Only proceed if ready!
    # Validate implementation
    if calibration == True:
        lib.calibrate(units)
    else:
        pass

    while True:
        data = lib.get_data(client_list, t_0)
        lib.append_data_csv(file_title = file_title, data = data)
        print('Measuring every %s seconds. Current file size:%s KB'%(interval, lib.get_file_size(file_title)/1024))
        print("Time:%.4s"%(time.time()-t_0))
        time.sleep(interval - (time.time() % interval))
except:
    print("Exception occurred")
    lib.KillServers(server_list)
finally:
    lib.KillServers(server_list)