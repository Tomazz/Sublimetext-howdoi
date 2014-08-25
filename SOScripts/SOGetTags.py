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

"""
Script that collects the most popular tags on Stackoverflow and
aggregates the synonym tags together

"""

sys.path.append('.')
site = stackexchange.Site(stackexchange.StackOverflow,"wZjX24zp2Y3wv6THqhZyPQ((")
site.be_inclusive()
popularLanguages = ["java","c#","python","c++","sql","mysql",\
"objective-c",".net","ruby-on-rails","ruby",\
"ajax","javascript","jquery","php","c","android","iphone",\
"sql-server","html","css","django","vb.net","html5","asp.net-mvc","ios","wpf",\
"ruby-on-rails-3","asp.net","facebook","osx","swing","angularjs","node.js"]

def aggregateTags(tagDict):
	for tagSynonym in tagSynonymResults:
		if tagSynonym.to_tag in tagDict:
			print(int(tagSynonym.applied_count))
			tagDict[tagSynonym.to_tag] += int(tagSynonym.applied_count)

#create the directory for the mined StackOverflow code snippets
directory = os.getcwd() + "\\StackOverflowData"
if not os.path.exists(directory):
	os.makedirs(directory)

sys.stdout.flush()
infoFile = open(directory + "\\" + "TagStats.json","w")
infoDict = {}
infoDict["description"] = "this file contains the stats regarding the most popular tags on Stackoverflow"
infoDict["content"] = {}

stackSearchResults = site.tags(pagesize=100,sort="popular",min=8000)
tagSynonymResults = site.tag_synonyms(pagesize=100,sort="applied",min=200)

for tag in stackSearchResults:
	infoDict["content"][tag.name] = tag.count

aggregateTags(infoDict["content"])

json.dump(infoDict,infoFile)
infoFile.close()