# This file contains default values that are used for the implementations to supply them with 
#   working, albeit mostly useless arguments.
#   You can also use this file as an example to create your custom responses. Feel free to remove
#   Once you have replaced every occurrence of the defaults with more reasonable values.
#   Or you continue using this file, supplying good defaults..

# import the required packages
import sila2lib.framework.SiLAFramework_pb2 as silaFW_pb2
import sila2lib.framework.SiLABinaryTransfer_pb2 as silaBinary_pb2
from .gRPC import AlarmService_pb2 as pb2

# initialise the default dictionary so we can add keys. 
#   We need to do this separately/add keys separately, so we can access keys already defined e.g.
#   for the use in data type identifiers
default_dict = dict()


default_dict['GetAlarmLimitMaximum_Parameters'] = {
    
}

default_dict['GetAlarmLimitMaximum_Responses'] = {
    'CurrentAlarmLimitMaximum': silaFW_pb2.Real(value=0.0)
}

default_dict['SetAlarmLimitMaximum_Parameters'] = {
    'SetAlarmLimitMaximum': silaFW_pb2.Real(value=0.0)
}

default_dict['SetAlarmLimitMaximum_Responses'] = {
    'Status': silaFW_pb2.String(value='default string'),
    'IndexPointing': silaFW_pb2.String(value='default string')
}

default_dict['GetAlarmLimitMinimum_Parameters'] = {
    
}

default_dict['GetAlarmLimitMinimum_Responses'] = {
    'CurrentAlarmLimitMinimum': silaFW_pb2.String(value='default string')
}

default_dict['SetAlarmLimitMinimum_Parameters'] = {
    'SetAlarmLimitMinimum': silaFW_pb2.Real(value=0.0)
}

default_dict['SetAlarmLimitMinimum_Responses'] = {
    'Status': silaFW_pb2.String(value='default string'),
    'IndexPointing': silaFW_pb2.String(value='default string')
}

default_dict['GetAlarmMode_Parameters'] = {
    
}

default_dict['GetAlarmMode_Responses'] = {
    'CurrentAlarmMode': silaFW_pb2.String(value='default string')
}

default_dict['SetAlarmMode_Parameters'] = {
    'SetAlarmMode': silaFW_pb2.Integer(value=0)
}

default_dict['SetAlarmMode_Responses'] = {
    'Status': silaFW_pb2.String(value='default string'),
    'IndexPointing': silaFW_pb2.String(value='default string')
}

default_dict['GetAlarmOutputMode_Parameters'] = {
    
}

default_dict['GetAlarmOutputMode_Responses'] = {
    'CurrentAlarmOutputMode': silaFW_pb2.String(value='default string')
}

default_dict['SetAlarmOutputMode_Parameters'] = {
    'SetAlarmOutputMode': silaFW_pb2.Integer(value=0)
}

default_dict['SetAlarmOutputMode_Responses'] = {
    'Status': silaFW_pb2.String(value='default string'),
    'IndexPointing': silaFW_pb2.String(value='default string')
}

default_dict['GetAlarmSetpoint_Parameters'] = {
    
}

default_dict['GetAlarmSetpoint_Responses'] = {
    'CurrentAlarmSetpointMode': silaFW_pb2.String(value='default string')
}

default_dict['SetAlarmSetpoint_Parameters'] = {
    'SetAlarmSetpoint': silaFW_pb2.Integer(value=0)
}

default_dict['SetAlarmSetpoint_Responses'] = {
    'Status': silaFW_pb2.String(value='default string'),
    'IndexPointing': silaFW_pb2.String(value='default string')
}


