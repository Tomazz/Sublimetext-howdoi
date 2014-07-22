import sys
import xml.etree.ElementTree as ET
import stackexchange
import os
from lxml import etree
from io import StringIO
import pygal
import psycopg2
import getpass
import datetime

#Script that collects tag synonyms from Stackoverflow and
#puts them into a database

#The table attribute names and values for the dates are in a differnt format because 

sys.path.append('.')
site = stackexchange.Site(stackexchange.StackOverflow,"wZjX24zp2Y3wv6THqhZyPQ((")
site.be_inclusive()

conn = psycopg2.connect(dbname="internship2014", user="postgres", password=getpass.getpass(prompt="Password: ",stream=None))

def loadFromDictToDB(connection):
	cursorDB = connection.cursor()
	attributesList = ["id","applied_count","from_tag","to_tag"]
	tagSynonymResults = site.tag_synonyms(pagesize=100,sort="applied",min=200)
	idCount = 0
	for result in tagSynonymResults:
		idCount+=1
		resultDictionary = result.json
		resultDictionary["id"] = str(idCount)

		attributesToStr = ','.join(attributesList)
		attributesToInsert = "%("+attributesList[0]+")s"
		for x in range(1,len(attributesList)):
			attributesToInsert +=",%("+attributesList[x]+")s"

		query = ("INSERT INTO TagSynonyms ("+attributesToStr+") VALUES ("+attributesToInsert+")")
		#print(cursorDB.mogrify(query,resultDictionary))
		cursorDB.execute(query,resultDictionary)
		conn.commit()

	cursorDB.close()
	connection.close()


loadFromDictToDB(conn)