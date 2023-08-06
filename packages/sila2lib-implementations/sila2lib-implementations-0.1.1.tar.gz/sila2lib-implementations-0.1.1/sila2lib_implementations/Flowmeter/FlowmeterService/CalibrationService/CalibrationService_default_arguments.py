# This file contains default values that are used for the implementations to supply them with 
#   working, albeit mostly useless arguments.
#   You can also use this file as an example to create your custom responses. Feel free to remove
#   Once you have replaced every occurrence of the defaults with more reasonable values.
#   Or you continue using this file, supplying good defaults..

# import the required packages
import sila2lib.framework.SiLAFramework_pb2 as silaFW_pb2
import sila2lib.framework.SiLABinaryTransfer_pb2 as silaBinary_pb2
from .gRPC import CalibrationService_pb2 as pb2

# initialise the default dictionary so we can add keys. 
#   We need to do this separately/add keys separately, so we can access keys already defined e.g.
#   for the use in data type identifiers
default_dict = dict()


default_dict['GetCalibrationCertificate_Parameters'] = {
    
}

default_dict['GetCalibrationCertificate_Responses'] = {
    'LastCalibrationCertificate': silaFW_pb2.String(value='default string')
}

default_dict['SetCalibrationCertificate_Parameters'] = {
    'SetCalibrationCertificate': silaFW_pb2.String(value='default string')
}

default_dict['SetCalibrationCertificate_Responses'] = {
    'Status': silaFW_pb2.String(value='default string'),
    'IndexPointing': silaFW_pb2.String(value='default string')
}

default_dict['GetCalibrationDate_Parameters'] = {
    
}

default_dict['GetCalibrationDate_Responses'] = {
    'LastCalibrationDate': silaFW_pb2.String(value='default string')
}

default_dict['SetCalibrationDate_Parameters'] = {
    'SetCalibrationDate': silaFW_pb2.String(value='default string')
}

default_dict['SetCalibrationDate_Responses'] = {
    'Status': silaFW_pb2.String(value='default string'),
    'IndexPointing': silaFW_pb2.String(value='default string')
}

default_dict['GetServiceNumber_Parameters'] = {
    
}

default_dict['GetServiceNumber_Responses'] = {
    'LastServiceNumber': silaFW_pb2.String(value='default string')
}

default_dict['SetServiceNumber_Parameters'] = {
    
}

default_dict['SetServiceNumber_Responses'] = {
    'Status': silaFW_pb2.String(value='default string'),
    'IndexPointing': silaFW_pb2.String(value='default string')
}

default_dict['GetServiceDate_Parameters'] = {
    
}

default_dict['GetServiceDate_Responses'] = {
    'LastServiceDate': silaFW_pb2.String(value='default string')
}

default_dict['SetServiceDate_Parameters'] = {
    'SetServiceDate': silaFW_pb2.String(value='default string')
}

default_dict['SetServiceDate_Responses'] = {
    'Status': silaFW_pb2.String(value='default string'),
    'IndexPointing': silaFW_pb2.String(value='default string')
}

default_dict['GetSensorCalibrationTemperature_Parameters'] = {
    
}

default_dict['GetSensorCalibrationTemperature_Responses'] = {
    'CurrentSensorCalibrationTemperature': silaFW_pb2.Real(value=0.0)
}

default_dict['SetSensorCalibrationTemperature_Parameters'] = {
    'SetSensorCalibrationTemperature': silaFW_pb2.Real(value=0.0)
}

default_dict['SetSensorCalibrationTemperature_Responses'] = {
    'Status': silaFW_pb2.Real(value=0.0),
    'IndexPointing': silaFW_pb2.String(value='default string')
}


