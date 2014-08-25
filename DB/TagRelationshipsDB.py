"""
This script cmmunicates with the database 
to produce charts that represent relationships between two or more tags ex:
What different tags(and their frequency) appear alongside the tag "python" 

"""

import os
import psycopg2
import getpass
from collections import Counter
import pygal
import argparse
import json


def _addMonths(sourcedate,months):
     month = sourcedate.month - 1 + months
     year = int(sourcedate.year + month / 12)
     month = month % 12 + 1
     day = min(sourcedate.day,calendar.monthrange(year,month)[1])
     return datetime.datetime(year,month,day)

def _getMaxDateDB():
	conn = psycopg2.connect(dbname="internship2014", user="postgres", password="password")
	maxDateQuery = "SELECT MAX(creationdate)\
				FROM posts"
	cursorDB1 = conn.cursor()
	cursorDB1.execute(maxDateQuery)
	maxDate = cursorDB.fetchone()[0].replace(tzinfo=None)
	cursorDB1.close()
	return maxDate

def _getMinDateDB():
	conn = psycopg2.connect(dbname="internship2014", user="postgres", password="password")
	maxDateQuery = "SELECT MIN(creationdate)\
				FROM posts"
	cursorDB1 = conn.cursor()
	cursorDB1.execute(maxDateQuery)
	maxDate = cursorDB.fetchone()[0].replace(tzinfo=None)
	cursorDB1.close()
	return maxDate

def _saveToJSON(tag,tagDict):
	directory = os.getcwd() + "\\TagRelationship"
	if not os.path.exists(directory):
		os.makedirs(directory)
	with open(directory + "\\" + "TagRel_"+ tag +".json","w") as infoFile:
		json.dump(tagDict,infoFile)

def _generateBarChart(tag,tagCounter):
	tagList = tagCounter.most_common(25)
	bar_chart = pygal.Bar()
	bar_chart.title = 'Tags associated with tag: ' + tag
	for element in tagList:
		bar_chart.add(element[0],element[1])
	bar_chart.render_to_file(os.getcwd() + "\\TagRelationship\\chart_"+ tag +".svg")


def relatedTags(tag,startDate,endDate):
	conn = psycopg2.connect(dbname="internship2014", user="postgres", password="password")
	cursorDB = conn.cursor()

	maxDate = _getMaxDateDB()
	minDate = _getMinDateDB()
	#set the endDate and startDate for the intervals
	#if user did not specify the endDate or startDate
	if startDate == None:
		startDate = minDate
	else:
		startDate = datetime.datetime.strptime(startdDate,"%d-%m-%Y")
		#if the user specified the startDate but it's later than the latest entry in the DB
		#set it to the minDate of the DB
		if startDate < minDate:
			startDate = minDate

	if endDate == None:
		endDate = maxDate
	else:
		endDate = datetime.datetime.strptime(endDate,"%d-%m-%Y")
		#if the user specified the endDate but it's later than the latest entry in the DB
		#set it to the maxDate of the DB
		if endDate > maxDate:
			endDate = maxDate

	query = "SELECT tags\
			FROM posts\
			WHERE creationdate > '{0}'\
			AND creationdate < '{1}'\
			AND tags LIKE '%<{2}>%'".format(startDate,endDate,tag)
	cursorDB.execute(query) #execute query
	resultList = cursorDB.fetchall() #fetch the results
	tagCounter = Counter() #create a counter for the results
	#each result is a list of tags in a format : <tag1><tag2><tag3>... <<need to transform it to a list: [tag1,tag2,tag3....]
	for result in resultList:
		tagList = (''.join(result))[1:-1].split("><")
		for x in tagList:
			tagCounter[x] +=1

	tagCounter[tag] = 0
	cursorDB.close()
	conn.close()
	return tagCounter

"""
tag - tag for which you would like to find other tags associated with it
startDate - start date from which the program will count the intervals
endDate - end date to which the intervals will be counted
interval - number of months per interval
returns a list of counters for each of the intervals

"""
def relatedTagsTimeInterval(tag,startDate,endDate,interval):
	finalResults = []
	conn = psycopg2.connect(dbname="internship2014", user="postgres", password="password")
	intervals = []
	maxDate = _getMaxDateDB()
	minDate = _getMinDateDB()
	#set the endDate and startDate for the intervals
	#if user did not specify the endDate or startDate
	if startDate == None:
		startDate = minDate
	else:
		startDate = datetime.datetime.strptime(startdDate,"%d-%m-%Y")
		#if the user specified the startDate but it's later than the latest entry in the DB
		#set it to the minDate of the DB
		if startDate < minDate:
			startDate = minDate

	if endDate == None:
		endDate = maxDate
	else:
		endDate = datetime.datetime.strptime(endDate,"%d-%m-%Y")
		#if the user specified the endDate but it's later than the latest entry in the DB
		#set it to the maxDate of the DB
		if endDate > maxDate:
			endDate = maxDate

	#populate intervals
	intervalDate = startDate
	while intervalDate < maxDate:
		intervals += [copy.deepcopy(intervalDate)]
		intervalDate = _addMonths(intervalDate,interval)
	intervals = intervals[:-1]

	for date in intervals:
		begin = date
		end = _addMonths(date,interval)
		query = "SELECT tags\
			FROM posts\
			WHERE creationdate > '{0}'\
			AND creationdate < '{1}'\
			AND tags LIKE '%<{2}>%'".format(begin,end,tag)
		cursorDB2 = conn.cursor()
		cursorDB2.execute(query)
		resultList = cursorDB.fetchall() #fetch the results
		tagCounter = Counter() #create a counter for the results
		#each result is a list of tags in a format : <tag1><tag2><tag3>... <<need to transform it to a list: [tag1,tag2,tag3....]
		for result in resultList:
			tagList = (''.join(result))[1:-1].split("><")
			for x in tagList:
				tagCounter[x] +=1

		tagCounter[tag] = 0
		finalResults += tagCounter
		cursorDB2.close()

	conn.close()
	return finalResults


def main():
	""" if the module run independently """
	parser = argparse.ArgumentParser(description='This script cmmunicates with the database \n +\
												to produce charts that represent relationships between two or more tags. Ex: \n \n +\
												What different tags(and their frequency) appear alongside the tag "python"')
	parser.add_argument('-t','--tag', help='Name of the tag of which you want to know the other associated tags', required=True)
	parser.add_argument('--start', help='', required=False,default=None)
	parser.add_argument('--end', help='', required=False,default=None)
	parser.add_argument('-i','--interval', help='', required=False, default=6,type=int)
	parser.add_argument('-c','--chartdraw', help='use the flag if you want to generate a chart with top 25 tags associated with the tag',action='store_true', required=False, default=False)
	args = vars(parser.parse_args())
	relatedTags(args["tag"])

	if args["interval"]:
		tagsCounterList = relatedTagsTimeInterval(args["tag"],args["start"],args["end"],args["interval"])
		for tagCounter in tagsCounterList:
			if args["chartdraw"]:
				_generateBarChart(args["tag"],tagCounter)
				_saveToJSON(args["tag"],dict(tagCounter))
			else:
				_saveToJSON(args["tag"],dict(tagCounter))
	else:
		tagCounter = relatedTags(args["tag"],args["start"],args["end"])
		if args["chartdraw"]:
			_generateBarChart(args["tag"],tagCounter)
			_saveToJSON(args["tag"],dict(tagCounter))
		else:
			_saveToJSON(args["tag"],dict(tagCounter))

if __name__ == '__main__':
	main()