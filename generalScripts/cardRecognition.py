import tensorflow as tf
from tensorflow import keras
import numpy as np
import cv2

def recognizeObject(model, image):
    """
    Given a tensorflow model and an image, classify that image based on the TF model
    :param model:
    :param image:
    :return:
    """
    img = (np.expand_dims(image, 0))
    if img.shape[1:] != model.input_shape[1:]:
        # Input image is not the same size as the desired input
        error = 'Got input shape: ' +str(img.shape[1:]) + ', expected shape: ' + str(model.input_shape[1:])
        return error

    predictions = model.predict(img)
    return predictions

# Check for Foil
foilModel = keras.models.load_model('foilMode.h5')
testImg = cv2.imread('yourCardNameHere.jpg')
testImg = cv2.cvtColor(testImg, cv2.COLOR_RGB2HSV)[:,:,0] # IMPORTANT: Take only the H channel from HSV
inputShape = foilModel.input_shape[1:] # Get the model's desired input shape
resized = cv2.resize(testImg, inputShape[::-1]) # Resize the image to the desired input shape (note that x,y are flipped

print(recognizeObject(foilModel, resized)) # Recognize the image

# Check for set icon
setIconModel = keras.models.load_model('setIconModel.h5')
# Same procedure as above, just crop the card image to a black/white box around the set icon and pass in setIconModel