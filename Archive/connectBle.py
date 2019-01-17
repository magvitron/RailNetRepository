# This project requires PyBluez
import bluetooth

#the computer knows about.
print ("Searching for devices...")
print ("")
#Create an array with all the MAC
#addresses of the detected devices
nearby_devices = bluetooth.discover_devices()
#Run through all the devices found and list their name
num = 0
print ("Select your device by entering its coresponding number...")
for i in nearby_devices:
	num+=1
	print (num , ": " , bluetooth.lookup_name( i ))

#Allow the user to select their Arduino
#bluetooth module. They must have paired
#it before hand.
#selection = input("> ") - 1
print ("You have selected", "HC-05")
bd_addr = nearby_devices[2]
sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
sock.connect(("HC-05", 1))
