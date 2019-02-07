import smbus2
import time

bus = smbus.SMBus(1)

# slave address, set up in the arduino 
address = 0x08

def writeMsg(value):
	bus.write_byte(address, value)
	return 0

def readMsg():
	msg = bus.read_byte_data(address, 0)
	return msg

while True:
	data = raw_input("Enter data to be sent: ")
	data_list = list(data)
	for i in data_list:
		writeMsg(int(ord(i)))
		time.sleep(.1)

	msg = readMsg()
	print(msg) xcc