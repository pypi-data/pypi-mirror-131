# This file contains default values that are used for the implementations to supply them with 
#   working, albeit mostly useless arguments.
#   You can also use this file as an example to create your custom responses. Feel free to remove
#   Once you have replaced every occurrence of the defaults with more reasonable values.
#   Or you continue using this file, supplying good defaults..

# import the required packages
import sila2lib.framework.SiLAFramework_pb2 as silaFW_pb2
import sila2lib.framework.SiLABinaryTransfer_pb2 as silaBinary_pb2
from .gRPC import DriveControlServicer_pb2 as pb2

# initialise the default dictionary so we can add keys. 
#   We need to do this separately/add keys separately, so we can access keys already defined e.g.
#   for the use in data type identifiers
default_dict = dict()


default_dict['StartPump_Parameters'] = {
    
}

default_dict['StartPump_Responses'] = {
    'StartStatus': silaFW_pb2.String(value='default string')
}

default_dict['StopPump_Parameters'] = {
    
}

default_dict['StopPump_Responses'] = {
    'StopStatus': silaFW_pb2.String(value='default string')
}

default_dict['GetPumpDirection_Parameters'] = {
    'Channel': silaFW_pb2.Integer(value=0)
}

default_dict['GetPumpDirection_Responses'] = {
    'PumpDirection': silaFW_pb2.String(value='default string')
}

default_dict['SetDirectionClockwise_Parameters'] = {
    
}

default_dict['SetDirectionClockwise_Responses'] = {
    'SetDirectionClockwiseSet': silaFW_pb2.String(value='default string')
}

default_dict['SetDirectionCounterClockwise_Parameters'] = {
    
}

default_dict['SetDirectionCounterClockwise_Responses'] = {
    'SetDirectionCounterClockwiseSet': silaFW_pb2.String(value='default string')
}


