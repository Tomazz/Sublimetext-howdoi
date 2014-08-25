from google import search

# Get the first 20 hits for "Mariposa botnet" in Google Spain
from google import search
for url in search('init allintext:python stackoverflow', stop=20):
	print(url)
