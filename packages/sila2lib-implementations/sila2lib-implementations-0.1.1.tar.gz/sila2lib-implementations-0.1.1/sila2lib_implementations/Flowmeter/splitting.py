# Is there a a constant length? yes, 14 digits
# What`s the max length-14
# What`s the min length-14
# How long is the header-10
# How long can the message be?Min, max? 4 digits
# How long is the tail? Do we know the length of the tail before receiving the message (Yes)
from struct import * #used to code binary protocol

'''
print('------------------------------          ACII          -----------------------------')

#Alarmservice: ASCII, Alarm_limit_maximum_read_antwort
response = '06800461216121'
print("Binary test: read_answer")

splitat_1 = 10
splitat_2 = -4
header, message = response[:splitat_1], response[splitat_2:]
print(header, message)
print([header[i:i+2] for i in range(0, len(header), 2)])
length, node, command, process_query, parameter_query = [header[i:i+2] for i in range(0, len(header), 2)]
print(f'length: {length} \nnode: {node} \ncommand: {command} \nprocess_query: {process_query}\nparameter_query: {parameter_query}')
message_dec = int(message,16)
message_percent = message_dec/320
print(f'message_hex: {message} \nmessage_decimal: {message_dec} \nmessage:in_percent: {message_percent}' )
'''
'''
print('------------------------------   Enhanced Binary     -----------------------------')

#Alarmservice: Binary, Alarm_limit_maximum_read_antwort
print("Binary test read_answer")
response = b'\x10\x02\x01\x03\x04\x02a\x03\x00\x10\x03'
#              10  02  01  03  04  97  03  00  10  03
#response = b'\x10\x02\x01\x03\x05\x04\x01!\x01 \x10\x03' #response from process we know it works
query = unpack_from('bbbbbbbbbbb', response)
print(query)
#query.split =(',')
#Alarmservice: binary protocol , Alarm_limit_maximum_read

#splitat_1 = 16
#splitat_2 = -4

#header, message, tail = response[:splitat_1], response[splitat_1:splitat_2], response[splitat_2:]
#print(header, message, tail)

#print([header[i:i+2] for i in range(0, len(header), 2)])
# dle, stx, message_sequence, node, length, command,  process_query, parmeter_query, message,
#dle, stx, message_sequence, node, length, command, process_query, parameter_query, message, dle2, etx = [query[i:i+2] for i in range(0, len(query), 1)]
dle, stx, message_sequence, node, length, command, process_query, parameter_query, message, dle2, etx = str(query).split(',')


print(f'message_sequence: {message_sequence} \nnode: {node} \nlength: {length}, \ncommand: {command} \nprocess_query: {process_query}\nparameter_query: {parameter_query} ', )
#converts answer to decimal and shows it
message_dec = int(message,16)
message_percent = message_dec/320
print(f'message_hex: {message} \nmessage_decimal: {message_dec} \nmessage:in_percent: {message_percent}' )
'''
