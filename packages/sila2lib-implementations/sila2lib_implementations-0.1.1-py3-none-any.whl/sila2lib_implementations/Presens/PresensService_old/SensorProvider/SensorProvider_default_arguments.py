# This file contains default values that are used for the implementations to supply them with 
#   working, albeit mostly useless arguments.
#   You can also use this file as an example to create your custom responses. Feel free to remove
#   Once you have replaced every occurrence of the defaults with more reasonable values.
#   Or you continue using this file, supplying good defaults..

# import the required packages
import sila2lib.framework.SiLAFramework_pb2 as silaFW_pb2
import sila2lib.framework.SiLABinaryTransfer_pb2 as silaBinary_pb2
from .gRPC import SensorProvider_pb2 as pb2

# initialise the default dictionary so we can add keys. 
#   We need to do this separately/add keys separately, so we can access keys already defined e.g.
#   for the use in data type identifiers
default_dict = dict()


default_dict['GetSingleO2_Parameters'] = {
    'Channel': silaFW_pb2.Integer(value=0)
}

default_dict['GetSingleO2_Responses'] = {
    'CurrentChannelNumber': silaFW_pb2.String(value='default string'),
    'CurrentSensorType': silaFW_pb2.String(value='default string'),
    'CurrentAmplitude': silaFW_pb2.Integer(value=0),
    'CurrentPhase': silaFW_pb2.Real(value=0.0),
    'CurrentTemperature': silaFW_pb2.Real(value=0.0),
    'CurrentO2': silaFW_pb2.Real(value=0.0),
    'CurrentErrorCode': silaFW_pb2.String(value='default string')
}

default_dict['GetSinglePH_Parameters'] = {
    'Channel': silaFW_pb2.Integer(value=0)
}

default_dict['GetSinglePH_Responses'] = {
    'CurrentChannelNumber': silaFW_pb2.Integer(value=0),
    'CurrentSensorType': silaFW_pb2.String(value='default string'),
    'CurrentAmplitude': silaFW_pb2.Integer(value=0),
    'CurrentPhase': silaFW_pb2.Real(value=0.0),
    'CurrentTemperature': silaFW_pb2.Real(value=0.0),
    'CurrentPH': silaFW_pb2.Real(value=0.0),
    'CurrentErrorCode': silaFW_pb2.String(value='default string')
}

default_dict['GetAllO2_Parameters'] = {
    
}

default_dict['GetAllO2_Responses'] = {
    'CurrentSensorType': [silaFW_pb2.String(value='default string')],
    'CurrentAmplitude': [silaFW_pb2.Integer(value=0)],
    'CurrentPhase': [silaFW_pb2.Real(value=0.0)],
    'CurrentTemperature': [silaFW_pb2.Real(value=0.0)],
    'CurrentO2': [silaFW_pb2.Real(value=0.0)],
    'CurrentErrorCode': [silaFW_pb2.String(value='default string')]
}

default_dict['GetAllPH_Parameters'] = {
    
}

default_dict['GetAllPH_Responses'] = {
    'CurrentSensorType': [silaFW_pb2.String(value='default string')],
    'CurrentAmplitude': [silaFW_pb2.Integer(value=0)],
    'CurrentPhase': [silaFW_pb2.Real(value=0.0)],
    'CurrentTemperature': [silaFW_pb2.Real(value=0.0)],
    'CurrentPH': [silaFW_pb2.Real(value=0.0)],
    'CurrentErrorCode': [silaFW_pb2.String(value='default string')]
}

default_dict['Get_TotalChannels_Responses'] = {
    'TotalChannels': silaFW_pb2.Integer(value=0)
}

default_dict['Get_TotalBars_Responses'] = {
    'TotalBars': silaFW_pb2.Integer(value=0)
}

default_dict['Get_BarSensors_Responses'] = {
    'BarSensors': silaFW_pb2.Integer(value=0)
}
