
class TestDOServicerGet:
    """ Test all DOServicer Get functions. Control a DASGIP DO module. Enables read and write operations for various parameters, including DO sensor, controller, and alarm. """



class TestGassingServicerSet:
    """ Test all GassingServicer Set functions. """


class TestIlluminationServicerGet:
    """ Test all IlluminationServicer Get functions."""


class TestLevelServicer:
""" Test all LevelServicer Get functions """



class TestOffgasServicerGet:
    """ Test all OffgasServicer Get functions. Control a DASGIP offgas module. Enables read and write operations for various parameters.  """



class TestOverlayServicer:
    """ Test all OverlayServicer Get functions """


# todo: sort this list somehow?

Pumps A-D = basic
AgitationServicer = basic + little Actuator stuff
ReactorServicer = only minimal Volume stuff
OffgasServicer = basic + minimal new features
TurbidityServicer = basic + minimal new features

IlluminationServicer = basic + (a lot of Actuator)
OverlayServicer = basic + lots of stuff
GassingServicer = basic + maybe equal to Overlay (or Offgas)

pressure servicer (basic + controller -Alarms
LevelServicer = basic + Alarm + slope etc

pH servicer = Redox servicer = DOServicer = (basic + Controler + Alarms)
TemperatureServicer = basic + Sensor + COntroller + Alarm




class TestPHServicer:
""" Test all PHServicer Get functions """


class TestPressureServicerGet:
""" Test all PressureServicer Get functions. Control a DASGIP pressure module. Enables read and write operations for various parameters, including pressure sensor and controller.  """
    sila_client = DASGIP_ServiceClient(server_ip=ip, server_port=port)


# outsourced -> 97 tests
class TestPumpAServicer:
    """ Test all PumpAServicer Get functions """

class TestPumpBServicer:
    """ Test all PumpBServicer Get functions """

class TestPumpCServicer:
""" Test all PumpCServicer Get functions """

class TestPumpDServicerGet:
    """ Test all PumpDServicer Get functions """



class TestReactorServicerGet:
    """ Test all ReactorServicer Get functions """



class TestRedoxServicerGet:
    """ Test all RedoxServicer Get functions. Control a DASGIP Redox module. Enables read and write operations for various parameters, including Redox sensor, controller, and alarm.  """




class TestTemperatureServicerSet:
""" Test all TemperatureServicer Set functions. Control a DASGIP temperature module. Enables read and write operations for various parameters, including temperature sensor, controller, and alarm. """




class TestTurbidityServicer:
    """ Test all TurbidityServicer Get functions """

