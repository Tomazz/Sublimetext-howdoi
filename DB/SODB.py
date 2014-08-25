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


"""
Very DB intensive query
the DB will have to iterate through all the records to find answers that correspond to the chosen question

"""
def getSnippetsByQuestionID(ID):
	parser = etree.HTMLParser()
	conn = psycopg2.connect(dbname="internship2014", user="postgres", password="password")
	cursorDB1 = conn.cursor('questionCursor')
	cursorDB2 = conn.cursor('answersCursor')
	query1 = "SELECT body, title FROM posts WHERE id = '{0}'".format(ID)
	query2 = "SELECT * FROM posts WHERE parentid = '{0}'".format(ID) # "tag" and "score" are keys in the args dictionary. Load the tag from the dictionary into the query
	cursorDB1.execute(query1) #execute query thet gets the question contents
	questionRow = copy.deepcopy(cursorDB1.fetchone())
	print("QUESTION","\n",questionRow[0],"\n",questionRow[1],"\n***************")
	cursorDB2.execute(query2) #execute query that gets the answers
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

"""
This is a slightly limited version of the above function.
It returns a question-chosen answer pair(DB tuple contains a reference to the answer chosen by the person who asked the question)
because of the above, the DBMS doesn't have to search through the entire DB to retrieve the answer

returns a list [question,answer(if exists)]

"""
def getQuestionAndAnswer(ID):
	parser = etree.HTMLParser()
	conn = psycopg2.connect(dbname="internship2014", user="postgres",password="password")
	cursorDB1 = conn.cursor()
	cursorDB2 = conn.cursor()
	query1 = "SELECT * FROM posts WHERE id = '{0}'".format(ID)
	query2 = "SELECT * FROM posts WHERE id = %(acceptedAndwerId)s AND %(acceptedAndwerId)s IS NOT NUll" #id = accepted answer id
	cursorDB1.execute(query1) #execute query thet gets the question contents
	question = copy.deepcopy(cursorDB1.fetchone())
	cursorDB2.execute(query2,{"acceptedAndwerId":questionRow[3]})
	acceptedAnswer = copy.deepcopy(cursorDB2.fetchone())
	cursorDB1.close()
	cursorDB2.close()
	conn.close()
	if acceptedAnswerRow != None:
		return [question,acceptedAnswer]
	else:
		return [question,None]


"""
same as above but you can supply a list of question IDs

"""
def getQuestionAndAnswerList(IdList):
	parser = etree.HTMLParser()
	conn = psycopg2.connect(dbname="internship2014", user="postgres",password="password")
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

#TODO
def getSnippetListByQuery(query):
	pass


"""
given an ID, retrieve the post(can be question or answer) code snippets from the DB

"""
def getPostCodeSnippets(ID):
	conn = psycopg2.connect(dbname="internship2014", user="postgres", password="password")
	cursorDB = conn.cursor()
	query = "SELECT body FROM posts WHERE id = '{0}'".format(ID)
	cursorDB.execute(query) #execute query thet gets the post body contents
	result = copy.deepcopy(cursorDB.fetchone())

	parser = etree.HTMLParser()
	root = etree.parse(StringIO(result[0]), parser=parser)
	codeSnippets = root.findall(".//code")
	snippetList = []
	for snippet in codeSnippets:
		snippetList += [snippet.text]

	cursorDB.close()
	conn.close()
	return snippetList

"""
given an ID, retrieve the post(can be question or answer) content from the DB

"""
def getPostContent(ID):
	parser = etree.HTMLParser()
	conn = psycopg2.connect(dbname="internship2014", user="postgres", password="password")
	cursorDB = conn.cursor()
	query1 = "SELECT * FROM posts WHERE id = '{0}'".format(ID)
	cursorDB.execute(query1) #execute query thet gets the question contents
	post = copy.deepcopy(cursorDB.fetchone())
	cursorDB.close()
	conn.close()
	return post


"""
EXTRAS. MIGHT BE REMOVED LATER

"""
def openInWebsite(resultListUrls):
	#open up the first 5 urls returned by google in your default browser
	for x in range(5):
		webbrowser.open(resultListUrls[x])

def main():
	with open("C:\\Users\\Tomazz\\Documents\\SummerInternship2014\\DB\\buffer.txt","r") as buff:
		searchString = buff.read()

	#get SO question IDs and full urls
	resultList = WebModule.getSOUrls(searchString,returnIds = True)
	resultListUrls = WebModule.getSOUrls(searchString)

	#query the internal SO database to retrieve the question content and and and answer(if there was one)
	getQuestionAndAnswerList(resultList[0:3])

	openInWebsite(resultListUrls)

main()


