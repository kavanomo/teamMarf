#i2cComms testing

import i2cComms
from time import sleep

while(1):
	text = input("Command to send: ")
	text = int(text)

	if(text == 0):
		print("initialize")
		i2cComms.writeNumber(0)
	elif(text == 1):
		print("vacuum")
		i2cComms.writeNumber(8)
	elif(text == 2):
		print("rotate tree")
		turns = input("num turns: ")
		direc = input("direction: ")
		msg = 16 + (2*int(turns)) + int(direc)
		print(bin(msg))
		i2cComms.writeNumber(msg)
	elif(text == 3):
		print("deinitialize")
		i2cComms.writeNumber(24)

	done = i2cComms.readNumber()
	print(done)
	while(done != 1):
		sleep(1)
		done = i2cComms.readNumber()
		print(done)

# limit switch and stuff testing
'''
import RPi.GPIO as GPIO

# Limit switch setup. 36 - Tower. 38 - Bucket Tree.
GPIO.setup(36, GPIO.IN)
GPIO.setup(38, GPIO.IN)

while(1):
	if (GPIO.input(36)):
		print("Tower Limit")
	if (GPIO.input(38)):
		print("Bucket Tree Limit")
'''