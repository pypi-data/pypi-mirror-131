import os
import sys

sys.path.insert(0, os.path.abspath('.'))

from lib_new_test import decode_response_write, decode_response_read



#response = '0480000005' #write ascii: always 10digits
#response = '06800261211F40'#read ascii 14digits
#response = '058002610578' #read ascii 12 digits
#response = b'\x10\x02\x01\x03\x03\x00\x04\x05\x10\x03'

response = ':0480000005\r\n'
#response = b'\x10\x02\x01\x03\x03\x00\x00\x01\x10\x03'
#protocol = 'binary'
protocol = 'ascii'



decoded_write_response = decode_response_write(protocol=protocol, message_str=response)
print(decoded_write_response)
#decoded_read_response = decode_response_read(protocol=protocol, message_str=response)
#print(decoded_read_response)
