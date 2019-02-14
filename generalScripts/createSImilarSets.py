import cv2
import numpy as np
import os
import json

def getImageList():
    """
    Get a 2d list of all set icons. First column should be directory/path to file, second should be the set name
    :return:
    """
    pathName = os.path.join('./setIcons/')
    imgList = []
    iterPaths = iter(os.walk(pathName))

    for obj in iterPaths:
        path, subDir, image = obj
        imgList.append([obj[0], obj[2]])

    return imgList[1:]


def imgEquivalence(imgA, imgB):
    diff = np.mean(imgA != imgB)
    if diff < .02:
        return True
    return False

    # return np.array_equal(imgA, imgB)


def constructSimilarSets(imgList):
    similarSets = []

    for i in range(len(imgList)):
        if i > len(imgList) - 1:
            break

        path, image = imgList[i]
        imPath = os.path.join(path, image[0])
        currentImage = cv2.imread(imPath)
        setName = image[0][:-4]
        setGroup = {setName: [imPath]}

        simSetIndeces = []

        for j in range(i+1, i+10):
            if j > len(imgList)-1:
                break

            nextPath, nextImage = imgList[j]
            nextImPath = os.path.join(nextPath, nextImage[0])
            nextImage = cv2.imread(nextImPath)

            if imgEquivalence(currentImage, nextImage):
                setGroup[setName].append(nextImPath)
                simSetIndeces.append(j)

        for index in sorted(simSetIndeces, reverse=True):
            del imgList[index]

        similarSets.append(setGroup)

    return similarSets


if __name__ == "__main__":
    imList = getImageList()
    simSetList = constructSimilarSets(imList)
    f = open('SimilarSets.json', 'w')
    json.dump(simSetList, f)

