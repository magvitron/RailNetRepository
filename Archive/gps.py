#!/usr/bin/env python
import datetime as dt
import os
import serial
import pygame, sys
from pygame.locals import *

gps_con = 0
settime = 0
fix = 0
text0 = ""
text1 = ""
text2 = ""
text4 = ""
offset = 0
font = 24
width = font * 25
height = font * 17
gps1 = [0,0,0,0,0,0,0,0,0,0,0,0]
gps1[7] = 0

def keys2(msg,fsize,fcolor,fx,fy,upd):
   greenColor = pygame.Color(0,255,0)
   blackColor = pygame.Color(0,0,0)
   redColor = pygame.Color(255,0,0)
   colors = [blackColor,greenColor,greenColor,redColor]
   color = colors[fcolor]
   fontObj = pygame.font.Font('freesansbold.ttf',fsize)
   if upd ==1:
      pygame.draw.rect(windowSurfaceObj,blackColor,Rect(fx,fy, font * 10, 32))
   msgSurfaceObj = fontObj.render(msg, False,color)
   msgRectobj = msgSurfaceObj.get_rect()
   msgRectobj.topleft =(fx,fy)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             
   windowSurfaceObj.blit(msgSurfaceObj, msgRectobj)
   if upd ==1:
      pygame.display.update(pygame.Rect(fx,fy,font * 10,font))
   return()

listz = ['Date:', 'Time:', 'Fix Quality:', '3D Fix:','Longtitude:','Latitude:','Altitude:','Speed Knots:','Speed Km/Hr:','Direction True:','Direction Mag:','No. of Sats:','Sats: ','PDOP:','HDOP:','VDOP']
listf = ['invalid', 'GPS fix (SPS)', 'DGPS fix', 'PPS fix', 'Real Time Kinematic', 'Float RTK', 'estimated', 'Manual input mode', 'Simulation Mode']
list3 = ['No fix', '2D Fix', '3D Fix']
pygame.init()
pygame.display.set_caption('GPS')

windowSurfaceObj = pygame.display.set_mode((width,height),1,24)

x = 0
a = 10
while x < 16:
    keys2 (listz[x],font,3,a,(x * font) + 2,1)
    x +=1

while gps_con == 0:
   if os.path.exists('/dev/ttyUSB0') == True:
      if gps_con != 1:
         ser = serial.Serial('/dev/ttyUSB0',115200,timeout = 10)
         gps_con = 1
   elif os.path.exists('/dev/ttyUSB1') == True:
      if gps_con != 1:
         ser = serial.Serial('/dev/ttyUSB1',115200,timeout = 10)
         gps_con = 1
         
while True:               
   # get data from gps
   gps = ser.readline()
   if gps[1 : 6] == "GPGGA":
      fix = '0'
      gps1 = gps.split(',',12)
      if len(gps) > 68 and (gps1[3] == "N" or gps1[3] == "S"):
         fix = gps1[6]
         keys2 (gps1[6] + " - " + listf[int(fix)],font,2,font * 8,(font * 2) + 2,1)
         keys2 (gps1[9] + "M",font,2,font * 8,(font * 6) + 2,1)
         keys2 (gps1[7],font,2,font * 8,(font * 11) + 2,1)
                    
   if gps[1 : 6] == "GPGSA" and gps1[7] > 0:
      gps4 = gps.split(',',18)
      if len(gps) > 40:
         keys2 (gps4[2] + "D",font,2,font * 8,(font * 3) + 2,1)
         y = 0
         while y < int(gps1[7]):
            keys2 (gps4[y+3] + ",",font,2,(font * (8 + (y*1.4))),(font * 12) + 2,1)
            y +=1
         keys2 (gps4[15],font,2,font * 8,(font * 13) + 2,1)
         keys2 (gps4[16],font,2,font * 8,(font * 14) + 2,1)
         gps5 = gps4[17].split('*',2)
         keys2 (gps5[0],font,2,font * 8,(font * 15) + 2,1)
                       
   if gps[1 : 6] == "GPRMC" and fix != '0':
      gps2 = gps.split(',',12)
      if len(gps) > 60 and (gps2[4] == "N" or gps2[4] == "S"):
         hour = int(gps2[1][0:2])
         hour = hour + offset
         if hour > 23:
            hour = hour - 24
         if hour < 0:
            hour = hour + 24
         keys2 (str(hour) + ":" + gps2[1][2:4] + ":" + gps2[1][4:6],font,2,font * 8,(font * 1) + 2,1)
         keys2 ("20" + gps2[9][4:6] + "-" + gps2[9][2:4] + "-" + gps2[9][0:2],font,2,font * 8,(font * 0) + 2,1)
         lon = str(gps2[5][:3])+ "." + str(gps2[5][3:5]) + "." + str(gps2[5][6:10])
         keys2 (lon + " " + gps2[6],font,2,font * 8,(font * 4) + 2,1)
         lat = str(gps2[3][:2])+ "." + str(gps2[3][2:4]) + "." + str(gps2[3][5:9])
         keys2 (lat + " " + gps2[4] ,font,2,font * 8,(font * 5) + 2,1)

                        
   if gps[1 : 6] == "GPVTG" and fix != '0':
      gps3 = gps.split(',',8)
      if len(gps) > 26 and gps3[2] == "T":
         keys2 (gps3[5],font,2,font * 8,(font * 7) + 2,1)
         keys2 (gps3[7],font,2,font * 8,(font * 8) + 2,1)
         keys2 (gps3[1],font,2,font * 8,(font * 9) + 2,1)
         keys2 (gps3[3],font,2,font * 8,(font * 10) + 2,1)
