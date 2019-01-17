import bluetooth
import sys
bd_addr = "00:21:13:00:13:3D"
port = 1
sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
sock.connect((bd_addr, port))
print ('Connected')
#sock.settimeout(1.0)

count = 0;
sock.send('O')
#while (count < 10):
#    data = sock.recv(12)
#    print ('received: %s'%data)#

#    count += 1


sock.close()








#import bluetooth

#print("performing inquiry...")

#nearby_devices = bluetooth.discover_devices(
#        duration=8, lookup_names=True, flush_cache=True, lookup_class=False)

#print("found %d devices" % len(nearby_devices))

#for addr, name in nearby_devices:
 #   try:
  #      print("  %s - %s" % (addr, name))
   # except UnicodeEncodeError:
    #    print("  %s - %s" % (addr, name.encode('utf-8', 'replace')))

#import serial
#port = serial.Serial("/dev/ttyAMA0", baudrate=9600, timeout=8.0)
#while True:
 #       rcv = port.readline()
  #      print(rcv)
