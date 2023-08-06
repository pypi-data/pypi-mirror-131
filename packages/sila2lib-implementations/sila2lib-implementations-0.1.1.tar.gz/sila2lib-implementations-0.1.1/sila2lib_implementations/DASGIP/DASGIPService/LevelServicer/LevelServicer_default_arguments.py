# This file contains default values that are used for the implementations to supply them with 
#   working, albeit mostly useless arguments.
#   You can also use this file as an example to create your custom responses. Feel free to remove
#   Once you have replaced every occurrence of the defaults with more reasonable values.
#   Or you continue using this file, supplying good defaults..

# import the required packages
import sila2lib.framework.SiLAFramework_pb2 as silaFW_pb2
import sila2lib.framework.SiLABinaryTransfer_pb2 as silaBinary_pb2
from .gRPC import LevelServicer_pb2 as pb2

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

default_dict['GetSensorPVRaw_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetSensorPVRaw_Responses'] = {
    'CurrentSensorPVRaw': silaFW_pb2.Real(value=0.0)
}

default_dict['GetSensorSlope_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetSensorSlope_Responses'] = {
    'CurrentSensorSlope': silaFW_pb2.Real(value=0.0)
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


