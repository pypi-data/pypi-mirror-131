import time
import numpy as np
import DASGIP_Service_client as client

"""
Test-program for DASGIP interface
Every command possible should be executed once to check for bugs in the implementation. 
In order to avoid an active change of values when invoking set-commands, set-commands 
will be executed after the respective get-command, using the current value that was recieved 
by the get-command. Each feature will have its own test routine that will be invoked in THIS 
file. 

Each test file should include a simple get/set command for each function. Logic functions
could be used, but aren't totally necessary, e.g is the "low" value smaller than the "high" 
value. 
"""

var = client.DASGIP_ServiceClient()



#var.run()
#print(var.server_version)

#var.PHServicer_SetSP(1,1)

#a = var.PumpAServicer_GetActuatorCalibration(1) #.PumpAServicer#._GetActuatorCalibration(1)#.CurrentActuatorCalibration.value

### Pump_Info
PV_1_A = var.PumpAServicer_GetPV(1)
PVInt_1_A = var.PumpAServicer_GetPVInt(1)
SP_1_A = var.PumpAServicer_GetSP(1)
SPM_1_A = var.PumpAServicer_GetSPM(1)
SPE_1_A = var.PumpAServicer_GetSPE(1)
SPA_1_A = var.PumpAServicer_GetSPA(1)
SPR_1_A = var.PumpAServicer_GetSPR(1)

PV_1_B = var.PumpAServicer_GetPV(1)
PVInt_1_B = var.PumpAServicer_GetPVInt(1)
SP_1_B = var.PumpAServicer_GetSP(1)
SPM_1_B = var.PumpAServicer_GetSPM(1)
SPE_1_B = var.PumpAServicer_GetSPE(1)
SPA_1_B = var.PumpAServicer_GetSPA(1)
SPR_1_B = var.PumpAServicer_GetSPR(1)

PV_1_C = var.PumpAServicer_GetPV(1)
PVInt_1_C = var.PumpAServicer_GetPVInt(1)
SP_1_C = var.PumpAServicer_GetSP(1)
SPM_1_C = var.PumpAServicer_GetSPM(1)
SPE_1_C = var.PumpAServicer_GetSPE(1)
SPA_1_C = var.PumpAServicer_GetSPA(1)
SPR_1_C = var.PumpAServicer_GetSPR(1)

### REACTOR Info
VInitial_1 = var.ReactorServicer_GetVInitial(1)
VLiquid_1 = var.ReactorServicer_GetVLiquid(1)

### Temperature Info
T_1 = var.TemperatureServicer_GetPV(1)

### Get General Info
#print(PV_1_A, PVInt_1_A, SP_1_A, SPM_1_A, SPA_1_A, SPE_1_A, SPR_1_A, SP_1_B, SPM_1_B, SPA_1_B, SPE_1_B, SPR_1_B, VInitial_1, VLiquid_1)
print(PV_1_A, PVInt_1_A, SP_1_A, PV_1_B, PVInt_1_B, SP_1_B, PV_1_C, PVInt_1_C, VInitial_1, SP_1_C, VLiquid_1, T_1)
#var.GetRuntimeClock()

