# Robbie Lowles
# Download set icons and create sets of data to use to train a CNN

import json
import requests
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
import urllib
import os

def readAllSets():
    setData = json.loads((requests.get('https://api.scryfall.com/sets').content).decode('utf8'))['data']
    setList = [[i["name"], i["icon_svg_uri"]] for i in setData]
    return sorted(setList, key=lambda k: k[0])


def downloadSetIcons(setList):
    for set in setList:
        name = set[0].replace(' ','_').replace(':','_').replace('/','')

        # Create directory for that image
        pathName = os.path.join('setIcons', name)
        os.makedirs(pathName)

        urllib.request.urlretrieve(set[1], name+'.svg')
        f = open(name+'.svg')
        svgimage = svg2rlg(f)
        f.close()

        renderPM.drawToFile(svgimage, pathName +'\\'+ name + '.png', fmt="PNG")

        if os.path.exists(pathName + '\\' + name+'.png'):
            os.remove(name+'.svg')


if __name__ == "__main__":
    # Read in all sets
    setList = readAllSets()
    downloadSetIcons(setList[467:])
