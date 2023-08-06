import os
import sys

sys.path.insert(0, os.path.abspath('.'))

from lib import decode_response_write, decode_response_read


#response = '1002010303000000051003'#write binary
#response = '06800261215DC0' #write ascii
#response = '100201800504217D001003' #read binary
response = '06800261211F40'#read ascii
#protocol = 'binary'
protocol = 'ascii'

decoded_write_response = decode_response_write(protocol=protocol, message=response)
print(decoded_write_response)
decoded_read_response = decode_response_read(protocol=protocol, message=response)
print(decoded_read_response)
