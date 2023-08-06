# This file contains default values that are used for the implementations to supply them with 
#   working, albeit mostly useless arguments.
#   You can also use this file as an example to create your custom responses. Feel free to remove
#   Once you have replaced every occurrence of the defaults with more reasonable values.
#   Or you continue using this file, supplying good defaults..

# import the required packages
import sila2lib.framework.SiLAFramework_pb2 as silaFW_pb2
import sila2lib.framework.SiLABinaryTransfer_pb2 as silaBinary_pb2
from .gRPC import CalibrationServicer_pb2 as pb2

# initialise the default dictionary so we can add keys. 
#   We need to do this separately/add keys separately, so we can access keys already defined e.g.
#   for the use in data type identifiers
default_dict = dict()


default_dict['GetO2CalLow_Parameters'] = {
    
}

default_dict['GetO2CalLow_Responses'] = {
    'CurrentO2CalLow': [silaFW_pb2.Real(value=0.0)]
}

default_dict['SetO2CalLow_Parameters'] = {
    'SetO2CalLow': [silaFW_pb2.Real(value=0.0)]
}

default_dict['SetO2CalLow_Responses'] = {
    'CurrentO2CalLow': [silaFW_pb2.Real(value=0.0)]
}

default_dict['GetO2CalHigh_Parameters'] = {
    
}

default_dict['GetO2CalHigh_Responses'] = {
    'CurrentO2CalHigh': [silaFW_pb2.Real(value=0.0)]
}

default_dict['SetO2CalHigh_Parameters'] = {
    'SetO2CalHigh': [silaFW_pb2.Real(value=0.0)]
}

default_dict['SetO2CalHigh_Responses'] = {
    'CurrentO2CalHigh': [silaFW_pb2.Real(value=0.0)]
}

default_dict['GetO2CalTemp_Parameters'] = {
    
}

default_dict['GetO2CalTemp_Responses'] = {
    'CurrentO2CalTemp': [silaFW_pb2.Real(value=0.0)]
}

default_dict['SetO2CalTemp_Parameters'] = {
    'SetO2CalTemp': [silaFW_pb2.Real(value=0.0)]
}

default_dict['SetO2CalTemp_Responses'] = {
    'CurrentO2CalTemp': [silaFW_pb2.Real(value=0.0)]
}

default_dict['GetPHlmax_Parameters'] = {
    
}

default_dict['GetPHlmax_Responses'] = {
    'CurrentPHlmax': [silaFW_pb2.Real(value=0.0)]
}

default_dict['SetPHlmax_Parameters'] = {
    'SetPHlmax': [silaFW_pb2.Real(value=0.0)]
}

default_dict['SetPHlmax_Responses'] = {
    'CurrentPHlmax': [silaFW_pb2.Real(value=0.0)]
}

default_dict['GetPHlmin_Parameters'] = {
    
}

default_dict['GetPHlmin_Responses'] = {
    'CurrentPHlmin': [silaFW_pb2.Real(value=0.0)]
}

default_dict['SetPHlmin_Parameters'] = {
    'SetPHlmin': [silaFW_pb2.Real(value=0.0)]
}

default_dict['SetPHlmin_Responses'] = {
    'CurrentPHlmin': [silaFW_pb2.Real(value=0.0)]
}

default_dict['GetPHpH0_Parameters'] = {
    
}

default_dict['GetPHpH0_Responses'] = {
    'CurrentPHpH0': [silaFW_pb2.Real(value=0.0)]
}

default_dict['SetPHpH0_Parameters'] = {
    'SetPHpH0': [silaFW_pb2.Real(value=0.0)]
}

default_dict['SetPHpH0_Responses'] = {
    'CurrentPHpH0': [silaFW_pb2.Real(value=0.0)]
}

default_dict['GetPHdpH_Parameters'] = {
    
}

default_dict['GetPHdpH_Responses'] = {
    'CurrentPHdpH': [silaFW_pb2.Real(value=0.0)]
}

default_dict['SetPHdpH_Parameters'] = {
    'SetPHdpH': [silaFW_pb2.Real(value=0.0)]
}

default_dict['SetPHdpH_Responses'] = {
    'CurrentPHdpH': [silaFW_pb2.Real(value=0.0)]
}

default_dict['GetPHCalTemp_Parameters'] = {
    
}

default_dict['GetPHCalTemp_Responses'] = {
    'CurrentPHCalTemp': [silaFW_pb2.Real(value=0.0)]
}

default_dict['SetPHCalTemp_Parameters'] = {
    'SetPHCalTemp': [silaFW_pb2.Real(value=0.0)]
}

default_dict['SetPHCalTemp_Responses'] = {
    'CurrentPHCalTemp': [silaFW_pb2.Real(value=0.0)]
}


