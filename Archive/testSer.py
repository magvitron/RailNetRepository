#! /usr/bin/python

import serial
import pprint

serialConn = {}
for vtr in range(0,12):
    tryPort='/dev/ttyUSB' +str(vtr)
    try:
        ser = serial.Serial(port=tryPort, baudrate=19200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS)
        serialConn[tryPort[8:]] = ser
        print ("++ found serial on " + tryPort)
    except:
        print ("-- no serial on " + tryPort)

pp = pprint.PrettyPrinter(indent=4)
print (" ")
print ("++ serial ports open (open=True):")
pprint.pprint(serialConn)


serialConn['USB0'].open()
print (serialConn['USB0'].isOpen())

for con in serialConn:
    serialConn[con].close()

print (" ")
print ("++ serial ports open (open=False):")
pprint.pprint(serialConn)
