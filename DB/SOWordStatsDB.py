import sys
import xml.etree.ElementTree as ET
import os
from lxml import etree
from io import StringIO
import json
import string
import nltk
import re
from collections import Counter
from nltk.corpus import stopwords
import os
import psycopg2
import getpass
import pygal
import argparse

#Script that reads the contents of the json file with the full contents of SO questions and parses them

#content is in HTML format
#this function removes the <code></code> elements from the question, 
#then strips off all the HTML tags,
#cleans the text a bit from the punctuation, whitespaces etc.
#and returns a list containing all the words from the question
def parseQuestionContentToList(body,title):
	root = etree.HTML(body)
	etree.strip_elements(root,'code',with_tail=False)
	etree.strip_tags(root,'*')
	nonPunct = re.compile('.*[A-Za-z0-9].*')
	text = str(etree.tostring(root,pretty_print = True)[10:-11])[1:].lower()\
	.replace('\\n',' ')\
	.replace("\\",'')\
	.replace("?",' ')
	title = title.lower().replace("?"," ")
	text += " " + title
	tokens = nltk.word_tokenize(text)
	filtered = [w for w in tokens if nonPunct.match(w)]
	#get rid of the punctuation that got left around the words
	for word in filtered:
		front = 0
		back = 0
		for letter in word:
			if letter not in string.punctuation:
				break
			front += 1
		for letter in reversed(word):
			if letter not in string.punctuation:
				break
			back -= 1
		if back == 0 :
			back = None
		word  = word[front:back]

	return filtered


def drawABarChart(wordCounter,directory,cmdArgs):
	wordList = wordCounter.most_common(25)
	bar_chart = pygal.Bar()
	bar_chart.title = 'Word Count stats for '+cmdArgs["tag"]
	for element in wordList:
		bar_chart.add(element[0],element[1])
	bar_chart.render_to_file(directory + "\\chart_wordstats_"+cmdArgs["tag"]+".svg")

	#how vs why
	bar_chart_hw = pygal.Bar()
	bar_chart_hw.title = 'How vs Why stats for '+cmdArgs["tag"] +" in "+str(questionCounter)+" questions"
	bar_chart_hw.add("How",wordCounter["how"])
	bar_chart_hw.add("Why",wordCounter["why"])
	bar_chart_hw.render_to_file(directory + "\\howVSwhy_"+cmdArgs["tag"]+".svg")

def readDBQuestionsToCounter(cmdArgs):
	global questionCounter
	conn = psycopg2.connect(dbname="internship2014", user="postgres", password=getpass.getpass(prompt="Password: ",stream=None))
	cursorDB = conn.cursor('wordStatsCursor')
	query1 = "SELECT body, title FROM posts WHERE tags LIKE '%<{tag}>%' AND score > {score} AND posttypeid = '1'".format(**cmdArgs) # "tag" and "score" are keys in the args dictionary. Load the tag from the dictionary into the query
	cursorDB.execute(query1) #execute query
	#create a Counter
	#then produce a list of the parsed body and title contents of the question
	wordCounter = Counter()
	for row in cursorDB:
		questionWordList = parseQuestionContentToList(row[0],row[1]) #parse the question content
		wordCounter.update(questionWordList)
		questionCounter +=1
	cursorDB.close()
	conn.close()
	return wordCounter

def saveResultsToJSON(wordCounter,cmdArgs):
	#create the directory for the mined StackOverflow code snippets
	directory = os.getcwd() + "\\data"
	if not os.path.exists(directory):
		os.makedirs(directory)

	with open(directory + "\\" + "WordStats_"+cmdArgs["tag"]+".json","w") as infoFile:
		infoDict = {}
		infoDict["description"] = "this file contains the stats regarding the word frequencies for the questions associated with the tag: "+cmdArgs["tag"]
		infoDict["content"] = dict(wordCounter)
		json.dump(infoDict,infoFile)


def removeStopwords(wordCounter):
	#get rid of the stopwords
	stops = set(stopwords.words('english'))
	for stopword in stops:
		if stopword not in ["why","how"]: #leave why and how. zero out all the other stopwords
			wordCounter[stopword] = 0

	cleaning = ["'s","n't","'m","y","f","|y","'ve","",""]
	for word in cleaning:
		if word in wordCounter:
			wordCounter[word] = 0


	return wordCounter


def main():
	mainDir = os.getcwd()
	parser = argparse.ArgumentParser(description='This script cmmunicates with the database \n +\
												to produce charts that represent word statistics for questions given a certain question tag . Ex: \n \n +\
												What words appear most frequently in the questions marked by the tag "python"')
	parser.add_argument('--tag', help='Name of the tag', required=True)
	parser.add_argument('--score', help='minimum score of a question (default 20)', type=int, default=20)
	parser.add_argument('--save', help='use this flag if you want to save the results to a JSON file', action="store_true", default=False)
	args = vars(parser.parse_args())

	wordCounter = readDBQuestionsToCounter(args)
	wordCounter = removeStopwords(wordCounter) #remove the stopwords and other useless bits of text

	if args["save"]:
		saveResultsToJSON(wordCounter,args)

	drawABarChart(wordCounter,mainDir,args)

questionCounter = 0
main()