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

def read():
    ser = serial.Serial ("/dev/ttyAMA0")                           #Open named p$
    ser.baudrate = 9600                                            #Set baud rat$
    data = ser.read(12)                                            #Read 12 char$
    ser.close ()  
    print("your cardID was:")
    print data
    return data 
    
def userEntry(name):
    print("Hi! " +name)
    display.lcdWriteFirstLine("Hi! " +name)
    mysql.insertReading(name,"entry")
    os.system("sudo fswebcam -d /dev/video0 -r 640x480 -S 6 /home/pi/attendance/pics/%m-%d-%y-%H%M.jpg")
    print("your data was recorded")
    display.lcdWriteSecondLine("your data was recorded")
    print("done")

def userLeave(name):
    print("Hi! " +name)
    display.lcdWriteFirstLine("Hi! " +name)
    mysql.insertReading(name,"leave")
    os.system("sudo fswebcam -d /dev/video0 -r 640x480 -S 6 /home/pi/attendance/pics/%m-%d-%y-%H%M.jpg")
    print("your data was recorded")
    display.lcdWriteSecondLine("your data was recorded")


def getLastEntry(tag):
    lastentry=mysql.getLastReading(tag)
    print("Hi!",tag)
    print(lastentry)
    os.system("sudo fswebcam -d /dev/video0 -r 640x480 -S 6 /home/pi/attendance/pics/%m-%d-%y-%H%M.jpg")

def deleteLastEntry(tag):
    mysql.deleteLastReading(tag)
    os.system("sudo fswebcam -d /dev/video0 -r 640x480 -S 6 /home/pi/attendance/pics/%m-%d-%y-%H%M.jpg")

def actualprocess(ivalue):
   if(ivalue==1):
     print("Entry!...")
     print("Swipe your card!")
     display.lcdWriteFirstLine("Hi Their!. Please..")
     display.lcdWriteSecondLine("Swipe your Card")
     reqID= read()
     if(reqID=="18008DAE4D76"):
           userEntry("Ateeq")
     elif(reqID=="4000634B650D"):
           userEntry("Altaf")
     elif(reqID=="40006352D8A9"):
           userEntry("John")
   if(ivalue==2):
     print("Leave..")
     print("Swipe your card!")
     display.lcdWriteFirstLine("Hi Their!. Please..")
     display.lcdWriteSecondLine("Swipe your Card")
     reqID= read()
     if(reqID=="18008DAE4D76"):
           userLeave("Ateeq")
     elif(reqID=="4000634B650D"):
           userLeave("Altaf")
     elif(reqID=="40006352D8A9"):
           userLeave("John")
   if(ivalue==3):
     print("View Last Entry!")
     print("Swipe your card!")
     display.lcdWriteFirstLine("Hi Their!. Please..")
     display.lcdWriteSecondLine("Swipe your Card")
     reqID= read()
     if(reqID=="18008DAE4D76"):
           getLastEntry("Ateeq")
     elif(reqID=="4000634B650D"):
           getLastEntry("Altaf")
     elif(reqID=="40006352D8A9"):
           getLastEntry("John")
   if(ivalue==4):
     print("Remove Last Entry..")
     print("Swipe your card!")
     display.lcdWriteFirstLine("Hi Their!. Please..")
     display.lcdWriteSecondLine("Swipe your Card")
     reqID= read()
     if(reqID=="18008DAE4D76"):
          deleteLastEntry("Ateeq")
     elif(reqID=="4000634B650D"):
          deleteLastEntry("Altaf")
     elif(reqID=="40006352D8A9"):
          deleteLastEntry("John")

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
	if 0 < a < 5:
	  actualprocess(a)
	else:
	  print("Please press valid opton")
    except KeyboardInterrupt:
       GPIO.cleanup()
       pass

GPIO.cleanup()

if __name__ == '__main__':
    main()

 

     
