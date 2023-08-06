import numpy as np
import LAUDA_ThermostatService_client as client
#from sila2lib import SiLAFramework_pb2 as fwpb2
#import TemperatureSetpointController_pb2
#import TemperatureSetpointController_pb2_grpc


var = client.LAUDA_ThermostatServiceClient()
print(var)
#print(var.Get_FeatureDefinition("TemperatureControlServicer"))
#print(var.Get_ImplementedFeatures())
#print(var.Get_FeatureDefinition("SimulationController"))
a = var.TemperatureControlServicer_SetPointTemperature(10)
print(a.SetTemperatureSet.value)
#var.StartRealMode()
