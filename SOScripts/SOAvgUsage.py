import sys
import xml.etree.ElementTree as ET
import stackexchange
from stackauth import StackAuth
import json
import os
import datetime
from dateutil.relativedelta import relativedelta
import fleming
import pygal

sys.path.append('.')
site = stackexchange.Site(stackexchange.StackOverflow,"wZjX24zp2Y3wv6THqhZyPQ((")
#stackexchange.web.WebRequestManager.debug = True
site.be_inclusive()
date = datetime.datetime(2014,7,1)
numberOfMonths = 3
tagList = []


with open("SOConfig.txt","r") as tagFile:
    for line in tagFile:
        tagList = line.split(",")


directory = os.getcwd() + "\\StackOverflow\\AverageCommunitySize"
if not os.path.exists(directory):
	os.makedirs(directory)

sys.stdout.flush()
infoFile = open(directory + "\\" + "AverageCommunitySize.json","w")
infoDict = {}
infoDict["description"] = "this file contains information about the number of views for each tag in a specified period of time. here: one month"
infoDict["content"] = {}

for tag in tagList:
	infoDict["content"][tag] = 0

for m in range(numberOfMonths):
	fromDate = date - relativedelta(months= m + 1)
	toDate = date - relativedelta(months= m)
	print (fromDate,toDate)
	for tag in tagList:
		stackSearchResults = site.search(pagesize=100,tagged=tag,fromdate = str(fleming.unix_time(fromDate)),
		todate=str(fleming.unix_time(toDate)))
		total_count = 0
		for question in stackSearchResults:
			total_count += question.view_count

		infoDict["content"][tag] += total_count
		print("Total number of views for ----  {0}  ----is :".format(tag),total_count)
		print()

dataList = []
for tag in tagList:
	infoDict["content"][tag] = infoDict["content"][tag]/numberOfMonths
	dataList += [infoDict["content"][tag]]


###Chart
bar_chart = pygal.Bar()
bar_chart.title = 'Average community size'
bar_chart.x_labels = tagList
bar_chart.add('Average Number of Views', dataList)
bar_chart.render_to_file(directory + "\\chart.svg")


json.dump(infoDict,infoFile)
infoFile.close()
