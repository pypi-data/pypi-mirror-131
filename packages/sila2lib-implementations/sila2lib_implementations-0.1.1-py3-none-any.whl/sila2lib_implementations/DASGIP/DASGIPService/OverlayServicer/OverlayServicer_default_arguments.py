# This file contains default values that are used for the implementations to supply them with 
#   working, albeit mostly useless arguments.
#   You can also use this file as an example to create your custom responses. Feel free to remove
#   Once you have replaced every occurrence of the defaults with more reasonable values.
#   Or you continue using this file, supplying good defaults..

# import the required packages
import sila2lib.framework.SiLAFramework_pb2 as silaFW_pb2
import sila2lib.framework.SiLABinaryTransfer_pb2 as silaBinary_pb2
from .gRPC import OverlayServicer_pb2 as pb2

# initialise the default dictionary so we can add keys. 
#   We need to do this separately/add keys separately, so we can access keys already defined e.g.
#   for the use in data type identifiers
default_dict = dict()


default_dict['GetPV_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetPV_Responses'] = {
    'CurrentPV': silaFW_pb2.Real(value=0.0)
}

default_dict['GetSP_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetSP_Responses'] = {
    'CurrentSP': silaFW_pb2.Real(value=0.0)
}

default_dict['GetFPV_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetFPV_Responses'] = {
    'CurrentFPV': silaFW_pb2.Real(value=0.0)
}

default_dict['GetVPV_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetVPV_Responses'] = {
    'CurrentVPV': silaFW_pb2.Real(value=0.0)
}

default_dict['GetFSP_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetFSP_Responses'] = {
    'CurrentFSP': silaFW_pb2.Real(value=0.0)
}

default_dict['SetFSPM_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0),
    'FSPM': silaFW_pb2.Real(value=0.0)
}

default_dict['SetFSPM_Responses'] = {
    'FSPMSet': silaFW_pb2.Real(value=0.0)
}

default_dict['GetFSPM_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetFSPM_Responses'] = {
    'CurrentFSPM': silaFW_pb2.Real(value=0.0)
}

default_dict['SetFSPE_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0),
    'FSPE': silaFW_pb2.Real(value=0.0)
}

default_dict['SetFSPE_Responses'] = {
    'FSPESet': silaFW_pb2.Real(value=0.0)
}

default_dict['GetFSPE_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetFSPE_Responses'] = {
    'CurrentFSPE': silaFW_pb2.Real(value=0.0)
}

default_dict['GetFSPA_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetFSPA_Responses'] = {
    'CurrentFSPA': silaFW_pb2.Real(value=0.0)
}

default_dict['GetFSPR_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetFSPR_Responses'] = {
    'CurrentFSPR': silaFW_pb2.Real(value=0.0)
}

default_dict['GetFSPL_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetFSPL_Responses'] = {
    'CurrentFSPL': silaFW_pb2.Real(value=0.0)
}

default_dict['SetFMode_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0),
    'FMode': silaFW_pb2.Integer(value=0)
}

default_dict['SetFMode_Responses'] = {
    'FModeSet': silaFW_pb2.Integer(value=0)
}

default_dict['GetFMode_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetFMode_Responses'] = {
    'CurrentFMode': silaFW_pb2.Integer(value=0)
}

default_dict['SetFSetpointSelect_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0),
    'FSetpointSelect': silaFW_pb2.Integer(value=0)
}

default_dict['SetFSetpointSelect_Responses'] = {
    'FSetpointSelectSet': silaFW_pb2.Integer(value=0)
}

default_dict['GetFSetpointSelect_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetFSetpointSelect_Responses'] = {
    'CurrentFSetpointSelect': silaFW_pb2.Integer(value=0)
}

default_dict['GetXCO2PV_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetXCO2PV_Responses'] = {
    'CurrentXCO2PV': silaFW_pb2.Real(value=0.0)
}

default_dict['GetXCO2SP_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetXCO2SP_Responses'] = {
    'CurrentXCO2SP': silaFW_pb2.Real(value=0.0)
}

default_dict['SetXCO2SPM_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0),
    'XCO2SPM': silaFW_pb2.Real(value=0.0)
}

default_dict['SetXCO2SPM_Responses'] = {
    'XCO2SPMSet': silaFW_pb2.Real(value=0.0)
}

default_dict['GetXCO2SPM_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetXCO2SPM_Responses'] = {
    'CurrentXCO2SPM': silaFW_pb2.Real(value=0.0)
}

default_dict['SetXCO2SPE_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0),
    'XCO2SPE': silaFW_pb2.Real(value=0.0)
}

default_dict['SetXCO2SPE_Responses'] = {
    'XCO2SPESet': silaFW_pb2.Real(value=0.0)
}

default_dict['GetXCO2SPE_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetXCO2SPE_Responses'] = {
    'CurrentXCO2SPE': silaFW_pb2.Real(value=0.0)
}

default_dict['GetXCO2SPA_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetXCO2SPA_Responses'] = {
    'CurrentXCO2SPA': silaFW_pb2.Real(value=0.0)
}

default_dict['GetXCO2SPR_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetXCO2SPR_Responses'] = {
    'CurrentXCO2SPR': silaFW_pb2.Real(value=0.0)
}

default_dict['GetXCO2SPL_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetXCO2SPL_Responses'] = {
    'CurrentXCO2SPL': silaFW_pb2.Real(value=0.0)
}

default_dict['SetXCO2Mode_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0),
    'XCO2Mode': silaFW_pb2.Integer(value=0)
}

default_dict['SetXCO2Mode_Responses'] = {
    'XCO2ModeSet': silaFW_pb2.Integer(value=0)
}

default_dict['GetXCO2Mode_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetXCO2Mode_Responses'] = {
    'CurrentXCO2Mode': silaFW_pb2.Integer(value=0)
}

default_dict['SetXCO2SetpointSelect_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0),
    'XCO2SetpointSelect': silaFW_pb2.Integer(value=0)
}

default_dict['SetXCO2SetpointSelect_Responses'] = {
    'XCO2SetpointSelectSet': silaFW_pb2.Integer(value=0)
}

default_dict['GetXCO2SetpointSelect_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetXCO2SetpointSelect_Responses'] = {
    'CurrentXCO2SetpointSelect': silaFW_pb2.Integer(value=0)
}

default_dict['GetXO2PV_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetXO2PV_Responses'] = {
    'CurrentXO2PV': silaFW_pb2.Real(value=0.0)
}

default_dict['GetXO2SP_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetXO2SP_Responses'] = {
    'CurrentXO2SP': silaFW_pb2.Real(value=0.0)
}

default_dict['SetXO2SPM_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0),
    'XO2SPM': silaFW_pb2.Real(value=0.0)
}

default_dict['SetXO2SPM_Responses'] = {
    'XO2SPMSet': silaFW_pb2.Real(value=0.0)
}

default_dict['GetXO2SPM_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetXO2SPM_Responses'] = {
    'CurrentXO2SPM': silaFW_pb2.Real(value=0.0)
}

default_dict['SetXO2SPE_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0),
    'XO2SPE': silaFW_pb2.Real(value=0.0)
}

default_dict['SetXO2SPE_Responses'] = {
    'XO2SPESet': silaFW_pb2.Real(value=0.0)
}

default_dict['GetXO2SPE_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetXO2SPE_Responses'] = {
    'CurrentXO2SPE': silaFW_pb2.Real(value=0.0)
}

default_dict['GetXO2SPA_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetXO2SPA_Responses'] = {
    'CurrentXO2SPA': silaFW_pb2.Real(value=0.0)
}

default_dict['GetXO2SPR_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetXO2SPR_Responses'] = {
    'CurrentXO2SPR': silaFW_pb2.Real(value=0.0)
}

default_dict['GetXO2SPL_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetXO2SPL_Responses'] = {
    'CurrentXO2SPL': silaFW_pb2.Real(value=0.0)
}

default_dict['SetXO2Mode_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0),
    'XO2Mode': silaFW_pb2.Integer(value=0)
}

default_dict['SetXO2Mode_Responses'] = {
    'XO2ModeSet': silaFW_pb2.Integer(value=0)
}

default_dict['GetXO2Mode_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetXO2Mode_Responses'] = {
    'CurrentXO2Mode': silaFW_pb2.Integer(value=0)
}

default_dict['SetXO2SetpointSelect_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0),
    'XO2SetpointSelect': silaFW_pb2.Integer(value=0)
}

default_dict['SetXO2SetpointSelect_Responses'] = {
    'XO2SetpointSelectSet': silaFW_pb2.Integer(value=0)
}

default_dict['GetXO2SetpointSelect_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetXO2SetpointSelect_Responses'] = {
    'CurrentXO2SetpointSelect': silaFW_pb2.Integer(value=0)
}

default_dict['GetFAirPV_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetFAirPV_Responses'] = {
    'CurrentFAirPV': silaFW_pb2.Real(value=0.0)
}

default_dict['GetVAirPV_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetVAirPV_Responses'] = {
    'CurrentVAirPV': silaFW_pb2.Real(value=0.0)
}

default_dict['GetFAirSP_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetFAirSP_Responses'] = {
    'CurrentFAirSP': silaFW_pb2.Real(value=0.0)
}

default_dict['SetFAirSPM_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0),
    'FAirSPM': silaFW_pb2.Real(value=0.0)
}

default_dict['SetFAirSPM_Responses'] = {
    'FAirSPMSet': silaFW_pb2.Real(value=0.0)
}

default_dict['GetFAirSPM_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetFAirSPM_Responses'] = {
    'CurrentFAirSPM': silaFW_pb2.Real(value=0.0)
}

default_dict['SetFAirSPE_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0),
    'FAirSPE': silaFW_pb2.Real(value=0.0)
}

default_dict['SetFAirSPE_Responses'] = {
    'FAirSPESet': silaFW_pb2.Real(value=0.0)
}

default_dict['GetFAirSPE_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetFAirSPE_Responses'] = {
    'CurrentFAirSPE': silaFW_pb2.Real(value=0.0)
}

default_dict['GetFAirSPA_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetFAirSPA_Responses'] = {
    'CurrentFAirSPA': silaFW_pb2.Real(value=0.0)
}

default_dict['GetFAirSPR_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetFAirSPR_Responses'] = {
    'CurrentFAirSPR': silaFW_pb2.Real(value=0.0)
}

default_dict['SetFAirMode_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0),
    'FAirMode': silaFW_pb2.Integer(value=0)
}

default_dict['SetFAirMode_Responses'] = {
    'FAirModeSet': silaFW_pb2.Integer(value=0)
}

default_dict['GetFAirMode_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetFAirMode_Responses'] = {
    'CurrentFAirMode': silaFW_pb2.Integer(value=0)
}

default_dict['SetFAirSetpointSelect_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0),
    'FAirSetpointSelect': silaFW_pb2.Integer(value=0)
}

default_dict['SetFAirSetpointSelect_Responses'] = {
    'FAirSetpointSelectSet': silaFW_pb2.Integer(value=0)
}

default_dict['GetFAirSetpointSelect_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetFAirSetpointSelect_Responses'] = {
    'CurrentFAirSetpointSelect': silaFW_pb2.Integer(value=0)
}

default_dict['GetFO2PV_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetFO2PV_Responses'] = {
    'CurrentFO2PV': silaFW_pb2.Real(value=0.0)
}

default_dict['GetVO2PV_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetVO2PV_Responses'] = {
    'CurrentVO2PV': silaFW_pb2.Real(value=0.0)
}

default_dict['GetFO2SP_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetFO2SP_Responses'] = {
    'CurrentFO2SP': silaFW_pb2.Real(value=0.0)
}

default_dict['SetFO2SPM_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0),
    'FO2SPM': silaFW_pb2.Real(value=0.0)
}

default_dict['SetFO2SPM_Responses'] = {
    'FO2SPMSet': silaFW_pb2.Real(value=0.0)
}

default_dict['GetFO2SPM_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetFO2SPM_Responses'] = {
    'CurrentFO2SPM': silaFW_pb2.Real(value=0.0)
}

default_dict['SetFO2SPE_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0),
    'FO2SPE': silaFW_pb2.Real(value=0.0)
}

default_dict['SetFO2SPE_Responses'] = {
    'FO2SPESet': silaFW_pb2.Real(value=0.0)
}

default_dict['GetFO2SPE_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetFO2SPE_Responses'] = {
    'CurrentFO2SPE': silaFW_pb2.Real(value=0.0)
}

default_dict['GetFO2SPA_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetFO2SPA_Responses'] = {
    'CurrentFO2SPA': silaFW_pb2.Real(value=0.0)
}

default_dict['GetFO2SPR_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetFO2SPR_Responses'] = {
    'CurrentFO2SPR': silaFW_pb2.Real(value=0.0)
}

default_dict['SetFO2Mode_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0),
    'FO2Mode': silaFW_pb2.Integer(value=0)
}

default_dict['SetFO2Mode_Responses'] = {
    'FO2ModeSet': silaFW_pb2.Integer(value=0)
}

default_dict['GetFO2Mode_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetFO2Mode_Responses'] = {
    'CurrentFO2Mode': silaFW_pb2.Integer(value=0)
}

default_dict['SetFO2SetpointSelect_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0),
    'FO2SetpointSelect': silaFW_pb2.Integer(value=0)
}

default_dict['SetFO2SetpointSelect_Responses'] = {
    'FO2SetpointSelectSet': silaFW_pb2.Integer(value=0)
}

default_dict['GetFO2SetpointSelect_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetFO2SetpointSelect_Responses'] = {
    'CurrentFO2SetpointSelect': silaFW_pb2.Integer(value=0)
}

default_dict['GetFCO2PV_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetFCO2PV_Responses'] = {
    'CurrentFCO2PV': silaFW_pb2.Real(value=0.0)
}

default_dict['GetVCO2PV_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetVCO2PV_Responses'] = {
    'CurrentVCO2PV': silaFW_pb2.Real(value=0.0)
}

default_dict['GetFCO2SP_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetFCO2SP_Responses'] = {
    'CurrentFCO2SP': silaFW_pb2.Real(value=0.0)
}

default_dict['SetFCO2SPM_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0),
    'FCO2SPM': silaFW_pb2.Real(value=0.0)
}

default_dict['SetFCO2SPM_Responses'] = {
    'FCO2SPMSet': silaFW_pb2.Real(value=0.0)
}

default_dict['GetFCO2SPM_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetFCO2SPM_Responses'] = {
    'CurrentFCO2SPM': silaFW_pb2.Real(value=0.0)
}

default_dict['SetFCO2SPE_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0),
    'FCO2SPE': silaFW_pb2.Real(value=0.0)
}

default_dict['SetFCO2SPE_Responses'] = {
    'FCO2SPESet': silaFW_pb2.Real(value=0.0)
}

default_dict['GetFCO2SPE_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetFCO2SPE_Responses'] = {
    'CurrentFCO2SPE': silaFW_pb2.Real(value=0.0)
}

default_dict['GetFCO2SPA_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetFCO2SPA_Responses'] = {
    'CurrentFCO2SPA': silaFW_pb2.Real(value=0.0)
}

default_dict['GetFCO2SPR_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetFCO2SPR_Responses'] = {
    'CurrentFCO2SPR': silaFW_pb2.Real(value=0.0)
}

default_dict['SetFCO2Mode_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0),
    'FCO2Mode': silaFW_pb2.Integer(value=0)
}

default_dict['SetFCO2Mode_Responses'] = {
    'FCO2ModeSet': silaFW_pb2.Integer(value=0)
}

default_dict['GetFCO2Mode_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetFCO2Mode_Responses'] = {
    'CurrentFCO2Mode': silaFW_pb2.Integer(value=0)
}

default_dict['SetFCO2SetpointSelect_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0),
    'FCO2SetpointSelect': silaFW_pb2.Integer(value=0)
}

default_dict['SetFCO2SetpointSelect_Responses'] = {
    'FCO2SetpointSelectSet': silaFW_pb2.Integer(value=0)
}

default_dict['GetFCO2SetpointSelect_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetFCO2SetpointSelect_Responses'] = {
    'CurrentFCO2SetpointSelect': silaFW_pb2.Integer(value=0)
}

default_dict['GetFN2PV_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetFN2PV_Responses'] = {
    'CurrentFN2PV': silaFW_pb2.Real(value=0.0)
}

default_dict['GetVN2PV_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetVN2PV_Responses'] = {
    'CurrentVN2PV': silaFW_pb2.Real(value=0.0)
}

default_dict['GetFN2SP_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetFN2SP_Responses'] = {
    'CurrentFN2SP': silaFW_pb2.Real(value=0.0)
}

default_dict['SetFN2SPM_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0),
    'FN2SPM': silaFW_pb2.Real(value=0.0)
}

default_dict['SetFN2SPM_Responses'] = {
    'FN2SPMSet': silaFW_pb2.Real(value=0.0)
}

default_dict['GetFN2SPM_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetFN2SPM_Responses'] = {
    'CurrentFN2SPM': silaFW_pb2.Real(value=0.0)
}

default_dict['SetFN2SPE_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0),
    'FN2SPE': silaFW_pb2.Real(value=0.0)
}

default_dict['SetFN2SPE_Responses'] = {
    'FN2SPESet': silaFW_pb2.Real(value=0.0)
}

default_dict['GetFN2SPE_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetFN2SPE_Responses'] = {
    'CurrentFN2SPE': silaFW_pb2.Real(value=0.0)
}

default_dict['GetFN2SPA_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetFN2SPA_Responses'] = {
    'CurrentFN2SPA': silaFW_pb2.Real(value=0.0)
}

default_dict['GetFN2SPR_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetFN2SPR_Responses'] = {
    'CurrentFN2SPR': silaFW_pb2.Real(value=0.0)
}

default_dict['SetFN2Mode_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0),
    'FN2Mode': silaFW_pb2.Integer(value=0)
}

default_dict['SetFN2Mode_Responses'] = {
    'FN2ModeSet': silaFW_pb2.Integer(value=0)
}

default_dict['GetFN2Mode_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetFN2Mode_Responses'] = {
    'CurrentFN2Mode': silaFW_pb2.Integer(value=0)
}

default_dict['SetFN2SetpointSelect_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0),
    'FN2SetpointSelect': silaFW_pb2.Integer(value=0)
}

default_dict['SetFN2SetpointSelect_Responses'] = {
    'FN2SetpointSelectSet': silaFW_pb2.Integer(value=0)
}

default_dict['GetFN2SetpointSelect_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetFN2SetpointSelect_Responses'] = {
    'CurrentFN2SetpointSelect': silaFW_pb2.Integer(value=0)
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

default_dict['SetGassingMode_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0),
    'GassingMode': silaFW_pb2.Integer(value=0)
}

default_dict['SetGassingMode_Responses'] = {
    'GassingModeSet': silaFW_pb2.Integer(value=0)
}

default_dict['GetGassingMode_Parameters'] = {
    'UnitID': silaFW_pb2.Integer(value=0)
}

default_dict['GetGassingMode_Responses'] = {
    'CurrentGassingMode': silaFW_pb2.Integer(value=0)
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


