import sys
import xml.etree.ElementTree as ET
import stackexchange
import os
from lxml import etree
from io import StringIO
import json
import string
import nltk
import re
from collections import Counter
import pygal
from nltk.corpus import stopwords

#Script that reads the contents of the json file with the full contents of SO questions and parses them

#content is in HTML format
#this function removes the <code></code> elements from the question, 
#then strips off all the HTML tags,
#cleans the text a bit from the punctuation, whitespaces etc.
#and returns a list containing all the words from the question
def parseQuestionContentToList(content):
	root = etree.HTML(content)
	etree.strip_elements(root,'code',with_tail=False)
	etree.strip_tags(root,'*')
	print()
	nonPunct = re.compile('.*[A-Za-z0-9].*')
	text = str(etree.tostring(root,pretty_print = True)[10:-11])[1:].lower()\
	.replace('\\n',' ')\
	.replace("\\",'')\
	.replace("?","")
	tokens = nltk.word_tokenize(text)
	filtered = [w for w in tokens if nonPunct.match(w)]
	return filtered

def countWordsInQuestion(QuestionWordList):
	return Counter(QuestionWordList)

def drawABarChart(wordCounter,directory):
	wordList = wordCounter.most_common(30)
	bar_chart = pygal.Bar()
	bar_chart.title = 'Word Count stats'
	for element in wordList:
		bar_chart.add(element[0],element[1])
	bar_chart.render_to_file(directory + "\\chart.svg")

def readJSONQuestionsToDict(directory):
	infoDict = {}
	with open(directory,"r") as infoFile:
		infoDict = json.loads(infoFile.read())
		print(len(infoDict["content"]))
	return infoDict["content"]


def main():
	mainDir = os.getcwd() + "\\StackOverflow\\MostPopularQuestions\\"
	directory = os.getcwd() + "\\StackOverflow\\MostPopularQuestions\\MostPopularQuestions.json"
	questionsDict = readJSONQuestionsToDict(directory)
	wordCounter = Counter()
	for key in questionsDict:
		questionsDict[key] = parseQuestionContentToList(questionsDict[key])
		questionsDict[key] = countWordsInQuestion(questionsDict[key])
		print(type(questionsDict[key]))
		wordCounter.update(questionsDict[key])

	#get rid of the stopwords
	wordCounter["|y"] = 0
	stops = set(stopwords.words('english'))
	for stopword in stops:
		if stopword not in ["why","how"]:
			wordCounter[stopword] = 0
	drawABarChart(wordCounter,mainDir)

main()