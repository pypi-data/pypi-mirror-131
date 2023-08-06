# This file contains default values that are used for the implementations to supply them with 
#   working, albeit mostly useless arguments.
#   You can also use this file as an example to create your custom responses. Feel free to remove
#   Once you have replaced every occurrence of the defaults with more reasonable values.
#   Or you continue using this file, supplying good defaults..

# import the required packages
import sila2lib.framework.SiLAFramework_pb2 as silaFW_pb2
import sila2lib.framework.SiLABinaryTransfer_pb2 as silaBinary_pb2
from .gRPC import ParameterControlServicer_pb2 as pb2

# initialise the default dictionary so we can add keys. 
#   We need to do this separately/add keys separately, so we can access keys already defined e.g.
#   for the use in data type identifiers
default_dict = dict()


default_dict['SetRPMMode_Parameters'] = {
    
}

default_dict['SetRPMMode_Responses'] = {
    'PumpModeSet': silaFW_pb2.String(value='default string')
}

default_dict['SetFlowRateMode_Parameters'] = {
    
}

default_dict['SetFlowRateMode_Responses'] = {
    'PumpModeSet': silaFW_pb2.String(value='default string')
}

default_dict['SetDispenseVolumeMode_Parameters'] = {
    
}

default_dict['SetDispenseVolumeMode_Responses'] = {
    'PumpModeSet': silaFW_pb2.String(value='default string')
}

default_dict['SetDispenseTimeMode_Parameters'] = {
    
}

default_dict['SetDispenseTimeMode_Responses'] = {
    'PumpModeSet': silaFW_pb2.String(value='default string')
}

default_dict['SetPauseTimeMode_Parameters'] = {
    
}

default_dict['SetPauseTimeMode_Responses'] = {
    'PumpModeSet': silaFW_pb2.String(value='default string')
}

default_dict['SetDispenseTimePauseTimeMode_Parameters'] = {
    
}

default_dict['SetDispenseTimePauseTimeMode_Responses'] = {
    'PumpModeSet': silaFW_pb2.String(value='default string')
}

default_dict['SetDispenseVolumePauseTimeMode_Parameters'] = {
    
}

default_dict['SetDispenseVolumePauseTimeMode_Responses'] = {
    'PumpModeSet': silaFW_pb2.String(value='default string')
}

default_dict['GetDispenseVolume_Parameters'] = {
    
}

default_dict['GetDispenseVolume_Responses'] = {
    'DispenseVolume': silaFW_pb2.Real(value=0.0)
}

default_dict['SetDispenseVolume_Parameters'] = {
    'Volume': silaFW_pb2.Real(value=0.0)
}

default_dict['SetDispenseVolume_Responses'] = {
    'VolumeSet': silaFW_pb2.String(value='default string')
}

default_dict['SetDispenseVolumeModeVolume_Parameters'] = {
    'Volume': silaFW_pb2.Real(value=0.0)
}

default_dict['SetDispenseVolumeModeVolume_Responses'] = {
    'VolumeSet': silaFW_pb2.String(value='default string')
}

default_dict['GetFlowRate_Parameters'] = {
    
}

default_dict['GetFlowRate_Responses'] = {
    'CurrentFlowRate': silaFW_pb2.Real(value=0.0)
}

default_dict['SetFlowRate_Parameters'] = {
    'FlowRate': silaFW_pb2.Real(value=0.0)
}

default_dict['SetFlowRate_Responses'] = {
    'SetFlowRateSet': silaFW_pb2.String(value='default string')
}

default_dict['GetRPM_Parameters'] = {
    
}

default_dict['GetRPM_Responses'] = {
    'CurrentRPM': silaFW_pb2.Real(value=0.0)
}

default_dict['SetRPM_Parameters'] = {
    'RPM': silaFW_pb2.Real(value=0.0)
}

default_dict['SetRPM_Responses'] = {
    'SetRPMSet': silaFW_pb2.String(value='default string')
}

default_dict['GetPauseTime_Parameters'] = {
    
}

default_dict['GetPauseTime_Responses'] = {
    'CurrentPauseTime': silaFW_pb2.Real(value=0.0)
}

default_dict['SetPauseTime_Parameters'] = {
    'PauseTimeS': silaFW_pb2.Real(value=0.0),
    'PauseTimeMin': silaFW_pb2.Integer(value=0),
    'PauseTimeH': silaFW_pb2.Integer(value=0)
}

default_dict['SetPauseTime_Responses'] = {
    'SetPauseTimeSet': silaFW_pb2.String(value='default string')
}

default_dict['GetDispenseCycles_Parameters'] = {
    
}

default_dict['GetDispenseCycles_Responses'] = {
    'DispenseCycles': silaFW_pb2.Integer(value=0)
}

default_dict['SetDispenseCycles_Parameters'] = {
    'DispenseCycles': silaFW_pb2.Integer(value=0)
}

default_dict['SetDispenseCycles_Responses'] = {
    'SetDispenseCycleSet': silaFW_pb2.String(value='default string')
}

default_dict['GetDispenseTime_Parameters'] = {
    
}

default_dict['GetDispenseTime_Responses'] = {
    'CurrentDispenseTime': silaFW_pb2.Real(value=0.0)
}

default_dict['SetDispenseTime_Parameters'] = {
    'CurrentDispenseTimeS': silaFW_pb2.Real(value=0.0),
    'CurrentDispenseTimeMin': silaFW_pb2.Real(value=0.0),
    'CurrentDispenseTimeH': silaFW_pb2.Real(value=0.0)
}

default_dict['SetDispenseTime_Responses'] = {
    'SetDispenseTimeSet': silaFW_pb2.String(value='default string')
}

default_dict['GetRollerSteps_Parameters'] = {
    
}

default_dict['GetRollerSteps_Responses'] = {
    'CurrentRollerSteps': silaFW_pb2.Integer(value=0)
}

default_dict['SetRollerSteps_Parameters'] = {
    'CurrentRollerSteps': silaFW_pb2.Integer(value=0)
}

default_dict['SetRollerSteps_Responses'] = {
    'SetRollerStepsSet': silaFW_pb2.Integer(value=0)
}

default_dict['GetRollerStepVolume_Parameters'] = {
    
}

default_dict['GetRollerStepVolume_Responses'] = {
    'CurrentRollerStepVolume': silaFW_pb2.Integer(value=0)
}

default_dict['SetRollerStepVolume_Parameters'] = {
    'CurrentRollerStepVolume': silaFW_pb2.Integer(value=0)
}

default_dict['SetRollerStepVolume_Responses'] = {
    'SetRollerStepVolumeSet': silaFW_pb2.Integer(value=0)
}

default_dict['ResetRollerStepVolume_Parameters'] = {
    
}

default_dict['ResetRollerStepVolume_Responses'] = {
    'ResetRollerStepVolumeSet': silaFW_pb2.Integer(value=0)
}

default_dict['GetRollerBackSteps_Parameters'] = {
    
}

default_dict['GetRollerBackSteps_Responses'] = {
    'CurrentRollerBackSteps': silaFW_pb2.Integer(value=0)
}

default_dict['SetRollerBackSteps_Parameters'] = {
    'CurrentRollerBackSteps': silaFW_pb2.Integer(value=0)
}

default_dict['SetRollerBackSteps_Responses'] = {
    'SetRollerBackStepsSet': silaFW_pb2.Integer(value=0)
}

default_dict['SaveApplicationParameters_Parameters'] = {
    
}

default_dict['SaveApplicationParameters_Responses'] = {
    'SaveResponse': silaFW_pb2.String(value='default string')
}

default_dict['GetTubingDiameter_Parameters'] = {
    
}

default_dict['GetTubingDiameter_Responses'] = {
    'CurrentTubingDiameter': silaFW_pb2.Real(value=0.0)
}

default_dict['SetTubingDiameter_Parameters'] = {
    'TubingDiameter': silaFW_pb2.Real(value=0.0)
}

default_dict['SetTubingDiameter_Responses'] = {
    'TubingDiameterSet': silaFW_pb2.String(value='default string')
}


