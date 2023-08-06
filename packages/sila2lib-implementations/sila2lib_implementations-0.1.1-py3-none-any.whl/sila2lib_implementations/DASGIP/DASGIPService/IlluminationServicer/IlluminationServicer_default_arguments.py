# This file contains default values that are used for the implementations to supply them with 
#   working, albeit mostly useless arguments.
#   You can also use this file as an example to create your custom responses. Feel free to remove
#   Once you have replaced every occurrence of the defaults with more reasonable values.
#   Or you continue using this file, supplying good defaults..

# import the required packages
import sila2lib.framework.SiLAFramework_pb2 as silaFW_pb2
import sila2lib.framework.SiLABinaryTransfer_pb2 as silaBinary_pb2
from .gRPC import IlluminationServicer_pb2 as pb2

# initialise the default dictionary so we can add keys. 
#   We need to do this separately/add keys separately, so we can access keys already defined e.g.
#   for the use in data type identifiers
default_dict = dict()


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

default_dict['GetActuatorAPV_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetActuatorAPV_Responses'] = {
    'CurrentActuatorAPV': silaFW_pb2.Real(value=0.0)
}

default_dict['GetActuatorAPVInt_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetActuatorAPVInt_Responses'] = {
    'CurrentActuatorAPVInt': silaFW_pb2.Real(value=0.0)
}

default_dict['GetActuatorASource_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetActuatorASource_Responses'] = {
    'CurrentActuatorASource': silaFW_pb2.String(value='default string')
}

default_dict['SetActuatorASPM_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0),
    'ActuatorASPM': silaFW_pb2.Real(value=0.0)
}

default_dict['SetActuatorASPM_Responses'] = {
    'ActuatorASPMSet': silaFW_pb2.Real(value=0.0)
}

default_dict['SetActuatorASPE_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0),
    'ActuatorASPE': silaFW_pb2.Real(value=0.0)
}

default_dict['SetActuatorASPE_Responses'] = {
    'ActuatorASPESet': silaFW_pb2.Real(value=0.0)
}

default_dict['GetActuatorASP_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetActuatorASP_Responses'] = {
    'CurrentActuatorASP': silaFW_pb2.Real(value=0.0)
}

default_dict['GetActuatorASPA_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetActuatorASPA_Responses'] = {
    'CurrentActuatorASPA': silaFW_pb2.Real(value=0.0)
}

default_dict['GetActuatorASPM_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetActuatorASPM_Responses'] = {
    'CurrentActuatorASPM': silaFW_pb2.Real(value=0.0)
}

default_dict['GetActuatorASPE_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetActuatorASPE_Responses'] = {
    'CurrentActuatorASPE': silaFW_pb2.Real(value=0.0)
}

default_dict['GetActuatorASPR_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetActuatorASPR_Responses'] = {
    'CurrentActuatorASPR': silaFW_pb2.Real(value=0.0)
}

default_dict['SetActuatorAMode_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0),
    'ActuatorAMode': silaFW_pb2.Integer(value=0)
}

default_dict['SetActuatorAMode_Responses'] = {
    'ActuatorAModeSet': silaFW_pb2.Integer(value=0)
}

default_dict['GetActuatorAMode_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetActuatorAMode_Responses'] = {
    'CurrentActuatorAMode': silaFW_pb2.Integer(value=0)
}

default_dict['SetActuatorASetpointSelect_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0),
    'ActuatorASetpointSelect': silaFW_pb2.Integer(value=0)
}

default_dict['SetActuatorASetpointSelect_Responses'] = {
    'ActuatorASetpointSelectSet': silaFW_pb2.Integer(value=0)
}

default_dict['GetActuatorASetpointSelect_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetActuatorASetpointSelect_Responses'] = {
    'CurrentActuatorASetpointSelect': silaFW_pb2.Integer(value=0)
}

default_dict['GetActuatorAAvailable_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetActuatorAAvailable_Responses'] = {
    'CurrentActuatorAAvailable': silaFW_pb2.Integer(value=0)
}

default_dict['GetActuatorAName_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetActuatorAName_Responses'] = {
    'CurrentActuatorAName': silaFW_pb2.String(value='default string')
}

default_dict['GetActuatorBPV_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetActuatorBPV_Responses'] = {
    'CurrentActuatorBPV': silaFW_pb2.Real(value=0.0)
}

default_dict['GetActuatorBPVInt_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetActuatorBPVInt_Responses'] = {
    'CurrentActuatorBPVInt': silaFW_pb2.Real(value=0.0)
}

default_dict['GetActuatorBSource_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetActuatorBSource_Responses'] = {
    'CurrentActuatorBSource': silaFW_pb2.String(value='default string')
}

default_dict['SetActuatorBSPM_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0),
    'ActuatorBSPM': silaFW_pb2.Real(value=0.0)
}

default_dict['SetActuatorBSPM_Responses'] = {
    'ActuatorBSPMSet': silaFW_pb2.Real(value=0.0)
}

default_dict['SetActuatorBSPE_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0),
    'ActuatorBSPE': silaFW_pb2.Real(value=0.0)
}

default_dict['SetActuatorBSPE_Responses'] = {
    'ActuatorBSPESet': silaFW_pb2.Real(value=0.0)
}

default_dict['GetActuatorBSP_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetActuatorBSP_Responses'] = {
    'CurrentActuatorBSP': silaFW_pb2.Real(value=0.0)
}

default_dict['GetActuatorBSPA_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetActuatorBSPA_Responses'] = {
    'CurrentActuatorBSPA': silaFW_pb2.Real(value=0.0)
}

default_dict['GetActuatorBSPM_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetActuatorBSPM_Responses'] = {
    'CurrentActuatorBSPM': silaFW_pb2.Real(value=0.0)
}

default_dict['GetActuatorBSPE_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetActuatorBSPE_Responses'] = {
    'CurrentActuatorBSPE': silaFW_pb2.Real(value=0.0)
}

default_dict['GetActuatorBSPR_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetActuatorBSPR_Responses'] = {
    'CurrentActuatorBSPR': silaFW_pb2.Real(value=0.0)
}

default_dict['SetActuatorBMode_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0),
    'ActuatorBMode': silaFW_pb2.Integer(value=0)
}

default_dict['SetActuatorBMode_Responses'] = {
    'ActuatorBModeSet': silaFW_pb2.Integer(value=0)
}

default_dict['GetActuatorBMode_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetActuatorBMode_Responses'] = {
    'CurrentActuatorBMode': silaFW_pb2.Integer(value=0)
}

default_dict['SetActuatorBSetpointSelect_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0),
    'ActuatorBSetpointSelect': silaFW_pb2.Integer(value=0)
}

default_dict['SetActuatorBSetpointSelect_Responses'] = {
    'ActuatorBSetpointSelectSet': silaFW_pb2.Integer(value=0)
}

default_dict['GetActuatorBSetpointSelect_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetActuatorBSetpointSelect_Responses'] = {
    'CurrentActuatorBSetpointSelect': silaFW_pb2.Integer(value=0)
}

default_dict['GetActuatorBAvailable_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetActuatorBAvailable_Responses'] = {
    'CurrentActuatorBAvailable': silaFW_pb2.Integer(value=0)
}

default_dict['GetActuatorBName_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetActuatorBName_Responses'] = {
    'CurrentActuatorBName': silaFW_pb2.String(value='default string')
}

default_dict['GetActuatorCPV_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetActuatorCPV_Responses'] = {
    'CurrentActuatorCPV': silaFW_pb2.Real(value=0.0)
}

default_dict['GetActuatorCPVInt_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetActuatorCPVInt_Responses'] = {
    'CurrentActuatorCPVInt': silaFW_pb2.Real(value=0.0)
}

default_dict['GetActuatorCSource_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetActuatorCSource_Responses'] = {
    'CurrentActuatorCSource': silaFW_pb2.String(value='default string')
}

default_dict['SetActuatorCSPM_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0),
    'ActuatorCSPM': silaFW_pb2.Real(value=0.0)
}

default_dict['SetActuatorCSPM_Responses'] = {
    'ActuatorCSPMSet': silaFW_pb2.Real(value=0.0)
}

default_dict['SetActuatorCSPE_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0),
    'ActuatorCSPE': silaFW_pb2.Real(value=0.0)
}

default_dict['SetActuatorCSPE_Responses'] = {
    'ActuatorCSPESet': silaFW_pb2.Real(value=0.0)
}

default_dict['GetActuatorCSP_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetActuatorCSP_Responses'] = {
    'CurrentActuatorCSP': silaFW_pb2.Real(value=0.0)
}

default_dict['GetActuatorCSPA_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetActuatorCSPA_Responses'] = {
    'CurrentActuatorCSPA': silaFW_pb2.Real(value=0.0)
}

default_dict['GetActuatorCSPM_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetActuatorCSPM_Responses'] = {
    'CurrentActuatorCSPM': silaFW_pb2.Real(value=0.0)
}

default_dict['GetActuatorCSPE_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetActuatorCSPE_Responses'] = {
    'CurrentActuatorCSPE': silaFW_pb2.Real(value=0.0)
}

default_dict['GetActuatorCSPR_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetActuatorCSPR_Responses'] = {
    'CurrentActuatorCSPR': silaFW_pb2.Real(value=0.0)
}

default_dict['SetActuatorCMode_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0),
    'ActuatorCMode': silaFW_pb2.Integer(value=0)
}

default_dict['SetActuatorCMode_Responses'] = {
    'ActuatorCModeSet': silaFW_pb2.Integer(value=0)
}

default_dict['GetActuatorCMode_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetActuatorCMode_Responses'] = {
    'CurrentActuatorCMode': silaFW_pb2.Integer(value=0)
}

default_dict['SetActuatorCSetpointSelect_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0),
    'ActuatorCSetpointSelect': silaFW_pb2.Integer(value=0)
}

default_dict['SetActuatorCSetpointSelect_Responses'] = {
    'ActuatorCSetpointSelectSet': silaFW_pb2.Integer(value=0)
}

default_dict['GetActuatorCSetpointSelect_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetActuatorCSetpointSelect_Responses'] = {
    'CurrentActuatorCSetpointSelect': silaFW_pb2.Integer(value=0)
}

default_dict['GetActuatorCAvailable_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetActuatorCAvailable_Responses'] = {
    'CurrentActuatorCAvailable': silaFW_pb2.Integer(value=0)
}

default_dict['GetActuatorCName_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetActuatorCName_Responses'] = {
    'CurrentActuatorCName': silaFW_pb2.String(value='default string')
}


