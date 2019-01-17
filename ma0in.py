######################################
# main.py
######################################
#dependency: guizero, Tkinter
#
######################################
import os
import time
from guizero import *
import ftplib
import serial
import re
import csv
import threading
import bluetooth
import sys
import RPi.GPIO as GPIO
import SimpleMFRC522
import shutil

GPScount=0
latitude = None
longitude = None
flag = None

ser = serial.Serial(
    port='/dev/ttyUSB0',\
    baudrate=9600,\
    parity=serial.PARITY_NONE,\
    stopbits=serial.STOPBITS_ONE,\
    bytesize=serial.EIGHTBITS,\
        timeout=0)
#all definitions
#take videos
########################################################################
# Support function.
######################################################################## 
def timeStamped(fname, fmt='%Y-%m-%d-%H-%M-%S-{fname}'):
  import datetime
  # This creates a timestamped filename
  return datetime.datetime.now().strftime(fmt).format(fname=fname)  
def convertNema(inval):
	searchObj = re.search( r'(\d{2})?(\d{2}\.\d+)', inval, re.M|re.I)
	degree = float(searchObj.group(1)) + (float(searchObj.group(2)))/60
	return degree 
def readGPS():
  
  print("connected to: " + ser.portstr)
  txt=""
  global latitude
  global longitude
  while 1: 
      txt = ser.readline()
      if txt != "" and 'GPGGA'.encode() in txt:
          while 'M'.encode() not in txt:
              txt += ser.readline()
          searchObj = re.search( r'\$.*?,.*?,(.*?),(.+?),(.*?),(.+?),(\d)?,.*?,', txt.decode(), re.M|re.I)
          if searchObj:
              latitude = (searchObj.group(1))
              longitude = (searchObj.group(3))
              if not latitude:
                return 0
              else:
                return 1
          else:
              return 0
########################################################################
# Emergency requests
######################################################################## 
def process_Em_Req(val):
  print("got" + val)
  confwindow.show()
  
  pic = Picture(confwindow,image="Media/Alert.jpg", grid=[0,0,2,1])
  buttonNo = PushButton(confwindow, command=recordVideo, args = "1", image="Media/NO.jpg", grid=[0,1])
  buttonYes = PushButton(confwindow, command=recordVideo, args = "2",image="Media/YES.jpg", grid=[1,1])
  return;
######################################################################## 
def recordVideo(btnval):
  if btnval=="2":
    #ffmpeg -f v4l2 -r 25 -s 640x480 -i /dev/video0 out.avi
    cmd ='ffmpeg -y -f v4l2 -r 25 -t 00:00:10 -video_size 1280x720 -i /dev/video0 '
    #cmd += time.strftime("%Y_%m_%d_%H_%M")
    cmd+="movie.avi"
    #fname = time.strftime("%Y_%m_%d_%H_%M")
    os.system(cmd)
    cmd='ffmpeg -y -i movie.avi -preset ultrafast -crf 27 movie.mp4'
    os.system(cmd)
    confwindow.hide()
    window.hide()
    print("upload....")
    session = ftplib.FTP('indianrailwaytest.atwebpages.com','2836956_railtest','akhil01234')
    file = open('movie.mp4','rb')                  # file to send
    session.storbinary('STOR movie.mp4', file)     # send the file
    file.close()                                    # close file and FTP
    session.quit()
    shutil.copy("movie.mp4", "MediaBackUp/VideoEvidence/" + timeStamped("EmgVideo.mp4"))
    print("done")
  else:
    print ("exit")
    confwindow.hide()
    window.hide()
######################################################################## 
def EMGSTOP():
  window.show()
  #button = PushButton(app, command=process_Em_Req, text="hello", grid=[0,0])
  button1 = PushButton(window, command=process_Em_Req, args = "1",image="Media/num1.jpg", grid=[0,0])
  button2 = PushButton(window, command=process_Em_Req, args = "2", image="Media/num2.jpg", grid=[1,0])
  button3  = PushButton(window, command=process_Em_Req,  args = "3",image="Media/NUM3.jpg", grid=[2,0])
  button4  = PushButton(window, command=process_Em_Req,  args = "4",image="Media/NUM4.jpg", grid=[0,1])
  button5  = PushButton(window, command=process_Em_Req,  args = "5",image="Media/NUM5.jpg", grid=[1,1])
  button6  = PushButton(window, command=process_Em_Req,  args = "6",image="Media/NUM6.jpg", grid=[2,1])  
########################################################################
# Support function.
######################################################################## 
def trackTainGPS():
  print ("Traking train")
  if readGPS() == 1:
    if setLat != None:
      #print (abs(convertNema(latitude)-convertNema(setLat)) + abs(convertNema(longitude)-convertNema(setLong)))
      if (abs(convertNema(latitude)-convertNema(setLat)) < .05 and abs(convertNema(longitude)-convertNema(setLong)) < .05):
        print("Station adjacent, Connecting to Alarm")
        bd_addr = "00:21:13:00:13:3D"
        port = 1
        sock = bluetooth.BluetoothSocket( bluetooth.RFCOMM )
        sock.connect((bd_addr, port))
        for i in range(5):
          sock.send('O')
      else:
        print("station not reached")
  threading.Timer(5.0,trackTainGPS).start()
  
def you_chose(selected_value):
    with open('InputData/stationList.csv') as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for rows in readCSV:
            if selected_value ==  rows[2]:
                print (selected_value) 
                global setLat
                setLat = rows[0]
                print(setLat)
                global setLong
                setLong = rows[1]
                print(setLong)
                ######################################################################## 
def set_Alarm():
  print ("set alarm")
  trackTainGPS()
######################################################################## 
def destAlrmHide():
  destAlrm.hide()
def processSeat(seatNum):
  print (seatNum)
  comboMenuStation=[]
  with open('InputData/stationList.csv') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for rows in readCSV:
        comboMenuStation.append(rows[2])
  instructions = Text(destAlrm, text="Choose destination Station",grid=[0,0])
  instructions.text_color = "white"
  instructions.text_size=23
  combo = ListBox(destAlrm,items=comboMenuStation ,command=you_chose,grid=[1,0],scrollbar=True)
  combo.text_size=23
  combo.height=30
  combo.text_color="white"
  combo.width=25
  combo.height=3
  buttonNo = PushButton(destAlrm, command=destAlrmHide, image="Media/NO.jpg", grid=[0,1])
  buttonYes = PushButton(destAlrm, command=set_Alarm,image="Media/YES.jpg", grid=[1,1])
  selectSeat.hide()
  destAlrm.show()
######################################################################## 
def DestAlarm():
  print("DestinationAlarm")
  selectSeat.show()
  
  button1 = PushButton(selectSeat, command=processSeat, args = "1",image="Media/num1.jpg", grid=[0,0])
  button2 = PushButton(selectSeat, command=processSeat, args = "2", image="Media/num2.jpg", grid=[1,0])
  button3  = PushButton(selectSeat, command=processSeat,  args = "3",image="Media/NUM3.jpg", grid=[2,0])
  button4  = PushButton(selectSeat, command=processSeat,  args = "4",image="Media/NUM4.jpg", grid=[0,1])
  button5  = PushButton(selectSeat, command=processSeat,  args = "5",image="Media/NUM5.jpg", grid=[1,1])
  button6  = PushButton(selectSeat, command=processSeat,  args = "6",image="Media/NUM6.jpg", grid=[2,1])
########################################################################
# Live Tarcking function.
########################################################################       
def hideLiveTrack():
  LiveTrack.hide()
  #threading.Timer(5.0,hideLiveTrack).start()
 # if   Set_thread == None:
   # Set_thread=1
   # if flag==None:
    #  flag=1
    #  global flag
    ##  print("not hide") 
   # else:
    #  flag=None
    ##  print("hide")
    #  LiveTrack.hide()
######################################################################## 
def track():
  print("Live tracking")
  LiveTrack.show()
  station_found=0
  picture = PushButton(LiveTrack,command=hideLiveTrack,image = "Media/PrevStation.jpg",grid=[0,0])
  picture = PushButton(LiveTrack,command=hideLiveTrack,image = "Media/CurStation.jpg",grid=[1,0])
  picture = PushButton(LiveTrack,command=hideLiveTrack,image = "Media/NextStation.jpg",grid=[2,0])
  flagCount=0
  PrevStatn=""
  if readGPS() == 1:
    print("Currrent Latitude:" + latitude + ", long: " + longitude) 
    with open('InputData/stationList.csv') as csvfile:
      readCSV = csv.reader(csvfile, delimiter=',')
      for row in readCSV:
        print ("GPS: " + str(abs(convertNema(latitude)-convertNema(row[0]))) + " Read: " + str(abs(convertNema(longitude)-convertNema(row[1]))))
        
        if (abs(convertNema(latitude)-convertNema(row[0])) < .05 and abs(convertNema(longitude)-convertNema(row[1])) < .05):
          print (row[2])
          station_found=1
          Text(LiveTrack,row[2],size = 30,grid=[1,1],color ="white")
        else:
          PrevStatn = row[2]
        if station_found ==1:
          if flagCount == 0:
            Text(LiveTrack,PrevStatn,size = 30,grid=[2,1],color ="white")
            flagCount =1
          else:
            Text(LiveTrack,row[2] ,size= 30,grid=[0,1],color ="white")
            station_found=0
          
  else:
    Text(LiveTrack,"GPS NO SIG!",size = 30,grid=[0,1])
    Text(LiveTrack,"GPS NO SIG!",size = 30,grid=[1,1])
    Text(LiveTrack,"GPS NO SIG!",size = 30,grid=[2,1])
########################################################################
# Rail Rakshak login function.
########################################################################
def displayrakshakname(Rakname):
  #warn("info","please wait")
  railRakshakNameDisp.show()
  Text(railRakshakNameDisp,"Welcome:" + Rakname , size =20,grid=[0,0],color ="white")
  cmd="fswebcam -p YUYV -d /dev/video0 -r 640x480 officerOnDuty.jpg"
  os.system(cmd)
  session = ftplib.FTP('indianrailwaytest.atwebpages.com','2836956_railtest','akhil01234')
  file = open('officerOnDuty.jpg','rb')                  # file to send
  session.storbinary('STOR officerOnDuty.jpg', file)     # send the file
  file.close()                                    # close file and FTP
  session.quit()
  shutil.copy("officerOnDuty.jpg", "MediaBackUp/OfficerOnDuty/" + timeStamped("DutyOff.jpg"))
  buttonYes = PushButton(railRakshakNameDisp, command=hiderailRakshakwin,image="Media/OK.jpg", grid=[1,1])
######################################################################## 
def hiderailRakshakwin():
  railRakshakwin.hide()
  railRakshakNameDisp.hide()
######################################################################## 
def railRakshakOpwin():
  print ("option")
  reader = SimpleMFRC522.SimpleMFRC522()
  try:
    id, text = reader.read()
    print(id)
    print(text)
    displayrakshakname(text)
  finally:
    GPIO.cleanup()
    displayrakshakname(text)
######################################################################## 
def RailRakshak():
  print ("RFID reader")
  railRakshakwin.show()
  Text(railRakshakwin, "Swipe the card " , size=50,grid=[0,0],color ="white")
  buttonNo = PushButton(railRakshakwin, command= hiderailRakshakwin,image="Media/NO.jpg", grid=[0,1])
  buttonYes = PushButton(railRakshakwin, command=railRakshakOpwin,image="Media/YES.jpg", grid=[1,1])
########################################################################
def hideTTWind():
  calTTwnd.hide()
def hideMedWind():
  medEm.hide()
def callTT():
  print ("Call TT")
  pic = Picture(medEm,image="Media/MedicalEmConf.png", grid=[0,0,2,1])
  buttonNo = PushButton(medEm, command=hideMedWind, args = "1", image="Media/NO.jpg", grid=[0,1])
  buttonYes = PushButton(medEm, command=hideMedWind, args = "2",image="Media/YES.jpg", grid=[1,1])
  medEm.show()
def MedEmerg():
  print("Medical Emergency")
  pic = Picture(calTTwnd,image="Media/TTcallConfirmation.png", grid=[0,0,2,1])
  buttonNo = PushButton(calTTwnd, command=hideTTWind, args = "1", image="Media/NO.jpg", grid=[0,1])
  buttonYes = PushButton(calTTwnd, command=hideTTWind, args = "2",image="Media/YES.jpg", grid=[1,1])
  calTTwnd.show()
######################################
app = App(title="RailRakshak", width=1024,height=600, layout="grid",bg="black")
destAlrm = Window(app, width=1024,height=600, layout="grid",bg="black")
LiveTrack = Window(app, width=1024,height=600, layout="grid",bg="black")
confwindow = Window(app, width=1024,height=600,layout="grid",bg="black")
window = Window(app, width=1024,height=600,layout="grid",bg="black")
calTTwnd = Window(app, width=1024,height=600,layout="grid",bg="black")
medEm = Window(app, width=1024,height=600,layout="grid",bg="black")
selectSeat = Window(app, width=1024,height=600,layout="grid",bg="black")
railRakshakwin = Window(app, width=1024,height=600,layout="grid",bg="black")
railRakshakNameDisp = Window(app, width=1024,height=600,layout="grid",bg="black")

railRakshakNameDisp.hide()
medEm.hide()
calTTwnd.hide()
railRakshakwin.hide()
LiveTrack.hide()
destAlrm.hide()
window.hide() 
confwindow.hide()
selectSeat.hide()

#app.tk.overrideredirect(True)
#app.tk.geometry("{0}x{1}+0+0".format(app.tk.winfo_screenwidth(), app.tk.winfo_screenheight()))
#app.tk.resizable(width=0, height=0)
#app.tk.protocol('WM_DELETE_WINDOW','donothing')
#app.tk.wm_attributes('-type', 'splash')
#app.tk.wm_attributes('-fullscreen','true')
#all buttons are defined here

button = PushButton(app, command=EMGSTOP,image="Media/EMSTP.jpg",grid=[2,0])
button = PushButton(app, command=RailRakshak,image="Media/rail rakshak.jpg",grid=[1,0])
button = PushButton(app, command=MedEmerg,image="Media/Medical.jpg",grid=[0,0])
button = PushButton(app, command=callTT,image="Media/TT.jpg",grid=[2,1])
button = PushButton(app, command=DestAlarm,image="Media/DestAlarm.jpg",grid=[1,1])
button = PushButton(app, command=track,image="Media/train running info.jpg",grid=[0,1])

app.display()
