from os import listdir
import os.path
import os
import argparse
from lxml import etree

"""Script that for testing purposes transfers n first entries of a very large(GBs) XML file 
   to a smaller XML file in a different directory 
"""

def getAChunk(path,numOfRecords):
	path = os.path.normpath(path)
	chunkedPath = path+os.path.normpath("\\chunked")
	if not os.path.exists(chunkedPath):
		os.makedirs(chunkedPath)
	#check if the supplied path leads to a single file or a whole directory
	if os.path.isdir(path):		
		onlyFiles = [ f for f in listdir(path) if os.path.isfile(os.path.join(path,f)) ]
		for filename in onlyFiles:
			if os.path.splitext(filename)[1] == ".xml":
				with open(path+"\\"+filename,"r",encoding='utf-8') as SODumpFile:
					with open(chunkedPath+"\\"+filename,"w",encoding='utf-8') as chunkedFile:
						for x in range(numOfRecords):
							chunkedFile.write(SODumpFile.readline())
						chunkedFile.write("</"+(os.path.splitext(filename)[0]).lower()+">")
	elif os.path.isfile(path):
		if os.path.splitext(path)[1] == ".xml":
			with open(path+"\\"+filename,"r",encoding='utf-8') as SODumpFile:
				with open(chunkedPath+"\\"+filename,"w",encoding='utf-8') as chunkedFile:
					for x in range(numOfRecords):
						chunkedFile.write(SODumpFile.readline())
					chunkedFile.write("</"+(os.path.splitext(filename)[0]).lower()+">")
	else:
		raise ValueError('--path has to be either a path to a file or a directory')
		
def splitIntoTerrierFiles(xmlpath):
	trecFolder = os.getcwd()+"\\trec"
	if not os.path.exists(trecFolder):
		os.makedirs(trecFolder)
	rowDict = {}
	for element in etree.iterparse(xmlpath, tag="row"):
		# etree Element >> element[1]
		with open(os.getcwd()+"\\"++".trec","a",encoding='utf-8') as trecFile:
		# rowDict = dict(element[1].attrib)
		# for attribute in attributesList:
		# 	if attribute in rowDict and attribute in datetimeAttributes:
		# 		rowDict[attribute] = parser.parse(rowDict[attribute]).isoformat()
		# 	if attribute not in rowDict:
		# 		rowDict[attribute] = None

		# element[0].clear()
		# element[1].clear()

def addTerrierEndingTags(trecFolder):
	files = [ f for f in os.listdir(trecFolder) if os.path.isfile(os.path.join(trecFolder,f)) ]
	for f in files:
		with open(f,"a",encoding='utf-8') as trecFile:
			trecFile.write("</DOC>")

def main():
	""" if the module run independently """
	parser = argparse.ArgumentParser(description='helper module for interaction with the web')
	#parser.add_argument('-p','--path', help='absolute path to the folder with XML files', required=True)
	parser.add_argument('-n','--numofrecords', help='Given a stackoverflow url return the question ID', required=False,type=int,default=50000)
	args = vars(parser.parse_args())

	#getAChunk(args["path"],args["numofrecords"])
	splitIntoFiles("Posts.xml")

if __name__ == '__main__':
	main()
