import time
import serial
import threading
from queue import Queue
import _reglo_lib as lib

p = lib.Pump()

ser = serial.Serial(port='/dev/ttyO2', baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,
                    bytesize=8, timeout=1, xonxoff=0)
volume_queue = Queue()
stop_queue = Queue()


def check():
    try:
        volume = 0
        stop = None
        while True:
            read = ser.readline().rstrip()
            # print("Read:%s"%(bytes.decode(read)))
            if bytes.decode(read) == 'Done':
                stop = True
                stop_queue.put(stop)
            if bytes.decode(read) != '' and bytes.decode(read) != 'Done':  # to add: read dependance:   if 'volume=' in bytes.decode(read):
                volume += 8                       # volume+= float(bytes.decode(read)[8:])
                volume_queue.put(volume)        # to add: feedback regarding reservoir used -> variable channel
                volume = 0
            else:
                pass
    finally:
        ser.close()
        print('Connection closed')


def pump():
    volume = 0
    while True:
        if volume_queue.empty() is False:          # as soon as a numeric object is put into queue, the volume to pump is increased by that number. The queue is cleared
            volume = volume + volume_queue.get()   # If optional args block is true and timeout is None (the default), block if necessary until an item is available.
        if volume > 0:
            if p.pump_status() == '-':                     # if the pump is not running, then method to pump set volume is started. Volume variable is cleared
                print('volume to pump = ', volume)
                print(p.pump_set_volume_at_flow_rate(channels=[1], volume=[volume], rotation=['K']))
                volume = 0
        if stop_queue.empty() is False and p.pump_tatus() == '-' and volume == 0:     # if 'Done' feedback is received and the pump has finished dispensing, channel is stopped (outpunt in the terminal) and program is terminated
            print(p.pump_stop(channels=[1]))
            return
        elif stop_queue.empty() is False and p.pump_status() == '+' and volume == 0:   # if 'Done' feedback is received but the pump is not finished dispensing, thread waites 1s to repeat the loop
            time.sleep(1)
            # Attention: delete this option (and p.PumpStatues()=='-' condition above) if refilled
            # medium is not further used and immediate stop after 'Done' message is desired
            continue
        time.sleep(0.1)


check = threading.Thread(target=check)
check.daemon = True
check.setDaemon(True)
check.start()

pump()
