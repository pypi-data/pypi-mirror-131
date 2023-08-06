from ..OpcuaClient import basemethod as bm
from enum import Enum as enum

#Make this kind of sequential indexing obsolete! Not implemented yet 
class MeasureControlDevices(enum):
    pH = 0
    DO = 1
    Temperature = 2
    Redox = 3
    Pressure = 4

class MeasureDevices(enum):
    Level  = 10

class ControlDevices(enum):
    Agitation  = 21
    PumpA= 22
    PumpB= 23
    PumpC= 24
    PumpD= 25

class GassingDevices(enum):
    Gassing  = 31

class OffgasDevices(enum):
    Offgas  = 41

class OverlayDevices(enum):
    Overlay  = 51

class TurbidityDevices(enum):
    Turbidity  = 61

class ReactorDevices(enum):
    Reactor  = 71

class IlluminationDevices(enum):
    Illumination  = 81

class DeviceDevices(enum):
    Device = 91

"""
Subunit definitions:
All subunits are made-up out of several base methods. Allowed get or set attributes can be defined here to be passed on to the base method. 
If not further specified, default get/set attributes are used. 
"""
class MeasureControl:
    path: str
    def __init__(self, client, parent_path, subunit_type: MeasureControlDevices):
        #if subunit_type in MeasureControlDevices.__members__:  
        if subunit_type == MeasureControlDevices.pH.name:
            self.path = parent_path + '/' + 'pH'
        elif subunit_type == MeasureControlDevices.DO.name:
            self.path = parent_path + '/' + 'DO'
        elif subunit_type == MeasureControlDevices.Temperature.name:
            self.path = parent_path + '/' + 'Temperature'
        elif subunit_type == MeasureControlDevices.Redox.name:
            self.path = parent_path + '/' + 'Redox'
        elif subunit_type == MeasureControlDevices.Pressure.name:
            self.path = parent_path + '/' + 'Pressure'
        else:
            pass

        self.setter = bm.Setter(client=client, opc_path=self.path)
        self.sysinfo = bm.SysInfo(client=client, opc_path=self.path)
        self.status = bm.Status(client=client, opc_path=self.path)
        self.alarm = bm.Alarm(client=client, opc_path=self.path + '/' + 'Alarm')
        self.controller = bm.Controller(client=client, opc_path=self.path + '/' + 'Controller')
        #Careful with Redox sensor. Slope is not defined on DASGIP server but is kept as viable command to OPC-UA node
        self.sensor = bm.Sensor(client=client, opc_path=self.path + '/' + 'Sensor')
        
class Measure:
    path = None
    def __init__(self, client, parent_path, subunit_type: MeasureDevices):
        if subunit_type == MeasureDevices.Level.name:
            self.path = parent_path + '/' + 'Level'
        else:
            pass
        self.setter = bm.Setter(
            client=client, 
            opc_path=self.path, 
            allowed_get=['PV'], 
            allowed_set=[]
            )
        self.sysinfo = bm.SysInfo(client=client, opc_path=self.path)
        self.alarm = bm.Alarm(client=client, opc_path=self.path + '/' + 'Alarm')
        self.sensor = bm.Sensor(client=client, opc_path=self.path + '/' + 'Sensor')

class Control:
    path = str
    def __init__(self, client, parent_path, subunit_type: ControlDevices):
        #For Pumps use allowed_get list
        allowed_get = ['PVInt', 'PV', 'SP', 'SPA', 'SPM', 'SPE', 'SPR', 'SetpointSelect']

        if subunit_type == ControlDevices.Agitation.name:
            self.path = parent_path + '/' + 'Agitation'
            self.setter = bm.Setter(client=client, opc_path=self.path, allowed_get=None, allowed_set=None)
        else: 
            pass

        if subunit_type == ControlDevices.PumpA.name:
            self.path = parent_path + '/' + 'PumpA'
            self.setter = bm.Setter(client=client, opc_path=self.path, allowed_get=allowed_get, allowed_set=None)
        elif subunit_type == ControlDevices.PumpB.name:
            self.path = parent_path + '/' + 'PumpB'
            self.setter = bm.Setter(client=client, opc_path=self.path, allowed_get=allowed_get, allowed_set=None)
        elif subunit_type == ControlDevices.PumpC.name:
            self.path = parent_path + '/' + 'PumpC'
            self.setter = bm.Setter(client=client, opc_path=self.path, allowed_get=allowed_get, allowed_set=None)
        elif subunit_type == ControlDevices.PumpD.name:
            self.path = parent_path + '/' + 'PumpD'
            self.setter = bm.Setter(client=client, opc_path=self.path, allowed_get=allowed_get, allowed_set=None)
        else:
            pass

        self.sysinfo = bm.SysInfo(client=client, opc_path=self.path)
        self.status = bm.Status(client=client, opc_path=self.path)
        self.actuator = bm.ActuatorControl(
            client=client, 
            opc_path=self.path + '/' + 'Actuator',
            allowed_get=None, 
            allowed_set=None
            )
    def __getattr__(self, attr):
        if attr in ['path', 'setter', 'sysinfo', 'actuator']:
            return object.__getattribute__(self, attr)

class Illumination:
    path = str
    def __init__(self, client, parent_path, subunit_type: IlluminationDevices):
        
        if subunit_type == IlluminationDevices.Illumination.name:
            self.path = parent_path + '/' + 'Illumination'
        else:
            pass
        self.sysinfo = bm.SysInfo(client=client, opc_path=self.path)
        self.actuatora = bm.ActuatorIllumination(client=client, opc_path=self.path + '/' + 'ActuatorA')
        self.actuatorb = bm.ActuatorIllumination(client=client, opc_path=self.path + '/' + 'ActuatorB')
        self.actuatorc = bm.ActuatorIllumination(client=client, opc_path=self.path + '/' + 'ActuatorC')

class Gassing:
    path: str
    def __init__(self, client, parent_path, subunit_type: GassingDevices):
        if subunit_type == GassingDevices.Gassing.name:
            self.path = parent_path + '/' + 'Gassing'

        else:
            pass
        allowedSetters = ['SP', 'SPA', 'SPM', 'SPE', 'SPR', 'Mode']
        MeasuredFlowsAndConcentrations= ['F', 'FAir', 'FO2', 'FN2', 'FCO2', 'XO2', 'XCO2']
        LogicFlowsAndConcentrations = ['F', 'XCO2', 'XO2']
        AllFlowsConcentrationsVolumetrics = ['F', 'FAir', 'XO2', 'XCO2', 'FO2', 'FN2', 'FCO2', 'V', 'VAir', 'VCO2', 'VO2', 'VN2' ]

        allowed_set = ['PV', 'SP', 'Access', 'Cmd', 'GassingMode', 'State']
        for i,cmd in enumerate(AllFlowsConcentrationsVolumetrics):
            tmp = ['%s.PV'%(cmd)]
            allowed_set.extend(tmp)
        for i,cmd in enumerate(MeasuredFlowsAndConcentrations):
            tmp = ['%sSetpointSelect'%(cmd)]
            allowed_set.extend(tmp)
            for j,setter in enumerate(allowedSetters):
                tmp = ['%s.%s'%(cmd,setter)]
                allowed_set.extend(tmp)
        for i,cmd in enumerate(LogicFlowsAndConcentrations):
            tmp = ['%s.SPL'%(cmd)]
            allowed_set.extend(tmp)

        allowed_get = allowed_set
        allowed_get.extend('PV')
        for i,cmd in enumerate(AllFlowsConcentrationsVolumetrics):
            tmp = ['%s.PV'%(cmd)]
            allowed_get.extend(tmp)

        self.setter = bm.Setter(
            client=client, 
            opc_path=self.path, 
            allowed_get=allowed_get, 
            allowed_set=allowed_set
            )

        self.sysinfo = bm.SysInfo(client=client, opc_path=self.path)
        allowed_get = ['Access', 'Cmd', 'GassingMode', 'State']
        allowed_set = ['Access', 'Cmd', 'GassingMode', 'State']
        self.status = bm.Status(client=client, opc_path=self.path, allowed_get=allowed_get, allowed_set=allowed_set)


    # Magic functions that translate the string for forbidden characters such as "." in python syntax that are necessary for node directory name.     
    def __getattr__(self, attr):
        if attr in ['path', 'setter', 'sysinfo', 'status']:
            return object.__getattribute__(self, attr)
        if attr.split('_', 1)[0] in ['F', 'FAir', 'FO2', 'FN2', 'FCO2', 'XO2', 'XCO2', 'V', 'VAir', 'VCO2', 'VO2', 'VN2']:
            return self.setter.__getattr__(attr.split('_', 1)[0]+'.'+attr.split('_', 1)[1])

    
    def __setattr__(self, attr, value):
        if attr in ['path', 'setter', 'sysinfo', 'status']:
            return object.__setattr__(self, attr, value)
        if attr.split('_', 1)[0] in ['F', 'FAir', 'FO2', 'FN2', 'FCO2', 'XO2', 'XCO2', 'V', 'VAir', 'VCO2', 'VO2', 'VN2']:
            return self.setter.__setattr__(attr.split('_', 1)[0]+'.'+attr.split('_', 1)[1], value)

class Offgas:
    path: str
    def __init__(self, client, parent_path, subunit_type: OffgasDevices):
        if subunit_type == OffgasDevices.Offgas.name:
            self.path = parent_path + '/' + 'Offgas'
        else:
            pass

        allowed_set = []
        allowedGetter = ['CTR', 'F', 'OTR', 'RQ', 'XCO2', 'XO2', 'VCT', 'VOT']
        allowed_get = []
        for i,cmd in enumerate(allowedGetter):
            tmp = ['%s.PV'%(cmd)]
            allowed_get.extend(tmp)
        print(allowed_get)

        self.sysinfo = bm.SysInfo(client=client, opc_path=self.path)
        self.status = bm.Status(
            client=client, 
            opc_path=self.path,
            allowed_get=['State'], 
            allowed_set=[]
            )
        self.setter = bm.Setter(
            client=client, 
            opc_path=self.path, 
            allowed_get=allowed_get, 
            allowed_set=allowed_set
            )

    # Magic functions that translate the string for forbidden characters such as "." in python syntax that are necessary for node directory name.     
    def __getattr__(self, attr):
        if attr in ['path', 'setter', 'sysinfo','status']:
            return object.__getattribute__(self, attr)
        if attr.split('_', 1)[0] in ['CTR', 'F', 'OTR', 'RQ', 'XCO2', 'XO2', 'VCT', 'VOT']:
            return self.setter.__getattr__(attr.split('_', 1)[0]+'.'+attr.split('_', 1)[1])
    
    def __setattr__(self, attr, value):
        if attr in ['path', 'setter', 'sysinfo', 'status']:
            return object.__setattr__(self, attr, value)
        if attr.split('_', 1)[0] in ['CTR', 'F', 'OTR', 'RQ', 'XCO2', 'XO2', 'VCT', 'VOT']:
            return self.setter.__setattr__(attr.split('_', 1)[0]+'.'+attr.split('_', 1)[1], value)

class Overlay:
    path: str
    def __init__(self, client, parent_path, subunit_type: OverlayDevices):
        if subunit_type == OverlayDevices.Overlay.name:
            self.path = parent_path + '/' + 'Overlay'
        else:
            pass
        allowedSetters = ['SP', 'SPA', 'SPM', 'SPE', 'SPR', 'Mode']
        MeasuredFlowsAndConcentrations= ['F', 'FAir', 'FO2', 'FN2', 'FCO2', 'XO2', 'XCO2']
        LogicFlowsAndConcentrations = ['F', 'XCO2', 'XO2']
        AllFlowsConcentrationsVolumetrics = ['F', 'FAir', 'XO2', 'XCO2', 'FO2', 'FN2', 'FCO2', 'V', 'VAir', 'VCO2', 'VO2', 'VN2' ]

        allowed_set = ['PV', 'SP', 'Access', 'Cmd', 'GassingMode', 'State']
        for i,cmd in enumerate(AllFlowsConcentrationsVolumetrics):
            tmp = ['%s.PV'%(cmd)]
            allowed_set.extend(tmp)
        for i,cmd in enumerate(MeasuredFlowsAndConcentrations):
            tmp = ['%sSetpointSelect'%(cmd)]
            allowed_set.extend(tmp)
            for j,setter in enumerate(allowedSetters):
                tmp = ['%s.%s'%(cmd,setter)]
                allowed_set.extend(tmp)
        for i,cmd in enumerate(LogicFlowsAndConcentrations):
            tmp = ['%s.SPL'%(cmd)]
            allowed_set.extend(tmp)

        allowed_get = allowed_set
        allowed_get.extend('PV')
        for i,cmd in enumerate(AllFlowsConcentrationsVolumetrics):
            tmp = ['%s.PV'%(cmd)]
            allowed_get.extend(tmp)

        self.setter = bm.Setter(
            client=client, 
            opc_path=self.path, 
            allowed_get=allowed_get, 
            allowed_set=allowed_set
            )

        self.sysinfo = bm.SysInfo(client=client, opc_path=self.path)
        allowed_get = ['Access', 'Cmd', 'GassingMode', 'State']
        allowed_set = ['Access', 'Cmd', 'GassingMode', 'State']
        self.status = bm.Status(client=client, opc_path=self.path, allowed_get=allowed_get, allowed_set=allowed_set)


    # Magic functions that translate the string for forbidden characters such as "." in python syntax that are necessary for node directory name.     
    def __getattr__(self, attr):
        if attr in ['path', 'setter', 'sysinfo', 'status']:
            return object.__getattribute__(self, attr)
        if attr.split('_', 1)[0] in ['F', 'FAir', 'FO2', 'FN2', 'FCO2', 'XO2', 'XCO2', 'V', 'VAir', 'VCO2', 'VO2', 'VN2']:
            return self.setter.__getattr__(attr.split('_', 1)[0]+'.'+attr.split('_', 1)[1])

    
    def __setattr__(self, attr, value):
        if attr in ['path', 'setter', 'sysinfo', 'status']:
            return object.__setattr__(self, attr, value)
        if attr.split('_', 1)[0] in ['F', 'FAir', 'FO2', 'FN2', 'FCO2', 'XO2', 'XCO2', 'V', 'VAir', 'VCO2', 'VO2', 'VN2']:
            return self.setter.__setattr__(attr.split('_', 1)[0]+'.'+attr.split('_', 1)[1], value)

class Turbidity:
    path: str
    def __init__(self, client, parent_path, subunit_type: TurbidityDevices):
        if subunit_type == TurbidityDevices.Turbidity.name:
            self.path = parent_path + '/' + 'Turbidity'
        else:
            pass
        print(self.path)
        allowed_set = []
        allowedGetters = ['AU', 'CX']
        allowed_get = []
        for i,cmd in enumerate(allowedGetters):
            tmp = ['%s.PV'%(cmd)]
            allowed_get.extend(tmp)
        
        self.sysinfo = bm.SysInfo(client=client, opc_path=self.path)
        self.setter = bm.Setter(
            client=client, 
            opc_path=self.path, 
            allowed_get=allowed_get, 
            allowed_set=allowed_set
            )

    # Magic functions that translate the string for forbidden characters such as "." in python syntax that are necessary for node directory name.     
    def __getattr__(self, attr):
        if attr in ['path', 'setter', 'sysinfo']:
            return object.__getattribute__(self, attr)
        if attr.split('_', 1)[0] in ['AU', 'CX']:
            return self.setter.__getattr__(attr.split('_', 1)[0]+'.'+attr.split('_', 1)[1]) 
    
    def __setattr__(self, attr, value):
        if attr in ['path', 'setter', 'sysinfo']:
            return object.__setattr__(self, attr, value)
        if attr.split('_', 1)[0] in ['AU', 'CX']:
            return self.setter.__setattr__(attr.split('_', 1)[0]+'.'+attr.split('_', 1)[1], value)

class Reactor:
    path: str
    def __init__(self, client, parent_path, subunit_type: ReactorDevices):
        if subunit_type == ReactorDevices.Reactor.name:
            self.path = parent_path + '/' + 'Reactor'
        else:
            pass

        allowed_set = ['VInitial', 'VLiquid', 'VMax', 'VMin', 'VTotal']
        allowed_get = ['VInitial', 'VLiquid', 'VMax', 'VMin', 'VTotal']
        self.sysinfo = bm.SysInfo(client=client, opc_path=self.path)
        self.setter = bm.Setter(
            client=client, 
            opc_path=self.path, 
            allowed_get=allowed_get, 
            allowed_set=allowed_set
            )

class Device:
    path: str
    def __init__(self, client, parent_path, subunit_type: DeviceDevices):
        if subunit_type == DeviceDevices.Device.name:
            self.path = parent_path
        else:
            pass

        allowed_get = ['Available', 'RuntimeClock', 'StartedUTC', 'Started', 'StoppedUTC', 'Stopped', 'UserId', 'BatchId', 'InoculatedUTC', 'Inoculated', 'Available', 'Name', 'Version']      
        allowed_set = [] 
        self.service = bm.Service(
            client=client,
            opc_path=self.path,
            allowed_get=allowed_get,
            allowed_set=allowed_set
        )
