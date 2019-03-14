import requests
import simplejson as json

base_URL = 'http://127.0.0.1:5000'
command = '/sortCommands'
catalogue = '/postCollection'
info = '/cardInfo'

debug = False

# Grabs the sort/catalogue command from the DB
def getCommand():
	url = base_URL + command

	if(debug):
		r = requests.get(url, json={'debug': 1})
	else:
		r = requests.get(url, json={})

	print(r.content)
	r = json.loads(r.content)
	return r

# Requests the card information from the database
def getCardInfo(sortCol, cardName):
	url = base_URL + info
	
	if sortCol:
		r = requests.get(url, json={'cardName': cardName, 'limit': 1})
	else:
		r = requests.get(url, json={'cardName': cardName})

	cardInfo = json.loads(r.content)
	return cardInfo

# Sends the collection to the database
def sendCollection(collection):
	url = base_URL + catalogue

	r = requests.post(url, data=collection)