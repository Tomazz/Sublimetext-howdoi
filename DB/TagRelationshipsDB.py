#This script cmmunicates with the database 
#to produce charts that represent relationships between two or more tags
#ex:
#What different tags(and their frequency) appear alongside the tag "python"

import os
import psycopg2
import getpass
from collections import Counter
import pygal
import argparse

parser = argparse.ArgumentParser(description='This script cmmunicates with the database \n +\
												to produce charts that represent relationships between two or more tags. Ex: \n \n +\
												What different tags(and their frequency) appear alongside the tag "python"')
parser.add_argument('-t','--tag', help='Name of the tag of which you want to know the other associated tags', required=True)
args = vars(parser.parse_args())

conn = psycopg2.connect(dbname="internship2014", user="postgres", password=getpass.getpass(prompt="Password: ",stream=None))
cursorDB = conn.cursor()

query1 = "SELECT tags FROM posts WHERE tags LIKE '%<{tag}>%'".format(**args) # "tag" is a key in the args dictionary. Load the tag from the dictionary into the query
cursorDB.execute(query1) #execute query
resultList = cursorDB.fetchall() #fetch the results
tagCounter = Counter() #create a counter for the results
#each result is a list of tags in a format : <tag1><tag2><tag3>... <<need to transform it to a list: [tag1,tag2,tag3....]
for result in resultList:
	tagList = (''.join(result))[1:-1].split("><")
	for tag in tagList:
		tagCounter[tag] +=1

tagCounter[args["tag"]] = 0

tagList = tagCounter.most_common(25)
bar_chart = pygal.Bar()
bar_chart.title = 'Tags associated with tag: '+args["tag"]
for element in tagList:
	bar_chart.add(element[0],element[1])
bar_chart.render_to_file(os.getcwd() + "\\chart_relatedTags_"+args["tag"]+".svg")

cursorDB.close()
conn.close()