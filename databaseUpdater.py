# Robbie Lowles
# This script is designed to query an online API of M:TG cards and update a MySQL database with relevant info

import json
import mysql.connector
import datetime
import requests

secrets = json.load(open('secrets.json', encoding="utf8"))
output = requests.get('https://api.cardmarket.com/ws/v2.0/priceguide')

teamMarfDB = mysql.connector.connect(
    host=secrets['host'],
    port=secrets['port'],
    user=secrets['user'],
    password=secrets['password'],
    db=secrets['db']
)

# Every 2 weeks, run this curl command and update access_token
# curl --include --request POST --header "applicationt_type=client_credentials&client_id=85688862-7348-41C7-AE6A-C5F970B6A6A6&client_secret=F29D0FAC-8ED2-4C84-9346-4301D4656DA3" 'https://api.tcgplayer.com/token'

tcgApiSecrets = {
    "publicKey": secrets['publicKey'],
    "privateKey": secrets['privateKey'],
    "applicationId": secrets['applicationId'],
    "token": secrets["accessToken"]
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

def authTcgApi():
    url = tcgApiEndpoints['auth'] + tcgApiSecrets["token"]
    response = requests.request("POST", url)
    print(response.text)


def readAllCards():
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
    setsApiResponse = json.loads((requests.get('https://api.scryfall.com/sets').content).decode('utf8'))['data']
    allSets = []
    for element in setsApiResponse:
        setTuple = (element['name'], element['icon_svg_uri'])
        allSets.append(setTuple)
    return allSets


def getPricingData():
    jsonData = json.load(open('scryfall-default-cards.json', encoding="utf8"))
    allCards = []
    currentTime = datetime.datetime.now()
    headers = {"Authorization": "bearer " + tcgApiSecrets['token']}
    url = tcgApiEndpoints["catalog"]
    response = requests.request("GET", url, headers=headers)
    print(response.text)

if __name__ == "__main__":
    processOptions = ['populate cards', 'populate sets', 'update']
    processType = processOptions[2]  # sys.argv[1] if sys.argv[1] else processOptions[0]
    mycursor = teamMarfDB.cursor()

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
        # TODO: Redo this with some sort of query builder as opposed to raw sql
        getPricingData()
