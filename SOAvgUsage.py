import sys
import xml.etree.ElementTree as ET
import stackexchange
from stackauth import StackAuth
import json
import os
import simpledate

sys.path.append('.')
site = stackexchange.Site(stackexchange.StackOverflow,"wZjX24zp2Y3wv6THqhZyPQ((")
site.be_inclusive()

tagList = ["Matlab","Fortran","R","Octave","Freemat"]

#create the directory for the mined StackOverflow code snippets
directory = os.getcwd() + "\\StackOverflow\\AverageCommunitySize"
if not os.path.exists(directory):
	os.makedirs(directory)

sys.stdout.flush()
infoFile = open(directory + "\\" + "AverageCommunitySize.json","w")
infoDict = {}
infoDict["description"] = "this file contains information about the number of views for each tag in a specified period of time. here: one month"
infoDict["content"] = {}

for tag in tagList:
	stackSearchResults = site.search(tagged=tag,fromdate = str(int(simpledate.SimpleDate('2014-04-01',tz='UTC').timestamp)),
	todate=str(int(simpledate.SimpleDate('2014-04-10',tz='UTC').timestamp)))
	total_count = 0
	for question in stackSearchResults:
		sys.stdout.flush()
		#print(question)
		#fetch all the data about the question
		#question.fetch()
		#print(question.view_count)
		#sys.stdout.flush()
		total_count += question.view_count
		#counter = counter - 1
		#if len(question.answers)>2:
		#	for answer in question.answers:
		#		if answer.json["is_accepted"] or answer.score > 12:
		#			root = ET.fromstring("<StackOverflowXML>" + answer.body + "</StackOverflowXML>")
		#			for element in root.iter(tag = "code"):
		#				#print(element.text)
		#				pass
		#	print()
		#	print(('{0:d} answers.'.format(len(question.answers))))
	infoDict["content"][tag] = total_count
	print("Total number of views for ----  {0}  ----is :".format(tag),total_count)
	print()
json.dump(infoDict,infoFile)
infoFile.close()
