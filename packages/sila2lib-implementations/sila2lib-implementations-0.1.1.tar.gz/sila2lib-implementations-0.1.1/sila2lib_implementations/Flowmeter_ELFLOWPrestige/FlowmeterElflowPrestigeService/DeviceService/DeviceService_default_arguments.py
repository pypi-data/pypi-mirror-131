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


default_dict['GetValveOutput_Parameters'] = {
    
}

default_dict['GetValveOutput_Responses'] = {
    'CurrentValveOutput': silaFW_pb2.Real(value=0.0)
}

default_dict['GetCapacity100_Parameters'] = {
    
}

default_dict['GetCapacity100_Responses'] = {
    'CurrentCapacity100': silaFW_pb2.Real(value=0.0)
}

default_dict['GetCapacityUnit_Parameters'] = {
    
}

default_dict['GetCapacityUnit_Responses'] = {
    'CurrentCapacityUnit': silaFW_pb2.String(value='default string')
}

default_dict['GetSerialNumber_Parameters'] = {
    
}

default_dict['GetSerialNumber_Responses'] = {
    'CurrentSerialNumber': silaFW_pb2.String(value='default string')
}

default_dict['GetPrimaryNodeAddress_Parameters'] = {
    
}

default_dict['GetPrimaryNodeAddress_Responses'] = {
    'CurrentPrimaryNodeAddress': silaFW_pb2.String(value='default string')
}

default_dict['GetFirmwareVersion_Parameters'] = {
    
}

default_dict['GetFirmwareVersion_Responses'] = {
    'CurrentFirmwareVersion': silaFW_pb2.String(value='default string')
}

default_dict['GetCommunicationProtocol_Parameters'] = {
    
}

default_dict['GetCommunicationProtocol_Responses'] = {
    'CurrentCommunicationProtocol': silaFW_pb2.String(value='default string')
}

default_dict['SetCommunicationProtocolBinary_Parameters'] = {
    
}

default_dict['SetCommunicationProtocolBinary_Responses'] = {
    'CurrentCommunicationProtocolBinary': silaFW_pb2.String(value='default string')
}

default_dict['SetCommunicationProtocolAscii_Parameters'] = {
    
}

default_dict['SetCommunicationProtocolAscii_Responses'] = {
    'CurrentCommunicationProtocolAscii': silaFW_pb2.String(value='default string')
}

default_dict['GetSerialPort_Parameters'] = {
    
}

default_dict['GetSerialPort_Responses'] = {
    'CurrentSerialPort': silaFW_pb2.String(value='default string')
}

default_dict['SetSerialPort_Parameters'] = {
    'SetSerialPort': silaFW_pb2.String(value='default string')
}

default_dict['SetSerialPort_Responses'] = {
    'NewSerialPort': silaFW_pb2.String(value='default string')
}


