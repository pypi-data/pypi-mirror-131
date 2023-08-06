import time
import serial
import threading
import _reglo_lib as lib
p = lib.Pump()

ser = serial.Serial(port='/dev/ttyO2', baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE,
                    bytesize=8, timeout=1, xonxoff=0)

stoplock = threading.Lock()
volumelock = threading.Lock()


class Trigger():
    volume = 0
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
            if bytes.decode(read) == '8 ml pipetted' and bytes.decode(read) != 'Done':      # to add: read dependance:   if 'volume=' in bytes.decode(read):
                with volumelock:
                    received_volume = received_volume + 8 
                    Trigger.volume = Trigger.volume + 8

            else:
                pass
    finally:
        ser.close()
        print('Serial connection closed')

def pump():
    cumulative_volume = 0
    localvolume = 0
    localstop = False
    while True:
        # check if pump is supposed to be pumped
        with volumelock:
            localvolume = localvolume + Trigger.volume
            Trigger.volume = 0

            
        if localvolume > 0 and p.pump_status() == '-':
            cumulative_volume = cumulative_volume + localvolume  # if the pump is not running, then method to pump set volume is started. Volume variable is cleared
            print('cumulative dispensed volume is: ', cumulative_volume)
            print('volume to pump = ', localvolume)
            print(p.pump_set_volume_at_flow_rate(channels=[1, 2], volume=[localvolume/2, localvolume/2], rotation=['K', 'K'])) # the pump volume is divided by 2 because two channels are used at the same time
            localvolume = 0

        # check if the pump is supposed to stop
        with stoplock: 
            if Trigger.stop is True:
                localstop = True
        if localstop is True and p.pump_status() == '+':   # if 'Done' feedback is received but the pump is not finished dispensing, thread waites 1s to repeat the loop
            time.sleep(0.1)       # Attention: delete this option (and p.PumpStatues()=='-' condition above) if refilled medium is not further used and immediate stop after 'Done' message is desired
            continue
        elif localstop is True and p.pump_status() == '-' and localvolume == 0:    # if 'Done' feedback is received and the pump has finished dispensing, channel is stopped (outpunt in the terminal) and program is terminated
            print(p.pump_stop(channels=[1, 2, 3, 4]))
            return
        time.sleep(0.1)

check = threading.Thread(target=check)
check.daemon = True
check.setDaemon(True)
check.start()

pump()
