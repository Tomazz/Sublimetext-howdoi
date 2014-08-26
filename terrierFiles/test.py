from os import listdir
import os.path
import os
import argparse
from lxml import etree

"""change tag string format from <tag1><tag2>... to tag1,tag2..."""
def _prepareTags(tags):
	return ', '.join(tags[1:-1].split("><"))

"""first get all the questions"""
def splitIntoTerrierFiles(xmlpath):
	trecFolder = os.getcwd()+"/trec"
	if not os.path.exists(trecFolder):
		os.makedirs(trecFolder)

	for element in etree.iterparse(xmlpath, tag="row"):
		# etree Element >> element[1]
		#print(dict(element[1].attrib))
		rowDict = dict(element[1].attrib)
		#if the record is a question
		if rowDict["PostTypeId"] == "1":
			with open(trecFolder+"/"+rowDict["Id"]+".trec","a",encoding='utf-8') as trecFile:
				trecFile.write("<DOC>")
				trecFile.write("<DOCNO>"+rowDict["Id"]+"</DOCNO>")
				trecFile.write("<TITLE>"+rowDict["Title"]+"</TITLE>")
				trecFile.write("<BODY>"+rowDict["Body"]+"</BODY>")
				trecFile.write("<TAGS>"+_prepareTags(rowDict["Tags"])+"</TAGS>")
				trecFile.write("<SCORE>"+rowDict["Score"]+"</SCORE>")
				trecFile.write("<FAVOURITECOUNT>"+rowDict["FavouriteCount"]+"</FAVOURITECOUNT>")
				trecFile.write("<VIEWCOUNT>"+rowDict["ViewCount"]+"</VIEWCOUNT>")
				trecFile.write("<ANSWERCOUNT>"+rowDict["AnswerCount"]+"</ANSWERCOUNT>")
				trecFile.write("<COMMENTCOUNT>"+rowDict["CommentCount"]+"</COMMENTCOUNT>")		

def insertAnswers(xmlpath):
	for element in etree.iterparse(xmlpath, tag="row"):
		# etree Element >> element[1]
		#print(dict(element[1].attrib))
		rowDict = dict(element[1].attrib)
		#if the record is a question
		if rowDict["PostTypeId"] == "2":
			with open(trecFolder+"/"+rowDict["Id"]+".trec","a",encoding='utf-8') as trecFile:
				# trecFile.write("<DOC>")
				# trecFile.write("<DOCNO>"+rowDict["Id"]+"</DOCNO>")
				trecFile.write("<TITLE>"+rowDict["Title"]+"</TITLE>")
				trecFile.write("<BODY>"+rowDict["Body"]+"</BODY>")
				trecFile.write("<TAGS>"+_prepareTags(rowDict["Tags"])+"</TAGS>")
				trecFile.write("<SCORE>"+rowDict["Score"]+"</SCORE>")
				trecFile.write("<COMMENTCOUNT>"+rowDict["CommentCount"]+"</COMMENTCOUNT>")

def closeTRECFiles(trecFolder):
	files = [ f for f in os.listdir(trecFolder) if os.path.isfile(os.path.join(trecFolder,f)) ]
	for f in files:
		with open(f,"a",encoding='utf-8') as trecFile:
			trecFile.write("</DOC>")


splitIntoTerrierFiles("Posts.xml")
