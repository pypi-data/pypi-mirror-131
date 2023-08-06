# This file contains default values that are used for the implementations to supply them with 
#   working, albeit mostly useless arguments.
#   You can also use this file as an example to create your custom responses. Feel free to remove
#   Once you have replaced every occurrence of the defaults with more reasonable values.
#   Or you continue using this file, supplying good defaults..

# import the required packages
import sila2lib.framework.SiLAFramework_pb2 as silaFW_pb2
import sila2lib.framework.SiLABinaryTransfer_pb2 as silaBinary_pb2
from .gRPC import ReactorServicer_pb2 as pb2

# initialise the default dictionary so we can add keys. 
#   We need to do this separately/add keys separately, so we can access keys already defined e.g.
#   for the use in data type identifiers
default_dict = dict()


default_dict['GetVInitial_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetVInitial_Responses'] = {
    'CurrentVInitial': silaFW_pb2.Real(value=0.0)
}

default_dict['GetVLiquid_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetVLiquid_Responses'] = {
    'CurrentVLiquid': silaFW_pb2.Real(value=0.0)
}

default_dict['GetVMax_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetVMax_Responses'] = {
    'CurrentVMax': silaFW_pb2.Real(value=0.0)
}

default_dict['GetVMin_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetVMin_Responses'] = {
    'CurrentVMin': silaFW_pb2.Real(value=0.0)
}

default_dict['GetVTotal_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetVTotal_Responses'] = {
    'CurrentVTotal': silaFW_pb2.Real(value=0.0)
}
