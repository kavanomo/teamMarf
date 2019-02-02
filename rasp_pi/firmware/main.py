import serial
import RPi.GPIO as GPIO
import time

ser = serial.Serial("/dev/ttyACM0", 9600)
ser.baudrate = 9600
time.sleep(2) #This is needed to let the Arduino set up first, according to its documentation
ser.write(b'this is a test message')