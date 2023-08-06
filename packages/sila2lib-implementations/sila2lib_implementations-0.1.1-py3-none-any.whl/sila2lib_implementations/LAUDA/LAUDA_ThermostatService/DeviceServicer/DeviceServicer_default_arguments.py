# This file contains default values that are used for the implementations to supply them with 
#   working, albeit mostly useless arguments.
#   You can also use this file as an example to create your custom responses. Feel free to remove
#   Once you have replaced every occurrence of the defaults with more reasonable values.
#   Or you continue using this file, supplying good defaults..

# import the required packages
import sila2lib.framework.SiLAFramework_pb2 as silaFW_pb2
import sila2lib.framework.SiLABinaryTransfer_pb2 as silaBinary_pb2
from .gRPC import DeviceServicer_pb2 as pb2

# initialise the default dictionary so we can add keys. 
#   We need to do this separately/add keys separately, so we can access keys already defined e.g.
#   for the use in data type identifiers
default_dict = dict()


default_dict['GetLog_Parameters'] = {
    
}

default_dict['GetLog_Responses'] = {
    'CurrentLogLevel': silaFW_pb2.Integer(value=0),
    #'CurrentLogTimestamp': silaFW_pb2.Timestamp(value=2020-04-17T12:22:01+0000),
    'CurrentLogTimestamp': silaFW_pb2.Timestamp(
        second=0,
        minute=0,
        hour=0,
        day=0,
        month=0,
        year=0,
        timezone=silaFW_pb2.Timezone(
            hours=00,
            minutes=00
        )
    ),
    'CurrentLogMessage': silaFW_pb2.String(value='default string')
}

default_dict['SetKeyLockMode_Parameters'] = {
    'KeyLockMode': silaFW_pb2.String(value='')
}

default_dict['SetKeyLockMode_Responses'] = {
    'KeyLockModeSet': silaFW_pb2.String(value='')
}

default_dict['GetKeyLockMode_Parameters'] = {
    
}

default_dict['GetKeyLockMode_Responses'] = {
    'CurrentKeyLockMode': silaFW_pb2.String(value='')
}

default_dict['StartThermostat_Parameters'] = {
    'Start': silaFW_pb2.String(value='')
}

default_dict['StartThermostat_Responses'] = {
    'StartStatus': silaFW_pb2.String(value='')
}

default_dict['StopThermostat_Parameters'] = {
    'Stop': silaFW_pb2.String(value='')
}

default_dict['StopThermostat_Responses'] = {
    'StopStatus': silaFW_pb2.String(value='')
}

default_dict['GetDeviceStatus_Parameters'] = {
    'DeviceStatus': silaFW_pb2.String(value='')
}

default_dict['GetDeviceStatus_Responses'] = {
    'CurrentDeviceStatus': silaFW_pb2.String(value='')
}

default_dict['GetDeviceStatusDiagnosis_Parameters'] = {
    'DeviceStatusDiagnosis': silaFW_pb2.String(value='')
}

default_dict['GetDeviceStatusDiagnosis_Responses'] = {
    'CurrentDeviceStatusDiagnosis': silaFW_pb2.String(value='')
}

default_dict['GetPowerStatus_Parameters'] = {
    
}

default_dict['GetPowerStatus_Responses'] = {
    'CurrentPowerStatus': silaFW_pb2.String(value='')
}

default_dict['Subscribe_CurrentStatus_Responses'] = {
    'CurrentStatus': silaFW_pb2.String(value='')
}

default_dict['Get_CurrentSoftwareVersion_Responses'] = {
    'CurrentSoftwareVersion': silaFW_pb2.String(value='')
}
