import serial
from struct import *

ser = serial.Serial(port='/dev/tty.usbserial-AL0347P6', baudrate=38400, bytesize=8, parity='N', stopbits=1, timeout=1)

#--------------------------------(test ascii)---------------------------------------- bereits getestet

length = '07'
command = '04'              # 04=Request parameter, will be answered with 02
process_query = '71'        # Process number in hexadecimal
parameter_query = '63'      # Parameter query in hexadecimal
process_response = '71'     # Process response in hexadecimal
parameter_response = '6300'   # Parameter response in hexadecimal
node = '03'

#query = f':{length}{node}{command}{process_query}{parameter_query}{process_response}' \
        #f'{parameter_response}\r\n'
#query = ':0603010121\r\n'
query = b'\x10\x02\x01\x03\x05\x04\x01\x10\x01\x10\x10\x03'

#:0780047163716300\r\n #serial number
#capacity 100
#capacity unit
#valve
print(query)
#ser.write(str.encode(query)) #ASCII

read = ser.read_until('\r\n') #binary
read = str(ser.read_until('\r\n'))
print(read)



#1st test
#ser.write(str.encode(':06030461036103\r\n')) #GetAlarmModeASCII
#ser.write(str.encode('100201030504610361031003')) #GetAlarmModebinary
#ser.write(str.encode(':0180050461036103\r\n')) #GetAlarmModebinary

#query = b'\x10\x02\x01\x03\x05\x04\x01\x21\x01\x20\x10\x03'




#read = str(bytes.decode(ser.readline()))



#-----------------------------(test 15.03.21)---------------------------------------
'''
node='80'
process_query_decimal = '71'
parameter_inicial = '08'

data_type = '0'

char=       10
integer=    20
Long=       40

process_query_hex = hex(process_query_decimal)
parameter_inicial_hex=  hex(parameter_inicial)

process_query_hex= hex(process_query_decimal)
process_response_complete_hex= parameter_inicial_hex + data_type
process_response_complete_dec = int(process_response_complete_hex, 16)
protocol='ascii'

if protocol == 'ascii':
    # ascii transfer protocol
    length = '06'
    command = '01'          # 01=write parameter, will be answered with type 00(Status Parameter)
    process_query = '74'    # Process number in hexadecimal
    parameter_query = '60'  # Parameter query in hexadecimal
    query = f':{length}{node}{command}{process_query}{parameter_query}{hex_input_padded}\r\n'
else:
    # Binary transfer protocol.
    dle = 16
    stx = 2
    seq = 1
    node = 3
    length = 5
    command = 1  # 01=Write  parameter
    process_query = 116  # Process number in decimal-61 Hexa
    parameter_query = 96  # Process response in decimal-21 in Hexa
    etx = 3
    query = pack('BbbbbbbbbBb', dle, stx, seq, node, length, command, process_query, parameter_query,
                 input_integer_decimal, dle, etx)

    print(query)
'''
