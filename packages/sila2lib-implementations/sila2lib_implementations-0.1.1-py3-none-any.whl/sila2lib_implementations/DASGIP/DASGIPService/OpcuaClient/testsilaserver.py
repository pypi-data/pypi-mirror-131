# Insert this command into the respective implementation of the SiLA server at ....Servicer_Real.py
from .client_DASGIP import clientDASGIP as opc_client
import asyncio
import numpy as np

number_units = 4
reactors = []
#nitialize all units that are specified in the number of units, number_units
for i in np.arange(1,number_units+1,1):
    vars()["unit_ID%s"%i]=i
    print("Initializing: Unit%s..."%vars()["unit_ID%s"%i])
    vars()["reactor_%s"%i] = opc_client(unit_ID = vars()["unit_ID%s"%i])
    print(vars()["reactor_%s"%i],"Initialized")
    reactors.append(vars()["reactor_%s"%i])

async def myrun(): 
    for i, reactor in enumerate(reactors):
        print("___________________________Starting Unit%s___________________________"%(i+1))
        await reactor.run()
        print("___________________________Started Unit%s___________________________"%(i+1))

async def disconnect(): 
    for i, reactor in enumerate(reactors):
        print("___________________________Disconnecting Unit%s___________________________"%(i+1))
        await reactor.disconnect()
        print("___________________________Disconnected Unit%s___________________________"%(i+1))


async def command():
    a = reactor_3.unit.pH.setter.PV
    
    return a

async def get_value(a):
#    a = await command()
#    print("HALLO%s"%a)
    b = await a.get_value()
#    print("HEYHOO%s"%b)
    return b


async def myquery():
    await myrun()
    a=await command()
    print("Im a!:%s"%a)
    b=await get_value(a)
    print("Im b!:%s"%b)

    await disconnect()
    #a = reactor_3.unit.pH.setter.PV
    #print("HEEYYYY %s"%a)

    #return 
    #await a.get_



#async def close():
 #   await get_value()
 #   await disconnect()

#async def myquery2():
#    await myquery()
#    
#    print("HEEYYYY myquery2 %s"%a)
#    #await a.get_value()
#    #return 
#   #await a.get_


async def main():
    tasks = []
    #tasks.append(asyncio.ensure_future(myrun()))
    tasks.append(asyncio.ensure_future(myquery()))
#    tasks.append(asyncio.ensure_future(close()))
    await asyncio.gather(*tasks)

loop = asyncio.get_event_loop()

try:
    loop.run_until_complete(main())
finally:
    loop.close()
