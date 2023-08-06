import _reglo_lib as lib  # -> predefined Classes

p = lib.Pump()


'''
Vorpumpen -> 17.8ml vom Reaktor zu Vorratsbehälter
Begasung : 120 stL/h,  N(reaktor)=200U/min
'''


print(p.pump_set_volume_to_flow_rate(channels=[1], flowrate=[27], volume=[97.8], rotation=['K']))

print(p.pump_time_at_flow_rate(channels=[1], flowrate=[27], runtime=[10.5, 5.3], rotation=['K']))

print(p.pump_stop(channels=[1]))

print(p.pump_status())
