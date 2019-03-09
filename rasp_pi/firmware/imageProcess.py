from PIL import Image
from picamera import PiCamera
import pytesseract
import argparse
import cv2
import os
# from time import sleep

camera = PiCamera()
path = '/home/pi/firmware/imageRec/image.jpg'

'''
Takes a picture and saves it in the specified "path" (global variable)
Commented out parts allow you to view the image on a display, then take
the picture by pressing a key.

PARAMETERS
none

RETURNS
none
'''
def takePicture():
	#camera.start_preview()
	#input()
	camera.capture(path)
	#camera.stop_preview()
	#sleep(2)


'''
Function that compares values returned from set symbol recognition thing 
with the confidenceArray and decides on the most likely set symbol 
(probably put in the imageProcess file)

PARAMETERS
class_names: The list of sets that are mapped to the confidence array
possibleSets: The list of possible sets

RETURNS
The most likely set that the card belongs to

'''
def setRecognition(classNames, possibleSets):
	################ PLACEHOLDER HARDCODED VALUES ################
	confidenceArray = [1.6707758e-06, 8.3274145e-08, 9.8423456e-08, 1.9251273e-07]
	################ PLACEHOLDER HARDCODED VALUES ################
	confidence = 0
	likelySet = "None"

	for i in possibleSets:
		index = classNames.index(i)
		if (confidenceArray[index] > confidence):
			likelySet = i
			confidence = confidenceArray[index]

	return likelySet

'''
Processes the image taken and uses PyTesseract to extract the card name

PARAMETERS
none

RETURNS
The text extracted from the card (the name)
'''
def textRecognition():
	# load the example image and convert it to grayscale
	image = cv2.imread(path)

	#TODO: These numbers will need to be fiddled around with
	crop_img = image[0:100, 105:1000]
	gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)
	#gray = cv2.bitwise_not(gray)
	gray = cv2.threshold(gray, 0, 255,
		cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
	 
	# write the grayscale image to disk as a temporary file so we can
	# apply OCR to it
	filename = "{}.png".format(os.getpid())
	cv2.imwrite(filename, gray)

	# load the image as a PIL/Pillow image, apply OCR, and then delete
	# the temporary file
	text = pytesseract.image_to_string(Image.open(filename))	
	os.remove(filename)

	return text
