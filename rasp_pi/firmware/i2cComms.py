import smbus2
import time

#Set to 3 because we're using software i2c
bus = smbus2.SMBus(3)

address = 0x04

#Writes a value to the Uno
def writeNumber(value):
    bus.write_byte(address, value)
    return -1

#Reads a value from the Uno
def readNumber():
    number = bus.read_byte(address)
    return number