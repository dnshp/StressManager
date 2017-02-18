import json
import os
import csv
from os.path import join, dirname
from watson_developer_cloud import AlchemyLanguageV1

alchemy_language = AlchemyLanguageV1(api_key="521aadb81fb565335229d278046fc068a6cb319c")
STRESS_THRESHOLD = 0.9

userInput = "We the People of the United States, in Order to form a more perfect Union, establish Justice, insure domestic Tranquility, provide for the common defence, promote the general Welfare, and secure the Blessings of Liberty to ourselves and our Posterity, do ordain and establish this Constitution for the United States of America."

def get_emotion(userMessage):
	emotionsDict = json.loads(json.dumps(alchemy_language.emotion(text=userMessage), indent=2))['docEmotions']
	for i in emotionsDict:
		emotionsDict[i] = float(emotionsDict[i])
	return max(emotionsDict, key=emotionsDict.get), 1 - emotionsDict['joy']

def get_all_keywords(userMessage):
	dataDump = json.loads(json.dumps(alchemy_language.keywords(text=userMessage), indent=2))['keywords']
	keywords = []
	for i in range(len(dataDump)):
		keywords.append(dataDump[i]['text'])
	return keywords

def check_in(message):
	#dominantEmotion, stressRating = get_emotion(message)
	#keywords = get_all_keywords(message)
	dominantEmotion, keywords, stressRating = "joy", ["a"], 0.34
	if stressRating > STRESS_THRESHOLD:
		# Do thing about suicide prevention here
		suicide_prevention(keywords)
		return
	if dominantEmotion == "joy":
		update_history(message, keywords)
	else:
		return stress_relief()

def load_history():
	historyDict = {}
	with open("history.txt", "r") as csvfile:
		csvreader = csv.reader(csvfile, delimiter=',')
		for line in csvreader:
			historyDict[line[0]] = line[1]
	return historyDict

def write_history(history):
	os.remove("history.txt")
	with open("history.txt", "w") as csvfile:
		csvwriter = csv.writer(csvfile)
		for i in history:
			csvwriter.writerow([i, history[i]])

def update_history(message, keywords):
	historyDict = load_history()
	print(historyDict)
	for k in keywords:
		if k not in historyDict:
			historyDict[k] = 0
		historyDict[k] = int(historyDict[k]) + 1
	write_history(historyDict)
	return historyDict

def stress_relief():
	historyDict = load_history()
	suggestions = []
	for i in range(3):
		rmkey = max(historyDict, key=historyDict.get)
		suggestions.append(rmkey)
		historyDict.pop(rmkey)
	return suggestions

def suicide_prevention(keywords):
	return keywords

print(check_in("joy"))