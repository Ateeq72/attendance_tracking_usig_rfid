#!/usr/bin/python
import serial
from Adafruit_CharLCD import Adafruit_CharLCD
import mysql
import datetime
import time
import os
import sys
import tty
import termios
import logging
import RPi.GPIO as GPIO
import thread
import time
from time import sleep
import math, operator
from PIL import Image

VERBOSE=True

lcd = Adafruit_CharLCD()

lcd.begin(16, 1)

global timestp 
timestp = time.strftime("%Y:%m:%d-%H:%M:%S")

def cmpimg(file1,file2):
    h1 = Image.open(file1).histogram()
    h2 = Image.open(file2).histogram()

    rms = math.sqrt(reduce(operator.add,
                                map(lambda a,b: (a-b)**2, h1, h2))/len(h1))
    print rms
    return rms



def onScreen(message):
    if(VERBOSE):
        print(message)


def printDateToDisplay():
    while True:
        #Display current time on display, until global variable is set
        if displayTime!=True:
            thread.exit()
        display.message(time.strftime("%d.%m. %H:%M:%S", time.localtime()))
        onScreen(time.strftime("%d.%m.%Y %H:%M:%S", time.localtime()))
        time.sleep(1)

def addnewUser():
    print("Swipe Your Card Now!")
    tag = read()
    name = raw_input("Enter Your Name : ") #used when connected via ssh
    surname = raw_input("Enter Your Surname **Needed : ")
    cmd='sudo fswebcam -d /dev/video0 -r 640x480 -S 6 /home/pi/attendance/users/%s.jpg' % (name)
    os.system(cmd)
    print("Processing!")
    mysql.addUser(tag,name,surname)

def removeExistUser():
   tagdata = read()
   tag = mysql.getuserName(tagdata)
   onlyname = mysql.getonlyName(tagdata)
   print(tag)
   print("Proccesing!")
   mysql.removeUser(tag)
   cmd='sudo rm /home/pi/attendance/users/%s.jpg' % (onlyname)
   os.system(cmd) 

def read():
    ser = serial.Serial ("/dev/ttyAMA0")                           #Open named p$
    ser.baudrate = 9600                                            #Set baud rat$
    data = ser.read(12)
    sleep(1)                                            #Read 12 char$
    ser.close ()  
    print("your cardID was:")
    print data
    return data 
    
def userEntry():
    tagdata = read()
    onlyname = mysql.getonlyName(tagdata)
    name = mysql.getuserName(tagdata)
    print(name)
    print("Hi! " +name)
    os.system(' echo " Hi ! ' + name + ' " | festival --tts ')
    lcd.clear()
    lcd.message("Hi! " +name)
    lcd.message("\n Entry!... ")    
    cmd='sudo fswebcam -d /dev/video0 -r 640x480 -S 6 /home/pi/attendance/pictures/%s_entry_%s.jpg' % (onlyname, timestp)
    os.system(cmd)
    pic1='/home/pi/attendance/users/%s.jpg' % (onlyname)
    pic2='/home/pi/attendance/pictures/%s_entry_%s.jpg' % (onlyname, timestp)
    sleep(2)
    lcd.message("\n your data was obtained")
    sleep(2)
    cmpvalue = cmpimg(pic1, pic2)
    if cmpvalue < 50:
      mysql.insertReading(name,"entry")
      print("your data was recorded")
      os.system(' echo " your data was recorded " | festival --tts ')
      lcd.clear()
      lcd.message("your data was recorded")
      print("done")
    elif cmpvalue < 50:
      print("Not a Match!")
      lcd.clear()
      lcd.message("Not a Match!")

def userLeave():
    tagdata = read()
    name = mysql.getuserName(tagdata)
    onlyname = mysql.getonlyName(tagdata)
    print(name)
    print("Hi! " +name)
    os.system(' echo " Hi ! ' + name + ' " | festival --tts ')
    lcd.clear()
    lcd.message("Hi! " +name)
    lcd.message("\n Leave!...")
    mysql.insertReading(name,"leave")
    cmd='sudo fswebcam -d /dev/video0 -r 640x480 -S 6 /home/pi/attendance/pictures/%s_leave_%s.jpg' % (onlyname, timestp)
    os.system(cmd)
    print("your data was recorded")
    lcd.clear()
    lcd.message("your data was \n recorded")
    os.system(' echo " Thanks See you Again " | festival --tts ')


def getLastEntry():
    tagdata = read()
    tag = mysql.getuserName(tagdata)
    print(tag)
    lastentry=mysql.getLastReading(tag)
    print("Hi!",tag)
    print(lastentry)
    lcd.clear()
    lcd.message("Last Entry \n " + lastentry)
    #os.system("sudo fswebcam -d /dev/video0 -r 640x480 -S 6 /home/pi/attendance/pics/%m-%d-%y-%H%M.jpg")

def deleteLastEntry():
    tagdata = read()
    tag = mysql.getuserName(tagdata)
    onlyname = mysql.getonlyName(tagdata)
    print(tag)
    mysql.deleteLastReading(tag)
    print("Hi!.. ",tag)
    lcd.clear()
    lcd.message("Deleted")
    cmd='sudo fswebcam -d /dev/video0 -r 640x480 -S 6 /home/pi/attendance/pictures/deleted_last_entry_%s_%s.jpg' % (onlyname, timestp)
    os.system(cmd)

def actualprocess(ivalue):
   lcd.clear()
   if(ivalue==1):
     print("Entry!...")
     print("Swipe your card!")
     lcd.message("Hi Their! Please..")
     lcd.message("\n Swipe your Card")
     os.system(' echo " Action Entry was selected " | festival --tts ')
     userEntry()

   if(ivalue==2):
     print("Leave..")
     print("Swipe your card!")
     lcd.message("Hi Their! Please..")
     lcd.message("\n Swipe your Card")
     os.system(' echo " Action Leave was selected " | festival --tts ')
     userLeave()
     
   if(ivalue==3):
     print("View Last Entry!")
     print("Swipe your card!")
     lcd.message("Hi Their! Please..")
     lcd.message("\n Swipe your Card")
     os.system(' echo " Getting last entry " | festival --tts ')
     getLastEntry()

   if(ivalue==4):
     print("Remove Last Entry..")
     print("Swipe your card!")
     lcd.message("Hi Their! Please..")
     lcd.message("\n Swipe your Card")
     os.system(' echo " Deleting last entry " | festival --tts ')
     deleteLastEntry()     

   if(ivalue==5):
     print("Adding User!")
     lcd.message("Adding User!")
     lcd.message("\n Swipe your Card")
     addnewUser()

   if(ivalue==6):
     print("Removing User")
     lcd.message("Removing User!")
     lcd.message("\n Swipe your Card")
     removeExistUser()

def main():
    try:
      while True: 
        lcd.clear()
        lcd.message('Choose an action...')
	lcd.message("\n 1,2,3,4,5,6")
        os.system(' echo " Please Choose an Action " | festival --tts ')
	global displayTime
        displayTime=True
        thr = thread.start_new_thread(printDateToDisplay, ())
	displayTime=False
	a = input("Enter a Appropriate value : ")
	if 0 < a < 7:
	  actualprocess(a)
	else:
	  print("Please press valid opton")
	  os.system(' echo " Please Choose a valid Action " | festival --tts ')
    except KeyboardInterrupt:
       GPIO.cleanup()
       pass


if __name__ == '__main__':
    main()

 

     
