import serverComms
#import i2cComms
import time
#import RPi.GPIO as GPIO

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
	diff = abs(postNow - postBefore)
	special = False

	#TODO: Think of a better algorithm for this....
	if (diff == 0):
		return 0
	elif (diff == 4):
		diff = 2
		special = True
	elif (dif == 5):
		diff = 1
		special = True

	# Bit shifting to the left by 1 is equivalent to multiplying by 2
	diff = diff * 2

	# Adding 1 = right, left otherwise
	if (special):
		if (posBefore >= 4):
			diff = diff + 1
	else:
		if ((diff == 3) or (posNow > posBefore)):
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
	'''
	Don't forget: check if bucket is full, update the bucket capacities, etc.
	'''
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
	return 0


# Initialization 
'''i2cComms.writeNumber(0)
GPIO.setmode(GPIO.BOARD)
# The swivel head motor. 13 - D1 on/off. 15 - D2 direction
GPIO.setup(13, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)
# Limit switch setup. 36 - Tower. 38 - Bucket Tree.
GPIO.setup(36, GPIO.IN)
GPIO.setup(38, GPIO.IN)'''

# This is for if the sortType is catalogue
collection = list()
totalValue = 0

cmd = serverComms.getCommand()
while(len(cmd) == 0):
	cmd = serverComms.getCommand()
	print(cmd)

cmd = cmd[0]

# TODO: Grab the username from the command
username = 'Test'

# sortTypes can be "cat", "col", or "val"
sortType = cmd['data']['sortType']

if (sortType != 'cat'):
	cats = cmd['data']['categories']
	categories = list()
	for i in cats:
		categories.append(cmd['data']['categories'][i])
		print(categories)

# THIS IS WHEN LOOPING SHOULD HAPPEN TO TAKE PICS

# TAKE PICTURE AND GET THE NAME
# PLACEHOLDER HARDCODED VALUES		
sortType = 'val'
col = {'blue': 0, 'green': 0, 'red': 0, 'white': 0, 'black': 0}
cardName = 'Arcbound Ravager'
# PLACEHOLDER HARDCODED VALUES	

if (sortType == 'col'):
	cardInfo = serverComms.getCardInfo(True, cardName)
	colour = cardInfo['cardInfo']['colour']

	# Move the bucket tree to the correct position
	numTurns = findBucket(colour, sortType, categories)
	# 16 = B10000
	msg = 16 + numTurns
	#i2cComms.writeNumber(msg)
	pickUpCard()

elif (sortType == 'val'):
	cardInfo = serverComms.getCardInfo(False, cardName)
	# TODO: We need to do some more processing here to figure out the actual set and foiled
	foiled = True # replace with function
	possibleSets = cardInfo['sets']
	cardSet = 'Darksteel' # replace with function, give in the sets as a parameter
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
	#i2cComms.writeNumber(msg)
	pickUpCard()

else:
	cardInfo = serverComms.getCardInfo(False, cardName)
	colour = cardInfo['cardInfo']['colour']
	# TODO: We need to do some more processing here to figure out the actual set and foiled
	foiled = True # replace with function
	possibleSets = cardInfo['sets']
	cardSet = 'Darksteel' # replace with function, give in the sets as a parameter
	if (foiled):
		value = cardInfo['sets'][cardSet]['foilPrice']
		print(value)
	else:
		value = cardInfo['sets'][cardSet]['cardPriceUSD']
		print(value)

	entry = {
		"name": cardName,
		"colour": colour,
		"price": value,
		"foiled": foiled
	}
	collection.append(entry)
	totalValue = totalValue + value 

	# Move the bucket tree to the correct position
	numTurns = findBucket(0, sortType, categories)
	# 16 = B10000
	msg = 16 + numTurns
	#i2cComms.writeNumber(msg)
	pickUpCard()

