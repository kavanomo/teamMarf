import tensorflow as tf
from tensorflow import keras
import numpy as np
import matplotlib.pyplot as plt
import os
import cv2
from random import sample, random

checkpointPath = 'checkpoints'
checkpointDir = os.path.dirname(checkpointPath)


def plot_image(i, predictions_array, true_label, img):
    predictions_array, true_label, img = predictions_array[i], true_label[i], img[i]
    plt.grid(False)
    plt.xticks([])
    plt.yticks([])

    plt.imshow(img, cmap=plt.cm.binary)

    predicted_label = np.argmax(predictions_array)
    if predicted_label == true_label:
        color = 'blue'
    else:
        color = 'red'

    plt.xlabel("{} {:2.0f}% ({})".format(classNames[predicted_label],
                                         100 * np.max(predictions_array),
                                         classNames[true_label]),
               color=color)


def plot_value_array(i, predictions_array, true_label):
    predictions_array, true_label = predictions_array[i], true_label[i]
    plt.grid(False)
    plt.xticks([])
    plt.yticks([])
    thisplot = plt.bar(range(2), predictions_array, color="#777777")
    plt.ylim([0, 1])
    predicted_label = np.argmax(predictions_array)

    thisplot[predicted_label].set_color('red')
    thisplot[true_label].set_color('blue')


def createTrainingData():
    basePathName = './foilTraining/'
    foilPath = basePathName + 'foilCards/'
    regPath = basePathName + 'regularCards/'
    iterPathFoil = [[x[0], x[2]] for x in os.walk(basePathName)][1:]
    imgList = []
    testImgList = []
    imgLabels = []
    testImgLabels = []
    classNames = []
    for i, (path, cardList) in enumerate(iterPathFoil):
        classNames.append(path[len(basePathName):])
        for card in cardList:
            img = cv2.imread(os.path.join(path, card))
            img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
            img = cv2.resize(img, (54,46))
            rand = random()
            if random() < .2:
                testImgLabels.append(i)
                testImgList.append(img[:,:,0]/255.0)
            else:
                imgList.append(img[:,:,0]/255.0)
                imgLabels.append(i)

    imgList = np.asarray(imgList)
    imgLabels = np.asarray(imgLabels)
    testImgList = np.asarray(testImgList)
    testImgLabels = np.asarray(testImgLabels)
    return imgList, imgLabels, testImgList, testImgLabels, classNames


def createTestingData(trainImages, trainLabels):
    maxSize = len(trainLabels)
    numTestImages = maxSize//5
    randIndexes = sorted(sample(range(maxSize),numTestImages), reverse=True)
    testImages = np.take(trainImages, randIndexes)
    testLabels = np.take(trainLabels, randIndexes)
    trainLabels = np.delete(trainLabels, randIndexes)
    trainImages = np.delete(trainImages, randIndexes)

    return testImages, testLabels, trainImages, trainLabels


(trainImages, trainLabels, testImages, testLabels, classNames) = createTrainingData()
# (testImages, testLabels, trainImages, trainLabels) = createTestingData(trainImages, trainLabels)

model = keras.Sequential([
    keras.layers.Flatten(input_shape=(46, 54)),
    keras.layers.Dense(64, activation=tf.nn.relu, kernel_regularizer=keras.regularizers.l2(.003)),
    keras.layers.Dense(64, activation=tf.nn.relu, kernel_regularizer=keras.regularizers.l2(.003)),
    keras.layers.Dense(len(trainLabels), activation=tf.nn.softmax)
])

callbackCheck = tf.keras.callbacks.ModelCheckpoint(checkpointPath, save_weights_only=True, verbose=1)

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

model.fit(trainImages, trainLabels, epochs=50) #, callbacks=callbackCheck)

testLoss, testAcc = model.evaluate(testImages, testLabels)
model.save('foilMode.h5')
predictions = model.predict(testImages)[:,:2]

num_rows = 5
num_cols = 3
num_images = num_rows*num_cols
plt.figure(figsize=(2*2*num_cols, 2*num_rows))
for i in range(num_images):
  plt.subplot(num_rows, 2*num_cols, 2*i+1)
  plot_image(i, predictions, testLabels, testImages)
  plt.subplot(num_rows, 2*num_cols, 2*i+2)
  plot_value_array(i, predictions, testLabels)
plt.show()