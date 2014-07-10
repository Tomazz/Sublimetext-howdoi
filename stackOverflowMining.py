import sys
import xml.etree.ElementTree as ET
import stackexchange
from stackauth import StackAuth
import os

sys.path.append('.')
site = stackexchange.Site(stackexchange.StackOverflow,"wZjX24zp2Y3wv6THqhZyPQ((")
site.be_inclusive()

#create the directory for the mined StackOverflow code snippets
directory = os.getcwd() + "\\" + "StackOverflowData"
if not os.path.exists(directory):
	os.makedirs(directory)

stackSearchResults = site.search(intitle="python", tagged="dictionary",answers_count ="3")

counter = 10
for question in stackSearchResults:
	#grab the first 10 results
	#print(question.json)
	if counter<=0:
		break
	counter = counter - 1
	#question = site.question(questionID)
	question.fetch()
	print()
	if len(question.answers)>2:
		for answer in question.answers:
			if answer.json["is_accepted"] or answer.score > 12:
				root = ET.fromstring("<StackOverflowXML>" + answer.body + "</StackOverflowXML>")
				for element in root.iter(tag = "code"):
					print(element.text)
					pass
		print()
		print(('{0:d} answers.'.format(len(question.answers))))