from sila2lib_implementations.BioREACTOR48.BioREACTOR48Service.SerialDetector import serial_ports
ports_required = ['COM12', 'COM13', 'COM14', 'COM15', 'COM7', 'COM8']
# Opening a serial port for data communication automatically. ONLY use if no other COM ports exist!
available_ports = serial_ports()
print(available_ports)
ports = []
ports_not_required = []
for i in range(0,len(available_ports),1):
    if available_ports[i] in ports_required:
        ports.append(available_ports[i])
    else:
        ports_not_required.append(available_ports[i])
unavailable_ports = list(set(ports_required) - set(ports))
if unavailable_ports is not []:
    print("The following COM/USB ports are not available: {ports}".format(ports=unavailable_ports))
if ports == []:
    print("Ho")
# for:
# ports = ports_required.remove(unavailable_ports)
# print(ports)
