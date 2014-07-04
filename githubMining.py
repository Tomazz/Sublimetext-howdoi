from github3 import login
from github3 import search_repositories
import json
import getpass
import os

#log in
login = login(input("Github username or email: "), password = getpass.getpass(prompt="Password: ",stream=None))
user = login.user()

#Create a directory for the mined repos
miningDirectory = os.getcwd() + "\\GithubMining\\"
if not os.path.exists(miningDirectory):
    os.makedirs(miningDirectory)

#read the queries from the file
queryList = []
with open("GithubQueries","r") as queriesFile:
    for line in queriesFile:
        queryList +=[str(line)]

#execute the queries
for x in range(len(queryList)):
	#returns a collection of RepositorySearchResults
	queriedRepos = search_repositories(queryList[x], sort=None, order=None, per_page=50, number=10)
	miningDirectory = miningDirectory + "\\Query " + str(x) + "\\"
	#additionally add a fille with the query for each folder
	with open(miningDirectory + "\\" + "query","w") as queryFile:
		queryFile.write(queryList[x])
    #create a directory with the name of the repo
    #create a "details.json" file and a zip of the repo in that directory
	for repo in queriedRepos:
		print(repo.repository.name)
		jsonRepoDict = repo.repository.to_json()
		directory = miningDirectory + repo.repository.name
		if not os.path.exists(directory):
			os.makedirs(directory)
		#create a zip of the repo
		repo.repository.archive("zipball",path=(directory+ "\\" +repo.repository.name+".zip"))
		with open(directory + "\\" + "details.json","w") as detailsFile:
			json.dump(jsonRepoDict,detailsFile)
			print("-------------------------")
