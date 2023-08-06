# This file contains default values that are used for the implementations to supply them with 
#   working, albeit mostly useless arguments.
#   You can also use this file as an example to create your custom responses. Feel free to remove
#   Once you have replaced every occurrence of the defaults with more reasonable values.
#   Or you continue using this file, supplying good defaults..

# import the required packages
import sila2lib.framework.SiLAFramework_pb2 as silaFW_pb2
import sila2lib.framework.SiLABinaryTransfer_pb2 as silaBinary_pb2
from .gRPC import DeviceController_pb2 as pb2

# initialise the default dictionary so we can add keys. 
#   We need to do this separately/add keys separately, so we can access keys already defined e.g.
#   for the use in data type identifiers
default_dict = dict()


default_dict['GetReport_Parameters'] = {
    
}

default_dict['GetReport_Responses'] = {
    'CurrentReport': [silaFW_pb2.String(value='default string')]
}

default_dict['GetTComp_Parameters'] = {
    
}

default_dict['GetTComp_Responses'] = {
    'CurrentTComp': silaFW_pb2.Real(value=0.0)
}

default_dict['SetTComp_Parameters'] = {
    'SetTComp': [silaFW_pb2.Real(value=0.0)]
}

default_dict['SetTComp_Responses'] = {
    'CurrentTComp': silaFW_pb2.Real(value=0.0)
}

default_dict['GetDynAveraging_Parameters'] = {
    
}

default_dict['GetDynAveraging_Responses'] = {
    'CurrentDynAverage': silaFW_pb2.Integer(value=0)
}

default_dict['SetDynAveraging_Parameters'] = {
    'SetDynAverage': [silaFW_pb2.Real(value=0.0)]
}

default_dict['SetDynAveraging_Responses'] = {
    'CurrentDynAverage': silaFW_pb2.Integer(value=0)
}

default_dict['SwitchOffDevice_Parameters'] = {
    
}

default_dict['SwitchOffDevice_Responses'] = {
    'CurrentStatus': silaFW_pb2.String(value='default string')
}


