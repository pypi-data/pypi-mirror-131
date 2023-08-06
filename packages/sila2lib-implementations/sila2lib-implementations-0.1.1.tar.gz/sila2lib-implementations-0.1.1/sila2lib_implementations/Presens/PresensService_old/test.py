import sila2lib_implementations.Presens.PresensService.PresensService_client as client
import time
presens = client.PresensServiceClient(server_ip="127.0.0.1", server_port=50002)

# SensorProvider
## Oxygen sensor
print(presens.Get_ImplementedFeatures())
print(presens.Get_SensorProvider_BarSensors())
print(presens.Get_SensorProvider_TotalBars())
print(presens.Get_SensorProvider_TotalChannels())

print(presens.SensorProvider_GetSingleO2(24).CurrentO2)
print(presens.SensorProvider_GetSinglePH(2))

# SensorProvider
## PH sensor

# CalibrationServicer
## Oxygen sensor
CalLow = presens.CalibrationServicer_GetO2CalLow()
print(CalLow)
tmp=[]
for i in range(0,6,1):
    print(CalLow.CurrentO2CalLow[i].value)
    tmp.append(CalLow.CurrentO2CalLow[i].value)
print(presens.CalibrationServicer_SetO2CalLow(tmp))

CalHigh = presens.CalibrationServicer_GetO2CalHigh()
print(CalHigh)
tmp=[]
for i in range(0,6,1):
    print(CalHigh.CurrentO2CalHigh[i].value)
    tmp.append(CalHigh.CurrentO2CalHigh[i].value)
print(presens.CalibrationServicer_SetO2CalHigh(tmp))

CalTemp = presens.CalibrationServicer_GetO2CalTemp()
print(CalTemp)
tmp=[]
for i in range(0,6,1):
    print(CalTemp.CurrentO2CalTemp[i].value)
    tmp.append(CalTemp.CurrentO2CalTemp[i].value)
print(presens.CalibrationServicer_SetO2CalTemp(tmp))

# CalibrationServicer
## PH sensor
PHlmax = presens.CalibrationServicer_GetPHlmax()
print(PHlmax)
tmp=[]
for i in range(0,6,1):
    print(PHlmax.CurrentPHlmax[i].value)
    tmp.append(PHlmax.CurrentPHlmax[i].value)
print(presens.CalibrationServicer_SetPHlmax(tmp))

PHlmin = presens.CalibrationServicer_GetPHlmin()
print(PHlmin)
tmp=[]
for i in range(0,6,1):
    print(PHlmin.CurrentPHlmin[i].value)
    tmp.append(PHlmin.CurrentPHlmin[i].value)
print(presens.CalibrationServicer_SetPHlmin(tmp))

PHpH0 = presens.CalibrationServicer_GetPHpH0()
print(PHpH0)
tmp=[]
for i in range(0,6,1):
    print(PHpH0.CurrentPHpH0[i].value)
    tmp.append(PHpH0.CurrentPHpH0[i].value)
print(presens.CalibrationServicer_SetPHpH0(tmp))

PHdpH = presens.CalibrationServicer_GetPHdpH()
print(PHdpH)
tmp=[]
for i in range(0,6,1):
    print(PHdpH.CurrentPHdpH[i].value)
    tmp.append(PHdpH.CurrentPHdpH[i].value)
print(presens.CalibrationServicer_SetPHdpH(tmp))

PHCalTemp = presens.CalibrationServicer_GetPHCalTemp()
print(PHCalTemp)
tmp=[]
for i in range(0,6,1):
    print(PHCalTemp.CurrentPHCalTemp[i].value)
    tmp.append(PHCalTemp.CurrentPHCalTemp[i].value)
print(presens.CalibrationServicer_SetPHCalTemp(tmp))
