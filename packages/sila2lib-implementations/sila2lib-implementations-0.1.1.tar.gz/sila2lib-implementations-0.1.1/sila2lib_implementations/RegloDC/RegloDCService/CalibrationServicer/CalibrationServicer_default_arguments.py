# This file contains default values that are used for the implementations to supply them with 
#   working, albeit mostly useless arguments.
#   You can also use this file as an example to create your custom responses. Feel free to remove
#   Once you have replaced every occurrence of the defaults with more reasonable values.
#   Or you continue using this file, supplying good defaults..

# import the required packages
import sila2lib.framework.SiLAFramework_pb2 as silaFW_pb2
import sila2lib.framework.SiLABinaryTransfer_pb2 as silaBinary_pb2
from .gRPC import CalibrationServicer_pb2 as pb2

# initialise the default dictionary so we can add keys. 
#   We need to do this separately/add keys separately, so we can access keys already defined e.g.
#   for the use in data type identifiers
default_dict = dict()


default_dict['StartCalibrationTime_Parameters'] = {
    
}

default_dict['StartCalibrationTime_Responses'] = {
    'CalibrationResult': silaFW_pb2.String(value='default string')
}

default_dict['StartCalibrationVolume_Parameters'] = {
    
}

default_dict['StartCalibrationVolume_Responses'] = {
    'CalibrationResult': silaFW_pb2.String(value='default string')
}

default_dict['GetDefaultFlowRate_Parameters'] = {
    
}

default_dict['GetDefaultFlowRate_Responses'] = {
    'DefaultFlowRate': silaFW_pb2.Real(value=999.9)
}

default_dict['GetCalibratedFlowRate_Parameters'] = {
    
}

default_dict['GetCalibratedFlowRate_Responses'] = {
    'CalibratedFlowRate': silaFW_pb2.Real(value=999.9)
}

default_dict['SetCalibratedFlowRate_Parameters'] = {
    
}

default_dict['SetCalibratedFlowRate_Responses'] = {
    'CalibratedFlowRate': silaFW_pb2.Real(value=999.9)
}

default_dict['SetCalibrationTargetVolume_Parameters'] = {
    'TargetVolume': silaFW_pb2.Real(value=0.0)
}

default_dict['SetCalibrationTargetVolume_Responses'] = {
    'TargetVolumeSet': silaFW_pb2.String(value='default string')
}

default_dict['SetCalibrationTargetTime_Parameters'] = {
    'TargetTime': silaFW_pb2.Real(value=0.0)
}

default_dict['SetCalibrationTargetTime_Responses'] = {
    'TargetTimeSet': silaFW_pb2.String(value='default string')
}

default_dict['SetActualVolume_Parameters'] = {
    'ActualVolume': silaFW_pb2.Real(value=0.0)
}

default_dict['SetActualVolume_Responses'] = {
    'ActualVolumeSet': silaFW_pb2.String(value='default string')
}

default_dict['GetTargetVolume_Parameters'] = {
    'TargetVolume': silaFW_pb2.Real(value=0.0)
}

default_dict['GetTargetVolume_Responses'] = {
    'CurrentTargetVolume': silaFW_pb2.Real(value=0.0)
}

default_dict['SetActualTime_Parameters'] = {
    'ActualTime': silaFW_pb2.Real(value=0.0)
}

default_dict['SetActualTime_Responses'] = {
    'ActualTimeSet': silaFW_pb2.String(value='default string')
}

default_dict['GetTargetTime_Parameters'] = {
    'TargetTime': silaFW_pb2.Real(value=0.0)
}

default_dict['GetTargetTime_Responses'] = {
    'CurrentTargetTime': silaFW_pb2.Real(value=0.0)
}

default_dict['SetDirectionCalibration_Parameters'] = {
    'Direction': silaFW_pb2.String(value='default string')
}

default_dict['SetDirectionCalibration_Responses'] = {
    'SetDirectionCalibrationSet': silaFW_pb2.String(value='default string')
}

default_dict['GetDirectionCalibration_Parameters'] = {
    'Direction': silaFW_pb2.String(value='default string')
}

default_dict['GetDirectionCalibration_Responses'] = {
    'CurrentDirectionCalibration': silaFW_pb2.String(value='default string')
}

default_dict['GetLastCalibrationTime_Parameters'] = {
    
}

default_dict['GetLastCalibrationTime_Responses'] = {
    'LastCalibrationTime': silaFW_pb2.String(value='default string')
}


