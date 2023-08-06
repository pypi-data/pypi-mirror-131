import BlueVaryService_client as client

ip = "127.0.0.1"
#ip = "10.152.248.108"
port = 50001
unit_1 = client.BlueVaryServiceClient(server_ip=ip, server_port=port)

#print(unit_1.SensorServicer_GetResults().O2.value)

#print(unit_1.SensorServicer_GetHumidity().Humidity.value)
#print(unit_1.SensorServicer_GetHumidity().Temperature.value)
#print(unit_1.SensorServicer_GetHumidity().AbsoluteHumidity.value)


#print(unit_1.SensorServicer_GetHumidity().AbsoluteHumidity.value)
a = unit_1.Get_ImplementedFeatures()

print(a)
print(a[2].value)
b = unit_1.Get_FeatureDefinition(str.encode(a[2].value))

print(b)