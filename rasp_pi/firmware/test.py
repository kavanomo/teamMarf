# picture taking -> text recognition -> server comms testing
import serverComms
import imageProcess
import simplejson as json

#Global Definitions
bucketCaps = [0, 0, 0, 0, 0, 0]
currPos = 0

'''
Determines the correct number of turns as well as the direction

PARAMETERS
posNow - The current position
posBefore - The old position

RETURNS
The number of turns needed with direction, encoded into the appropriate number
'''
def calcNumTurns(posBefore, posNow):
	diff = abs(posNow - posBefore)
	special = False

	#TODO: Think of a better algorithm for this....
	if (diff == 0):
		return 0
	elif (diff == 4):
		diff = 2
		special = True
	elif (diff == 5):
		diff = 1
		special = True

	# Bit shifting to the left by 1 is equivalent to multiplying by 2
	diff = diff * 2

	# Adding 1 = right, left otherwise
	if (special):
		if (posBefore >= 4):
			diff = diff + 1
	else:
		if ((diff == 6) or (posNow > posBefore)):
			diff = diff + 1

	return diff

'''
Finds the correct bucket to put the card into. Returns the number of turns 
to the main function

PARAMETERS
cur - the value (price or colour) of the card currently being sorted
sortBy - what we're sorting by
buckets - a list of all the categories we're sorting by

RETURNS
The number of turns needed
'''
def findBucket(cur, sortBy, buckets):
	global bucketCaps
	global currPos
	count = 0
	oldPos = currPos
	match = False
	
	if (sortBy == "col"):
		for i in buckets:
			if cur == i:
				currPos = count
				match = True
			else:
				count = count + 1

	elif (sortBy == "val"):
		for i in buckets:
			if ((cur >= (i["val1"])) and (cur <= (i["val2"]))):
				currPos = count
				match = True
			else:
				count = count + 1

	else:
		# This is the default case for if we're cataloguing
		match = True

	# Check to see if the bucket we're supposed to put it in is full/not matched
	# Put into the overflow bucket otherwise, or the next if cataloguing
	if ((bucketCaps[currPos] == 150) or (not match)):
		if (sortBy == "cat"):
			currPos = currPos + 1
		else:
			currPos = 5

	# Increase the number of cards in the current bucket
	bucketCaps[currPos] = bucketCaps[currPos] + 1

	# Calculate the number of turns needed depending on the old and new positions
	numTurns = calcNumTurns(oldPos, currPos)
	return numTurns

#################################### MAIN ####################################

with open('SimilarSets.json') as f:
	data = json.load(f)

classNames = []
for i in range(0, len(data["sets"])):
	classNames.append(data["sets"][i]["name"])

cmd = serverComms.getCommand()
while(len(cmd) == 0):
	cmd = serverComms.getCommand()
	print("CMD")
	print(cmd)

cmd = cmd[0]

username = cmd['data']['userName']
sortType = cmd['data']['sortType']

if (sortType != 'cat'):
	cats = cmd['data']['categories']
	categories = []
	for i in cats:
		categories.append(cmd['data']['categories'][i])
	print("CATEGORIES")
	print(categories)

imageProcess.takePicture()
imageProcess.preProcessImage()
cardName = imageProcess.textRecognition()
print("CARDNAME")
print(cardName)

cardInfo = serverComms.getCardInfo(True, cardName)

if (sortType == 'col'):
	colour = cardInfo['cardInfo']['colour']
	print(colour)

	# Move the bucket tree to the correct position
	numTurns = findBucket(colour, sortType, categories)
	# 16 = B10000
	msg = 16 + numTurns
	print("msg: " + str(msg))
	print("currPos: " + str(currPos))
	print(bucketCaps)

# User collection testing
'''
import serverComms
import json

totalValue = 0
collection = []

for i in range (0, 11):
	cardName = "card" + str(i)
	value = i
	if (i % 2 == 0):
		foiled = 1
	else:
		foiled = 0

	entry = {"name": cardName, "price": value, "foiled": foiled}

	collection.append(entry)
	totalValue = totalValue + value

username = "Thomas Senlin"

userCollect = {"userName": username, "collectionValue": totalValue, "collection": collection}

#print(userCollect)

serverComms.sendCollection(userCollect)

results = serverComms.getCollection()
username = results["username"]
print(username)
value = results["value"]
print(value)
collection = results["collection"]
collect = json.loads(collection)
print(collect)
print(collect[0]["name"])
'''


#############################################################

#i2cComms testing
'''
import i2cComms
from time import sleep

while(1):
	text = input("Command to send: ")
	text = int(text)

	if(text == 0):
		print("initialize")
		i2cComms.writeNumber(0)
	elif(text == 1):
		print("vacuum")
		i2cComms.writeNumber(8)
	elif(text == 2):
		print("rotate tree")
		turns = input("num turns: ")
		direc = input("direction: ")
		msg = 16 + (2*int(turns)) + int(direc)
		print(bin(msg))
		i2cComms.writeNumber(msg)
	elif(text == 3):
		print("deinitialize")
		i2cComms.writeNumber(24)

	done = i2cComms.readNumber()
	print(done)
	while(done != 1):
		sleep(1)
		done = i2cComms.readNumber()
		print(done)
'''