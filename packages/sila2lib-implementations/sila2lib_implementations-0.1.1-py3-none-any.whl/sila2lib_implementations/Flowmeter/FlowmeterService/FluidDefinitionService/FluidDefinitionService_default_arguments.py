# This file contains default values that are used for the implementations to supply them with 
#   working, albeit mostly useless arguments.
#   You can also use this file as an example to create your custom responses. Feel free to remove
#   Once you have replaced every occurrence of the defaults with more reasonable values.
#   Or you continue using this file, supplying good defaults..

# import the required packages
import sila2lib.framework.SiLAFramework_pb2 as silaFW_pb2
import sila2lib.framework.SiLABinaryTransfer_pb2 as silaBinary_pb2
from .gRPC import FluidDefinitionService_pb2 as pb2

# initialise the default dictionary so we can add keys. 
#   We need to do this separately/add keys separately, so we can access keys already defined e.g.
#   for the use in data type identifiers
default_dict = dict()


default_dict['GetFluidSetProperties_Parameters'] = {
    
}

default_dict['GetFluidSetProperties_Responses'] = {
    'CurrentFluidsetProperties': silaFW_pb2.String(value='default string')
}

default_dict['SetFluidsetProperties_Parameters'] = {
    'SetFluidProperties': silaFW_pb2.String(value='default string')
}

default_dict['SetFluidsetProperties_Responses'] = {
    'Status': silaFW_pb2.String(value='default string'),
    'IndexPointing': silaFW_pb2.String(value='default string')
}

default_dict['GetFluidNumber_Parameters'] = {
    
}

default_dict['GetFluidNumber_Responses'] = {
    'CurrentFuidNumber': silaFW_pb2.String(value='default string')
}

default_dict['SetFluidNumber_Parameters'] = {
    'SetFluidNumber': silaFW_pb2.String(value='default string')
}

default_dict['SetFluidNumber_Responses'] = {
    'Status': silaFW_pb2.String(value='default string'),
    'IndexPointing': silaFW_pb2.String(value='default string')
}

default_dict['GetFluidName_Parameters'] = {
    
}

default_dict['GetFluidName_Responses'] = {
    'CurrentFluidName': silaFW_pb2.String(value='default string')
}

default_dict['SetFluidName_Parameters'] = {
    'SetFluidName': silaFW_pb2.String(value='default string')
}

default_dict['SetFluidName_Responses'] = {
    'Status': silaFW_pb2.String(value='default string'),
    'IndexPointing': silaFW_pb2.String(value='default string')
}

default_dict['GetHeatCapacity_Parameters'] = {
    
}

default_dict['GetHeatCapacity_Responses'] = {
    'CurrentHeatCapacity': silaFW_pb2.Real(value=0.0)
}

default_dict['SetHeatCapacity_Parameters'] = {
    'SetHeatCapacity': silaFW_pb2.Real(value=0.0)
}

default_dict['SetHeatCapacity_Responses'] = {
    'Status': silaFW_pb2.String(value='default string'),
    'IndexPointing': silaFW_pb2.String(value='default string')
}

default_dict['GetViscosity_Parameters'] = {
    
}

default_dict['GetViscosity_Responses'] = {
    'CurrentViscosity': silaFW_pb2.Real(value=0.0)
}

default_dict['SetViscosity_Parameters'] = {
    'SetViscosity': silaFW_pb2.Real(value=0.0)
}

default_dict['SetViscosity_Responses'] = {
    'Status': silaFW_pb2.String(value='default string'),
    'IndexPointing': silaFW_pb2.String(value='default string')
}


