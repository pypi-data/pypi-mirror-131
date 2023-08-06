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
    'CurrentLogLevel': silaFW_pb2.String(value='default string'),
    #'CurrentLogTimestamp': silaFW_pb2.Timestamp(value=2020-04-16T10:18:48+0000),
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

default_dict['SetPumpAddress_Parameters'] = {
    'Address': silaFW_pb2.Integer(value=1)
}

default_dict['SetPumpAddress_Responses'] = {
    'PumpAddressSet': silaFW_pb2.String(value='default string')
}

default_dict['GetPumpStatus_Parameters'] = {
    
}

default_dict['GetPumpStatus_Responses'] = {
    'CurrentPumpStatus': silaFW_pb2.String(value='default string')
}

default_dict['GetVersionType_Parameters'] = {
    
}

default_dict['GetVersionType_Responses'] = {
    'CurrentVersionType': silaFW_pb2.String(value='default string')
}

default_dict['GetVersionSoftware_Parameters'] = {
    
}

default_dict['GetVersionSoftware_Responses'] = {
    'CurrentVersionSoftware': silaFW_pb2.String(value='default string')
}

default_dict['GetPumpID_Parameters'] = {
    
}

default_dict['GetPumpID_Responses'] = {
    'ID': silaFW_pb2.String(value='default string')
}

default_dict['SetPumpID_Parameters'] = {
    'PumpID': silaFW_pb2.Integer(value=0)
}

default_dict['SetPumpID_Responses'] = {
    'ID': silaFW_pb2.String(value='default string')
}

default_dict['ResetToDefault_Parameters'] = {
    'Reset': silaFW_pb2.String(value='0')
}

default_dict['ResetToDefault_Responses'] = {
    'ResetStatus': silaFW_pb2.String(value='default string')
}

default_dict['GetTotalVolume_Parameters'] = {
    
}

default_dict['GetTotalVolume_Responses'] = {
    'TotalVolume': silaFW_pb2.Real(value=0.0)
}

default_dict['ResetTotalVolume_Parameters'] = {
    
}

default_dict['ResetTotalVolume_Responses'] = {
    'ResetResponse': silaFW_pb2.String(value='default string')
}

default_dict['UnlockControlPanel_Parameters'] = {
    
}

default_dict['UnlockControlPanel_Responses'] = {
    'ControlPanelUnlocked': silaFW_pb2.String(value='default string')
}

default_dict['LockControlPanel_Parameters'] = {
    
}

default_dict['LockControlPanel_Responses'] = {
    'ControlPanelLocked': silaFW_pb2.String(value='default string')
}

default_dict['SetDisplayNumbers_Parameters'] = {
    'DisplayNumbers': silaFW_pb2.Real(value=0.0)
}

default_dict['SetDisplayNumbers_Responses'] = {
    'DisplayNumbersSet': silaFW_pb2.String(value='default string')
}

default_dict['SetDisplayLetters_Parameters'] = {
    'DisplayLetters': silaFW_pb2.String(value='default string')
}

default_dict['SetDisplayLetters_Responses'] = {
    'DisplayLettersSet': silaFW_pb2.String(value='default string')
}

default_dict['SetCommunicationPort_Parameters'] = {
    'PortName': silaFW_pb2.String(value=''),
    'BaudRate': silaFW_pb2.Integer(value=9600),
    'Parity': silaFW_pb2.String(value='NONE'),
    'StopBits': silaFW_pb2.String(value='ONE'),
    'Timeout': silaFW_pb2.Real(value=1)
}

default_dict['SetCommunicationPort_Responses'] = {
    'SetCommunicationPortStatus': silaFW_pb2.String(value='default string')
}

default_dict['ConnectDevice_Parameters'] = {
    
}

default_dict['ConnectDevice_Responses'] = {
    'ConnectionStatus': silaFW_pb2.String(value='default string')
}

default_dict['ResetOverload_Parameters'] = {
    
}

default_dict['ResetOverload_Responses'] = {
    'ResetOverloadStatus': silaFW_pb2.String(value='default string')
}

default_dict['Subscribe_CurrentStatus_Responses'] = {
    'CurrentStatus': silaFW_pb2.String(value='default string')
}

default_dict['Get_PortName_Responses'] = {
    'PortName': silaFW_pb2.String(value='default string')
}

default_dict['Get_BaudRate_Responses'] = {
    'BaudRate': silaFW_pb2.Integer(value=0)
}

default_dict['Get_Parity_Responses'] = {
    'Parity': silaFW_pb2.String(value='default string')
}

default_dict['Get_StopBits_Responses'] = {
    'StopBits': silaFW_pb2.String(value='default string')
}

default_dict['Get_Timeout_Responses'] = {
    'Timeout': silaFW_pb2.Real(value=0.0)
}
