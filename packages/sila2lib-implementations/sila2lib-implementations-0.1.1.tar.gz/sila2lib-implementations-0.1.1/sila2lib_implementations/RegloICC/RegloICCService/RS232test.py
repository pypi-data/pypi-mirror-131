#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import serial
import numpy as np
import glob


# define and encode commands (from handbook)
input = '2~1\r\n' # channel addressing
input = '2~\r\n' # get channel addressing

#input = '1M\r\n' # Set flow rate mode to mL/min mode

#input = '1?\r\n' # get maximum calibratet flow rate

#input = '1O\r\n' # set volume rate mode

#input = '1v2000+0\r\n' # set volume evtl. 4 Nachkommastellen

#input = '1f2000+0\r\n' #  Set flowrate

#input = '3H\r\n'

#input = '1!\r\n' # get maximum flow rate

#input = '1E\r\n' # get pump status

input = '2I\r'  # Stop
#input = '1H\r'  # Start

#input = '@1\r'
#lock_as_bytes = str.encode(lock)
#read_command_as_bytes = str.encode(read_command)
#key_as_bytes = str.encode(key)
input_as_bytes = str.encode(input)
#start_as_bytes = str.encode(start)
#stop_as_bytes = str.encode(stop)

ports = glob.glob('/dev/tty[U][S][B]*')
ser = serial.Serial(port=ports[0], baudrate=9600, parity=serial.PARITY_NONE,
                                                        stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS,
                                                        timeout=1, xonxoff=0)
# open serial connection via usb adapter
#ser = serial.Serial(port='/dev/ttyO2', baudrate = 9600,parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,bytesize=8,timeout=1, xonxoff=0)
#print(ser.name)#bytesize=serial.EIGHTBITS
#print(ser.baudrate)
#print(ser.read())
#print(ser.is_open)
# check if connection is open, if yes, close it and reopen it
#if (ser.isOpen() == True):
#  ser.close()
#ser.open()


# process actual commands
try:
    #ser.write(read_command_as_bytes)
    ser.write(input_as_bytes)
    print("Write:%s"%input_as_bytes)
    #for i in np.arange(0,10,1):
    for i in np.arange(0,10,5):
        read = ser.readline().rstrip()
        read = bytes.decode(read)
        read = read.split('ml')[0]
        print(bool(read))
        print("Read:%s" % read)
        #time.sleep(0.001)
        #time.sleep(0.001)
    #for i in np.arange(0,1,1):
    #    read = ser.readline().rstrip()
    #    print(read),print('Online')
    #    time.sleep(1)

finally:
    ser.close()
    print('Verbindung getrennt')
'''
# set new output
ser.write(output_as_bytes)
read = ser.readline().rstrip()
print(output)
print(read)


# start system
ser.write(start_as_bytes)
read = ser.readline().rstrip()
print(start)
print(read)

# lock system
ser.write(lock_as_bytes)
read = ser.readline().rstrip()
print(lock)
print(read)

# wait for some time, gather data
for i in range(30):
    ser.write(read_command_as_bytes)
    read = ser.readline().rstrip()
    print(read)
    time.sleep(2)

# shut system down
ser.write(stop_as_bytes)
read = ser.readline().rstrip()
print(stop)
print(read)
'''
# close connection





