# This file contains default values that are used for the implementations to supply them with 
#   working, albeit mostly useless arguments.
#   You can also use this file as an example to create your custom responses. Feel free to remove
#   Once you have replaced every occurrence of the defaults with more reasonable values.
#   Or you continue using this file, supplying good defaults..

# import the required packages
import sila2lib.framework.SiLAFramework_pb2 as silaFW_pb2
import sila2lib.framework.SiLABinaryTransfer_pb2 as silaBinary_pb2
from .gRPC import DeviceServicer_pb2 as pb2

# initialise the default dictionary so we can add keys. 
#   We need to do this separately/add keys separately, so we can access keys already defined e.g.
#   for the use in data type identifiers
default_dict = dict()


default_dict['GetLog_Parameters'] = {
    
}

default_dict['GetLog_Responses'] = {
    'CurrentLogLevel': silaFW_pb2.String(value='default string'),
    #'CurrentLogTimestamp': silaFW_pb2.Timestamp(value=2020-04-16T10:19:57+0000),
    'CurrentLogTimestamp': silaFW_pb2.Timestamp(
        second=0,
        minute=0,
        hour=0,
        day=0,
        month=0,
        year=0,
        timezone=silaFW_pb2.Timezone(
            hours=00,
            minutes=00
        )
    ),
    'CurrentLogMessage': silaFW_pb2.String(value='default string')
}

default_dict['SetPumpAddress_Parameters'] = {
    'Address': silaFW_pb2.Integer(value=0)
}

default_dict['SetPumpAddress_Responses'] = {
    'PumpAddressSet': silaFW_pb2.String(value='')
}

default_dict['SetLanguage_Parameters'] = {
    'Address': silaFW_pb2.Integer(value=0),
    'Language': silaFW_pb2.Integer(value=0)
}

default_dict['SetLanguage_Responses'] = {
    'LanguageSet': silaFW_pb2.String(value='')
}

default_dict['GetLanguage_Parameters'] = {
    'Address': silaFW_pb2.Integer(value=0)
}

default_dict['GetLanguage_Responses'] = {
    'CurrentLanguage': silaFW_pb2.Integer(value=0)
}

default_dict['GetPumpStatus_Parameters'] = {
    'Address': silaFW_pb2.Integer(value=0)
}

default_dict['GetPumpStatus_Responses'] = {
    'CurrentPumpStatus': silaFW_pb2.String(value='')
}

default_dict['GetVersionType_Parameters'] = {
    'Address': silaFW_pb2.Integer(value=0)
}

default_dict['GetVersionType_Responses'] = {
    'CurrentVersionType': silaFW_pb2.String(value='')
}

default_dict['CurrentVersionSoftware_Parameters'] = {
    'Address': silaFW_pb2.Integer(value=0)
}

default_dict['CurrentVersionSoftware_Responses'] = {
    'CurrentVersionSoftware': silaFW_pb2.String(value='')
}

default_dict['GetSerialNumber_Parameters'] = {
    'Address': silaFW_pb2.Integer(value=0)
}

default_dict['GetSerialNumber_Responses'] = {
    'SerialNumber': silaFW_pb2.String(value='')
}

default_dict['SetChannelAddressing_Parameters'] = {
    'Address': silaFW_pb2.Integer(value=0),
    'ChannelAddressing': silaFW_pb2.Boolean(value=False)
}

default_dict['SetChannelAddressing_Responses'] = {
    'ChannelAddressingSet': silaFW_pb2.String(value='')
}

default_dict['GetChannelAddressing_Parameters'] = {
    'Address': silaFW_pb2.Integer(value=0)
}

default_dict['GetChannelAddressing_Responses'] = {
    'ChannelAddressing': silaFW_pb2.Boolean(value=False)
}

default_dict['SetEventMessages_Parameters'] = {
    'Address': silaFW_pb2.Integer(value=0),
    'EventMessages': silaFW_pb2.Boolean(value=False)
}

default_dict['SetEventMessages_Responses'] = {
    'EventMessagesSet': silaFW_pb2.String(value='')
}

default_dict['GetEventMessages_Parameters'] = {
    'Address': silaFW_pb2.Integer(value=0)
}

default_dict['GetEventMessages_Responses'] = {
    'EventMessages': silaFW_pb2.Boolean(value=False)
}

default_dict['GetSerialProtocol_Parameters'] = {
    'Address': silaFW_pb2.Integer(value=0)
}

default_dict['GetSerialProtocol_Responses'] = {
    'SerialProtocol': silaFW_pb2.Integer(value=0)
}

default_dict['SetPumpName_Parameters'] = {
    'Address': silaFW_pb2.Integer(value=0),
    'PumpName': silaFW_pb2.String(value='')
}

default_dict['SetPumpName_Responses'] = {
    'PumpNameSet': silaFW_pb2.String(value='')
}

default_dict['GetChannelNumber_Parameters'] = {
    'Address': silaFW_pb2.Integer(value=0)
}

default_dict['GetChannelNumber_Responses'] = {
    'ChannelNumber': silaFW_pb2.Integer(value=0)
}

default_dict['SetChannelNumber_Parameters'] = {
    'Address': silaFW_pb2.Integer(value=0),
    'ChannelNumber': silaFW_pb2.Integer(value=0)
}

default_dict['SetChannelNumber_Responses'] = {
    'ChannelNumberSet': silaFW_pb2.String(value='')
}

default_dict['GetRevolutions_Parameters'] = {
    'Channel': silaFW_pb2.Integer(value=0)
}

default_dict['GetRevolutions_Responses'] = {
    'Revolutions': silaFW_pb2.Integer(value=0)
}

default_dict['GetChannelTotalVolume_Parameters'] = {
    'Channel': silaFW_pb2.Real(value=0.0)
}

default_dict['GetChannelTotalVolume_Responses'] = {
    'ChannelTotalVolume': silaFW_pb2.Real(value=0.0)
}

default_dict['GetTotalTime_Parameters'] = {
    'Channel': silaFW_pb2.Integer(value=0)
}

default_dict['GetTotalTime_Responses'] = {
    'TotalTime': silaFW_pb2.Integer(value=0)

}

default_dict['GetHeadModel_Parameters'] = {
    'Address': silaFW_pb2.Integer(value=0)
}

default_dict['GetHeadModel_Responses'] = {
    'HeadModel': silaFW_pb2.String(value='')
}

default_dict['SetHeadModel_Parameters'] = {
    'Address': silaFW_pb2.Integer(value=0),
    'HeadModel': silaFW_pb2.String(value='')
}

default_dict['SetHeadModel_Responses'] = {
    'HeadModelSet': silaFW_pb2.String(value='')
}

default_dict['SetUserInterface_Parameters'] = {
    'UserInterface': silaFW_pb2.String(value='')
}

default_dict['SetUserInterface_Responses'] = {
    'UserInterfaceSet': silaFW_pb2.String(value='')
}

default_dict['SetDisableInterface_Parameters'] = {
    'DisableInterface': silaFW_pb2.String(value='')
}

default_dict['SetDisableInterface_Responses'] = {
    'DisableInterfaceSet': silaFW_pb2.String(value='')
}

default_dict['SetDisplayNumbers_Parameters'] = {
    'Address': silaFW_pb2.Integer(value=0),
    'DisplayNumbers': silaFW_pb2.String(value='')
}

default_dict['SetDisplayNumbers_Responses'] = {
    'DisplayNumbersSet': silaFW_pb2.String(value='')
}

default_dict['SetDisplayLetters_Parameters'] = {
    'Address': silaFW_pb2.String(value=''),
    'DisplayLetters': silaFW_pb2.String(value='')
}

default_dict['SetDisplayLetters_Responses'] = {
    'DisplayLettersSet': silaFW_pb2.String(value='')
}

default_dict['GetTimeSetting_Parameters'] = {
    'Channel': silaFW_pb2.Integer(value=0)
}

default_dict['GetTimeSetting_Responses'] = {
    'TimeSetting': silaFW_pb2.Real(value=0.0)
}

default_dict['SetTimeSetting_Parameters'] = {
    'Channel': silaFW_pb2.Integer(value=0),
    'TimeSetting': silaFW_pb2.Real(value=0.0)
}

default_dict['SetTimeSetting_Responses'] = {
    'TimeSettingSet': silaFW_pb2.String(value='')
}

default_dict['SetRunTimeM_Parameters'] = {
    'Channel': silaFW_pb2.Integer(value=0),
    'RunTimeM': silaFW_pb2.Integer(value=0)
}

default_dict['SetRunTimeM_Responses'] = {
    'RunTimeMSet': silaFW_pb2.String(value='')
}

default_dict['SetRunTimeH_Parameters'] = {
    'Channel': silaFW_pb2.Integer(value=0),
    'RunTimeM': silaFW_pb2.Integer(value=0)
}

default_dict['SetRunTimeH_Responses'] = {
    'RunTimeHSet': silaFW_pb2.String(value='')
}

default_dict['GetRollerStepsLow_Parameters'] = {
    'Channel': silaFW_pb2.Integer(value=0)
}

default_dict['GetRollerStepsLow_Responses'] = {
    'RollerStepsLow': silaFW_pb2.Integer(value=0)
}

default_dict['SetRollerStepsLow_Parameters'] = {
    'Channel': silaFW_pb2.Integer(value=0),
    'RollerStepsLow': silaFW_pb2.Integer(value=0)
}

default_dict['SetRollerStepsLow_Responses'] = {
    'RollerStepsLowSet': silaFW_pb2.String(value='')
}

default_dict['GetRollerStepsHigh_Parameters'] = {
    'Channel': silaFW_pb2.Integer(value=0)
}

default_dict['GetRollerStepsHigh_Responses'] = {
    'RollerStepsHigh': silaFW_pb2.Integer(value=0)
}

default_dict['SetRollerStepsHigh_Parameters'] = {
    'Channel': silaFW_pb2.Integer(value=0),
    'RollerSteps': silaFW_pb2.Integer(value=0)
}

default_dict['SetRollerStepsHigh_Responses'] = {
    'RollerStepsHighSet': silaFW_pb2.String(value='')
}

default_dict['GetRSV_Parameters'] = {
    'Channel': silaFW_pb2.Integer(value=0)
}

default_dict['GetRSV_Responses'] = {
    'RSV': silaFW_pb2.Real(value=0.0)
}

default_dict['SetRSV_Parameters'] = {
    'Channel': silaFW_pb2.Real(value=0.0),
    'RSV': silaFW_pb2.Real(value=0.0)
}

default_dict['SetRSV_Responses'] = {
    'RSVSet': silaFW_pb2.String(value='')
}

default_dict['SetRSVReset_Parameters'] = {
    'RSVReset': silaFW_pb2.String(value='')
}

default_dict['SetRSVReset_Responses'] = {
    'RSVResetSet': silaFW_pb2.String(value='')
}

default_dict['ResetRSVTable_Parameters'] = {
    'RSVTableReset': silaFW_pb2.String(value='')
}

default_dict['ResetRSVTable_Responses'] = {
    'ResetRSVTableSet': silaFW_pb2.String(value='')
}

default_dict['SetNonFactoryRSV_Parameters'] = {
    'Channel': silaFW_pb2.Integer(value=0),
    'RollerCount': silaFW_pb2.Integer(value=0),
    'TubingID': silaFW_pb2.String(value=''),
    'NonFactoryRSV': silaFW_pb2.Real(value=0.0)
}

default_dict['SetNonFactoryRSV_Responses'] = {
    'SetNonFactoryRSVSet': silaFW_pb2.String(value='')
}

default_dict['GetPauseTime_Parameters'] = {
    'Channel': silaFW_pb2.Integer(value=0)
}

default_dict['GetPauseTime_Responses'] = {
    'PauseTime': silaFW_pb2.Real(value=0.0)
}

default_dict['SetPauseTime_Parameters'] = {
    'Channel': silaFW_pb2.Integer(value=0),
    'PauseTime': silaFW_pb2.Real(value=0.0)
}

default_dict['SetPauseTime_Responses'] = {
    'PauseTimeSet': silaFW_pb2.String(value='')
}

default_dict['SetPauseTimeM_Parameters'] = {
    'Channel': silaFW_pb2.Integer(value=0),
    'PauseTimeM': silaFW_pb2.Integer(value=0)
}

default_dict['SetPauseTimeM_Responses'] = {
    'PauseTimeMSet': silaFW_pb2.String(value='')
}

default_dict['SetPauseTimeH_Parameters'] = {
    'Channel': silaFW_pb2.Integer(value=0),
    'PauseTimeM': silaFW_pb2.Integer(value=0)
}

default_dict['SetPauseTimeH_Responses'] = {
    'PauseTimeHSet': silaFW_pb2.String(value='')
}

default_dict['GetTotalVolume_Parameters'] = {
    'Channel': silaFW_pb2.Integer(value=0)
}

default_dict['GetTotalVolume_Responses'] = {
    'CurrentTotalVolume': silaFW_pb2.Real(value=0.0)
}

default_dict['SaveSettings_Parameters'] = {
    'PumpAddress': silaFW_pb2.Integer(value=0)
}

default_dict['SaveSettings_Responses'] = {
    'Save': silaFW_pb2.String(value='')
}

default_dict['SaveSetRoller_Parameters'] = {
    'PumpAddress': silaFW_pb2.Integer(value=0)
}

default_dict['SaveSetRoller_Responses'] = {
    'Save': silaFW_pb2.String(value='')
}

default_dict['GetFootSwitchStatus_Parameters'] = {
    'PumpAddress': silaFW_pb2.Integer(value=0)
}

default_dict['GetFootSwitchStatus_Responses'] = {
    'FootSwitchStatus': silaFW_pb2.String(value='')
}

default_dict['SetRollersNumber_Parameters'] = {
    'Channel': silaFW_pb2.Integer(value=0),
    'RollersNumber': silaFW_pb2.Integer(value=0)
}

default_dict['SetRollersNumber_Responses'] = {
    'RollersNumber': silaFW_pb2.String(value='')
}

default_dict['GetRollersNumber_Parameters'] = {
    'Channel': silaFW_pb2.Integer(value=0)
}

default_dict['GetRollersNumber_Responses'] = {
    'RollersNumber': silaFW_pb2.Integer(value=0)
}

default_dict['SetPumpSerialNumber_Parameters'] = {
    'Address': silaFW_pb2.String(value=''),
    'PumpSerialNumber': silaFW_pb2.String(value='')
}

default_dict['SetPumpSerialNumber_Responses'] = {
    'PumpSerialNumberSet': silaFW_pb2.String(value='')
}

default_dict['Subscribe_CurrentStatus_Responses'] = {
    'CurrentStatus': silaFW_pb2.String(value='default string')
}
