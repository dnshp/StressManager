import json
import os
import csv
from os.path import join, dirname
from watson_developer_cloud import AlchemyLanguageV1
from textblob import TextBlob

alchemy_language = AlchemyLanguageV1(api_key="521aadb81fb565335229d278046fc068a6cb319c")

userInput = "We the People of the United States, in Order to form a more perfect Union, establish Justice, insure domestic Tranquility, provide for the common defence, promote the general Welfare, and secure the Blessings of Liberty to ourselves and our Posterity, do ordain and establish this Constitution for the United States of America."

#combined_operations = ['page-image', 'entity', 'keyword', 'title', 'author', 'taxonomy', 'concept', 'doc-emotion']

def getEmotion(userMood):
	emotionsDict = json.loads(json.dumps(alchemy_language.emotion(text=userInput), indent=2))['docEmotions']
	for i in emotionsDict:
		emotionsDict[i] = float(emotionsDict[i])
	return max(emotionsDict, key=emotionsDict.get)

#print(getEmotion("I saw a cute dog today"))

def getAllKeywords(userMessage):
	dataDump = json.loads(json.dumps(alchemy_language.keywords(text=userMessage), indent=2))['keywords']
	keywords = []
	for i in range(len(dataDump)):
		keywords.append(dataDump[i]['text'])
	return keywords

def checkIn(mood, message):
	dominantEmotion, keywords = getEmotion(mood), getAllKeywords(message)
	#dominantEmotion, keywords = "joy", ["a"]
	if dominantEmotion == "joy":
		updateHistory(mood, message)
	else:
		# Suggest stress relievers
		return

def updateHistory(mood, message):
		historyDict = {}
		with open("history.txt", "r") as csvfile:
			csvreader = csv.reader(csvfile, delimiter=',')
			for line in csvreader:
				historyDict[line[0]] = line[1]
		for k in keywords:
			if k not in historyDict:
				historyDict[k] = 0
			historyDict[k] = int(historyDict[k]) + 1
		print(historyDict)
		os.remove("history.txt")
		with open("history.txt", "w") as csvfile:
			csvwriter = csv.writer(csvfile)
			for i in historyDict:
				csvwriter.writerow([i, historyDict[i]])

updateHistory("I saw a cute dog today", userInput)
