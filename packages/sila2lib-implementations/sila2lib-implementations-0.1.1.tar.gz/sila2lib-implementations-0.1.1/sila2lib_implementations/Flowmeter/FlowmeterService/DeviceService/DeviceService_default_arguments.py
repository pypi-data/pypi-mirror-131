# This file contains default values that are used for the implementations to supply them with 
#   working, albeit mostly useless arguments.
#   You can also use this file as an example to create your custom responses. Feel free to remove
#   Once you have replaced every occurrence of the defaults with more reasonable values.
#   Or you continue using this file, supplying good defaults..

# import the required packages
import sila2lib.framework.SiLAFramework_pb2 as silaFW_pb2
import sila2lib.framework.SiLABinaryTransfer_pb2 as silaBinary_pb2
from .gRPC import DeviceService_pb2 as pb2

# initialise the default dictionary so we can add keys. 
#   We need to do this separately/add keys separately, so we can access keys already defined e.g.
#   for the use in data type identifiers
default_dict = dict()


default_dict['GetIdentificationString_Parameters'] = {
    
}

default_dict['GetIdentificationString_Responses'] = {
    'CurrentIdentificationString': silaFW_pb2.String(value='default string')
}

default_dict['GetPrimaryNodeAddress_Parameters'] = {
    
}

default_dict['GetPrimaryNodeAddress_Responses'] = {
    'CurrentPrimaryNodeAddress': silaFW_pb2.String(value='default string')
}

default_dict['SetPrimaryNodeAddress_Parameters'] = {
    'SetPrimaryNodeAddress': silaFW_pb2.String(value='default string')
}

default_dict['SetPrimaryNodeAddress_Responses'] = {
    'Status': silaFW_pb2.String(value='default string'),
    'IndexPointing': silaFW_pb2.String(value='default string')
}

default_dict['GetSecondaryNodeAddress_Parameters'] = {
    
}

default_dict['GetSecondaryNodeAddress_Responses'] = {
    'CurrentSecondaryNodeAddress': silaFW_pb2.String(value='default string')
}

default_dict['GetNextNodeAddress_Parameters'] = {
    
}

default_dict['GetNextNodeAddress_Responses'] = {
    'CurrentNextNodeAddress': silaFW_pb2.String(value='default string')
}

default_dict['GetLastNodeAddress_Parameters'] = {
    
}

default_dict['GetLastNodeAddress_Responses'] = {
    'CurrentLastNodeAddress': silaFW_pb2.String(value='default string')
}

default_dict['GetSensorType_Parameters'] = {
    
}

default_dict['GetSensorType_Responses'] = {
    'CurrentSensorType': silaFW_pb2.String(value='default string')
}

default_dict['GetAlarmInformation_Parameters'] = {
    
}

default_dict['GetAlarmInformation_Responses'] = {
    'CurrentAlarmInformation': silaFW_pb2.String(value='default string')
}

default_dict['GetDeviceType_Parameters'] = {
    
}

default_dict['GetDeviceType_Responses'] = {
    'CurrentDeviceType': silaFW_pb2.String(value='default string')
}

default_dict['GetFirmwareVersion_Parameters'] = {
    
}

default_dict['GetFirmwareVersion_Responses'] = {
    'CurrentFirmwareVersion': silaFW_pb2.String(value='default string')
}

default_dict['GetPressureSensorType_Parameters'] = {
    
}

default_dict['GetPressureSensorType_Responses'] = {
    'CurrentPressureSensorType': silaFW_pb2.String(value='default string')
}

default_dict['GetSensorName_Parameters'] = {
    
}

default_dict['GetSensorName_Responses'] = {
    'CurrentSensorName': silaFW_pb2.String(value='default string')
}

default_dict['GetIdentificationNumber_Parameters'] = {
    
}

default_dict['GetIdentificationNumber_Responses'] = {
    'CurrentIdentificationNumber': silaFW_pb2.String(value='default string')
}

default_dict['GetPowerMode_Parameters'] = {
    
}

default_dict['GetPowerMode_Responses'] = {
    'CurrentPowerMode': silaFW_pb2.String(value='default string')
}

default_dict['GetBusDiagnostic_Parameters'] = {
    
}

default_dict['GetBusDiagnostic_Responses'] = {
    'CurrentBusDiagnostic': silaFW_pb2.String(value='default string')
}

default_dict['GetFieldbus_Parameters'] = {
    
}

default_dict['GetFieldbus_Responses'] = {
    'CurrentFieldbus': silaFW_pb2.String(value='default string')
}

default_dict['GetInstrumentProperties_Parameters'] = {
    
}

default_dict['GetInstrumentProperties_Responses'] = {
    'CurrentInstrumentProperties': silaFW_pb2.String(value='default string')
}

default_dict['GetCommunicationProtocol_Parameters'] = {
    
}

default_dict['GetCommunicationProtocol_Responses'] = {
    'CurrentCommunicationProtocol': silaFW_pb2.String(value='default string')
}

default_dict['SetCommunicationProtocol_Parameters'] = {
    'SetCommunicationProtocol': silaFW_pb2.String(value='default string')
}

default_dict['SetCommunicationProtocol_Responses'] = {
    
}

default_dict['GetSerialPort_Parameters'] = {
    
}

default_dict['GetSerialPort_Responses'] = {
    
}

default_dict['SetSerialPort_Parameters'] = {
    'SetSerialPort': silaFW_pb2.String(value='default string')
}

default_dict['SetSerialPort_Responses'] = {
    
}


