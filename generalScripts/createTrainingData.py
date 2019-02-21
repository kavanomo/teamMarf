from PIL import Image, ImageOps
import json
import random
import os
import requests
import cv2
from io import BytesIO
import numpy as np
import urllib.request as url
import time

similarSets = json.load(open('SimilarSets.json', encoding='utf8'))


def getSmallerSize(img):
    size = 28
    return size, size
    # width, height = img.size
    # if width > height:
    #     scaleFactor = size/height
    #     width = int(width*scaleFactor)
    #     return width, size
    # else:
    #     scaleFactor = size/width
    #     height = int(height*scaleFactor)
    #     return size, height


def saltPepperNoise(img):
    prob = .08
    noiseImg = img.copy()
    (height, width) = noiseImg.size
    for pixH in range(height):
        for pixW in range(width):
            roll = random.random()
            if roll < prob/2:
                # Black pixel
                noiseImg.putpixel((pixH, pixW), (0, 0, 0))
            if roll > 1 - prob/2:
                # White pixel
                noiseImg.putpixel((pixH, pixW), (255, 255, 255))

    return noiseImg


def createTrainingData(setList):
    basePath = 'trainingData'
    for set in setList:
        setName = set['name']
        pathName = os.path.join(basePath, setName)
        os.makedirs(pathName)
        baseName = pathName + '\\' + setName
        image = Image.open(set['filePath'])
        width, height = getSmallerSize(image)

        for i in range(0,4):
            angle = i*90
            rotImage = image.rotate(angle,expand=True, resample=Image.BILINEAR)
            invertImage = ImageOps.invert(rotImage)
            rotImage = rotImage.resize((width, height), Image.ANTIALIAS)
            invertImage = invertImage.resize((width, height), Image.ANTIALIAS)

            noiseRotImage = saltPepperNoise(rotImage)
            noiseInvImage = saltPepperNoise(invertImage)

            rotImage.save(baseName + '_' + str(angle) + '.png')
            invertImage.save(baseName + '_inv_' + str(angle) + '.png')
            noiseRotImage.save(baseName + '_' + str(angle) + '_noise_' + '.png')
            noiseInvImage.save(baseName + '_inv_' + str(angle) + '_noise_' +'.png')


def readInSetList():
    return json.load(open('SimilarSets.json', encoding="utf8"))


def returnTrainingData():
    setImagePaths = json.load(open('SimilarSets.json', encoding="utf8"))
    pathName = './trainingData/'
    imgList = []
    imgLabels = []
    classNames = []
    iterPaths = [[x[0], x[2]] for x in os.walk(pathName)][1:]
    for i, (path, cardList) in enumerate(iterPaths):
        setName = path[len(pathName):]
        classNames.append(setName)
        for imgPath in cardList:
            img = cv2.imread(os.path.join(path, imgPath))
            imgList.append(img)
            imgLabels.append(i)

    return (imgList, imgLabels, classNames)


def findParentSet(setName):
    for set in similarSets:
        if setName in set['equivalents']:
            return set['name']


def createTestingData():
    scryfallCardList = json.load(open('scryfall-default-cards.json', encoding='utf8'))
    testLoc = 'testingData'
    os.makedirs(testLoc)
    testData = []
    for card in scryfallCardList:
        if 'image_uris' in card:
            imageUrl = card['image_uris']['large']

            try:
                imgResponse = url.urlopen(imageUrl)
                imgNpArray = np.array(bytearray(imgResponse.read()), dtype=np.uint8)
                img = cv2.imdecode(imgNpArray, -1)[530:630, 520:630]
                img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                ret, img_bw = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
                cardIdentifier = card['id']
                set = card['set_name'].replace(' ','_').replace(':','_').replace('/','')

                parentSet = findParentSet(set)
                imgLoc = os.path.join(testLoc, cardIdentifier)
                testData.append([imgLoc, parentSet])
                cv2.imwrite(imgLoc + '.png', img_bw)
            except:
                print('Failed:\n' + imageUrl)

            time.sleep(.1)


    f = open('TestDataList.json', 'w')
    json.dump(testData, f)




if __name__ == '__main__':
    createTestingData()

    # setList = readInSetList()
    # createTrainingData(setList)