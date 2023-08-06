# This file contains default values that are used for the implementations to supply them with 
#   working, albeit mostly useless arguments.
#   You can also use this file as an example to create your custom responses. Feel free to remove
#   Once you have replaced every occurrence of the defaults with more reasonable values.
#   Or you continue using this file, supplying good defaults..

# import the required packages
import sila2lib.framework.SiLAFramework_pb2 as silaFW_pb2
import sila2lib.framework.SiLABinaryTransfer_pb2 as silaBinary_pb2
from .gRPC import OffgasServicer_pb2 as pb2

# initialise the default dictionary so we can add keys. 
#   We need to do this separately/add keys separately, so we can access keys already defined e.g.
#   for the use in data type identifiers
default_dict = dict()


default_dict['GetCTRPV_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetCTRPV_Responses'] = {
    'CurrentCTRPV': silaFW_pb2.Real(value=0.0)
}

default_dict['GetFPV_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetFPV_Responses'] = {
    'CurrentFPV': silaFW_pb2.Real(value=0.0)
}

default_dict['GetOTRPV_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetOTRPV_Responses'] = {
    'CurrentOTRPV': silaFW_pb2.Real(value=0.0)
}

default_dict['GetRQPV_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetRQPV_Responses'] = {
    'CurrentRQPV': silaFW_pb2.Real(value=0.0)
}

default_dict['GetXCO2PV_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetXCO2PV_Responses'] = {
    'CurrentXCO2PV': silaFW_pb2.Real(value=0.0)
}

default_dict['GetVCTPV_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetVCTPV_Responses'] = {
    'CurrentVCTPV': silaFW_pb2.Real(value=0.0)
}

default_dict['GetVOTPV_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetVOTPV_Responses'] = {
    'CurrentVOTPV': silaFW_pb2.Real(value=0.0)
}

default_dict['GetState_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetState_Responses'] = {
    'CurrentState': silaFW_pb2.Integer(value=0)
}

default_dict['GetType_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetType_Responses'] = {
    'CurrentType': silaFW_pb2.String(value='default string')
}

default_dict['GetAvailable_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetAvailable_Responses'] = {
    'CurrentAvailable': silaFW_pb2.Integer(value=0)
}

default_dict['GetName_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetName_Responses'] = {
    'CurrentName': silaFW_pb2.String(value='default string')
}

default_dict['GetVersion_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetVersion_Responses'] = {
    'CurrentVersion': silaFW_pb2.String(value='default string')
}


