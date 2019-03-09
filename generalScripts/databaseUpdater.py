# Robbie Lowles
# This script is designed to query an online API of M:TG cards and update a MySQL database with relevant info

import random
import numpy as np
import json
import mysql.connector
import datetime
import dateutil.parser
import pytz
import requests
import collections
import sys
import time

utc = pytz.UTC

rand = random.SystemRandom()

secrets = json.load(open('../secrets.json', encoding="utf8"))

teamMarfDB = mysql.connector.connect(
    host=secrets['host'],
    port=secrets['port'],
    user=secrets['user'],
    password=secrets['password'],
    db=secrets['db']
)

tcgApiSecrets = {
    "publicKey": secrets['publicKey'],
    "privateKey": secrets['privateKey'],
    "applicationId": secrets['applicationId'],
    "token": secrets["accessToken"],
    "expires": secrets[".expires"]
}

colourKey = {'U': 'blue',
             'G': 'green',
             'R': 'red',
             'W': 'white',
             'B': 'black'}

tcgApiEndpoints = {
    "pricing": "http://api.tcgplayer.com/v1.19.0/pricing/product/",
    "auth": "http://api.tcgplayer.com/v1.19.0/app/authorize/",
    "catalog": "http://api.tcgplayer.com/v1.19.0/catalog/products/"
}


def getNewAccessToken():
    """
    If the access token is expired (it has a 2 week lifespan) we will need to update it. This function grabs the
    relevant authorization info from secrets and makes a call to TCGplayer's API. It'll now update the secrets file and
    the secrets object for the rest of the script
    :return:
    """
    headers = {'application': 'x-www-form-urlencoded'}
    data = 'grant_type=client_credentials&client_id='+tcgApiSecrets["publicKey"]+'&client_secret='+tcgApiSecrets["privateKey"]
    response = requests.post('https://api.tcgplayer.com/token', headers=headers, data=data).json()

    secrets['accessToken'] = response['access_token']
    secrets['expires'] = response['.expires']

    with open('secrets.json', 'w') as newSecrets:
        json.dump(secrets, newSecrets)
    tcgApiSecrets['token'] = response['access_token']


def authTcgApi():
    url = tcgApiEndpoints['auth'] + tcgApiSecrets["token"]
    response = requests.request("POST", url)
    print(response.text)


def readAllCards():
    """
    Open the bulk json file containing all MTG cards. Compile a list of important attributes in tuples for each card
    and return that list of card tuples.
    :return:
    """
    jsonData = json.load(open('scryfall-default-cards.json', encoding="utf8"))
    allCards = []
    currentTime = datetime.datetime.now()
    for element in jsonData:
        card = {"cardName": element['name'],
                "foil": element['foil'],
                "setName": element['set_name'],
                "cardIDNumber": element['id'],
                "typeLine": element['type_line'],
                "blue": 0,
                "green": 0,
                "red": 0,
                "white": 0,
                "black": 0,
                "lastUpdated": currentTime
                }

        # Convert array of colour initials into a string
        for colour in element['color_identity']:
            card[colourKey[colour]] = 1

        # Need specific order for the tuple
        tupleCard = (
            card["cardName"],
            card["foil"],
            card['setName'],
            card['cardIDNumber'],
            card['typeLine'],
            card['blue'],
            card['green'],
            card['red'],
            card['white'],
            card['black'],
            card['lastUpdated']
                     )
        allCards.append(tupleCard)
    return allCards


def callApiSets():
    """
    Use the Scryfall API to compile a list of all MTG sets and their icon
    Put these in a tuple so we can then populate the database
    :return:
    """
    setsApiResponse = json.loads((requests.get('https://api.scryfall.com/sets').content).decode('utf8'))['data']
    allSets = [(i["name"], i["icon_svg_uri"]) for i in setsApiResponse]
    return allSets


def splitLongQueries(longUrl, maxLength):
    """
    TCG Trader api has a max url length of 2000 characters. If we are querying a large number of cards individually,
    the url length can get quite long. This function will recursivelly break a long url into chunks less than maxLength.
    It is assumed that we want to split on a ','
    :param longUrl: A string whose length is greater than maxLength
    :param maxLength: Integer which is 2000 - the relevant url from tcgApiEndpoints
    :return: urlList: a list of urls, each of whcih are smaller than maxLength
    """
    urlList = []
    firstSlice = longUrl[:maxLength].rfind(',')
    urlList = [longUrl[:firstSlice], longUrl[firstSlice+1:]]
    if len(urlList[1]) > maxLength:
        recurList = splitLongQueries(urlList[1], maxLength)
        del urlList[-1]
        urlList.extend(recurList)

    return urlList


def getPricingData():
    """
    Update the pricing data for all cards. Update cards in batches defined by the sets
    :return:
    """

    currentTime = datetime.datetime.now().date()
    setsQuery = "SELECT setName FROM sets"
    mycursor.execute(setsQuery)
    setsOutput = mycursor.fetchall()
    headers = {"Authorization": "bearer " + tcgApiSecrets['token']}

    for set in setsOutput:
        cardsQuery = "SELECT tcgIdNumber FROM magicCards WHERE setName = \"%s\"" % (set[0])
        mycursor.execute(cardsQuery)
        cardSetList = mycursor.fetchall()

        maxLength = 2000 - len(tcgApiEndpoints['pricing'])
        cardUrlList = ','.join([str(i[0]) for i in cardSetList])
        if len(cardUrlList) > maxLength:
            cardUrlList = splitLongQueries(cardUrlList,maxLength)
            pricingData = []
            for url in cardUrlList:
                pricingData.extend(requests.request('GET', tcgApiEndpoints['pricing'] + url, headers=headers).json()['results'])

        else:
            pricingData = requests.request('GET', tcgApiEndpoints['pricing'] + cardUrlList, headers=headers).json()['results']

        cardPrices = collections.defaultdict(dict)
        for price in pricingData:
            cardPrices[str(price['productId'])][price['subTypeName']] = price['marketPrice']
            cardPrices[str(price['productId'])]['productId'] = price['productId']

        columns = 'cardPriceUSD = %(Normal)s, foilPrice = %(Foil)s, lastUpdated = \"' + str(currentTime) + '\"'
        updatePriceQuery = "UPDATE magicCards SET " + columns + " WHERE tcgIdNumber = %(productId)s;"
        mycursor.executemany(updatePriceQuery, cardPrices.values())
        teamMarfDB.commit()
        print('Updated pricing for set: ' + set[0])


    #response = requests.request("GET", url, headers=headers)
    #print(response.text)


def pushSort(sortObject):
    query = "INSERT INTO sortCommands (timestamp, sortType, numCat, categories) VALUES (%s, %s, %s, %s)"
    mycursor.execute(query, sortObject)
    teamMarfDB.commit()
    return


def createPlaceholderSorts(numSorts, sortInput):

    for sort in range(numSorts):
        currentTime = datetime.datetime.now()
        sortOptions = ['col', 'cat', 'val']
        numCats = rand.randint(1, 5)
        sortChoice = sortInput or sortOptions[rand.randint(0, len(sortOptions)-1)]
        sortJSON = {'categories': {}}

        if sortChoice == sortOptions[0]:
            # We are doing colour sorting
            colourObject = {'red': 0, 'green': 0, 'blue': 0, 'white': 0, 'black': 0}
            for cat in range(numCats):
                for col in range(rand.randint(0, 2)):
                    colourObject[np.random.choice(list(colourObject.keys()))] = 1

                sortJSON['categories']['cat'+str(cat)] = colourObject

        if sortChoice == sortOptions[1]:
            # We are doing cataloging
            numCats = 1
            sortJSON['categories'] = 'catalogue'

        if sortChoice == sortOptions[2]:
            lowBoundPrice = 0
            for cat in range(numCats):
                highBoundPrice = lowBoundPrice + rand.randint(3, 20)
                price = {'val1': lowBoundPrice, 'val2': highBoundPrice}
                sortJSON['categories']['cat'+str(cat)] = price
                lowBoundPrice = highBoundPrice

        sortObject = (currentTime, sortChoice, numCats, json.dumps(sortJSON))
        pushSort(sortObject)
        time.sleep(1)

if __name__ == "__main__":
    args = sys.argv
    processOptions = ['populate-cards', 'populate-sets', 'update', 'create-sorts']
    try:
        processType = args[1]
    except IndexError:
        processType = processOptions[3]

    mycursor = teamMarfDB.cursor()

    tokenExpiryDate = dateutil.parser.parse(tcgApiSecrets['expires'])
    if datetime.datetime.now(utc) > tokenExpiryDate:
        getNewAccessToken()

    # Read in a list of all cards
    if processType == processOptions[0]:
        allCards = readAllCards()
        placeholders = ', '.join(['%s']*len(allCards[0]))
        columns = 'cardName, foil, setName, cardIDNumber, typeLine, blue, green, red, white, black, lastUpdated'

        # TODO: Redo this with some sort of query builder as opposed to raw sql
        query = "INSERT INTO magicCards (%s) values (%s)" % (columns, placeholders)
        pages = round(len(allCards)/500)
        for page in range(pages+1):
            pageStart = page*500
            mycursor.executemany(query, allCards[pageStart:pageStart+499])
        teamMarfDB.commit()

    if processType == processOptions[1]:
        allSets = callApiSets()
        query = "INSERT INTO sets (setName, setImage) values (%s,%s)"
        mycursor.executemany(query, allSets)
        teamMarfDB.commit()

    # Update prices of cards
    if processType == processOptions[2]:
        getPricingData()

    if processType == processOptions[3]:
        try:
            numSorts = int(args[2])
        except IndexError:
            numSorts = 5

        try:
            sortInput = args[3]
        except IndexError:
            sortInput = None

        createPlaceholderSorts(numSorts, sortInput)
