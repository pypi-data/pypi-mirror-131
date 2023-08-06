# This file contains default values that are used for the implementations to supply them with 
#   working, albeit mostly useless arguments.
#   You can also use this file as an example to create your custom responses. Feel free to remove
#   Once you have replaced every occurrence of the defaults with more reasonable values.
#   Or you continue using this file, supplying good defaults..

# import the required packages
import sila2lib.framework.SiLAFramework_pb2 as silaFW_pb2
import sila2lib.framework.SiLABinaryTransfer_pb2 as silaBinary_pb2
from .gRPC import BalanceService_pb2 as pb2

# initialise the default dictionary so we can add keys. 
#   We need to do this separately/add keys separately, so we can access keys already defined e.g.
#   for the use in data type identifiers
default_dict = dict()
default_dict['DataType_StableWeightResponse'] = {
    'StableWeightResponse': pb2.DataType_StableWeightResponse.StableWeightResponse_Struct(WeightValue=silaFW_pb2.Real(value=1.0), IsStable=silaFW_pb2.Boolean(value=False))
}

default_dict['Zero_Parameters'] = {
    
}

default_dict['Zero_Responses'] = {
    'Success': silaFW_pb2.Boolean(value=False)
}

default_dict['ZeroImmediate_Parameters'] = {
    
}

default_dict['ZeroImmediate_Responses'] = {
    'Success': silaFW_pb2.Boolean(value=False),
    'IsStable': silaFW_pb2.Boolean(value=False)
}

default_dict['Tare_Parameters'] = {
    
}

default_dict['Tare_Responses'] = {
    'TareValue': silaFW_pb2.Real(value=1.0)
}

default_dict['WeightValueOnChange_Parameters'] = {
    'WeightChange': silaFW_pb2.Real(value=1.0)
}

default_dict['WeightValueOnChange_Responses'] = {
    'WeightValue': silaFW_pb2.Real(value=1.0),
    'IsStable': silaFW_pb2.Boolean(value=False)
}

default_dict['PresetTareWeight_Parameters'] = {
    'TarePresetValue': silaFW_pb2.Real(value=1.0)
}

default_dict['PresetTareWeight_Responses'] = {
    'TareWeightValue': silaFW_pb2.Real(value=1.0)
}

default_dict['ClearTareValue_Parameters'] = {
    
}

default_dict['ClearTareValue_Responses'] = {
    'TareWeightValue': silaFW_pb2.Real(value=1.0)
}

default_dict['TareImmediately_Parameters'] = {
    
}

default_dict['TareImmediately_Responses'] = {
    'TareWeightValue': silaFW_pb2.Real(value=1.0),
    'IsStable': silaFW_pb2.Boolean(value=False)
}

default_dict['Get_StableWeightValue_Responses'] = {
    'StableWeightValue': silaFW_pb2.Real(value=1.0)
}

default_dict['Get_ImmediateWeightValue_Responses'] = {
    'ImmediateWeightValue': pb2.DataType_StableWeightResponse(**default_dict['DataType_StableWeightResponse'])
}

default_dict['Subscribe_CurrentWeightValue_Responses'] = {
    'CurrentWeightValue': pb2.DataType_StableWeightResponse(**default_dict['DataType_StableWeightResponse'])
}

default_dict['Get_TareWeightValue_Responses'] = {
    'TareWeightValue': silaFW_pb2.Real(value=1.0)
}
