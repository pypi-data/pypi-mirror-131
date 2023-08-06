import time
import serial
import threading
import _reglo_lib as lib
p = lib.Pump()

ser = serial.Serial(port='/dev/ttyO2', baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,
                    bytesize=8, timeout=1, xonxoff=0)


stoplock = threading.Lock()
volumelock = threading.Lock()


# class that defines the globally available to-do values (only acess via lock!)
class Trigger:
    volume_channel1 = 0
    volume_channel2 = 0
    volume_channel3 = 0
    stop = False


def check():
    try:
        received_volume = 0
        while True:

            read = ser.readline().rstrip()
            if bytes.decode(read) == 'Done':
                with stoplock:
                    Trigger.stop = True
                    break
            # check for channel 1
            if bytes.decode(read) == 'reactor1_8ml' and bytes.decode(read) != 'Done':      # to add: read dependance:   if 'volume=' in bytes.decode(read):
                with volumelock:
                    Trigger.volume_channel1 = Trigger.volume_channel1 + 8
            # check for channel 2
            if bytes.decode(read) == 'reactor2_8ml' and bytes.decode(read) != 'Done':      # to add: read dependance:   if 'volume=' in bytes.decode(read):
                with volumelock:
                    Trigger.volume_channel2 = Trigger.volume_channel2 + 8
            # check for channel 3
            if bytes.decode(read) == 'reactor3_8ml' and bytes.decode(read) != 'Done':      # to add: read dependance:   if 'volume=' in bytes.decode(read):
                with volumelock:
                    Trigger.volume_channel3 = Trigger.volume_channel3 + 8

    finally:
        ser.close()
        print('Serial connection closed')

def pump():
    cumulative_volume = 0
    localvolume1 = 0
    localvolume2 = 0
    localvolume3 = 0
    localstop = False
    while True:
        # check if pump is supposed to  pump
        with volumelock:
            localvolume1 = localvolume1 + Trigger.volume_channel1
            Trigger.volume_channel1 = 0
            localvolume2 = localvolume2 + Trigger.volume_channel2
            Trigger.volume_channel2 = 0
            localvolume3 = localvolume3 + Trigger.volume_channel3
            Trigger.volume_channel3 = 0

        # check if pump is idle
        if p.pump_status() == '-':
        # pump for reactor 1
            if localvolume1 > 0:
                cumulative_volume = cumulative_volume + localvolume1  # if the pump is not running, then method to pump set volume is started. Volume variable is cleared
                print('cumulative dispensed volume is: ', cumulative_volume)
                print('volume to pump = ', localvolume1)
                print(p.pump_set_volume_at_flow_rate(channels=[1], volume=[localvolume1], rotation=['K']))
                localvolume1 = 0
                
            # pump for reactor 2
            if localvolume2 > 0:
                cumulative_volume = cumulative_volume + localvolume2  # if the pump is not running, then method to pump set volume is started. Volume variable is cleared
                print('cumulative dispensed volume is: ', cumulative_volume)
                print('volume to pump = ', localvolume2)
                print(p.pump_set_volume_at_flow_rate(channels=[2], volume=[localvolume2], rotation=['K']))
                localvolume2 = 0
    
            # pump for reactor 3
            if localvolume3 > 0:
                cumulative_volume = cumulative_volume + localvolume3  # if the pump is not running, then method to pump set volume is started. Volume variable is cleared
                print('cumulative dispensed volume is: ', cumulative_volume)
                print('volume to pump = ', localvolume3)
                print(p.pump_set_volume_at_flow_rate(channels=[3], volume=[localvolume3], rotation=['K']))
                localvolume3 = 0

        # check if the pump is supposed to stop
        with stoplock: 
            if Trigger.stop is True:
                localstop = True
        if localstop is True and p.pump_status() == '+':   # if 'Done' feedback is received but the pump is not finished dispensing, thread waites 1s to repeat the loop
            time.sleep(0.1)       # Attention: delete this option (and p.pump_statues()=='-' condition above) if refilled medium is not further used and immediate stop after 'Done' message is desired
            continue
        elif localstop is True and p.pump_status() == '-' and localvolume1 == 0 and localvolume2 == 0 and localvolume3 == 0:    # if 'Done' feedback is received and the pump has finished dispensing, channel is stopped (outpunt in the terminal) and program is terminated
            print(p.pump_stop(channels=[1, 2, 3, 4]))
            return

        time.sleep(0.1)


check = threading.Thread(target=check)
check.daemon = True
check.setDaemon(True)
check.start()

pump()
