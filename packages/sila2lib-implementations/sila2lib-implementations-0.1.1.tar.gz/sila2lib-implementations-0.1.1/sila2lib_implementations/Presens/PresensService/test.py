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

# CalibrationService
## Oxygen sensor
CalLow = presens.CalibrationService_GetO2CalLow()
print(CalLow)
tmp=[]
for i in range(0,6,1):
    print(CalLow.CurrentO2CalLow[i].value)
    tmp.append(CalLow.CurrentO2CalLow[i].value)
print(presens.CalibrationService_SetO2CalLow(tmp))

CalHigh = presens.CalibrationService_GetO2CalHigh()
print(CalHigh)
tmp=[]
for i in range(0,6,1):
    print(CalHigh.CurrentO2CalHigh[i].value)
    tmp.append(CalHigh.CurrentO2CalHigh[i].value)
print(presens.CalibrationService_SetO2CalHigh(tmp))

CalTemp = presens.CalibrationService_GetO2CalTemp()
print(CalTemp)
tmp=[]
for i in range(0,6,1):
    print(CalTemp.CurrentO2CalTemp[i].value)
    tmp.append(CalTemp.CurrentO2CalTemp[i].value)
print(presens.CalibrationService_SetO2CalTemp(tmp))

# CalibrationService
## PH sensor
PHImax = presens.CalibrationService_GetPHImax()
print(PHImax)
tmp=[]
for i in range(0,6,1):
    print(PHImax.CurrentPHImax[i].value)
    tmp.append(PHImax.CurrentPHImax[i].value)
print(presens.CalibrationService_SetPHImax(tmp))

PHImin = presens.CalibrationService_GetPHImin()
print(PHImin)
tmp=[]
for i in range(0,6,1):
    print(PHImin.CurrentPHImin[i].value)
    tmp.append(PHImin.CurrentPHImin[i].value)
print(presens.CalibrationService_SetPHImin(tmp))

PHpH0 = presens.CalibrationService_GetPHpH0()
print(PHpH0)
tmp=[]
for i in range(0,6,1):
    print(PHpH0.CurrentPHpH0[i].value)
    tmp.append(PHpH0.CurrentPHpH0[i].value)
print(presens.CalibrationService_SetPHpH0(tmp))

PHdpH = presens.CalibrationService_GetPHdpH()
print(PHdpH)
tmp=[]
for i in range(0,6,1):
    print(PHdpH.CurrentPHdpH[i].value)
    tmp.append(PHdpH.CurrentPHdpH[i].value)
print(presens.CalibrationService_SetPHdpH(tmp))

PHCalTemp = presens.CalibrationService_GetPHCalTemp()
print(PHCalTemp)
tmp=[]
for i in range(0,6,1):
    print(PHCalTemp.CurrentPHCalTemp[i].value)
    tmp.append(PHCalTemp.CurrentPHCalTemp[i].value)
print(presens.CalibrationService_SetPHCalTemp(tmp))
