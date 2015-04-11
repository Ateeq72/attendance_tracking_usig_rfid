#!/usr/bin/python
import serial
import display
import mysql

import datetime
import time
import os
import sys
import tty
import termios
import logging

import thread
import time

import RPi.GPIO as GPIO
VERBOSE=True

def onScreen(message):
    if(VERBOSE):
        print(message)


def printDateToDisplay():
    while True:
        #Display current time on display, until global variable is set
        if displayTime!=True:
            thread.exit()
        display.lcdWriteFirstLine(time.strftime("%d.%m. %H:%M:%S", time.localtime()))
        onScreen(time.strftime("%d.%m.%Y %H:%M:%S", time.localtime()))
        time.sleep(1)

def addnewUser():
    print("Swipe Your Card Now!")
    tag = read()
    name = raw_input("Enter Your Name : ") #used when connected via ssh
    surname = raw_input("Enter Your Surname **Needed : ")
    print("Processing!")
    mysql.addUser(tag,name,surname)

def removeExistUser():
   tagdata = read()
   tag = mysql.getuserName(tagdata)
   print(tag)
   print("Proccesing!")
   mysql.removeUser(tag) 

def read():
    ser = serial.Serial ("/dev/ttyAMA0")                           #Open named p$
    ser.baudrate = 9600                                            #Set baud rat$
    data = ser.read(12)                                            #Read 12 char$
    ser.close ()  
    print("your cardID was:")
    print data
    return data 
    
def userEntry():
    tagdata = read()
    name = mysql.getuserName(tagdata)
    print(name)
    print("Hi! " +name)
    display.lcdWriteFirstLine("Hi! " +name)
    mysql.insertReading(name,"entry")
    os.system("sudo fswebcam -d /dev/video0 -r 640x480 -S 6 /home/pi/attendance/pics/%m-%d-%y-%H%M.jpg")
    print("your data was recorded")
    display.lcdWriteSecondLine("your data was recorded")
    print("done")

def userLeave():
    tagdata = read()
    name = mysql.getuserName(tagdata)
    print(name)
    print("Hi! " +name)
    display.lcdWriteFirstLine("Hi! " +name)
    mysql.insertReading(name,"leave")
    os.system("sudo fswebcam -d /dev/video0 -r 640x480 -S 6 /home/pi/attendance/pics/%m-%d-%y-%H%M.jpg")
    print("your data was recorded")
    display.lcdWriteSecondLine("your data was recorded")


def getLastEntry():
    tagdata = read()
    tag = mysql.getuserName(tagdata)
    print(tag)
    lastentry=mysql.getLastReading(tag)
    print("Hi!",tag)
    print(lastentry)
    #os.system("sudo fswebcam -d /dev/video0 -r 640x480 -S 6 /home/pi/attendance/pics/%m-%d-%y-%H%M.jpg")

def deleteLastEntry():
    tagdata = read()
    tag = mysql.getuserName(tagdata)
    print(tag)
    mysql.deleteLastReading(tag)
    print("Hi!.. ",tag)
    os.system("sudo fswebcam -d /dev/video0 -r 640x480 -S 6 /home/pi/attendance/pics/%m-%d-%y-%H%M.jpg")

def actualprocess(ivalue):
   if(ivalue==1):
     print("Entry!...")
     print("Swipe your card!")
     display.lcdWriteFirstLine("Hi Their!. Please..")
     display.lcdWriteSecondLine("Swipe your Card")
     userEntry()

   if(ivalue==2):
     print("Leave..")
     print("Swipe your card!")
     display.lcdWriteFirstLine("Hi Their!. Please..")
     display.lcdWriteSecondLine("Swipe your Card")
     userLeave()
     
   if(ivalue==3):
     print("View Last Entry!")
     print("Swipe your card!")
     display.lcdWriteFirstLine("Hi Their!. Please..")
     display.lcdWriteSecondLine("Swipe your Card")
     getLastEntry()

   if(ivalue==4):
     print("Remove Last Entry..")
     print("Swipe your card!")
     display.lcdWriteFirstLine("Hi Their!. Please..")
     display.lcdWriteSecondLine("Swipe your Card")
     deleteLastEntry()     

   if(ivalue==5):
     print("Adding User!")
     display.lcdWriteFirstLine("Adding User!")
     display.lcdWriteSecondLine("Swipe your Card")
     addnewUser()

   if(ivalue==6):
     print("Removing User")
     display.lcdWriteFirstLine("Removing User!")
     display.lcdWriteSecondLine("Swipe your Card")
     removeExistUser()

def main():
    try:
      display.init()
      while True:
        display.lcdWriteSecondLine("Choose an action...")
	global displayTime
        displayTime=True
        thr = thread.start_new_thread(printDateToDisplay, ())
	displayTime=False
	a = input("Enter a Appropriate value : ")
	if 0 < a < 7:
	  actualprocess(a)
	else:
	  print("Please press valid opton")
    except KeyboardInterrupt:
       GPIO.cleanup()
       pass

GPIO.cleanup()

if __name__ == '__main__':
    main()

 

     
