'''
Created October, 2017
For extracting fichas from ahpn website. 
@author: halperta
'''

import sys
import csv
# from lxml import html
import requests
import re
# from selenium import webdriver

if __name__ == '__main__':
#get URLS to list
  with open('ficha_urls.csv', 'r') as f:
    reader = csv.reader(f)
    fichaURLS = list(reader)
  urlList = []
  for url in fichaURLS:
    for suburl in url:
      urlList.append(suburl)
  print urlList

  f = open("ficha_filepaths.txt", "w")
#get html from website.
  for url in urlList:
    page = requests.get(url)
    html_content = page.text
#    print html_content
    m = re.search("br.pages = \[\n.*\['(.+?)',", html_content)
    if m:
      found = m.group(1)
      print found
      f.write(found + "\n")
    else:
      print "no"
  f.close()

    # try:
    #   filename = re.search("br.pages = \[\n\[\'(.+?),", html_content).group(1)
    # except AttributeError:
    #   found = "nope"




