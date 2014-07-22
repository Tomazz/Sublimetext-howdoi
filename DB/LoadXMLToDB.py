import sys
from lxml import etree
import os
import psycopg2
import getpass
from datetime import datetime
from dateutil import parser

#Post attributes
attributesList = ["Id","PostTypeId","ParentId","AcceptedAnswerId","CreationDate","Score","ViewCount","Body","OwnerUserId","LastEditorUserId","LastEditorDisplayName","LastEditDate","LastActivityDate","CommunityOwnedDate","ClosedDate","Title","Tags","AnswerCount","CommentCount","FavoriteCount"]
#load the XML

#connect to the database
conn = psycopg2.connect(dbname="internship2014", user="postgres", password=getpass.getpass(prompt="Password: ",stream=None))


def readXML(path):
	rowDict = {}
	c = 0
	for element in etree.iterparse(path, tag="row"):
		rowDict = dict(element[1].attrib)
		for attribute in attributesList:
			if attribute in rowDict and attribute in ["CreationDate","LastEditDate","LastActivityDate","CommunityOwnedDate","ClosedDate"]:
				rowDict[attribute] = parser.parse(rowDict[attribute]).isoformat()
			if attribute not in rowDict:
				rowDict[attribute] = None
		c+=1
		if c>50000:
			break
		insertToDB(rowDict)
		element[1].clear()


def insertToDB(rowDictionary):
	cursorDB = conn.cursor()
	attributesToStr = attributesList[0].lower()
	attributesToInsert = "%("+attributesList[0]+")s"
	for x in range(1,len(attributesList)):
		attributesToInsert +=",%("+attributesList[x]+")s"
		attributesToStr+=","+attributesList[x].lower()

	query = ("INSERT INTO PostsTesting ("+attributesToStr+") VALUES ("+attributesToInsert+")")
	#print(cursorDB.mogrify(query),rowDictionary)
	cursorDB.execute(query,rowDictionary)
	conn.commit()
	cursorDB.close()

readXML("D:\\StackOverflowDBDump\\Posts.xml")

conn.close()