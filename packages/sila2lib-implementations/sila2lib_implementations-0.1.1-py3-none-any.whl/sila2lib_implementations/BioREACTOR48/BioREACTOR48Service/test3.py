import BioREACTOR48Service_observable_client

client = BioREACTOR48Service_observable_client.BioREACTOR48ServiceClient(server_ip='127.0.0.1', server_port=50001)

# ImplementedFeatures = client.Get_ImplementedFeatures()
# print(ImplementedFeatures)
print(client.Get_DeviceServicer_TotalReactors())
#print(client.DeviceServicer_GetReactorStatus())
#client.DeviceServicer_GetReactorStatus()
#print(client.MotorServicer_GetPower())


print(f'SERVER-LOG-LINE: {client.Subscribe_DeviceServicer_CurrentStatus().CurrentStatus.value}')
#print(client.DeviceServicer_GetLog())

















"""
import time
import logging
import sys
mylog = logging.getLogger()
mylog.setLevel(logging.DEBUG)


lh = logging.FileHandler(filename='./test_log')
lh.setLevel(logging.DEBUG)

mylog.addHandler(lh)
while True:
    mylog.warning(f'argh: {time.time()}')
    mylog.info('info')
    time.sleep(2)
"""
# OR this one:
# https://code.activestate.com/recipes/436477-filetailpy/
#(Check out the Git repo linked in the comments by Ronald Kaiser: https://github.com/cathoderay/filetail)

# from pythontail import tail
# tail.run(['dir/log/file.log'])
