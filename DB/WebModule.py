import google #edited
import argparse
import urllib


def getSOUrls(query,returnIds = False):
	""" Given a google query return the urls to the top 10 results """
	results = google.search(query, num=10, start=0, stop=10, pause=0.2)
	urlList = []
	for result in results:
		urlList += [result]

	if returnIds:
		for x in range(len(urlList)):
			urlList[x] = getIDFromUrl(urlList[x])
		urlList = tuple(urlList)
		return urlList
	else:
		return urlList


def getIDFromUrl(url):
	""" Given a stackoverflow url return the question ID """
	parsed = urllib.parse.urlparse(url)
	ID = (parsed.path).split('/')[2]
	return ID


def main():
	""" if the module run independently """
	parser = argparse.ArgumentParser(description='helper module for interaction with the web')
	parser.add_argument('--getId', help='Given a stackoverflow url return the question ID', required=False)
	parser.add_argument('--getSOUrls', help='use google search engine to search stackoverflow. Returns result urls', required=False)
	args = vars(parser.parse_args())

	if args["getId"]:
		getIDFromUrl(args["getId"])
	elif args["getSOUrls"]:
		getSOUrls(args["getSOUrls"])

if __name__ == '__main__':
    main()
