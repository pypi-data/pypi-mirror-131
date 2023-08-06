from ..OpcuaClient import subunit as su
from ..OpcuaClient import basemethod as bm
from opcua import Client


class Unit(bm.MethodExecutor):
    
    #Calculate size of list in advance. not implemented yet
    subunit: list
    unit_ID: int
    client: Client

    def __init__(self, client, unit_ID = None):
        
        if unit_ID is None:
            raise ValueError

        self.subunit = [None] * 99
        self.unit_ID = unit_ID

        # Store path to itself
        super().__init__(client=client, opc_path="/Root/Unit{number}".format(number=self.unit_ID))

        self.subunit[su.DeviceDevices.Device.value] = su.Device(client=self._client, parent_path=self._opc_path, subunit_type=su.DeviceDevices.Device.name)

        # LOADING SUBUNITS
        # Initalise MeasureControl subunits
        # [pH, DO, T, Redox, Pressure]
        self.subunit[su.MeasureControlDevices.pH.value] = su.MeasureControl(client=self._client, parent_path=self._opc_path, subunit_type=su.MeasureControlDevices.pH.name)
        self.subunit[su.MeasureControlDevices.DO.value] = su.MeasureControl(client=self._client, parent_path=self._opc_path, subunit_type=su.MeasureControlDevices.DO.name)
        self.subunit[su.MeasureControlDevices.Temperature.value] = su.MeasureControl(client=self._client, parent_path=self._opc_path, subunit_type=su.MeasureControlDevices.Temperature.name)
        self.subunit[su.MeasureControlDevices.Redox.value] = su.MeasureControl(client=self._client, parent_path=self._opc_path, subunit_type=su.MeasureControlDevices.Redox.name)
        self.subunit[su.MeasureControlDevices.Pressure.value] = su.MeasureControl(client=self._client, parent_path=self._opc_path, subunit_type=su.MeasureControlDevices.Pressure.name)

        # Initalise Measure subunits
        # [Level]
        self.subunit[su.MeasureDevices.Level.value] = su.Measure(client=self._client, parent_path=self._opc_path, subunit_type=su.MeasureDevices.Level.name)

        # Initalise Control subunits
        # [Agitation, PumpA, PumpB, PumpC, PumpD]
        self.subunit[su.ControlDevices.Agitation.value] = su.Control(client=self._client, parent_path=self._opc_path, subunit_type=su.ControlDevices.Agitation.name)
        self.subunit[su.ControlDevices.PumpA.value] = su.Control(client=self._client, parent_path=self._opc_path, subunit_type=su.ControlDevices.PumpA.name)
        self.subunit[su.ControlDevices.PumpB.value] = su.Control(client=self._client, parent_path=self._opc_path, subunit_type=su.ControlDevices.PumpB.name)
        self.subunit[su.ControlDevices.PumpC.value] = su.Control(client=self._client, parent_path=self._opc_path, subunit_type=su.ControlDevices.PumpC.name)
        self.subunit[su.ControlDevices.PumpD.value] = su.Control(client=self._client, parent_path=self._opc_path, subunit_type=su.ControlDevices.PumpD.name)

        # Initalise Illumination subunits
        # [Illumination]
        self.subunit[su.IlluminationDevices.Illumination.value] = su.Illumination(client=self._client, parent_path=self._opc_path, subunit_type=su.IlluminationDevices.Illumination.name)

        # Initalise Gassing subunits
        # [Gassing]
        self.subunit[su.GassingDevices.Gassing.value] = su.Gassing(client=self._client, parent_path=self._opc_path, subunit_type=su.GassingDevices.Gassing.name)
        
        # Initalise Offgassing subunits
        # [Offgas]
        self.subunit[su.OffgasDevices.Offgas.value] = su.Offgas(client=self._client, parent_path=self._opc_path, subunit_type=su.OffgasDevices.Offgas.name)
        
        # Initalise Overlay subunits
        # [Overlay]
        self.subunit[su.OverlayDevices.Overlay.value] = su.Overlay(client=self._client, parent_path=self._opc_path, subunit_type=su.OverlayDevices.Overlay.name)

        # Initalise Turbidity subunits
        # [Turbidity]
        self.subunit[su.TurbidityDevices.Turbidity.value] = su.Turbidity(client=self._client, parent_path=self._opc_path, subunit_type=su.TurbidityDevices.Turbidity.name)

        # Initalise Reactor Specification subunits
        # [Reactor]
        self.subunit[su.ReactorDevices.Reactor.value] = su.Reactor(client=self._client, parent_path=self._opc_path, subunit_type=su.ReactorDevices.Reactor.name)

        # Initalise Value subunits
        # [ExternalValues, InternalValues, OfflineValues]
        #self.subunit[su.GassingDevices.Gassing.value] = su.Gassing(client=self._client, parent_path=self._opc_path, subunit_type=su.GassingDevices.Gassing.name)



    def __getattr__(self, attr):
        map = {
            'pH': su.MeasureControlDevices.pH.value,
            'DO': su.MeasureControlDevices.DO.value,
            'Temperature': su.MeasureControlDevices.Temperature.value,
            'Redox': su.MeasureControlDevices.Redox.value,
            'Pressure': su.MeasureControlDevices.Pressure.value,
            'Level': su.MeasureDevices.Level.value,
            'Agitation': su.ControlDevices.Agitation.value,
            'PumpA': su.ControlDevices.PumpA.value,
            'PumpB': su.ControlDevices.PumpB.value,
            'PumpC': su.ControlDevices.PumpC.value,
            'PumpD': su.ControlDevices.PumpD.value,
            'Illumination': su.IlluminationDevices.Illumination.value,
            'Gassing':  su.GassingDevices.Gassing.value,
            'Offgas':   su.OffgasDevices.Offgas.value,
            'Overlay':  su.OverlayDevices.Overlay.value,
            'Turbidity':    su.TurbidityDevices.Turbidity.value,
            'Reactor':  su.ReactorDevices.Reactor.value,
            'Device': su.DeviceDevices.Device.value
        }
        if attr in map:
            return object.__getattribute__(self, 'subunit')[map[attr]]
        if attr in ['subunit', 'unit_ID']:
            return object.__getattribute__(self, attr)
        else:
            return super().__getattr__(attr)

    def __setattr__(self, attr, value):
        map = {
            'pH': su.MeasureControlDevices.pH.value,
            'DO': su.MeasureControlDevices.DO.value,
            'Temperature': su.MeasureControlDevices.Temperature.value,
            'Redox': su.MeasureControlDevices.Redox.value,
            'Level': su.MeasureDevices.Level.value,
            'Agitation': su.ControlDevices.Agitation.value,
            'PumpA': su.ControlDevices.PumpA.value,
            'PumpB': su.ControlDevices.PumpB.value,
            'PumpC': su.ControlDevices.PumpC.value,
            'PumpD': su.ControlDevices.PumpD.value,
            'Illumination': su.IlluminationDevices.Illumination.value,
            'Gassing':  su.GassingDevices.Gassing.value,
            'Offgas':   su.OffgasDevices.Offgas.value,
            'Overlay':  su.OverlayDevices.Overlay.value,
            'Turbidity':    su.TurbidityDevices.Turbidity.value,
            'Reactor':  su.ReactorDevices.Reactor.value,
            'Device': su.DeviceDevices.Device.value
        }
        if attr in map:
            return object.__setattr__(self, 'subunit')[map[attr]]
        if attr in ['subunit', 'unit_ID']:
            return object.__setattr__(self, attr, value)
        else:
            return super().__setattr__(attr, value)
