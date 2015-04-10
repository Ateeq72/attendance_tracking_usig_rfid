import serial  
import RPi.GPIO as GPIO                                                #import serial module

try:
 def read_rfid ():
   ser = serial.Serial ("/dev/ttyAMA0")                           #Open named port 
   ser.baudrate = 9600                                            #Set baud rate to 9600
   data = ser.read(12)                                            #Read 12 characters from serial port to data
   ser.close ()                                                   #Close port
   return data                                                    #Return data

 id = read_rfid ()                                              #Function call

#def sql(no):
# if no == "1":
#  print("Done")

 print id 

 def card_data ():
   return id
            
#if id == "18008DAE4D76":
# print('Hi Ateeq')
# print('your reg no. 191111009')
# sql(1)
# print('done')

except KeyboardInterrupt:
 pass
