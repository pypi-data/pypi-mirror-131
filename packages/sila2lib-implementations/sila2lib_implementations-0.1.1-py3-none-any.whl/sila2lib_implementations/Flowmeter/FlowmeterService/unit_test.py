import FlowmeterService_client

from sila2lib.framework import SiLAFramework_pb2 as silaFW_pb2

from AlarmService.gRPC import AlarmService_pb2


client = FlowmeterService_client.FlowmeterServiceClient(server_ip='127.0.0.1', server_port=50004)
client.run()

# Response get
responses = []
response = client.GetIdentificationString()
responses.append(response)
response = client.GetPrimaryNodeAddress()
responses.append(response)
response = client.GetSecondaryNodeAddress()
responses.append(response)
response = client.GetNextNodeAddress()
responses.append(response)
response = client.GetLastNodeAddress()
responses.append(response)
response = client.GetSensorType()
responses.append(response)
response = client.GetAlarmInformation()
responses.append(response)
response = client.GetDeviceType()
responses.append(response)
response = client.GetFirmwareVersion()
responses.append(response)
response = client.GetPressureSensorType()
responses.append(response)
response = client.GetSensorName()
responses.append(response)
response = client.GetIdentificationNumber()
responses.append(response)
response = client.GetPowerMode()
responses.append(response)
response = client.GetBusDiagnostic()
responses.append(response)
response = client.GetFieldbus()
responses.append(response)
response = client.GetInstrumentProperties()
responses.append(response)
response = client.GetAlarmLimitMaximum()
responses.append(response)
response = client.GetAlarmLimitMaximum()
responses.append(response)
response = client.GetAlarmLimitMaximum()
responses.append(response)
# print(response)



print(responses)

#response = client.SetAlarmLimitMaximum(parameter=AlarmService_pb2.SetAlarmLimitMaximum_Parameters(SetAlarmLimitMaximum=silaFW_pb2.Real(value=(0))))





# response set
#response = client.GetAlarmLimitMaximum()