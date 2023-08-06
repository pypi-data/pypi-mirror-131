# This file contains default values that are used for the implementations to supply them with 
#   working, albeit mostly useless arguments.
#   You can also use this file as an example to create your custom responses. Feel free to remove
#   Once you have replaced every occurrence of the defaults with more reasonable values.
#   Or you continue using this file, supplying good defaults..

# import the required packages
import sila2lib.framework.SiLAFramework_pb2 as silaFW_pb2
import sila2lib.framework.SiLABinaryTransfer_pb2 as silaBinary_pb2
from .gRPC import MeasurementSettingsService_pb2 as pb2

# initialise the default dictionary so we can add keys. 
#   We need to do this separately/add keys separately, so we can access keys already defined e.g.
#   for the use in data type identifiers
default_dict = dict()


default_dict['GetPistonOperationMode_Parameters'] = {
    
}

default_dict['GetPistonOperationMode_Responses'] = {
    'CurrentPistonOperationMode': silaFW_pb2.String(value='default string')
}

default_dict['SetPistonOperationMode_Parameters'] = {
    'SetPistonOperationMode': silaFW_pb2.String(value='default string')
}

default_dict['SetPistonOperationMode_Responses'] = {
    'Status': silaFW_pb2.String(value='default string'),
    'IndexPointing': silaFW_pb2.String(value='default string')
}

default_dict['GetTimeOut_Parameters'] = {
    
}

default_dict['GetTimeOut_Responses'] = {
    'CurrentTimeOut': silaFW_pb2.Integer(value=0)
}

default_dict['SetTimeOut_Parameters'] = {
    'SetTimeOut': silaFW_pb2.Integer(value=0)
}

default_dict['SetTimeOut_Responses'] = {
    'Status': silaFW_pb2.String(value='default string'),
    'IndexPointing': silaFW_pb2.String(value='default string')
}

default_dict['GetFrequency_Parameters'] = {
    
}

default_dict['GetFrequency_Responses'] = {
    'CurrentFrequency': silaFW_pb2.Real(value=0.0)
}

default_dict['SetFrequency_Parameters'] = {
    'SetFrequency': silaFW_pb2.Real(value=0.0)
}

default_dict['SetFrequency_Responses'] = {
    'Status': silaFW_pb2.String(value='default string'),
    'IndexPointing': silaFW_pb2.String(value='default string')
}

default_dict['GetDensityActual_Parameters'] = {
    
}

default_dict['GetDensityActual_Responses'] = {
    'CurrentDensity': silaFW_pb2.String(value='default string')
}

default_dict['SetDensityActual_Parameters'] = {
    'SetDensityActual': silaFW_pb2.String(value='default string')
}

default_dict['SetDensityActual_Responses'] = {
    'Status': silaFW_pb2.String(value='default string'),
    'IndexPointing': silaFW_pb2.String(value='default string')
}

default_dict['GetPressureInlet_Parameters'] = {
    
}

default_dict['GetPressureInlet_Responses'] = {
    'CurrentPressureInlet': silaFW_pb2.Real(value=0.0)
}

default_dict['SetPressureInlet_Parameters'] = {
    'SetPressureInlet': silaFW_pb2.Real(value=0.0)
}

default_dict['SetPressureInlet_Responses'] = {
    'Status': silaFW_pb2.String(value='default string'),
    'IndexPointing': silaFW_pb2.String(value='default string')
}

default_dict['GetPressureOutlet_Parameters'] = {
    
}

default_dict['GetPressureOutlet_Responses'] = {
    'CurrentPressureInlet': silaFW_pb2.Real(value=0.0)
}

default_dict['SetPressureOutlet_Parameters'] = {
    'SetPressureOutlet': silaFW_pb2.Real(value=0.0)
}

default_dict['SetPressureOutlet_Responses'] = {
    'Status': silaFW_pb2.String(value='default string'),
    'IndexPointing': silaFW_pb2.String(value='default string')
}

default_dict['GetFluidTemperature_Parameters'] = {
    
}

default_dict['GetFluidTemperature_Responses'] = {
    'CurrentFluidTemperature': silaFW_pb2.Real(value=0.0)
}

default_dict['SetFluidTemperature_Parameters'] = {
    'SetFluidTemperature': silaFW_pb2.Real(value=0.0)
}

default_dict['SetFluidTemperature_Responses'] = {
    'Status': silaFW_pb2.String(value='default string'),
    'IndexPointing': silaFW_pb2.String(value='default string')
}

default_dict['GetThermalConductivity_Parameters'] = {
    
}

default_dict['GetThermalConductivity_Responses'] = {
    'CurrentThermalConductivity': silaFW_pb2.Real(value=0.0)
}

default_dict['SetThermalConductivity_Parameters'] = {
    'SetThermalConductivity': silaFW_pb2.Real(value=0.0)
}

default_dict['SetThermalConductivity_Responses'] = {
    'Status': silaFW_pb2.String(value='default string'),
    'IndexPointing': silaFW_pb2.String(value='default string')
}

default_dict['GetStandardMassFlow_Parameters'] = {
    
}

default_dict['GetStandardMassFlow_Responses'] = {
    'CurrentStandardMassFlow': silaFW_pb2.Real(value=0.0)
}

default_dict['SetStandardMassFlow_Parameters'] = {
    'SetStandardFlow': silaFW_pb2.Real(value=0.0)
}

default_dict['SetStandardMassFlow_Responses'] = {
    'Status': silaFW_pb2.String(value='default string'),
    'IndexPointing': silaFW_pb2.String(value='default string')
}

default_dict['GetOrificeDiameter_Parameters'] = {
    
}

default_dict['GetOrificeDiameter_Responses'] = {
    'CurrentOrificeDiameter': silaFW_pb2.String(value='default string')
}

default_dict['SetOrificeDiameter_Parameters'] = {
    'SetOrificeDiameter': silaFW_pb2.String(value='default string')
}

default_dict['SetOrificeDiameter_Responses'] = {
    'Status': silaFW_pb2.String(value='default string'),
    'IndexPointing': silaFW_pb2.String(value='default string')
}

default_dict['GetBarometerPressure_Parameters'] = {
    
}

default_dict['GetBarometerPressure_Responses'] = {
    'CurrentBarometerPressure': silaFW_pb2.Real(value=0.0)
}

default_dict['SetBarometerPressure_Parameters'] = {
    'SetBarometerPressure': silaFW_pb2.Real(value=0.0)
}

default_dict['SetBarometerPressure_Responses'] = {
    'Status': silaFW_pb2.String(value='default string'),
    'IndexPointing': silaFW_pb2.String(value='default string')
}

default_dict['GetNumberVanes_Parameters'] = {
    
}

default_dict['GetNumberVanes_Responses'] = {
    'CurrentNumberVanes': silaFW_pb2.String(value='default string')
}

default_dict['SetNumberVanes_Parameters'] = {
    'SetNumberVanes': silaFW_pb2.String(value='default string')
}

default_dict['SetNumberVanes_Responses'] = {
    'Status': silaFW_pb2.String(value='default string'),
    'IndexPointing': silaFW_pb2.String(value='default string')
}


