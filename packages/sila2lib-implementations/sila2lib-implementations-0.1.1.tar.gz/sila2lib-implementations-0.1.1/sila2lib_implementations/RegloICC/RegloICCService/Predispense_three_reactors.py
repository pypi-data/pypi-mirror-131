import _reglo_lib as lib  # -> predefined Classes

p = lib.Pump()


'''Vorpumpen -> 17.8ml vom Reaktor zu Vorratsbehälter'''
'''Begasung : 120 stL/h,  N(reaktor)=200U/min'''

Tubevolume = 17.8 
Predispensevolume = Tubevolume + 50
#PredispensePerChannel = Predispensevolume / 2


print(p.pump_set_volume_at_flow_rate(channels=[1, 2, 3],
                                     volume=[Predispensevolume, Predispensevolume, Predispensevolume],
                                     rotation=['J', 'J', 'J']))
