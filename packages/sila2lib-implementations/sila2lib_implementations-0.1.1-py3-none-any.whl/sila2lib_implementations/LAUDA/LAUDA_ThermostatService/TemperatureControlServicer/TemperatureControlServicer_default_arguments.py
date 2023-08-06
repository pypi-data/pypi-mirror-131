# This file contains default values that are used for the implementations to supply them with 
#   working, albeit mostly useless arguments.
#   You can also use this file as an example to create your custom responses. Feel free to remove
#   Once you have replaced every occurrence of the defaults with more reasonable values.
#   Or you continue using this file, supplying good defaults..

# import the required packages
import sila2lib.framework.SiLAFramework_pb2 as silaFW_pb2
import sila2lib.framework.SiLABinaryTransfer_pb2 as silaBinary_pb2
from .gRPC import TemperatureControlServicer_pb2 as pb2

# initialise the default dictionary so we can add keys. 
#   We need to do this separately/add keys separately, so we can access keys already defined e.g.
#   for the use in data type identifiers
default_dict = dict()


default_dict['SetPointTemperature_Parameters'] = {
    'SetTemperature': silaFW_pb2.Real(value=0.0)
}

default_dict['SetPointTemperature_Responses'] = {
    'SetTemperatureSet': silaFW_pb2.String(value='')
}

default_dict['SetUpperLimTemperature_Parameters'] = {
    'UpperLimTemperature': silaFW_pb2.Real(value=0.0)
}

default_dict['SetUpperLimTemperature_Responses'] = {
    'UpperLimTemperatureSet': silaFW_pb2.String(value='')
}

default_dict['SetLowerLimTemperature_Parameters'] = {
    'LowerLimTemperature': silaFW_pb2.Real(value=0.0)
}

default_dict['SetLowerLimTemperature_Responses'] = {
    'LowerLimTemperatureSet': silaFW_pb2.String(value='')
}

default_dict['GetFeedLineTemperature_Parameters'] = {
    
}

default_dict['GetFeedLineTemperature_Responses'] = {
    'CurrentFeedLineTemperature': silaFW_pb2.String(value='')
}

default_dict['GetSetpointTemperature_Parameters'] = {
    
}

default_dict['GetSetpointTemperature_Responses'] = {
    'CurrentTemperatureSetpoint': silaFW_pb2.String(value='')
}

default_dict['GetUpperLimTemperature_Parameters'] = {
    
}

default_dict['GetUpperLimTemperature_Responses'] = {
    'CurrentUpperLimTemperature': silaFW_pb2.String(value='')
}

default_dict['GetLowerLimTemperature_Parameters'] = {
    
}

default_dict['GetLowerLimTemperature_Responses'] = {
    'CurrentLowerLimTemperature': silaFW_pb2.String(value='')
}


