import RegloICCService_client as testclient


#client = testclient.RegloICCServiceClient(server_ip='10.152.248.22', server_port=50008)
client = testclient.RegloICCServiceClient(server_ip='10.152.248.35', server_port=55001)
a = client.Get_ImplementedFeatures()
print(a)
print(a[3].value)

b = client.Get_FeatureDefinition(a[2].value)


print(b)