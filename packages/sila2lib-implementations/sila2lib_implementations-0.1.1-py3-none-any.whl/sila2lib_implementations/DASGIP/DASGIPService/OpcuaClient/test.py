#unit_number = '1'
#vars()["unit_%s"%unit_number] = 123
#print(unit_1)

#unit_ID = ()
"""
import asyncio
import time

async def myTask(number):
    time.sleep(1)
    print("Processing Task")
    return number*2

#async def myTaskGenerator():
#    for i in range(5):
#        asyncio.ensure_future(myTask())
#    pending = asyncio.Task.all_tasks()
#    print(pending)

async def main(coros):
    for futures in asyncio.as_completed(coros):
        print(await futures)

coros = [myTask(1) for i in range(5)]

loop=asyncio.get_event_loop()
loop.run_until_complete(main(coros))
print("Completed All tasks")
loop.close()
"""
from itertools import combinations 

#allowed_get=['F.PV', 'F.SP', 'F.SPA', 'F.SPM', 'F.SPE', 'F.SPR'], 
#allowed_PVs = ['PV'] 
allowedSetters = ['SP', 'SPA', 'SPM', 'SPE', 'SPR', 'Mode']
MeasuredFlowsAndConcentrations= ['F', 'FAir', 'FO2', 'FN2', 'FCO2', 'XO2', 'XCO2']
LogicFlowsAndConcentrations = ['F', 'XCO2', 'XO2']
AllFlowsConcentrationsVolumetrics = ['F', 'FAir', 'XO2', 'XCO2', 'FO2', 'FN2', 'FCO2', 'V', 'VAir', 'VCO2', 'VO2', 'VN2' ]

allowed_get = ['PV', 'SP', 'Access', 'Cmd', 'GassingMode', 'State']
for i,cmd in enumerate(AllFlowsConcentrationsVolumetrics):
    tmp = ['%s.PV'%(cmd)]
    allowed_get.extend(tmp)

for i,cmd in enumerate(MeasuredFlowsAndConcentrations):
    tmp = ['%sSetpointSelect'%(cmd)]
    allowed_get.extend(tmp)
    for j,setter in enumerate(allowedSetters):
        tmp = ['%s.%s'%(cmd,setter)]
        allowed_get.extend(tmp)
for i,cmd in enumerate(LogicFlowsAndConcentrations):
    tmp = ['%s.SPL'%(cmd)]
    allowed_get.extend(tmp)
