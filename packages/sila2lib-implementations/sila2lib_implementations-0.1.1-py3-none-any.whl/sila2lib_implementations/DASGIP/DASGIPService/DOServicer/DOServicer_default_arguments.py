# This file contains default values that are used for the implementations to supply them with 
#   working, albeit mostly useless arguments.
#   You can also use this file as an example to create your custom responses. Feel free to remove
#   Once you have replaced every occurrence of the defaults with more reasonable values.
#   Or you continue using this file, supplying good defaults..

# import the required packages
import sila2lib.framework.SiLAFramework_pb2 as silaFW_pb2
import sila2lib.framework.SiLABinaryTransfer_pb2 as silaBinary_pb2
from .gRPC import DOServicer_pb2 as pb2

# initialise the default dictionary so we can add keys. 
#   We need to do this separately/add keys separately, so we can access keys already defined e.g.
#   for the use in data type identifiers
default_dict = dict()


default_dict['GetPV_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetPV_Responses'] = {
    'CurrentPV': silaFW_pb2.Real(value=0.0)
}

default_dict['SetSPM_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0),
    'SPM': silaFW_pb2.Real(value=0.0)
}

default_dict['SetSPM_Responses'] = {
    'SPMSet': silaFW_pb2.Real(value=0.0)
}

default_dict['SetSPE_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0),
    'SPE': silaFW_pb2.Real(value=0.0)
}

default_dict['SetSPE_Responses'] = {
    'SPESet': silaFW_pb2.Real(value=0.0)
}

default_dict['GetSP_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetSP_Responses'] = {
    'CurrentSP': silaFW_pb2.Real(value=0.0)
}

default_dict['GetSPA_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetSPA_Responses'] = {
    'CurrentSPA': silaFW_pb2.Real(value=0.0)
}

default_dict['GetSPM_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetSPM_Responses'] = {
    'CurrentSPM': silaFW_pb2.Real(value=0.0)
}

default_dict['GetSPE_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetSPE_Responses'] = {
    'CurrentSPE': silaFW_pb2.Real(value=0.0)
}

default_dict['GetSPR_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetSPR_Responses'] = {
    'CurrentSPR': silaFW_pb2.Real(value=0.0)
}

default_dict['GetAccess_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetAccess_Responses'] = {
    'CurrentAccess': silaFW_pb2.Integer(value=0)
}

default_dict['SetCmd_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0),
    'Cmd': silaFW_pb2.Integer(value=0)
}

default_dict['SetCmd_Responses'] = {
    'CmdSet': silaFW_pb2.Integer(value=0)
}

default_dict['GetCmd_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetCmd_Responses'] = {
    'CurrentCmd': silaFW_pb2.Integer(value=0)
}

default_dict['SetMode_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0),
    'Mode': silaFW_pb2.Integer(value=0)
}

default_dict['SetMode_Responses'] = {
    'ModeSet': silaFW_pb2.Integer(value=0)
}

default_dict['GetMode_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetMode_Responses'] = {
    'CurrentMode': silaFW_pb2.Integer(value=0)
}

default_dict['SetSetpointSelect_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0),
    'SetpointSelect': silaFW_pb2.Integer(value=0)
}

default_dict['SetSetpointSelect_Responses'] = {
    'SetpointSelectSet': silaFW_pb2.Integer(value=0)
}

default_dict['GetSetpointSelect_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetSetpointSelect_Responses'] = {
    'CurrentSetpointSelect': silaFW_pb2.Integer(value=0)
}

default_dict['GetState_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetState_Responses'] = {
    'CurrentState': silaFW_pb2.Integer(value=0)
}

default_dict['GetType_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetType_Responses'] = {
    'CurrentType': silaFW_pb2.String(value='default string')
}

default_dict['GetAvailable_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetAvailable_Responses'] = {
    'CurrentAvailable': silaFW_pb2.Integer(value=0)
}

default_dict['GetName_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetName_Responses'] = {
    'CurrentName': silaFW_pb2.String(value='default string')
}

default_dict['GetVersion_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetVersion_Responses'] = {
    'CurrentVersion': silaFW_pb2.String(value='default string')
}

default_dict['SetSensorOffset_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0),
    'SensorOffset': silaFW_pb2.Real(value=0.0)
}

default_dict['SetSensorOffset_Responses'] = {
    'SensorOffsetSet': silaFW_pb2.Real(value=0.0)
}

default_dict['GetSensorOffset_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetSensorOffset_Responses'] = {
    'CurrentSensorOffset': silaFW_pb2.Real(value=0.0)
}

default_dict['GetSensorPVRaw_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetSensorPVRaw_Responses'] = {
    'CurrentSensorPVRaw': silaFW_pb2.Real(value=0.0)
}

default_dict['SetSensorSlope_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0),
    'SensorSlope': silaFW_pb2.Real(value=0.0)
}

default_dict['SetSensorSlope_Responses'] = {
    'SensorSlopeSet': silaFW_pb2.Real(value=0.0)
}

default_dict['GetSensorSlope_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetSensorSlope_Responses'] = {
    'CurrentSensorSlope': silaFW_pb2.Real(value=0.0)
}

default_dict['SetSensorCompensation_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0),
    'SensorCompensation': silaFW_pb2.Real(value=0.0)
}

default_dict['SetSensorCompensation_Responses'] = {
    'SensorCompensationSet': silaFW_pb2.Real(value=0.0)
}

default_dict['GetSensorCompensation_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetSensorCompensation_Responses'] = {
    'CurrentSensorCompensation': silaFW_pb2.Real(value=0.0)
}

default_dict['SetControllerDB_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0),
    'ControllerDB': silaFW_pb2.Real(value=0.0)
}

default_dict['SetControllerDB_Responses'] = {
    'ControllerDBSet': silaFW_pb2.Real(value=0.0)
}

default_dict['GetControllerDB_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetControllerDB_Responses'] = {
    'CurrentControllerDB': silaFW_pb2.Real(value=0.0)
}

default_dict['GetControllerOut_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetControllerOut_Responses'] = {
    'CurrentControllerOut': silaFW_pb2.Real(value=0.0)
}

default_dict['SetControllerP_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0),
    'ControllerP': silaFW_pb2.Real(value=0.0)
}

default_dict['SetControllerP_Responses'] = {
    'ControllerPSet': silaFW_pb2.Real(value=0.0)
}

default_dict['GetControllerP_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetControllerP_Responses'] = {
    'CurrentControllerP': silaFW_pb2.Real(value=0.0)
}

default_dict['SetControllerTd_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0),
    'ControllerTd': silaFW_pb2.Real(value=0.0)
}

default_dict['SetControllerTd_Responses'] = {
    'ControllerTdSet': silaFW_pb2.Real(value=0.0)
}

default_dict['GetControllerTd_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetControllerTd_Responses'] = {
    'CurrentControllerTd': silaFW_pb2.Real(value=0.0)
}

default_dict['SetControllerTi_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0),
    'ControllerTi': silaFW_pb2.Real(value=0.0)
}

default_dict['SetControllerTi_Responses'] = {
    'ControllerTiSet': silaFW_pb2.Real(value=0.0)
}

default_dict['GetControllerTi_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetControllerTi_Responses'] = {
    'CurrentControllerTi': silaFW_pb2.Real(value=0.0)
}

default_dict['SetControllerMin_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0),
    'ControllerMin': silaFW_pb2.Real(value=0.0)
}

default_dict['SetControllerMin_Responses'] = {
    'ControllerMinSet': silaFW_pb2.Real(value=0.0)
}

default_dict['GetControllerMin_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetControllerMin_Responses'] = {
    'CurrentControllerMin': silaFW_pb2.Real(value=0.0)
}

default_dict['SetControllerMax_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0),
    'ControllerMax': silaFW_pb2.Real(value=0.0)
}

default_dict['SetControllerMax_Responses'] = {
    'ControllerMaxSet': silaFW_pb2.Real(value=0.0)
}

default_dict['GetControllerMax_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetControllerMax_Responses'] = {
    'CurrentControllerMax': silaFW_pb2.Real(value=0.0)
}

default_dict['SetAlarmEnabled_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0),
    'AlarmEnabled': silaFW_pb2.Integer(value=0)
}

default_dict['SetAlarmEnabled_Responses'] = {
    'AlarmEnabledSet': silaFW_pb2.Integer(value=0)
}

default_dict['GetAlarmEnabled_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetAlarmEnabled_Responses'] = {
    'CurrentAlarmEnabled': silaFW_pb2.Integer(value=0)
}

default_dict['SetAlarmAlarmHigh_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0),
    'AlarmAlarmHigh': silaFW_pb2.Real(value=0.0)
}

default_dict['SetAlarmAlarmHigh_Responses'] = {
    'AlarmAlarmHighSet': silaFW_pb2.Real(value=0.0)
}

default_dict['GetAlarmAlarmHigh_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetAlarmAlarmHigh_Responses'] = {
    'CurrentAlarmAlarmHigh': silaFW_pb2.Real(value=0.0)
}

default_dict['SetAlarmAlarmLow_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0),
    'AlarmAlarmLow': silaFW_pb2.Real(value=0.0)
}

default_dict['SetAlarmAlarmLow_Responses'] = {
    'AlarmAlarmLowSet': silaFW_pb2.Real(value=0.0)
}

default_dict['GetAlarmAlarmLow_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetAlarmAlarmLow_Responses'] = {
    'CurrentAlarmAlarmLow': silaFW_pb2.Real(value=0.0)
}

default_dict['SetAlarmMode_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0),
    'AlarmMode': silaFW_pb2.Integer(value=0)
}

default_dict['SetAlarmMode_Responses'] = {
    'AlarmModeSet': silaFW_pb2.Integer(value=0)
}

default_dict['GetAlarmMode_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetAlarmMode_Responses'] = {
    'CurrentAlarmMode': silaFW_pb2.Integer(value=0)
}

default_dict['GetAlarmState_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetAlarmState_Responses'] = {
    'CurrentAlarmState': silaFW_pb2.Integer(value=0)
}

default_dict['SetAlarmDelay_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0),
    'AlarmDelay': silaFW_pb2.Real(value=0.0)
}

default_dict['SetAlarmDelay_Responses'] = {
    'AlarmDelaySet': silaFW_pb2.Real(value=0.0)
}

default_dict['GetAlarmDelay_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetAlarmDelay_Responses'] = {
    'CurrentAlarmDelay': silaFW_pb2.Real(value=0.0)
}

default_dict['SetAlarmWarnHigh_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0),
    'AlarmWarnHigh': silaFW_pb2.Real(value=0.0)
}

default_dict['SetAlarmWarnHigh_Responses'] = {
    'AlarmWarnHighSet': silaFW_pb2.Real(value=0.0)
}

default_dict['GetAlarmWarnHigh_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetAlarmWarnHigh_Responses'] = {
    'CurrentAlarmWarnHigh': silaFW_pb2.Real(value=0.0)
}

default_dict['SetAlarmWarnLow_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0),
    'AlarmWarnLow': silaFW_pb2.Real(value=0.0)
}

default_dict['SetAlarmWarnLow_Responses'] = {
    'AlarmWarnLowSet': silaFW_pb2.Real(value=0.0)
}

default_dict['GetAlarmWarnLow_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetAlarmWarnLow_Responses'] = {
    'CurrentAlarmWarnLow': silaFW_pb2.Real(value=0.0)
}


