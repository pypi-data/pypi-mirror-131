import time
import numpy as np
import RegloICCService_client as client

"""
Test-program for DASGIP interface
Every command possible should be executed once to check for bugs in the implementation. 
In order to avoid an active change of values when invoking set-commands, set-commands 
will be executed after the respective get-command, using the current value that was recieved 
by the get-command. Each feature will have its own test routine that will be invoked in THIS 
file. 

Each test file should include a simple get/set command for each function. Logic functions
could be used, but aren't totally necessary, e.g is the "low" value smaller than the "high" 
value. 
"""

#Define the implemented features that should be actively executed and tested for functionality
implemented_features = ['CalibrationServicer', 'ConfigurationServicer', 'ParameterControlServicer']#'DriveControlServicer']#,
                                                                                         # 'ParameterControlServicer']
                                                                        #'DeviceServicer'
#Create the client object
var = client.RegloICCServiceClient()

#Start a timer for performance measurements
time_start = time.time()

#Get a list of all implemented functions defined in the SiLA Client
#All functions that are defined in the feature .xml files as commands 
#will be in this list
variables = [i for i in dir(var) if not callable(i)]

# Create a dictionnary of all features and their respective functions split up into the respective
# get and set commands for each feature
tmp=var.Get_ImplementedFeatures()[:]
feature_dict = {}
feature_resp_get_dict ={}
feature_resp_set_dict ={}
print(tmp)
#In order to create a object call like var.PHServicer_GetPV(1).CurrentPV.value
#the call must be reconstrucetd automatically by joining 'feature-name'_'function'.'function-response'.value
#Cycle through each feature to get 'feature-name'
for i, feature in enumerate(var.Get_ImplementedFeatures()):
    feature_dict["%s_get"%tmp[i].value] = list()
    feature_dict["%s_set"%tmp[i].value] = list()
    
    #Create a dict entry for the feature_get and feauture_set commands
    #containing the respective commands of this feature, 'function'
    for j, cmd in enumerate(variables):
        if "%s_Get"%tmp[i].value in variables[j]:
            feature_dict["%s_get"%tmp[i].value].append(cmd)
        elif "%s_Set"%tmp[i].value in variables[j]:
            feature_dict["%s_set"%tmp[i].value].append(cmd)
        else:
            pass
    feature = tmp[i].value
    
    #Import proto files of each feature to retrieve the 'function-response', i.e. 'CurrentPV'.
    #Exclude SiLAService as there is no proto file for this feature
    if feature not in ["SiLAService", "SimulationController"]:
        #print("%s.gRPC.%s_pb2"%(feature,feature))
        resp_get=list()
        resp_set=list()
        module = __import__("%s.gRPC.%s_pb2"%(feature,feature),fromlist=[''])

        #Search the file for the respective function_response of the 'get'-commands in the form 
        #'_GETPV_RESPONSES'
        for i, cmd in enumerate(feature_dict["%s_get"%feature]):
            cmd = cmd.split('_')[1]
            cmd = cmd.upper()
            cmd = "_%s_RESPONSES"%cmd
            k = getattr(module, "%s"%cmd)
            l = getattr(k, "fields")  

            #l[i].name returns the desired string of the response variable   
            for i,var in enumerate(l):
                resp_get.append(l[i].name)
            #print(module)
        feature_resp_get_dict["%s_get"%feature] = resp_get
        
        #Search the file for the respective function_response of the 'set'-commands in the form 
        #'_SETSP_RESPONSES'
        for i, cmd in enumerate(feature_dict["%s_set"%feature]):
            cmd = cmd.split('_')[1]
            cmd = cmd.upper()
            cmd = "_%s_RESPONSES"%cmd
            k = getattr(module, "%s"%cmd)
            l = getattr(k, "fields")  
            #l[i].name returns the desired string of the response variable   
            for i,var in enumerate(l):
                resp_set.append(l[i].name)
        feature_resp_set_dict["%s_set"%feature] = resp_set
    else:
        pass

#Construct the object calls from the feature and function dictionnaries created above
var = client.RegloICCServiceClient() #Probably unnecessary/ Remove during next test

#Create a dict of the get-function to store their respective response values
#The response values will be used as input for the set-commands in order to 
#keep the actual set values unchanged throughout the testing procedure.
get_values_dict = {}
import csv

for i,feature in enumerate(feature_dict):
    #print(i,feature)
    for j, function in enumerate(feature_dict[feature]):
        #old: if "PHServicer" in function:
        if any(string in function for string in implemented_features):
            if "_Get" in function:
                k = getattr(var, "%s" % function)
                # print(k)
                #print(feature)
                print(feature_resp_get_dict["%s" % feature][j])
                print(getattr(k(1), "%s" % feature_resp_get_dict["%s" % feature][j]))
                l = getattr(k(1), "%s" % feature_resp_get_dict["%s" % feature][j])
                if feature in ["DeviceServicer_get"]:
                    #print(l)
                    get_values_dict['%s' % function] = l
                else:
                    #print(l.value)
                    ##print(feature_resp_get_dict["%s"%feature])
                    get_values_dict['%s'%function] = l.value
                #print(get_values_dict['%s'%function])
        if any(string in function for string in implemented_features):
            if "_Set" in function:
                try:
                    ##print("Feature: %s ; Function: %s"%(feature,function))
                    tmp1 = function.split("_Set")[0]
                    tmp2 = function.split("_Set")[1]
                    #print(tmp1, tmp2)
                    ##print("%s_Get%s"%(tmp1, tmp2))
                    #print(get_values_dict["%s_Get%s"%(tmp1, tmp2)])
                    k = getattr(var, "%s"%function)
                    ##print(k)
                    ##print(feature_resp_get_dict["%s"%feature][j])
                    if "%s_Get%s"%(tmp1, tmp2) in get_values_dict:
                        value = get_values_dict["%s_Get%s"%(tmp1, tmp2)]
                    else:
                        value = 0
                    print(get_values_dict)
                    print("THIS IS VALUE %s"%value)
                    print(value)
                    l = getattr(k(1, value), "%s" % feature_resp_set_dict["%s" % feature][j])
                except:
                    value = 0
                    l = getattr(k(1, value), "%s" % feature_resp_set_dict["%s" % feature][j])
                    print("%s: No corresponding get command available. Setting value to 0." % feature_resp_set_dict["%s" % feature][j])


                #print(feature_dict['AgitationServicer_get'])
#print(feature_dict['AgitationServicer_set'])
#print(get_values_dict)
#print(get_values_dict.keys())
# Write a file with all DASGIP default values as a backup if the set commands go awry.
w = csv.writer(open("output_get_cmd.csv", "w"),  delimiter=';')      
for key, val in get_values_dict.items():
    w.writerow([key, val])

time_now = time.time()
time_diff = time_now-time_start
print(time_diff)