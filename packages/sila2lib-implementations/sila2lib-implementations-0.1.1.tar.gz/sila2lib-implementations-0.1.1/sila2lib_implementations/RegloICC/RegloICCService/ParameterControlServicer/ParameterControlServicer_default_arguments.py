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


default_dict['SetFlowRate_Parameters'] = {
    'Channel': silaFW_pb2.Integer(value=0),
    'SetFlowRate': silaFW_pb2.Real(value=0.0)
}

default_dict['SetFlowRate_Responses'] = {
    'SetFlowRateSet': silaFW_pb2.Real(value=0.0)
}

default_dict['SetRPMMode_Parameters'] = {
    'PumpMode': silaFW_pb2.String(value='')
}

default_dict['SetRPMMode_Responses'] = {
    'PumpModeSet': silaFW_pb2.String(value='')
}

default_dict['SetFlowRateMode_Parameters'] = {
    'PumpMode': silaFW_pb2.String(value='')
}

default_dict['SetFlowRateMode_Responses'] = {
    'PumpModeSet': silaFW_pb2.String(value='')
}

default_dict['SetVolumeRateMode_Parameters'] = {
    'PumpMode': silaFW_pb2.String(value='')
}

default_dict['SetVolumeRateMode_Responses'] = {
    'PumpModeSet': silaFW_pb2.String(value='')
}

default_dict['SetVolumeTimeMode_Parameters'] = {
    'PumpMode': silaFW_pb2.String(value='')
}

default_dict['SetVolumeTimeMode_Responses'] = {
    'PumpModeSet': silaFW_pb2.String(value='')
}

default_dict['SetVolumePauseMode_Parameters'] = {
    'PumpMode': silaFW_pb2.String(value='')
}

default_dict['SetVolumePauseMode_Responses'] = {
    'PumpModeSet': silaFW_pb2.String(value='')
}

default_dict['SetTimeMode_Parameters'] = {
    'PumpMode': silaFW_pb2.String(value='')
}

default_dict['SetTimeMode_Responses'] = {
    'PumpModeSet': silaFW_pb2.String(value='')
}

default_dict['SetTimePauseMode_Parameters'] = {
    'PumpMode': silaFW_pb2.String(value='')
}

default_dict['SetTimePauseMode_Responses'] = {
    'PumpModeSet': silaFW_pb2.String(value='')
}

default_dict['SetVolume_Parameters'] = {
    'Channel': silaFW_pb2.Integer(value=0),
    'Volume': silaFW_pb2.Real(value=0.0)
}

default_dict['SetVolume_Responses'] = {
    'VolumeSet': silaFW_pb2.String(value='')
}

default_dict['GetFlowRate_Parameters'] = {
    'Channel': silaFW_pb2.Integer(value=0)
}

default_dict['GetFlowRate_Responses'] = {
    'CurrentFlowRate': silaFW_pb2.Real(value=0.0)
}

default_dict['GetMode_Parameters'] = {
    'Channel': silaFW_pb2.Integer(value=0)
}

default_dict['GetMode_Responses'] = {
    'CurrentPumpMode': silaFW_pb2.String(value='')
}

default_dict['GetVolume_Parameters'] = {
    'Channel': silaFW_pb2.Integer(value=0)
}

default_dict['GetVolume_Responses'] = {
    'CurrentVolume': silaFW_pb2.Real(value=0.0)
}

default_dict['GetMaximumFlowRate_Parameters'] = {
    'Channel': silaFW_pb2.Integer(value=0)
}

default_dict['GetMaximumFlowRate_Responses'] = {
    'MaximumFlowRate': silaFW_pb2.Real(value=0.0)
}

default_dict['GetMaximumFlowRateWithCalibration_Parameters'] = {
    'Channel': silaFW_pb2.Integer(value=0)
}

default_dict['GetMaximumFlowRateWithCalibration_Responses'] = {
    'MaximumFlowRateWithCalibration': silaFW_pb2.Real(value=0.0)
}

default_dict['GetSpeedSettingRPM_Parameters'] = {
    'Channel': silaFW_pb2.Integer(value=0)
}

default_dict['GetSpeedSettingRPM_Responses'] = {
    'CurrentSpeedSetting': silaFW_pb2.Real(value=0.0)
}

default_dict['SetSpeedSettingRPM_Parameters'] = {
    'Channel': silaFW_pb2.Integer(value=0),
    'Speed': silaFW_pb2.Real(value=0.0)
}

default_dict['SetSpeedSettingRPM_Responses'] = {
    'CurrentSpeedSetting': silaFW_pb2.String(value='')
}

default_dict['SetCurrentRunTime_Parameters'] = {
    'Channel': silaFW_pb2.Integer(value=0),
    'RunTime': silaFW_pb2.Real(value=0.0)
}

default_dict['SetCurrentRunTime_Responses'] = {
    'SetCurrentRunTimeSet': silaFW_pb2.String(value='')
}

default_dict['GetCurrentRunTime_Parameters'] = {
    'Channel': silaFW_pb2.Integer(value=0)
}

default_dict['GetCurrentRunTime_Responses'] = {
    'GetCurrentRunTime': silaFW_pb2.Integer(value=0)
}

default_dict['SetPumpingPauseTime_Parameters'] = {
    'Channel': silaFW_pb2.Integer(value=0),
    'PumpingPauseTime': silaFW_pb2.Real(value=0.0)
}

default_dict['SetPumpingPauseTime_Responses'] = {
    'SetPumpingPauseTimeSet': silaFW_pb2.String(value='')
}

default_dict['GetPumpingPauseTime_Parameters'] = {
    'Channel': silaFW_pb2.Integer(value=0)
}

default_dict['GetPumpingPauseTime_Responses'] = {
    'CurrentPumpingPauseTime': silaFW_pb2.Real(value=0.0)
}

default_dict['GetCycleCount_Parameters'] = {
    'Channel': silaFW_pb2.Integer(value=0)
}

default_dict['GetCycleCount_Responses'] = {
    'CurrentCycleCount': silaFW_pb2.Real(value=0.0)
}

default_dict['SetCycleCount_Parameters'] = {
    'Channel': silaFW_pb2.Integer(value=0),
    'CycleCount': silaFW_pb2.Real(value=0.0)
}

default_dict['SetCycleCount_Responses'] = {
    'SetCycleCountSet': silaFW_pb2.String(value='')
}

default_dict['GetDispenseTimeMlMin_Parameters'] = {
    'Channel': silaFW_pb2.Integer(value=0),
    'Volume': silaFW_pb2.Real(value=0.0),
    'FlowRate': silaFW_pb2.Real(value=0.0)
}

default_dict['GetDispenseTimeMlMin_Responses'] = {
    'CurrentDispenseTime': silaFW_pb2.Real(value=0.0)
}

default_dict['GetDispenseTimeRPM_Parameters'] = {
    'Channel': silaFW_pb2.Integer(value=0),
    'Volume': silaFW_pb2.Real(value=0.0),
    'FlowRate': silaFW_pb2.Real(value=0.0)
}

default_dict['GetDispenseTimeRPM_Responses'] = {
    'CurrentDispenseTime': silaFW_pb2.Real(value=0.0)
}

default_dict['GetFlowRateAtModes_Parameters'] = {
    'Channel': silaFW_pb2.Integer(value=0)
}

default_dict['GetFlowRateAtModes_Responses'] = {
    'CurrentFlowRate': silaFW_pb2.Boolean(value=False)
}

default_dict['SetFlowRateAtModes_Parameters'] = {
    'Channel': silaFW_pb2.Integer(value=0),
    'FlowRate': silaFW_pb2.Real(value=0.0)
}

default_dict['SetFlowRateAtModes_Responses'] = {
    'SetFlowRateSet': silaFW_pb2.String(value='')
}


