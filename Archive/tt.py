import serial
import re

ser = serial.Serial(
    port='/dev/ttyUSB0',\
    baudrate=9600,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
        timeout=0)

print("connected to: " + ser.portstr)
txt=""
GPScount=0
while 1: 
    txt = ser.readline()
    if txt !=""  and "GPGGA".encode() in txt:
        while 'M'.encode() not in txt:
            txt += ser.readline()
        searchObj = re.search( r'\$.*?,.*?,(.*?),(.+?),(.*?),(.+?),(\d)?,.*?,', txt.decode(), re.M|re.I)
        if searchObj:
            print (searchObj.group(1) + searchObj.group(2))
            print (searchObj.group(3) + searchObj.group(4))
            print (searchObj.group(5))
            if searchObj.group(1) !="":
                break
            else:
                GPScount = GPScount + 1
                if GPScount > 10:
                    break
       
