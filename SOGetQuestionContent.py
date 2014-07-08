import sys
import xml.etree.ElementTree as ET
import stackexchange
import os
from lxml import etree
from io import StringIO
import json

#Script that collects the full content of questions returned by the query

sys.path.append('.')
site = stackexchange.Site(stackexchange.StackOverflow,"wZjX24zp2Y3wv6THqhZyPQ((")
site.be_inclusive()
parser = etree.HTMLParser()

#create the directory for the mined StackOverflow code snippets
directory = os.getcwd() + "\\StackOverflow\\MostPopularQuestions"
if not os.path.exists(directory):
	os.makedirs(directory)

sys.stdout.flush()
infoFile = open(directory + "\\" + "MostPopularQuestions.json","w")
infoDict = {}
infoDict["description"] = "this file contains the content of questions returned by the query"
infoDict["content"] = {}

stackSearchResults = site.search(pagesize=100, tagged="python",sort="votes",min=1000)

for question in stackSearchResults:
	question.fetch()
	infoDict["content"][question.id] = question.body

json.dump(infoDict,infoFile)
infoFile.close()