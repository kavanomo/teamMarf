from PIL import Image, ImageOps
import json
import random
import os
import numpy as np


def getSmallerSize(img):
    size = 25
    width, height = img.size
    if width > height:
        scaleFactor = size/height
        width = int(width*scaleFactor)
        return width, size
    else:
        scaleFactor = size/width
        height = int(height*scaleFactor)
        return size, height



def saltPepperNoise(img):
    return img



def createTrainingData(setList):
    basePath = 'trainingData'
    for set in setList:
        setName = set['name']
        pathName = os.path.join(basePath, setName)
        # os.makedirs(pathName)
        baseName = pathName + '\\' + setName
        image = Image.open(set['filePath'])
        width, height = getSmallerSize(image)

        for i in range(0,4):
            angle = i*90
            rotImage = image.rotate(angle)
            invertImage = ImageOps.invert(rotImage)
            rotImage = rotImage.resize((width, height), Image.ANTIALIAS)
            invertImage = invertImage.resize((width, height), Image.ANTIALIAS)

            noiseRotImage = saltPepperNoise(rotImage)
            noiseInvImage = saltPepperNoise(invertImage)

            rotImage.save(baseName + '_' + str(angle) + '.png')
            invertImage.save(baseName + '_inv_' + str(angle) + '.png')
            noiseRotImage.save(baseName + '_' + str(angle) + '_n_' + '.png')
            noiseInvImage.save(baseName + '_inv_' + str(angle) + '_n_' +'.png')


def readInSetList():
    return json.load(open('SimilarSets.json', encoding="utf8"))


if __name__ == '__main__':
    setList = readInSetList()
    createTrainingData(setList[:1])