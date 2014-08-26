from os import listdir
import os.path
import os
import argparse
from lxml import etree
import fileinput

"""change tag string format from <tag1><tag2>... to tag1,tag2..."""
def _prepareTags(tags):
	return ', '.join(tags[1:-1].split("><"))

def _addAnswerScore(id,score):
	trecFile = os.getcwd()+"/trec/"+id+".trec"
	for line in fileinput.input(trecFile, inplace=True):
		if "terrierascores" in line:
			print(line + ","+score, end='\n')
		else:
			print(line, end='')

def _produceTheAverage(id):
	trecFile = os.getcwd()+"/trec/"+id+".trec"
	for line in fileinput.input(trecFile, inplace=True):
		if "terrierascores" in line:
			scores = line.split(",")[1:]
			aggregate = 0
			for score in scores:
				aggregate +=int(score)
			avg = aggregate/len(scores)
			print("<AVGANSWERSCORE>"+str(avg)+"</AVGANSWERSCORE>", end='\n')
		else:
			print(line, end='')

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
			with open(trecFolder+"/"+rowDict["Id"]+".trec","w",encoding='utf-8') as trecFile:
				trecFile.write("<DOC>\n")
				trecFile.write("<DOCNO>"+rowDict["Id"]+"</DOCNO>\n")
				trecFile.write("<SCORE>"+rowDict["Score"]+"</SCORE>\n")
				#trecFile.write("<FAVORITECOUNT>"+rowDict["FavoriteCount"]+"</FAVORITECOUNT>")
				trecFile.write("<VIEWCOUNT>"+rowDict["ViewCount"]+"</VIEWCOUNT>\n")
				#trecFile.write("<ANSWERCOUNT>"+rowDict["AnswerCount"]+"</ANSWERCOUNT>\n")		
				trecFile.write("terrierascores\n")#aggregate the scores of the answers here. Put their average at the end
				trecFile.write("<COMMENTCOUNT>"+rowDict["CommentCount"]+"</COMMENTCOUNT>\n")
				trecFile.write("<TITLE>"+rowDict["Title"]+"</TITLE>\n")
				trecFile.write("<QUESTION>"+rowDict["Body"]+"</QUESTION>\n")
				trecFile.write("<TAGS>"+_prepareTags(rowDict["Tags"])+"</TAGS>\n")

def insertAnswers(xmlpath):
	trecFolder = os.getcwd()+"/trec"
	for element in etree.iterparse(xmlpath, tag="row"):
		# etree Element >> element[1]
		#print(dict(element[1].attrib))
		rowDict = dict(element[1].attrib)
		#if the record is a question
		if rowDict["PostTypeId"] == "2":
			with open(trecFolder+"/"+rowDict["ParentID"]+".trec","a",encoding='utf-8') as trecFile:
				trecFile.write("<ANSWER>"+rowDict["Body"]+"</ANSWER>")
			
			#add the score here
			_addAnswerScore(rowDict["ParentID"],rowDict["Score"])


"""Have to calculate the average too"""
def closeTRECFiles():
	#need to write this:
	#trecFile.write("<AVGANSWERSCORE>"+rowDict["Body"]+"</AVGANSWERSCORE>")
	trecFolder = os.getcwd()+"/trec"
	files = [ f for f in os.listdir(trecFolder) if os.path.isfile(os.path.join(trecFolder,f)) ]
	for f in files:
		with open(f,"a",encoding='utf-8') as trecFile:
			trecFile.write("</DOC>")

_produceTheAverage("4")


#print("terrierascores,4,13,23,98".split(",")[1:])
#splitIntoTerrierFiles("Posts.xml")
#_addAnswerScore("4")
#insertAnswers("Posts.xml")
#closeTRECFiles()

# with open(trecFolder+"/163.trec","a+",encoding='utf-8') as trecFile:
# 	trecFile.seek(5)
# 	print(trecFile.readline())
