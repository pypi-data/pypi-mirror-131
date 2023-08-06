import _reglo_lib as lib  # -> predefined Classes

p = lib.Pump()

'''
Vorpumpen -> 17.8ml vom Reaktor zu Vorratsbehälter
Begasung : 120 stL/h,  N(reaktor)=200U/min
'''

#print(p.pump_set_volume_at_flow_rate(channels=[1], flowrate=[27], volume=[97.8], rotation=['K']))
#print(p.pump_set_volume_at_flow_rate(channels=[1,2,3,4], volume=[100, 100, 100, 100], rotation=['K', 'K', 'K', 'K']))
#print(p.pump_set_volume_at_flow_rate(channels=[2], volume=[10], rotation=['J']))
print(p.pump_time_at_flow_rate(channels=[1], runtime=[240], rotation=['K']))
#time.sleep(5)
#p.pump_stop(channels=[1, 2, 3, 4])
