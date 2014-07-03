from github3 import login
from github3 import search_repositories
import json
import getpass
import os


#log in
login = login(input("Github username or email: "), password = getpass.getpass(prompt="Password: ",stream=None))
tomazz = login.user()
#githubQuery = input("enter your github query: ")
#returns a collection of RepositorySearchResults
queriedRepos = search_repositories("language:MATLAB size:<1024", sort=None, order=None, per_page=50, number=2)

#create a directory with the name of the repo
#create a "details.json" file and a zip of the repo in that directory
for repo in queriedRepos:
	print(repo.repository.name)
	jsonRepoDict = repo.repository.to_json()
	directory = os.getcwd() + "\\" + repo.repository.name
	if not os.path.exists(directory):
		os.makedirs(directory)
	repo.repository.archive("zipball",path=(directory+ "\\" +repo.repository.name+".zip"))
	detailsFile = open(directory + "\\" + "details.json","w")
	json.dump(jsonRepoDict,detailsFile)
	detailsFile.close()
	print("-------------------------")
	
