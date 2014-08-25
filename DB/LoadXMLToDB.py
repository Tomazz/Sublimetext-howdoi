import sys
from lxml import etree
import os
import psycopg2
import getpass
from datetime import datetime
from dateutil import parser

#Post attributes
attributesList = ["Id","PostTypeId","ParentId","AcceptedAnswerId","CreationDate","Score","ViewCount","Body","OwnerUserId","LastEditorUserId","LastEditorDisplayName","LastEditDate","LastActivityDate","CommunityOwnedDate","ClosedDate","Title","Tags","AnswerCount","CommentCount","FavoriteCount"]
#date or datetime attributes
datetimeAttributes = ["CreationDate","LastEditDate","LastActivityDate","CommunityOwnedDate","ClosedDate"]

#load the XML to a database, given a path to the xml file
def readXML(path):
	#connect to the database
	conn = psycopg2.connect(dbname="internship2014", user="postgres", password=getpass.getpass(prompt="Password: ",stream=None))

	rowDict = {}
	for element in etree.iterparse(path, tag="row"):
		rowDict = dict(element[1].attrib)
		for attribute in attributesList:
			if attribute in rowDict and attribute in datetimeAttributes:
				rowDict[attribute] = parser.parse(rowDict[attribute]).isoformat()
			if attribute not in rowDict:
				rowDict[attribute] = None

		insertToDB(rowDict,conn) #Insert the data to the database
		element[0].clear()
		element[1].clear()
	conn.close()

def insertToDB(rowDictionary,connection):
	cursorDB = connection.cursor()
	attributesToStr = attributesList[0].lower() # attributes needed for SQL part
	attributesToInsert = "%("+attributesList[0]+")s" #above converted to format that psycopg2 can recognize and deal with when inserting values into the query
	for x in range(1,len(attributesList)):
		attributesToInsert +=",%("+attributesList[x]+")s"
		attributesToStr+=","+attributesList[x].lower()
	
	"""  
	!Important part! 
	below query has to be changed for different table.
	attributesToStr - list of attribute names: attribue1,attribute2,... <- all attributes from the attributesList 
	attributesToInsert - a specially formated version of the attributesToStr string above: %(attr1)s,%(attr1)s,... <- format required by psycopg2
						Otherwise the query execution does not work correctly.
						see: http://initd.org/psycopg/docs/usage.html

	"""
	query = ("INSERT INTO PostsTesting ("+attributesToStr+") VALUES ("+attributesToInsert+")")
	#print(cursorDB.mogrify(query),rowDictionary)
	cursorDB.execute(query,rowDictionary)
	connection.commit()
	cursorDB.close()


readXML("D:\\StackOverflowDBDump\\Posts.xml")