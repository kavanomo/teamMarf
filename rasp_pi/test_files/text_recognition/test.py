import imageProcess
import json
from pprint import pprint

# Grab the set names from the JSON file
#imageProcess.preProcessImage();
text = imageProcess.textRecognition();

if(text == "END"):
	print("We're at the end")
else:
	print("We're not at the end :( :( :( :( :( ")
print(text)
'''
with open('SimilarSets.json') as f:
	data = json.load(f)

classNames = []
for i in range(0, len(data["sets"])):
	classNames.append(data["sets"][i]["name"])

possibleSets = ["Aether_Revolt", "15th_Anniversary_Cards", "2016_Heroes_of_the_Realm"]

foiled = imageProcess.foilRecognition()
print("This card is foiled? " + str(foiled))

sets = imageProcess.setRecognition(classNames, possibleSets)
print("The set might be: " + sets)

text = imageProcess.textRecognition()
print("The name is: " + text)
'''