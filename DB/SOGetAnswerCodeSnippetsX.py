import sys
import xml.etree.ElementTree as ET
import os
from lxml import etree
from io import StringIO
import json
import psycopg2
import copy
import getpass
import WebModule
import webbrowser

sys.path.append('.')


def getSnippetsByQuestionID(ID):
	parser = etree.HTMLParser()
	conn = psycopg2.connect(dbname="internship2014", user="postgres", password=getpass.getpass(prompt="Password: ",stream=None))
	cursorDB1 = conn.cursor('questionCursor')
	cursorDB2 = conn.cursor('answersCursor')
	query1 = "SELECT body, title FROM posts WHERE id = '{0}'".format(ID)
	query2 = "SELECT * FROM posts WHERE parentid = '{0}'".format(ID) # "tag" and "score" are keys in the args dictionary. Load the tag from the dictionary into the query
	cursorDB1.execute(query1) #execute query thet gets the question contents
	questionRow = copy.deepcopy(cursorDB1.fetchone())
	print("QUESTION","\n",questionRow[0],"\n",questionRow[1],"\n***************")
	cursorDB2.execute(query2) #execute query thet gets the answers
	for answerRow in cursorDB2:
		print("Answer")
		if answerRow[3] == questionRow[0] or answerRow[19] > 6: # if answer is the accepted one or answer score is > 6
			root = etree.parse(StringIO(answerRow[6]), parser=parser)
			codeSnippets = root.findall(".//code")
			for snippet in codeSnippets:
				print(snippet.text)

	cursorDB1.close()
	cursorDB2.close()
	conn.close()


def getSnippetListByQuery(query):
	pass


def getQuestionContent(ID):
	parser = etree.HTMLParser()
	conn = psycopg2.connect(dbname="internship2014", user="postgres", password=getpass.getpass(prompt="Password: ",stream=None))
	cursorDB = conn.cursor()
	query1 = "SELECT * FROM posts WHERE id = '{0}'".format(ID)
	cursorDB.execute(query1) #execute query thet gets the question contents
	questionRow = cursorDB.fetchone()
	print("QUESTION","\n",questionRow[6],"\n",questionRow[14],"\n***************")
	cursorDB.close()
	conn.close()

def getQuestionContentList(IdList):
	parser = etree.HTMLParser()
	conn = psycopg2.connect(dbname="internship2014", user="postgres", password=getpass.getpass(prompt="Password: ",stream=None))
	cursorDB1 = conn.cursor()
	cursorDB2 = conn.cursor()
	query1 = "SELECT * FROM posts WHERE id IN %(idList)s"
	query2 = "SELECT * FROM posts WHERE id = %(acceptedAndwerId)s AND %(acceptedAndwerId)s IS NOT NUll" #id = accepted answer id
	cursorDB1.execute(query1,{"idList":IdList}) #execute query thet gets the question contents
	for questionRow in cursorDB1:
		print("QUESTION TITLE : ",questionRow[14],"\n",questionRow[6],"\n")
		cursorDB2.execute(query2,{"acceptedAndwerId":questionRow[3]})
		acceptedAnswerRow = cursorDB2.fetchone()
		if acceptedAnswerRow != None:
			print("ACCEPTED ANSWER: \n",acceptedAnswerRow[6]) 
	cursorDB1.close()
	cursorDB2.close()
	conn.close()

with open("buffer.txt","r") as buff:
	searchString = buff.read()

resultList = WebModule.getSOUrls(searchString,returnIds = True)
resultListUrls = WebModule.getSOUrls(searchString)
getQuestionContentList(resultList[0:3])

for x in range(3):
	webbrowser.open(resultListUrls[x])

