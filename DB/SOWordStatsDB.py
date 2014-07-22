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
	print()
	nonPunct = re.compile('.*[A-Za-z0-9].*')
	text = str(etree.tostring(root,pretty_print = True)[10:-11])[1:].lower()\
	.replace('\\n',' ')\
	.replace("\\",'')\
	.replace("?","")
	title = title.lower().replace("?","")
	tokens = nltk.word_tokenize(text + " " + title)
	filtered = [w for w in tokens if nonPunct.match(w)]
	return filtered


def drawABarChart(wordCounter,directory,cmdArgs):
	wordList = wordCounter.most_common(25)
	bar_chart = pygal.Bar()
	bar_chart.title = 'Word Count stats'
	for element in wordList:
		bar_chart.add(element[0],element[1])
	bar_chart.render_to_file(directory + "\\chart_wordstats_"+cmdArgs["tag"]+".svg")

def readDBQuestionsToCounter(cmdArgs):
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

	cursorDB.close()
	conn.close()
	return wordCounter


def main():
	mainDir = os.getcwd()
	parser = argparse.ArgumentParser(description='This script cmmunicates with the database \n +\
												to produce charts that represent word statistics for questions given a certain question tag . Ex: \n \n +\
												What words appear most frequently in the questions marked by the tag "python"')
	parser.add_argument('-t','--tag', help='Name of the tag', required=True)
	parser.add_argument('-s','--score', help='minimum score of a question (default 20)', type=int, default=20)
	args = vars(parser.parse_args())

	wordCounter = readDBQuestionsToCounter(args)

	#get rid of the stopwords
	stops = set(stopwords.words('english'))
	for stopword in stops:
		if stopword not in ["why","how"]:
			wordCounter[stopword] = 0

	cleaning = ["'s","n't","'m","y","f","|y",""]
	for word in cleaning:
		if word in wordCounter:
			wordCounter[word] = 0

	drawABarChart(wordCounter,mainDir,args)

main()