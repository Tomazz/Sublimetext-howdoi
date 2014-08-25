import sys
import xml.etree.ElementTree as ET
import stackexchange
import os
from lxml import etree
from io import StringIO
import json

sys.path.append('.')
site = stackexchange.Site(stackexchange.StackOverflow,"wZjX24zp2Y3wv6THqhZyPQ((")
site.be_inclusive()
parser = etree.HTMLParser()

#create the directory for the mined StackOverflow code snippets
directory = os.getcwd() + "\\" + "StackOverflowData"
if not os.path.exists(directory):
	os.makedirs(directory)

tagList = []
with open("SOConfig.txt","r") as tagFile:
    for line in tagFile:
        tagList = line.split(",")

sys.stdout.flush()
infoFile = open(directory + "\\" + "AnswerCodeSnippets.json","w") #possibly need to make the file name different for each query
infoDict = {}
infoDict["description"] = "This file contains code snippets of the questions selected by the query"
infoDict["content"] = {}

stackSearchResults = site.search(pagesize=100, tagged="python",sort="votes",min=1000)

for question in stackSearchResults:
	question.fetch()
	if len(question.answers)>2:
		for answer in question.answers:
			answerNum = 0
			if answer.json["is_accepted"] or answer.score > 12:
				codeSnippetNum = 0
				answerNum+=1
				infoDict["content"][question.id] = {}
				infoDict["content"][question.id]["answer"+str(answerNum)] = {}
				root = etree.parse(StringIO(answer.body), parser=parser)
				codeSnippets = root.findall(".//code")
				for snippet in codeSnippets:
					codeSnippetNum +=1
					infoDict["content"][question.id]["answer"+str(answerNum)]["codeSnippet"+str(codeSnippetNum)] = snippet.text
json.dump(infoDict,infoFile)
infoFile.close()