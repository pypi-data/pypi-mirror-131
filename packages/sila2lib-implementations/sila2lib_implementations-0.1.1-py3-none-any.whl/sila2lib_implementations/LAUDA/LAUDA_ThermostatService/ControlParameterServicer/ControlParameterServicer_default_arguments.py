# This file contains default values that are used for the implementations to supply them with 
#   working, albeit mostly useless arguments.
#   You can also use this file as an example to create your custom responses. Feel free to remove
#   Once you have replaced every occurrence of the defaults with more reasonable values.
#   Or you continue using this file, supplying good defaults..

# import the required packages
import sila2lib.framework.SiLAFramework_pb2 as silaFW_pb2
import sila2lib.framework.SiLABinaryTransfer_pb2 as silaBinary_pb2
from .gRPC import ControlParameterServicer_pb2 as pb2

# initialise the default dictionary so we can add keys. 
#   We need to do this separately/add keys separately, so we can access keys already defined e.g.
#   for the use in data type identifiers
default_dict = dict()


default_dict['SetControlParamXp_Parameters'] = {
    'ControlParamXp': silaFW_pb2.Real(value=0.0)
}

default_dict['SetControlParamXp_Responses'] = {
    'ControlParamXpSet': silaFW_pb2.String(value='')
}

default_dict['SetControlParamTn_Parameters'] = {
    'ControlParamTn': silaFW_pb2.Real(value=0.0)
}

default_dict['SetControlParamTn_Responses'] = {
    'ControlParamTnSet': silaFW_pb2.String(value='')
}

default_dict['SetControlParamTv_Parameters'] = {
    'ControlParamTv': silaFW_pb2.Real(value=0.0)
}

default_dict['SetControlParamTv_Responses'] = {
    'ControlParamTvSet': silaFW_pb2.String(value='')
}

default_dict['SetControlParamTd_Parameters'] = {
    'ControlParamTd': silaFW_pb2.Real(value=0.0)
}

default_dict['SetControlParamTd_Responses'] = {
    'ControlParamTdSet': silaFW_pb2.String(value='')
}

default_dict['GetControlParamXp_Parameters'] = {
    
}

default_dict['GetControlParamXp_Responses'] = {
    'CurrentControlParamXp': silaFW_pb2.String(value='')
}

default_dict['GetControlParamTn_Parameters'] = {
    
}

default_dict['GetControlParamTn_Responses'] = {
    'CurrentControlParamTn': silaFW_pb2.String(value='')
}

default_dict['GetControlParamTv_Parameters'] = {
    
}

default_dict['GetControlParamTv_Responses'] = {
    'CurrentControlParamTv': silaFW_pb2.String(value='')
}

default_dict['GetControlParamTd_Parameters'] = {
    
}

default_dict['GetControlParamTd_Responses'] = {
    'CurrentControlParamTd': silaFW_pb2.String(value='')
}


