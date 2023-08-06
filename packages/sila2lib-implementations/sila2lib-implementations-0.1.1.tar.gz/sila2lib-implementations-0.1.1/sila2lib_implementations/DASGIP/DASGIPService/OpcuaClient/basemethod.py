from enum import Enum as enum

from typing import List
from opcua import Client, Node, ua
"""
Main method executor that uses magic function syntax to get and set attributes through the OPC-UA protocol.
Method executor is called upon by base methods of subunits.
"""
class MethodExecutor():
    allowed_get: List
    allowed_set: List

    _opc_path: str

    def __init__(self, client, opc_path):
        self.allowed_get = []
        self.allowed_set = []
        self._opc_path = opc_path
        self._client = client
        
    def __getattr__(self, attr):
        if attr in ['_opc_path', '_client', 'allowed_get', 'allowed_set']:
            return super().__getattribute__(attr)
        elif attr in self.allowed_get:
            print("Get-command: The path:ns=2;s="+ self._opc_path + '/' + attr)
            tmp = self._client.get_node("ns=2;s=" + self._opc_path + '/' + attr)
            return tmp
        else:
            raise AttributeError(('Cannot get %s. Not in allowed_get'%attr))
    
    def __setattr__(self, attr, value):
        if attr in ['_opc_path', '_client', 'allowed_get', 'allowed_set']:
            return object.__setattr__(self, attr, value)
        elif attr in self.allowed_set:
            print("Set-command: The path:ns=2;s="+ self._opc_path + '/' + attr)
            print("THIS IS VALUE:%s"%value)
            tmp = self._client.get_node("ns=2;s=" + self._opc_path + '/' + attr)
            #print("HERE!!!!!!!!!!%s"%tmp.get_data_type())
            #print("HERE!!!!!!!!!!%s"%tmp.get_data_type_as_variant_type())
            tmp.set_value(ua.Variant(value, tmp.get_data_type_as_variant_type()))

            return ("ns=2;s=" + self._opc_path + '/' + attr)
        else:
            raise AttributeError(('Cannot set %s. Not in allowed_set'%attr))
             
"""
BASE METHODS
"""
class Service(MethodExecutor):
    def __init__(self, client, opc_path, allowed_get=None, allowed_set=None):
        super().__init__(client=client, opc_path=opc_path) 

        if allowed_get == None:
            self.allowed_get = []
        else:
            self.allowed_get = allowed_get

        if allowed_set == None:
            self.allowed_set = []
        else:
            self.allowed_set = allowed_set
    #def __getattr__(self, attr):
    #    if attr in ['path']:
    #        return object.__getattribute__(self, attr)


class Setter(MethodExecutor):
    def __init__(self, client, opc_path, allowed_get=None, allowed_set=None):
        super().__init__(client=client, opc_path=opc_path) 

        if allowed_get == None:
            self.allowed_get = ['PV', 'SP', 'SPA', 'SPM', 'SPE', 'SPR', 'SetpointSelect']
        else:
            self.allowed_get = allowed_get

        if allowed_set == None:
            self.allowed_set = ['SPM', 'SPE', 'SetpointSelect']
        else:
            self.allowed_set = allowed_set
        

class SysInfo(MethodExecutor):
    def __init__(self, client, opc_path, allowed_get=None, allowed_set=None):
        super().__init__(client=client, opc_path=opc_path)  
        if allowed_get == None:
            self.allowed_get = ['Type', 'Available', 'Name', 'Version' ]    
        else:
            self.allowed_get = allowed_get

        if allowed_set == None:
            self.allowed_set = []
        else:
            self.allowed_set = allowed_set

class Status(MethodExecutor):
    def __init__(self, client, opc_path, allowed_get=None, allowed_set=None):
        super().__init__(client=client, opc_path=opc_path)  
        if allowed_get == None:
            self.allowed_get = ['Cmd', 'State', 'Mode', 'Access']     
        else:
            self.allowed_get = allowed_get

        if allowed_set == None:
            self.allowed_set = ['Cmd', 'Mode']   
        else:
            self.allowed_set = allowed_set

class Alarm(MethodExecutor):
    def __init__(self, client, opc_path, allowed_get=None, allowed_set=None):
        super().__init__(client=client, opc_path=opc_path)  
        if allowed_get == None:
            self.allowed_get = ['Enabled', 'AlarmHigh', 'AlarmLow', 'Mode', 'State', 'Delay', 'WarnHigh', 'WarnLow']   
        else:
            self.allowed_get = allowed_get

        if allowed_set == None:
            self.allowed_set = ['Enabled', 'AlarmHigh', 'AlarmLow', 'Mode', 'Delay', 'WarnHigh', 'WarnLow']  
        else:
            self.allowed_set = allowed_set

class Controller(MethodExecutor):
    def __init__(self, client, opc_path, allowed_get=None, allowed_set=None):
        super().__init__(client=client, opc_path=opc_path) 
        if allowed_get == None:
            self.allowed_get = ['DB', 'Out', 'P', 'Td', 'Ti', 'Min', 'Max']   
        else:
            self.allowed_get = allowed_get

        if allowed_set == None:
            self.allowed_set = ['DB', 'Out', 'P', 'Td', 'Ti', 'Min', 'Max']    
        else:
            self.allowed_set = allowed_set

class Sensor(MethodExecutor):
    def __init__(self, client, opc_path, allowed_get=None, allowed_set=None):
        super().__init__(client=client, opc_path=opc_path) 
        if allowed_get == None:
            self.allowed_get = ['Offset', 'PVRaw', 'Slope', 'Compensation']   
        else:
            self.allowed_get = allowed_get

        if allowed_set == None:
            self.allowed_set = ['Offset', 'PVRaw', 'Slope', 'Compensation']    
        else:
            self.allowed_set = allowed_set

class ActuatorControl(MethodExecutor):
    def __init__(self, client, opc_path, allowed_get=None, allowed_set=None):
        super().__init__(client=client, opc_path=opc_path) 
        if allowed_get == None:
            self.allowed_get = ['Calibration','Dir.PV', 'Pwr.PV', 'TStir.PV','Dir_PV']    

        else:
            self.allowed_get = allowed_get
            #self.allowed_get = ['Calibration','Dir.PV', 'Pwr.PV', 'TStir.PV','Dir_PV']  


        if allowed_set == None:
            self.allowed_set = ['Calibration']     
        else:
            self.allowed_set = allowed_set
    # Magic functions that translate the string for forbidden characters such as "." in python syntax that are necessary for node directory name.     
    def __getattr__(self, attr):
        if attr in ['path']:
            return object.__getattribute__(self, attr)
        if attr.split('_', 1)[0] in ['Dir', 'Pwr', 'TStir']:
            return super().__getattr__(attr.split('_', 1)[0]+'.'+attr.split('_', 1)[1])
        if attr in ['Calibration']:
            return super().__getattr__('Calibration')
    """
    Not needed since there are no variables to be set in ActuatorControl
    def __setattr__(self, attr, value):
        if attr in ['path', 'setter', 'actuator']:
            return object.__setattr__(self, attr, value)
        if attr.split('_', 1)[0] in []:
            return super().__setattr__(attr.split('_', 1)[0]+'.'+attr.split('_', 1)[1], value)
    """

class ActuatorIllumination(MethodExecutor):
    def __init__(self, client, opc_path, allowed_get=None, allowed_set=None):
        super().__init__(client=client, opc_path=opc_path) 
        if allowed_get == None:
            self.allowed_get = ['Name', 'Available', 'Mode', 'SetpointSelect', 'PV', 'PVInt', 'Source'
            'SP', 'SPA', 'SPM', 'SPE', 'SPR']       
        else:
            self.allowed_get = allowed_get

        if allowed_set == None:
            self.allowed_set = ['Mode', 'SetpointSelect', 'Source', 'SPM', 'SPE']           
        else:
            self.allowed_set = allowed_set
