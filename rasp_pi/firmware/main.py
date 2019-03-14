import serverComms
import i2cComms
import imageProcess
import time
import json
import pressure
import RPi.GPIO as GPIO

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

'''
Picks up and deposits the card. The sequence of actions is as follows:
1. Bring the swivelhead over
2. Check if Uno is done setting the buckets
3. Start vacuuming
4. Check if uno has picked up card
5. Bring swivelhead back
6. Tell Uno to drop the card

PARAMETERS
none

RETURNS
none
'''
def pickUpCard():
	# Swivelhead over
	#TODO: These values WILL NEED TO BE CHECKED
	GPIO.output(15, GPIO.HIGH)

	while (not GPIO.input(36)):
		GPIO.output(13, GPIO.HIGH)
		sleep(0.015)
		GPIO.output(13, GPIO.LOW)
		sleep(0.015)

	# Check if Uno is done setting the buckets
	done = i2cComms.readNumber()
	while (not done):
		sleep(0.5)
		done = i2cComms.readNumber()

	# Send vacuuming command
	i2cComms.writeNumber(8)

	curPressure = pressure.pressure()
	while (curPressure < SOME VALUE):
		pass

	# Bring swivelhead back
	GPIO.output(15, GPIO.LOW)

	while (not GPIO(input(38))):
		GPIO.output(13, GPIO.HIGH)
		sleep(0.015)
		GPIO.output(13, GPIO.LOW)
		sleep(0.015)

	# Tell Uno to drop the card
	i2cComms.writeNumber(8)

# Initialization 
GPIO.setmode(GPIO.BOARD)
# The swivel head motor. 13 - D1 on/off. 15 - D2 direction
GPIO.setup(13, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(15, GPIO.OUT, initial=GPIO.LOW)
# Limit switch setup. 36 - Tower. 38 - Bucket Tree.
GPIO.setup(36, GPIO.IN)
GPIO.setup(38, GPIO.IN)

# This is for if the sortType is catalogue
collection = list()
totalValue = 0

# Grab the set names from the JSON file
with open('SimilarSets.json') as f:
	data = json.load(f)

classNames = []
for i in range(0, len(data["sets"])):
	classNames.append(data["sets"][i]["name"])

while(1):
	cmd = serverComms.getCommand()
	while(len(cmd) == 0):
		cmd = serverComms.getCommand()
		print(cmd)

	cmd = cmd[0]

	# Init the Uno
	i2cComms.writeNumber(0)

	# TODO: Grab the username from the command, as well as initial array for 
	# confidence comparison
	username = cmd['data']['userName']

	# sortTypes can be "cat", "col", or "val"
	sortType = cmd['data']['sortType']

	if (sortType != 'cat'):
		cats = cmd['data']['categories']
		categories = list()
		for i in cats:
			categories.append(cmd['data']['categories'][i])
			print(categories)

	imageProcess.takePicture()
	imageProcess.preProcessImage()
	cardName = imageProcess.textRecognition()

	while(cardName != 'END'):
		cardInfo = serverComms.getCardInfo(True, cardName)

		# We were unable to identify the cardName correctly
		if(cardInfo['sets'] == []):
			numTurns = calcNumTurns(currPos, 5)
			currPos = 5
			# 16 = B10000
			msg = 16 + numTurns
			i2cComms.writeNumber(msg)
			pickUpCard()
		else:
			if (sortType == 'col'):
				colour = cardInfo['cardInfo']['colour']

				# Move the bucket tree to the correct position
				numTurns = findBucket(colour, sortType, categories)
				# 16 = B10000
				msg = 16 + numTurns
				i2cComms.writeNumber(msg)
				pickUpCard()

			elif (sortType == 'val'):
				foiled = imageProcess.foilRecognition()
				possibleSets = cardInfo['sets']
				cardSet = imageProcess.setRecognition(classNames, possibleSets)

				if (foiled):
					value = cardInfo['sets'][cardSet]['foilPrice']
					print(value)
				else:
					value = cardInfo['sets'][cardSet]['cardPriceUSD']
					print(value)

				# Move the bucket tree to the correct position
				numTurns = findBucket(value, sortType, categories)
				# 16 = B10000
				msg = 16 + numTurns
				i2cComms.writeNumber(msg)
				pickUpCard()

			else:
				colour = cardInfo['cardInfo']['colour']
				foiled = imageProcess.foilRecognition()
				foil = "no"
				possibleSets = cardInfo['sets']
				cardSet = imageProcess.setRecognition(classNames, possibleSets)
				if (foiled):
					value = cardInfo['sets'][cardSet]['foilPrice']
					foil = "yes"
					print(value)
				else:
					value = cardInfo['sets'][cardSet]['cardPriceUSD']
					print(value)

				entry = {"name": cardName, "price": value, "foiled": foil}

				collection.append(entry)
				totalValue = totalValue + value 

				# Move the bucket tree to the correct position. This also includes the correct direction
				numTurns = findBucket(0, sortType, categories)
				# 16 = B10000
				msg = 16 + numTurns
				i2cComms.writeNumber(msg)
				pickUpCard()

		imageProcess.takePicture()
		imageProcess.preProcessImage()
		cardName = imageProcess.textRecognition()

	# Deinit the Uno
	i2cComms.writeNumber(24)

	# Now we send all data collected if we were cataloguing
	if (sortType == 'cat'):
		userCollect = {"userName": username, "collectionValue": totalValue, "collection": collection}
		serverComms.sendCollection(json.dumps(userCollect))

		# Reset everything for the next round
		collection = []
		totalValue = 0

