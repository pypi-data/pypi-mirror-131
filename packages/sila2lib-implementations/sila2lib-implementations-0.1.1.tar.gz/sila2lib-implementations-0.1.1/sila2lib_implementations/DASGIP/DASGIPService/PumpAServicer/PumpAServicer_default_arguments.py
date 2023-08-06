# This file contains default values that are used for the implementations to supply them with 
#   working, albeit mostly useless arguments.
#   You can also use this file as an example to create your custom responses. Feel free to remove
#   Once you have replaced every occurrence of the defaults with more reasonable values.
#   Or you continue using this file, supplying good defaults..

# import the required packages
import sila2lib.framework.SiLAFramework_pb2 as silaFW_pb2
import sila2lib.framework.SiLABinaryTransfer_pb2 as silaBinary_pb2
from .gRPC import PumpAServicer_pb2 as pb2

# initialise the default dictionary so we can add keys. 
#   We need to do this separately/add keys separately, so we can access keys already defined e.g.
#   for the use in data type identifiers
default_dict = dict()


default_dict['GetPVInt_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetPVInt_Responses'] = {
    'CurrentPVInt': silaFW_pb2.Real(value=0.0)
}

default_dict['GetPV_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetPV_Responses'] = {
    'CurrentPV': silaFW_pb2.Real(value=0.0)
}

default_dict['SetSPM_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0),
    'SPM': silaFW_pb2.Real(value=0.0)
}

default_dict['SetSPM_Responses'] = {
    'SPMSet': silaFW_pb2.Real(value=0.0)
}

default_dict['SetSPE_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0),
    'SPE': silaFW_pb2.Real(value=0.0)
}

default_dict['SetSPE_Responses'] = {
    'SPESet': silaFW_pb2.Real(value=0.0)
}

default_dict['GetSP_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetSP_Responses'] = {
    'CurrentSP': silaFW_pb2.Real(value=0.0)
}

default_dict['GetSPA_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetSPA_Responses'] = {
    'CurrentSPA': silaFW_pb2.Real(value=0.0)
}

default_dict['GetSPM_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetSPM_Responses'] = {
    'CurrentSPM': silaFW_pb2.Real(value=0.0)
}

default_dict['GetSPE_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetSPE_Responses'] = {
    'CurrentSPE': silaFW_pb2.Real(value=0.0)
}

default_dict['GetSPR_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetSPR_Responses'] = {
    'CurrentSPR': silaFW_pb2.Real(value=0.0)
}

default_dict['GetAccess_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetAccess_Responses'] = {
    'CurrentAccess': silaFW_pb2.Integer(value=0)
}

default_dict['SetCmd_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0),
    'Cmd': silaFW_pb2.Integer(value=0)
}

default_dict['SetCmd_Responses'] = {
    'CmdSet': silaFW_pb2.Integer(value=0)
}

default_dict['GetCmd_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetCmd_Responses'] = {
    'CurrentCmd': silaFW_pb2.Integer(value=0)
}

default_dict['SetMode_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0),
    'Mode': silaFW_pb2.Integer(value=0)
}

default_dict['SetMode_Responses'] = {
    'ModeSet': silaFW_pb2.Integer(value=0)
}

default_dict['GetMode_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetMode_Responses'] = {
    'CurrentMode': silaFW_pb2.Integer(value=0)
}

default_dict['SetSetpointSelect_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0),
    'SetpointSelect': silaFW_pb2.Integer(value=0)
}

default_dict['SetSetpointSelect_Responses'] = {
    'SetpointSelectSet': silaFW_pb2.Integer(value=0)
}

default_dict['GetSetpointSelect_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetSetpointSelect_Responses'] = {
    'CurrentSetpointSelect': silaFW_pb2.Integer(value=0)
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

default_dict['SetActuatorCalibration_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0),
    'ActuatorCalibration': silaFW_pb2.Real(value=0.0)
}

default_dict['SetActuatorCalibration_Responses'] = {
    'ActuatorCalibrationSet': silaFW_pb2.Real(value=0.0)
}

default_dict['GetActuatorCalibration_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetActuatorCalibration_Responses'] = {
    'CurrentActuatorCalibration': silaFW_pb2.Real(value=0.0)
}

default_dict['GetActuatorDirPV_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetActuatorDirPV_Responses'] = {
    'CurrentActuatorDirPV': silaFW_pb2.Integer(value=0)
}


