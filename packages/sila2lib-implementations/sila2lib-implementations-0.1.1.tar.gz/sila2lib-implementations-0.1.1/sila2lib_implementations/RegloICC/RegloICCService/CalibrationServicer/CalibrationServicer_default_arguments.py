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


default_dict['StartCalibration_Parameters'] = {
    'Calibrate': silaFW_pb2.String(value='')
}

default_dict['StartCalibration_Responses'] = {
    'StartCalibrationStatus': silaFW_pb2.String(value='')
}

default_dict['CancelCalibration_Parameters'] = {
    'Calibrate': silaFW_pb2.String(value='')
}

default_dict['CancelCalibration_Responses'] = {
    'CancelCalibrationStatus': silaFW_pb2.String(value='')
}

default_dict['SetTargetVolume_Parameters'] = {
    'Channel': silaFW_pb2.Integer(value=0),
    'TargetVolume': silaFW_pb2.Real(value=0.0)
}

default_dict['SetTargetVolume_Responses'] = {
    'TargetVolumeSet': silaFW_pb2.String(value='')
}

default_dict['SetActualVolume_Parameters'] = {
    'Channel': silaFW_pb2.Integer(value=0),
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

default_dict['SetDirectionCalibration_Parameters'] = {
    'Channel': silaFW_pb2.Integer(value=0),
    'Direction': silaFW_pb2.String(value='')
}

default_dict['SetDirectionCalibration_Responses'] = {
    'SetDirectionCalibrationSet': silaFW_pb2.String(value='')
}

default_dict['GetDirectionCalibration_Parameters'] = {
    'Direction': silaFW_pb2.String(value='')
}

default_dict['GetDirectionCalibration_Responses'] = {
    'CurrentDirectionCalibration': silaFW_pb2.String(value='')
}

default_dict['SetCalibrationTime_Parameters'] = {
    'Channel': silaFW_pb2.Integer(value=0),
    'Time': silaFW_pb2.Integer(value=0)
}

default_dict['SetCalibrationTime_Responses'] = {
    'SetCalibrationTimeSet': silaFW_pb2.String(value='')
}

default_dict['GetCalibrationTime_Parameters'] = {
    'Time': silaFW_pb2.Integer(value=0)
}

default_dict['GetCalibrationTime_Responses'] = {
    'CurrentCalibrationTime': silaFW_pb2.Integer(value=0)
}

default_dict['GetRunTimeCalibration_Parameters'] = {
    'Time': silaFW_pb2.Integer(value=0)
}

default_dict['GetRunTimeCalibration_Responses'] = {
    'CurrentRunTimeCalibration': silaFW_pb2.Integer(value=0)
}


