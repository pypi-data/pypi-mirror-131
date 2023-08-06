'''
dle = str.encode('\x01')
stx = str.encode('\x02')
sequence = str.encode('\x01')
etx = str.encode('\x03')
length = str.encode('\x05')
command = str.encode('\x04')  # 04=Request parameter, will be answered with 02
process_query = str.encode('\x01')  # Process number in hexadecimal
parameter_query = str.encode('\x21')  # Parameter query in hexadecimal
process_response = str.encode('\x01')  # Process response in hexadecimal
parameter_response = str.encode('\x20')  # Parameter response in hexadecimal
node = str.encode('\x03')

query = dle + stx + sequence + node + length + command + process_query + parameter_query + process_response + \
        parameter_response + dle + etx



print(query)

'''

#test Lukas

from struct import *
dte = 10
stx = 2
sth = 1
node = 3
length = 5
command = 4  # 04=Request parameter, will be answered with 02
process_query = 97  # Process number in hexadecimal
parameter_query = 33  # Parameter query in hexadecimal
process_response = 97  # Process response in hexadecimal
parameter_response = 33  # Parameter response in hexadecimal
etx = 3
query = pack('bbbbbbbbbbbb', dte, stx, sth, node, length, command, process_query, process_response, parameter_query, parameter_response, dte, etx)
