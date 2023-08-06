class TestCalibrationServicer:
""" Test all CalibrationServicer Get functions """
def test___init__(self):
    response = self.sila_client.CalibrationServicer___init__()
    assert response is not None
    assert isinstance(response)

def test__inject_implementation(self):
    response = self.sila_client.CalibrationServicer__inject_implementation()
    assert response is not None
    assert isinstance(response)

def test_switch_to_simulation_mode(self):
    response = self.sila_client.CalibrationServicer_switch_to_simulation_mode()
    assert response is not None
    assert isinstance(response)

def test_switch_to_real_mode(self):
    response = self.sila_client.CalibrationServicer_switch_to_real_mode()
    assert response is not None
    assert isinstance(response)

def test_StartCalibrationTime(self):
    response = self.sila_client.CalibrationServicer_StartCalibrationTime()
    assert response is not None
    assert isinstance(response)

def test_StartCalibrationVolume(self):
    response = self.sila_client.CalibrationServicer_StartCalibrationVolume()
    assert response is not None
    assert isinstance(response)

def test_GetDefaultFlowRate(self):
    response = self.sila_client.CalibrationServicer_GetDefaultFlowRate()
    assert response is not None
    assert isinstance(response)

def test_GetCalibratedFlowRate(self):
    response = self.sila_client.CalibrationServicer_GetCalibratedFlowRate()
    assert response is not None
    assert isinstance(response)

def test_SetCalibratedFlowRate(self):
    response = self.sila_client.CalibrationServicer_SetCalibratedFlowRate()
    assert response is not None
    assert isinstance(response)

def test_SetCalibrationTargetVolume(self):
    response = self.sila_client.CalibrationServicer_SetCalibrationTargetVolume()
    assert response is not None
    assert isinstance(response)

def test_SetCalibrationTargetTime(self):
    response = self.sila_client.CalibrationServicer_SetCalibrationTargetTime()
    assert response is not None
    assert isinstance(response)

def test_SetActualVolume(self):
    response = self.sila_client.CalibrationServicer_SetActualVolume()
    assert response is not None
    assert isinstance(response)

def test_GetTargetVolume(self):
    response = self.sila_client.CalibrationServicer_GetTargetVolume()
    assert response is not None
    assert isinstance(response)

def test_SetActualTime(self):
    response = self.sila_client.CalibrationServicer_SetActualTime()
    assert response is not None
    assert isinstance(response)

def test_GetTargetTime(self):
    response = self.sila_client.CalibrationServicer_GetTargetTime()
    assert response is not None
    assert isinstance(response)

def test_SetDirectionCalibration(self):
    response = self.sila_client.CalibrationServicer_SetDirectionCalibration()
    assert response is not None
    assert isinstance(response)

def test_GetDirectionCalibration(self):
    response = self.sila_client.CalibrationServicer_GetDirectionCalibration()
    assert response is not None
    assert isinstance(response)

def test_GetLastCalibrationTime(self):
    response = self.sila_client.CalibrationServicer_GetLastCalibrationTime()
    assert response is not None
    assert isinstance(response)

class TestDeviceServicer:
""" Test all DeviceServicer Get functions """
def test___init__(self):
    response = self.sila_client.DeviceServicer___init__()
    assert response is not None
    assert isinstance(response)

def test__inject_implementation(self):
    response = self.sila_client.DeviceServicer__inject_implementation()
    assert response is not None
    assert isinstance(response)

def test_switch_to_simulation_mode(self):
    response = self.sila_client.DeviceServicer_switch_to_simulation_mode()
    assert response is not None
    assert isinstance(response)

def test_switch_to_real_mode(self):
    response = self.sila_client.DeviceServicer_switch_to_real_mode()
    assert response is not None
    assert isinstance(response)

def test_GetLog(self):
    response = self.sila_client.DeviceServicer_GetLog()
    assert response is not None
    assert isinstance(response)

def test_GetLog_Info(self):
    response = self.sila_client.DeviceServicer_GetLog_Info()
    assert response is not None
    assert isinstance(response)

def test_GetLog_Result(self):
    response = self.sila_client.DeviceServicer_GetLog_Result()
    assert response is not None
    assert isinstance(response)

def test_SetPumpAddress(self):
    response = self.sila_client.DeviceServicer_SetPumpAddress()
    assert response is not None
    assert isinstance(response)

def test_GetPumpStatus(self):
    response = self.sila_client.DeviceServicer_GetPumpStatus()
    assert response is not None
    assert isinstance(response)

def test_GetVersionType(self):
    response = self.sila_client.DeviceServicer_GetVersionType()
    assert response is not None
    assert isinstance(response)

def test_GetVersionSoftware(self):
    response = self.sila_client.DeviceServicer_GetVersionSoftware()
    assert response is not None
    assert isinstance(response)

def test_GetPumpID(self):
    response = self.sila_client.DeviceServicer_GetPumpID()
    assert response is not None
    assert isinstance(response)

def test_SetPumpID(self):
    response = self.sila_client.DeviceServicer_SetPumpID()
    assert response is not None
    assert isinstance(response)

def test_ResetToDefault(self):
    response = self.sila_client.DeviceServicer_ResetToDefault()
    assert response is not None
    assert isinstance(response)

def test_GetTotalVolume(self):
    response = self.sila_client.DeviceServicer_GetTotalVolume()
    assert response is not None
    assert isinstance(response)

def test_ResetTotalVolume(self):
    response = self.sila_client.DeviceServicer_ResetTotalVolume()
    assert response is not None
    assert isinstance(response)

def test_UnlockControlPanel(self):
    response = self.sila_client.DeviceServicer_UnlockControlPanel()
    assert response is not None
    assert isinstance(response)

def test_LockControlPanel(self):
    response = self.sila_client.DeviceServicer_LockControlPanel()
    assert response is not None
    assert isinstance(response)

def test_SetDisplayNumbers(self):
    response = self.sila_client.DeviceServicer_SetDisplayNumbers()
    assert response is not None
    assert isinstance(response)

def test_SetDisplayLetters(self):
    response = self.sila_client.DeviceServicer_SetDisplayLetters()
    assert response is not None
    assert isinstance(response)

def test_SetCommunicationPort(self):
    response = self.sila_client.DeviceServicer_SetCommunicationPort()
    assert response is not None
    assert isinstance(response)

def test_ConnectDevice(self):
    response = self.sila_client.DeviceServicer_ConnectDevice()
    assert response is not None
    assert isinstance(response)

def test_ResetOverload(self):
    response = self.sila_client.DeviceServicer_ResetOverload()
    assert response is not None
    assert isinstance(response)

def test_Subscribe_CurrentStatus(self):
    response = self.sila_client.DeviceServicer_Subscribe_CurrentStatus()
    assert response is not None
    assert isinstance(response)

def test_Get_PortName(self):
    response = self.sila_client.DeviceServicer_Get_PortName()
    assert response is not None
    assert isinstance(response)

def test_Get_BaudRate(self):
    response = self.sila_client.DeviceServicer_Get_BaudRate()
    assert response is not None
    assert isinstance(response)

def test_Get_Parity(self):
    response = self.sila_client.DeviceServicer_Get_Parity()
    assert response is not None
    assert isinstance(response)

def test_Get_StopBits(self):
    response = self.sila_client.DeviceServicer_Get_StopBits()
    assert response is not None
    assert isinstance(response)

def test_Get_Timeout(self):
    response = self.sila_client.DeviceServicer_Get_Timeout()
    assert response is not None
    assert isinstance(response)

class TestDriveControlServicer:
""" Test all DriveControlServicer Get functions """
def test___init__(self):
    response = self.sila_client.DriveControlServicer___init__()
    assert response is not None
    assert isinstance(response)

def test__inject_implementation(self):
    response = self.sila_client.DriveControlServicer__inject_implementation()
    assert response is not None
    assert isinstance(response)

def test_switch_to_simulation_mode(self):
    response = self.sila_client.DriveControlServicer_switch_to_simulation_mode()
    assert response is not None
    assert isinstance(response)

def test_switch_to_real_mode(self):
    response = self.sila_client.DriveControlServicer_switch_to_real_mode()
    assert response is not None
    assert isinstance(response)

def test_StartPump(self):
    response = self.sila_client.DriveControlServicer_StartPump()
    assert response is not None
    assert isinstance(response)

def test_StopPump(self):
    response = self.sila_client.DriveControlServicer_StopPump()
    assert response is not None
    assert isinstance(response)

def test_GetPumpDirection(self):
    response = self.sila_client.DriveControlServicer_GetPumpDirection()
    assert response is not None
    assert isinstance(response)

def test_SetDirectionClockwise(self):
    response = self.sila_client.DriveControlServicer_SetDirectionClockwise()
    assert response is not None
    assert isinstance(response)

def test_SetDirectionCounterClockwise(self):
    response = self.sila_client.DriveControlServicer_SetDirectionCounterClockwise()
    assert response is not None
    assert isinstance(response)

class TestParameterControlServicer:
""" Test all ParameterControlServicer Get functions """
def test___init__(self):
    response = self.sila_client.ParameterControlServicer___init__()
    assert response is not None
    assert isinstance(response)

def test__inject_implementation(self):
    response = self.sila_client.ParameterControlServicer__inject_implementation()
    assert response is not None
    assert isinstance(response)

def test_switch_to_simulation_mode(self):
    response = self.sila_client.ParameterControlServicer_switch_to_simulation_mode()
    assert response is not None
    assert isinstance(response)

def test_switch_to_real_mode(self):
    response = self.sila_client.ParameterControlServicer_switch_to_real_mode()
    assert response is not None
    assert isinstance(response)

def test_SetRPMMode(self):
    response = self.sila_client.ParameterControlServicer_SetRPMMode()
    assert response is not None
    assert isinstance(response)

def test_SetFlowRateMode(self):
    response = self.sila_client.ParameterControlServicer_SetFlowRateMode()
    assert response is not None
    assert isinstance(response)

def test_SetDispenseVolumeMode(self):
    response = self.sila_client.ParameterControlServicer_SetDispenseVolumeMode()
    assert response is not None
    assert isinstance(response)

def test_SetDispenseTimeMode(self):
    response = self.sila_client.ParameterControlServicer_SetDispenseTimeMode()
    assert response is not None
    assert isinstance(response)

def test_SetPauseTimeMode(self):
    response = self.sila_client.ParameterControlServicer_SetPauseTimeMode()
    assert response is not None
    assert isinstance(response)

def test_SetDispenseTimePauseTimeMode(self):
    response = self.sila_client.ParameterControlServicer_SetDispenseTimePauseTimeMode()
    assert response is not None
    assert isinstance(response)

def test_SetDispenseVolumePauseTimeMode(self):
    response = self.sila_client.ParameterControlServicer_SetDispenseVolumePauseTimeMode()
    assert response is not None
    assert isinstance(response)

def test_GetDispenseVolume(self):
    response = self.sila_client.ParameterControlServicer_GetDispenseVolume()
    assert response is not None
    assert isinstance(response)

def test_SetDispenseVolume(self):
    response = self.sila_client.ParameterControlServicer_SetDispenseVolume()
    assert response is not None
    assert isinstance(response)

def test_SetDispenseVolumeModeVolume(self):
    response = self.sila_client.ParameterControlServicer_SetDispenseVolumeModeVolume()
    assert response is not None
    assert isinstance(response)

def test_GetFlowRate(self):
    response = self.sila_client.ParameterControlServicer_GetFlowRate()
    assert response is not None
    assert isinstance(response)

def test_SetFlowRate(self):
    response = self.sila_client.ParameterControlServicer_SetFlowRate()
    assert response is not None
    assert isinstance(response)

def test_GetRPM(self):
    response = self.sila_client.ParameterControlServicer_GetRPM()
    assert response is not None
    assert isinstance(response)

def test_SetRPM(self):
    response = self.sila_client.ParameterControlServicer_SetRPM()
    assert response is not None
    assert isinstance(response)

def test_GetPauseTime(self):
    response = self.sila_client.ParameterControlServicer_GetPauseTime()
    assert response is not None
    assert isinstance(response)

def test_SetPauseTime(self):
    response = self.sila_client.ParameterControlServicer_SetPauseTime()
    assert response is not None
    assert isinstance(response)

def test_GetDispenseCycles(self):
    response = self.sila_client.ParameterControlServicer_GetDispenseCycles()
    assert response is not None
    assert isinstance(response)

def test_SetDispenseCycles(self):
    response = self.sila_client.ParameterControlServicer_SetDispenseCycles()
    assert response is not None
    assert isinstance(response)

def test_GetDispenseTime(self):
    response = self.sila_client.ParameterControlServicer_GetDispenseTime()
    assert response is not None
    assert isinstance(response)

def test_SetDispenseTime(self):
    response = self.sila_client.ParameterControlServicer_SetDispenseTime()
    assert response is not None
    assert isinstance(response)

def test_GetRollerSteps(self):
    response = self.sila_client.ParameterControlServicer_GetRollerSteps()
    assert response is not None
    assert isinstance(response)

def test_SetRollerSteps(self):
    response = self.sila_client.ParameterControlServicer_SetRollerSteps()
    assert response is not None
    assert isinstance(response)

def test_GetRollerStepVolume(self):
    response = self.sila_client.ParameterControlServicer_GetRollerStepVolume()
    assert response is not None
    assert isinstance(response)

def test_SetRollerStepVolume(self):
    response = self.sila_client.ParameterControlServicer_SetRollerStepVolume()
    assert response is not None
    assert isinstance(response)

def test_ResetRollerStepVolume(self):
    response = self.sila_client.ParameterControlServicer_ResetRollerStepVolume()
    assert response is not None
    assert isinstance(response)

def test_GetRollerBackSteps(self):
    response = self.sila_client.ParameterControlServicer_GetRollerBackSteps()
    assert response is not None
    assert isinstance(response)

def test_SetRollerBackSteps(self):
    response = self.sila_client.ParameterControlServicer_SetRollerBackSteps()
    assert response is not None
    assert isinstance(response)

def test_SaveApplicationParameters(self):
    response = self.sila_client.ParameterControlServicer_SaveApplicationParameters()
    assert response is not None
    assert isinstance(response)

def test_GetTubingDiameter(self):
    response = self.sila_client.ParameterControlServicer_GetTubingDiameter()
    assert response is not None
    assert isinstance(response)

def test_SetTubingDiameter(self):
    response = self.sila_client.ParameterControlServicer_SetTubingDiameter()
    assert response is not None
    assert isinstance(response)

