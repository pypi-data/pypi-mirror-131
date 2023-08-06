# This file contains default values that are used for the implementations to supply them with 
#   working, albeit mostly useless arguments.
#   You can also use this file as an example to create your custom responses. Feel free to remove
#   Once you have replaced every occurrence of the defaults with more reasonable values.
#   Or you continue using this file, supplying good defaults..

# import the required packages
import sila2lib.framework.SiLAFramework_pb2 as silaFW_pb2
import sila2lib.framework.SiLABinaryTransfer_pb2 as silaBinary_pb2
from .gRPC import MotorServicer_pb2 as pb2

# initialise the default dictionary so we can add keys. 
#   We need to do this separately/add keys separately, so we can access keys already defined e.g.
#   for the use in data type identifiers
default_dict = dict()


default_dict['StartStirrer_Parameters'] = {
    
}

default_dict['StartStirrer_Responses'] = {
    'CurrentStatus': silaFW_pb2.String(value='default string')
}

default_dict['StopStirrer_Parameters'] = {
    
}

default_dict['StopStirrer_Responses'] = {
    'CurrentStatus': silaFW_pb2.String(value='default string')
}

default_dict['SetRPM_Parameters'] = {
    'RPM': silaFW_pb2.Integer(value=0)
}

default_dict['SetRPM_Responses'] = {
    'CurrentStatus': silaFW_pb2.String(value='default string')
}

default_dict['GetRPM_Parameters'] = {
    
}

default_dict['GetRPM_Responses'] = {
    'CurrentRPM': silaFW_pb2.Integer(value=0)
}

default_dict['SetPower_Parameters'] = {
    'Power': silaFW_pb2.Integer(value=0)
}

default_dict['SetPower_Responses'] = {
    'CurrentStatus': silaFW_pb2.String(value='default string')
}

default_dict['GetPower_Parameters'] = {
    
}

default_dict['GetPower_Responses'] = {
    'CurrentPower': silaFW_pb2.Integer(value=0)
}


