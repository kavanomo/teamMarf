from PIL import Image
from picamera import PiCamera
import pytesseract
import argparse
import cv2
import os

camera = PiCamera()
path = '/home/pi/firmware/imageRec/image.png'

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
