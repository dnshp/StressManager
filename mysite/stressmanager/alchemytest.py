import json
import os
import csv
from os.path import join, dirname
from watson_developer_cloud import AlchemyLanguageV1

alchemy_language = AlchemyLanguageV1(api_key="521aadb81fb565335229d278046fc068a6cb319c")
STRESS_THRESHOLD = 0.95

userInput="i feel happy when i take a nap"

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

def check_in(message, histFile, user):
	dominantEmotion, stressRating = get_emotion(message)
	keywords = get_all_keywords(message)
	if edge_cases(message):
		return suicide_prevention()
	if dominantEmotion == "joy":
		return update_history(message, keywords, histFile, user)
	else:
		return stress_relief(user)

def load_history(histFile, user):
	historyDict = {}
	others = []
	with open(histFile, "r") as csvfile:
		csvreader = csv.reader(csvfile)
		for line in csvreader:
			if line[0] == user:
				historyDict[line[1]] = line[2]
			else:
				others.append([line[0], line[1], line[2]])
	with open(histFile, "w") as csvfile:
		csvwriter = csv.writer(csvfile)
		for i in others:
			csvwriter.writerow(i)
	return historyDict

def write_history(history, histFile, user):
	others = []
	with open(histFile, "r") as csvfile:
		csvreader = csv.reader(csvfile)
		for line in csvreader:
			print(line)
			print(type(line))
			others.append(line)
	os.remove(histFile)
	with open(histFile, "w+") as csvfile:
		csvwriter = csv.writer(csvfile)
		for i in history:
			csvwriter.writerow([user, i, history[i]])
		for j in others:
			csvwriter.writerow(j)

def update_history(message, keywords, histFile, user):
	historyDict = load_history(histFile, user)
	for k in keywords:
		if k not in historyDict:
			historyDict[k] = 0
		historyDict[k] = int(historyDict[k]) + 1
	write_history(historyDict, histFile, user)
	return "Your response has been logged. Have a nice day! :)"

def stress_relief(user):
	historyDict = dict_items_to_ints(load_history("history.txt", user))
	suggestions = []
	if len(historyDict) < 3:
		return "In general, people find it helpful to meditate, rest, or interact with others when they are stressed. Do not be afraid to speak to professors and ask for any support that you may need."
	for i in range(3):
		rmkey = max(historyDict, key=historyDict.get)
		suggestions.append(rmkey)
		historyDict.pop(rmkey)
	rv = "According to your recent logs, the following things tend to make you feel better: "
	for i in range(len(suggestions) - 1):
		rv += suggestions[i] + ", "
	rv += suggestions[-1]
	return rv

def suicide_prevention():
	#Extreme case: stressRating > THRESHOLD
	return "You appear to be dealing with a significant amount of anxiety and stress. \n We suggest that you consider the following: \n 	1. Speak with other classmates if you are stressed \n 	2. Contact your professors if you need extensions on any assignments \n 	3. Contact support groups near you \n 	4. Contact your university's health or counseling center \n 	5. Contact the National Suicide Prevention Lifeline at 1-800-273-8255"

def dict_items_to_ints(dct):
	#Helper function to convert dictionary items to integers
	for i in dct:
		dct[i] = int(dct[i])
	return dct

def edge_cases(message):
	#Filters message for edge cases that would result in Extreme case
	forbidden_words=["cut myself", "jump off a cliff", "lethal injection", "self-slaughter", "commit suicide", "kill myself", "life is pointless", "i am worthless"]
	return any([w in message.lower() for w in forbidden_words])

#check_in(userInput, "history.txt")