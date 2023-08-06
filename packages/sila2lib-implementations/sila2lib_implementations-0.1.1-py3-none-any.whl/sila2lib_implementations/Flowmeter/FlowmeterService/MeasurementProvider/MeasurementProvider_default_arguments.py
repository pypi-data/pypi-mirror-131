# This file contains default values that are used for the implementations to supply them with 
#   working, albeit mostly useless arguments.
#   You can also use this file as an example to create your custom responses. Feel free to remove
#   Once you have replaced every occurrence of the defaults with more reasonable values.
#   Or you continue using this file, supplying good defaults..

# import the required packages
import sila2lib.framework.SiLAFramework_pb2 as silaFW_pb2
import sila2lib.framework.SiLABinaryTransfer_pb2 as silaBinary_pb2
from .gRPC import MeasurementProvider_pb2 as pb2

# initialise the default dictionary so we can add keys. 
#   We need to do this separately/add keys separately, so we can access keys already defined e.g.
#   for the use in data type identifiers
default_dict = dict()


default_dict['GetTemperature_Parameters'] = {
    
}

default_dict['GetTemperature_Responses'] = {
    'CurrentTemperature': silaFW_pb2.Real(value=0.0)
}

default_dict['GetPressure_Parameters'] = {
    
}

default_dict['GetPressure_Responses'] = {
    'CurrentPressure': silaFW_pb2.Real(value=0.0)
}

default_dict['GetTime_Parameters'] = {
    
}

default_dict['GetTime_Responses'] = {
    'RealTime': silaFW_pb2.Real(value=0.0)
}

default_dict['GetCalibratedVolume_Parameters'] = {
    
}

default_dict['GetCalibratedVolume_Responses'] = {
    'CurrentCalibratedVolume': silaFW_pb2.Real(value=0.0)
}

default_dict['GetSensorNumber_Parameters'] = {
    
}

default_dict['GetSensorNumber_Responses'] = {
    'CurrentSensorNumber': silaFW_pb2.Real(value=0.0)
}

default_dict['GetNormalVolumeFlow_Parameters'] = {
    
}

default_dict['GetNormalVolumeFlow_Responses'] = {
    'CurrentNormalVolumeFlow': silaFW_pb2.Real(value=0.0)
}

default_dict['GetVolumeFlow_Parameters'] = {
    
}

default_dict['GetVolumeFlow_Responses'] = {
    'CurrentVolumeFlow': silaFW_pb2.Real(value=0.0)
}

default_dict['GetDeltaPressure_Parameters'] = {
    
}

default_dict['GetDeltaPressure_Responses'] = {
    'CurrentDeltaPressure': silaFW_pb2.Real(value=0.0)
}

default_dict['GetMassFlow_Parameters'] = {
    
}

default_dict['GetMassFlow_Responses'] = {
    'CurrentMassFlow': silaFW_pb2.Real(value=0.0)
}

default_dict['GetMass_Parameters'] = {
    
}

default_dict['GetMass_Responses'] = {
    'CurrentMass': silaFW_pb2.Real(value=0.0)
}


