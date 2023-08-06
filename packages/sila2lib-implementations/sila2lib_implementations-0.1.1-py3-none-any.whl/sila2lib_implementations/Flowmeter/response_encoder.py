import serial
from struct import *

#-------------------------Test encoder binary 15.03.21------------------------------------------------------
dle = 16
stx = 2
seq = 1
node = 3
length_5 = 5
length_4 = 4
length_3 = 3
command_read = 4                    # 04=Request parameter
command_write= 1
command_read_response = 2
command_write_response = 0
process_query = 113                  # Process number in decimal-61 Hexa
parameter_query = 99                # Process response in decimal-21 in Hexa
process_response = 113               # Parameter query in decimal
parameter_response = 99             # Parameter response in hexa
response_length = 0
message =7
message2 = 65
message3 = 105
message4 =82
message5 =0
message6 =0
message7 =0
message8 = 0
message9 =0
message10=0
message11=23
message12=25
message_write = 0
index = 1
etx = 3

query_read = pack('BbbbbbbbbbBb', dle, stx, seq, node, length_5, command_read, process_query, parameter_query,
             process_response, parameter_response, dle, etx)

query_write = pack('BbbbbbbbbBb', dle, stx, seq, node, length_4, command_write, process_query, parameter_query,
             message, dle, etx)

response_read = pack('BbbbbbbbbBb', dle, stx, seq, node, length_4, command_read_response, process_query, parameter_query,
             message, dle, etx)

response_write = pack('BbbbbbbbBb', dle, stx, seq, node, length_3, command_write_response, message_write, index,
                      dle, etx)

response_read_length = pack('BbbbbbbbbbbBb', dle, stx, seq, node, length_5, command_read, process_query, parameter_query,
             process_response, parameter_response,response_length, dle, etx)

response_bin4 = pack('BbbbbbbbbbbbBb', dle, stx, seq, node, length_4, command_read_response, process_query, parameter_query,
             message, message2, message3, message4, dle, etx)


response_bin5 = pack('BbbbbbbbbbbbbBb', dle, stx, seq, node, length_4, command_read_response, process_query, parameter_query,
             message, message2, message3, message4, message5, dle, etx)

response_bin6 = pack('BbbbbbbbbbbbbbBb', dle, stx, seq, node, length_4, command_read_response, process_query, parameter_query,
             message, message2, message3, message4, message5, message6, dle, etx)

response_bin7 = pack('BbbbbbbbbbbbbbbBb', dle, stx, seq, node, length_4, command_read_response, process_query, parameter_query,
             message, message2, message3, message4, message5, message6, message7, dle, etx)

response_bin8 = pack('BbbbbbbbbbbbbbbbBb', dle, stx, seq, node, length_4, command_read_response, process_query, parameter_query,
             message, message2, message3, message4, message5, message6, message7, message8, dle, etx)

response_bin9 = pack('BbbbbbbbbbbbbbbbbBb', dle, stx, seq, node, length_4, command_read_response, process_query, parameter_query,
             message, message2, message3, message4, message5, message6, message7, message8, message9, dle, etx)


response_bin12 = pack('BbbbbbbbbbbbbbbbbbbbBb', dle, stx, seq, node, length_4, command_read_response, process_query, parameter_query,
             message, message2, message3, message4, message5, message6, message7, message8, message9, message10, message11,
                      message12, dle, etx)

print(f'------------------------------(query read)-------------------')
print(f'query read: {query_read}')

print('------------------------------(response read)-------------------')
print(f'response_read: {response_read}')

print('------------------------------(query write)-------------------')
print(f'query_write: {query_write}')

print('------------------------------(response write)-------------------')
print(f'query_write: {response_write}')

print('---------------------------------(response read bin4)---------------')
print(f'query_read_length: {response_bin4}')

print('---------------------------------(response read bin5)---------------')
print(f'query_read_length: {response_bin5}')

print('---------------------------------(response read bin6)---------------')
print(f'query_read_length: {response_bin6}')

print('---------------------------------(response read bin7)---------------')
print(f'query_read_length: {response_bin7}')

print('---------------------------------(response read bin8)---------------')
print(f'query_read_length: {response_bin8}')

print('---------------------------------(response read bin9)---------------')
print(f'query_read_length: {response_bin9}')

print('---------------------------------(response read bin12)---------------')
print(f'query_read_length: {response_bin12}')

