import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)
# The swivel head motor. 13 - D1 on/off. 15 - D2 direction
GPIO.setup(13, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(15, GPIO.OUT, initial=GPIO.LOW)

while(1):
	text = input("Direction (U - Up, D - Down): ")
	if(text == 'U'):
		print("We're going up")
		GPIO.output(15, GPIO.HIGH)

		for x in range(0, 33):
			GPIO.output(13, GPIO.HIGH)
			sleep(0.015)
			GPIO.output(13, GPIO.LOW)
			sleep(0.015)

	elif(text == 'D'):
		print("We're going down")
		GPIO.output(15, GPIO.LOW)

		for x in range(0, 33):
			GPIO.output(13, GPIO.HIGH)
			sleep(0.015)
			GPIO.output(13, GPIO.LOW)
			sleep(0.015)

