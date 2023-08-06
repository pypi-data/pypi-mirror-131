# Insert this command into the respective implementation of the SiLA server at ....Servicer_Real.py

from .client_DASGIP_UA import clientDASGIP as opc_client
import numpy as np

#Initialize all units that are specified in the number of units, number_units
number_units = 4
reactors = []
for i in np.arange(1,number_units+1,1):
    vars()["unit_ID%s"%i]=i
    print("Initializing: Unit%s..."%vars()["unit_ID%s"%i])
    vars()["reactor_%s"%i] = opc_client(unit_ID = vars()["unit_ID%s"%i])
    print(vars()["reactor_%s"%i],"Initialized")
    reactors.append(vars()["reactor_%s"%i])

def connectUnits(reactors): 
    for i, reactor in enumerate(reactors):
        print("___________________________Starting Unit%s___________________________"%(i+1))
        reactor.run()
        print("___________________________Started Unit%s___________________________"%(i+1))

def disconnectUnits(reactors): 
    for i, reactor in enumerate(reactors):
        print("___________________________Disconnecting Unit%s___________________________"%(i+1))
        reactor.close()
        print("___________________________Disconnected Unit%s___________________________"%(i+1))

connectUnits(reactors)
#print(reactor_1.unit.DO.setter.PV)
#a = reactor_1.unit.DO.setter.PV
#print(reactor_1.unit.PumpA.actuator.Calibration)
print(reactor_1.unit.Device.service.Available)
#a = reactor_1.unit.PumpA.actuator.Calibration
#print(a)
#print(a.get_data_type())
#print(a.get_value())
disconnectUnits(reactors)
#print(a)
