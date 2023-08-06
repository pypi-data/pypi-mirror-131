import sila2lib_implementations.BioREACTOR48.BioREACTOR48Service.BioREACTOR48Service_client as client
import csv
import time
reactor = client.BioREACTOR48ServiceClient(server_ip="127.0.0.1", server_port=50003)

Implemented_Features = reactor.Get_ImplementedFeatures()
print(Implemented_Features)
#print('First feature:', Implemented_Features[0].FeatureIdentifier.value)
#print('Second feature:', Implemented_Features[1].FeatureIdentifier.value)
#print('Third feature:', Implemented_Features[2].FeatureIdentifier.value)
#a = reactor.Get_FeatureDefinition(Implemented_Features[0].FeatureIdentifier.value)
#print('Third feature xml-file:', a)
print(reactor.MotorServicer_StartStirrer())
print(reactor.MotorServicer_StopStirrer())
print(reactor.MotorServicer_StartStirrer())

stop = reactor.MotorServicer_StopStirrer()

start = reactor.MotorServicer_StartStirrer()
setPower = reactor.MotorServicer_SetPower(100)
setRpm = reactor.MotorServicer_SetRPM(3000)

for i in range(0, 1000, 1):
    print(f'Iteration: {i}')
    if i % 100 == 0:
        print('Resetting ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        stop = reactor.MotorServicer_StopStirrer()
        start = reactor.MotorServicer_StartStirrer()
        setPower = reactor.MotorServicer_SetPower(100)
        setRpm = reactor.MotorServicer_SetRPM(3000)
    else:
        stop.CurrentStatus.value = 'waiting'
        start.CurrentStatus.value = 'waiting'
        setPower.CurrentStatus.value = 'waiting'
        setRpm.CurrentStatus.value = 'waiting'

    rpm = reactor.MotorServicer_GetRPM()
    power = reactor.MotorServicer_GetPower()
    deviceStatus = reactor.DeviceServicer_GetDeviceStatus()
    reactorStatus = reactor.DeviceServicer_GetReactorStatus()
    barNumber = reactor.Get_DeviceServicer_BarNumber()
    barReactors = reactor.Get_DeviceServicer_BarReactors()
    totalReactors = reactor.Get_DeviceServicer_TotalReactors()
    with open('test.csv', 'a', newline='') as csvfile:
        fieldnames = ['start',
                      'stop',
                      'setPower',
                      'setRpm',
                      'rpm',
                      'power',
                      'deviceStatus.Status',
                      'deviceStatus.Version',
                      'deviceStatus.Mode',
                      'deviceStatus.BarConnection',
                      'deviceStatus.Address',
                      'reactorStatus',
                      'barNumber',
                      'barReactors',
                      'totalReactors'
                      ]
        writer = csv.DictWriter(csvfile, delimiter=' ', fieldnames=fieldnames)
        if i==0:
            writer.writeheader()
        writer.writerow({
            'start': start.CurrentStatus.value,
            'stop': stop.CurrentStatus.value,
            'setPower': setPower.CurrentStatus.value,
            'setRpm': setRpm.CurrentStatus.value,
            'rpm': rpm.CurrentRPM.value,
            'power': power.CurrentPower.value,
            'deviceStatus.Status':deviceStatus.Status.value,
            'deviceStatus.Version': deviceStatus.Version.value,
            'deviceStatus.Mode': deviceStatus.Mode.value,
            'deviceStatus.BarConnection': deviceStatus.BarConnection.value,
            'deviceStatus.Address': deviceStatus.Address.value,
            'reactorStatus': [reactorStatus.ReactorStatus[i].value for i in range(0, 47, 1)],
            'barNumber': barNumber.BarNumber.value,
            'barReactors': barReactors.BarReactors.value,
            'totalReactors': totalReactors.TotalReactors.value
        })


#i = 0
#while i <= 3:
#    print(reactor.MotorServicer_SetRPM(3000))
#    print(reactor.MotorServicer_GetRPM())
#    print(reactor.MotorServicer_SetPower(100))
 #   print(reactor.MotorServicer_GetPower())
#    print(reactor.DeviceServicer_GetDeviceStatus())  # .BarConnection)
#    print(reactor.DeviceServicer_GetReactorStatus())  # .ReactorStatus)
#    print(reactor.Get_DeviceServicer_BarNumber())
#    print(reactor.Get_DeviceServicer_BarReactors())
#    print(reactor.Get_DeviceServicer_TotalReactors())
#    i = i + 1
#    time.sleep(1)
