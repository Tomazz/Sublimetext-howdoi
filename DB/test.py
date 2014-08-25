import datetime
import pytz
import calendar
import psycopg2
from collections import Counter
import copy


def _addMonths(sourcedate,months):
     month = sourcedate.month - 1 + months
     year = int(sourcedate.year + month / 12)
     month = month % 12 + 1
     day = min(sourcedate.day,calendar.monthrange(year,month)[1])
     return datetime.datetime(year,month,day)

def _getMaxDateDB():
	conn = psycopg2.connect(dbname="internship2014", user="postgres", password="password")
	maxDateQuery = "SELECT MAX(creationdate)\
				FROM poststesting"
	cursorDB = conn.cursor()
	cursorDB.execute(maxDateQuery)
	maxDate = cursorDB.fetchone()[0].replace(tzinfo=None)
	cursorDB.close()
	return maxDate

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
	startDate = datetime.datetime.strptime(startDate,"%d-%m-%Y")
	maxDate = _getMaxDateDB()
	#set the endDate for the intervals
	#if user did not specify the endDate
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
			FROM poststesting\
			WHERE creationdate > '{0}'\
			AND creationdate < '{1}'\
			AND tags LIKE '%<{2}>%'".format(begin,end,tag)
		cursorDB = conn.cursor()
		cursorDB.execute(query)
		resultList = cursorDB.fetchall() #fetch the results
		tagCounter = Counter() #create a counter for the results
		#each result is a list of tags in a format : <tag1><tag2><tag3>... <<need to transform it to a list: [tag1,tag2,tag3....]
		for result in resultList:
			tagList = (''.join(result))[1:-1].split("><")
			for x in tagList:
				tagCounter[x] +=1

		tagCounter[tag] = 0
		finalResults += [tagCounter]
		cursorDB.close()

	conn.close()
	return finalResults


res = relatedTagsTimeInterval("java","01-04-2008",None,1)
for x in res:
	print("\n","\n","\n")
	print(res)