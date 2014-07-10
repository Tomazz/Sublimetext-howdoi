import sys
import xml.etree.ElementTree as ET
import stackexchange
import os
from lxml import etree
from io import StringIO
import json
import time
import pygal
from collections import Counter

#Script that collects the full content of questions returned by the query

sys.path.append('.')
site = stackexchange.Site(stackexchange.StackOverflow,"wZjX24zp2Y3wv6THqhZyPQ((")
site.be_inclusive()

def readJSONQuestionsToDict(directory):
	infoDict = {}
	with open(directory+"\\TagStats.json","r") as infoFile:
		infoDict = json.loads(infoFile.read())
	return infoDict["content"]

def drawABarChart(tagDict,directory):
	popularLanguages = ["java","c#","python","c++","sql","mysql",\
	"objective-c",".net","ruby-on-rails","ruby",\
	"ajax","javascript","jquery","php","c","android","iphone",\
	"sql-server","html","css","django","vb.net","html5","asp.net-mvc","ios","wpf",\
	"ruby-on-rails-3","asp.net","facebook","osx","swing","angularjs","node.js","spring","actionscript-3","asp.net-mvc-3","winforms"]
	
	tagCounter = Counter(tagDict)
	for element in tagCounter:
		if element in popularLanguages:
			tagCounter[element] = 0

	dupa = tagCounter.most_common(100)
	for element in dupa:
		print(element)
	tagList = tagCounter.most_common(25)
	bar_chart = pygal.Bar()
	bar_chart.title = 'Tag popularity stats'
	for element in tagList:
		bar_chart.add(element[0],element[1])
	bar_chart.render_to_file(directory + "\\chart.svg")


#create the directory for the mined StackOverflow code snippets
directory = dataDirectory = os.getcwd() + "\\StackOverflow\\TagStats"
dataDirectory = os.getcwd() + "\\StackOverflowData"
if not os.path.exists(directory):
	os.makedirs(directory)

tagsDict = readJSONQuestionsToDict(dataDirectory)

drawABarChart(tagsDict,directory)
