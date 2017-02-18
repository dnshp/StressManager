import json
import os
import csv
from os.path import join, dirname
from watson_developer_cloud import AlchemyLanguageV1

alchemy_language = AlchemyLanguageV1(api_key="521aadb81fb565335229d278046fc068a6cb319c")
STRESS_THRESHOLD = 0.9

userInput = "We the People of the United States, in Order to form a more perfect Union, establish Justice, insure domestic Tranquility, provide for the common defence, promote the general Welfare, and secure the Blessings of Liberty to ourselves and our Posterity, do ordain and establish this Constitution for the United States of America."

def getEmotion(userMessage):
	emotionsDict = json.loads(json.dumps(alchemy_language.emotion(text=userMessage), indent=2))['docEmotions']
	for i in emotionsDict:
		emotionsDict[i] = float(emotionsDict[i])
	return max(emotionsDict, key=emotionsDict.get), 1 - emotionsDict['joy']

def getAllKeywords(userMessage):
	dataDump = json.loads(json.dumps(alchemy_language.keywords(text=userMessage), indent=2))['keywords']
	keywords = []
	for i in range(len(dataDump)):
		keywords.append(dataDump[i]['text'])
	return keywords

def checkIn(message):
	dominantEmotion, stressRating = getEmotion(message)
	keywords = getAllKeywords(message)
	#dominantEmotion, keywords, stressRating = "anger", ["a"], 0.34
	if stressRating > STRESS_THRESHOLD:
		# Do thing about suicide prevention here
		return
	if dominantEmotion == "joy":
		updateHistory(message)
	else:
		return stressRelief()

def loadHistory():
	historyDict = {}
	with open("history.txt", "r") as csvfile:
		csvreader = csv.reader(csvfile, delimiter=',')
		for line in csvreader:
			historyDict[line[0]] = line[1]
	return historyDict

def writeHistory(history):
	os.remove("history.txt")
	with open("history.txt", "w") as csvfile:
		csvwriter = csv.writer(csvfile)
		for i in history:
			csvwriter.writerow([i, historyDict[i]])

def updateHistory(message):
	historyDict = loadHistory()
	for k in keywords:
		if k not in historyDict:
			historyDict[k] = 0
		historyDict[k] = int(historyDict[k]) + 1
	writeHistory(historyDict)
	return historyDict

def stressRelief():
	historyDict = loadHistory()
	suggestions = []
	for i in range(3):
		rmkey = max(historyDict, key=historyDict.get)
		suggestions.append(rmkey)
		historyDict.pop(rmkey)
	return suggestions

#print(checkIn("joy", ["a","b"]))
