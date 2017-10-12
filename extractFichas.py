'''
Created October, 2017
For extracting fichas from ahpn website. 
@author: halperta
'''

import sys
import csv
import re
import requests

if __name__ == '__main__':
#get URLS to list
	with open('ficha_urls.csv', 'r') as f:
		reader = csv.reader(f)
		fichaURLS = list(reader)

#get html from website.
	for url in fichaURLS:
		page = requests.get(url)
		html_content = page.text
		try:
			filename = re.search("br.pages = \[\n\[\'(.+?),", html_content).group(1)
		except AttributeError:
			found = "nope"




