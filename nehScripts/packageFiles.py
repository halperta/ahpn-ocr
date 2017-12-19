'''
Created on Dec 18 2017
	Automatically packages a collection of transcribed files from the DH Dashboard for ingest to the Primeros Libros site. 
	rootTranscriptionPath = path to directory containing the transcribed files. Should be rootTranscriptionPath/bookid/....xml
	rootImagePath = path to directory containing the page images. Should be rootImagePath/bookid/....jpg
	rootOutputPath = path to directory where book directories contaning xml and text files will be output.

	python packageFiles.py /Users/hra288/Github/neh/TranscribedBooks /Users/hra288/Documents/primeros_media /Users/hra288/Github/neh/pl_packagedTranscriptions_12-18-2017
	python packageFiles.py /Users/hra288/Github/neh/testTranscribedBooks /Users/hra288/Documents/primeros_media /Users/hra288/Github/neh/testOutput

@author: halperta
'''

import sys
import subprocess
import glob
import os
import re
import shutil


def packageFiles(rootTranscriptionPath,rootImagePath,rootOutputPath):
#generate a list of all transcribed books
	bookPaths = rootTranscriptionPath + "/*/"
	listOfBookPaths = glob.glob(bookPaths)

	#for each book, concatenate 
	for bookPath in listOfBookPaths:

		#generate file names and paths
		bookName = re.search(r".*Books/(.*?)/.*", bookPath).group(1)
		TEXTPath = rootOutputPath + "/%(bookName)s/TEXT" % {"bookName": bookName}
		ALTOPath = rootOutputPath + "/%(bookName)s/ALTO" % {"bookName": bookName}
		imagePath = rootImagePath + "/" + bookName + "/1000/"
		print "Beginning book " + bookName

		#generate list of page file names
		allFileNamesOne = os.listdir(bookPath)
		allFileNames = list()
		for file in allFileNamesOne:
			if not file.startswith(".") or file.startswith("Thu"):
				allFileNames.append(file)

		#run three operations
		concatenateTextFiles(TEXTPath,allFileNames, bookName, rootTranscriptionPath)
		moveALTOFiles(allFileNames, bookName, ALTOPath)
		generateBlankXML(bookName,allFileNames,ALTOPath,imagePath)

def concatenateTextFiles(TEXTPath,allFileNames, bookName, rootTranscriptionPath):
#Create a TEXT folder that contains one file for plain text transcriptions, and one page for normalized transcriptions.
	print "Concatenating text files and printing to TEXT subdirectory: " + TEXTPath

	#Create output subdirectory
	if not os.path.exists(TEXTPath):
		os.makedirs(TEXTPath)

	normTextFileNames = list()
	transTextFileNames = list()
	#Make a list of all files for plain text diplomatic transcriptions (transTextFileNames) and normalized transcriptions (normTextFileNames) 
	for file in allFileNames:
		if not file.startswith(".") and not file.startswith("Thumbs"):
			if file[-7:] == "zed.txt": #normalized files
				filePath = rootTranscriptionPath + "/" + bookName + "/" + file
				normTextFileNames.append(filePath)
			if file[-7:] == "ion.txt": #diplomatic files
				filePath = rootTranscriptionPath  + "/" + bookName + "/" + file
				transTextFileNames.append(filePath)

	#concatenate diplomatic text and print to new file. Repeat with normalized text.
	normTextOutputPath = '%(TEXTPath)s/%(bookName)s_normalized.txt' %{"TEXTPath": TEXTPath, "bookName": bookName}
	if not os.path.exists(normTextOutputPath):
		with open(normTextOutputPath,'wb') as wfd:
			for f in normTextFileNames:
				with open(f,'rb') as fd:
					shutil.copyfileobj(fd, wfd)
	transTextOutputPath = '%(TEXTPath)s/%(bookName)s_transcription.txt' %{"TEXTPath": TEXTPath, "bookName": bookName}
	if not os.path.exists(transTextOutputPath):
		with open(transTextOutputPath,'wb') as wfd:
			for f in transTextFileNames:
				with open(f,'rb') as fd:
					shutil.copyfileobj(fd, wfd)

def generateBlankXML(bookName,allFileNames,ALTOPath,imagePath):
#Identify any pages that were not transcribed and create blank XML files for both normalized and dipomatic transcriptions.
	print "Generating blank XML."

	#create output subdirectory for XML files
	if not os.path.exists(ALTOPath):
		os.makedirs(ALTOPath)

	#make list of file names for all transcribed pages
	transcribedPages = list()
	for file in allFileNames:
		fileShort = file[:17]
		if not fileShort in transcribedPages:
			transcribedPages.append(fileShort)
	#make list of file names for all pages in book
	imageFileNamesLong = os.listdir(imagePath)
	imagePages = list()
	for file in imageFileNamesLong:
		if not file.startswith(".") and not file.startswith("Thu"):
			imagePages.append(file[:17])

	#identify pages that have not been transcribed, and generate blank xml.
	for page in imagePages:
		if page not in transcribedPages:
			imageNumber = page[-5:]
			fileName = page + "-1000"
			xmlText = (
				"""<?xml version="1.0" encoding="UTF-8"?>""",
				"""<alto xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns="http://www.loc.gov/standards/alto/ns-v3#" xsi:schemaLocation="http://www.loc.gov/standards/alto/ns-v3# http://www.loc.gov/standards/alto/v3/alto.xsd" xmlns:emop="http://emop.tamu.edu">""",
				"""  <Description>""",
				"""<MeasurementUnit>pixel</MeasurementUnit>""",
				"""<sourceImageInformation>""",
				"""  <fileName>%(fileName)s.jpg</fileName>""" % {"fileName": fileName},
				"""</sourceImageInformation>""",
				"""  </Description>""",
				"""  <Layout>""",
				"""<Page ID="%(shortFileName)s"  PHYSICAL_IMG_NR="%(imageNumber)s"></Page>""" % {"shortFileName": page, "imageNumber": imageNumber},
				"""  </Layout>""",
				"""</alto>""")
			  #f = open('%(xmlDirectoryPath)s/%(fileName)s_dipl.alto.xml' % {"xmlDirectoryPath": xmlDirectoryPath,"fileName": fileName},'w') # if you want to print to location of all xml files
			f = open('%(bookOutputPath)s/%(fileName)s_dipl.alto.xml' % {"bookOutputPath": ALTOPath, "fileName": fileName},'w')
			print "generating dipl xml for page " + page
			for line in xmlText:
				f.write("%s\n" % line)
			f.close()

			f = open('%(bookOutputPath)s/%(fileName)s_norm.alto.xml' % {"bookOutputPath": ALTOPath, "fileName": fileName},'w')
			print "generating norm xml for page " + page
			for line in xmlText:
				f.write("%s\n" % line)
			f.close()

def moveALTOFiles(allFileNames, bookName, ALTOPath):
#Create output subdirectory for XML files and copy all xml transcriptions to new directory
	print "Copying XML files to ALTO subdirectory: " + ALTOPath

	#Create output subdirectory for XML files
	if not os.path.exists(ALTOPath):
		os.makedirs(ALTOPath)

	#copy files to subdirectory.
	for file in allFileNames:
		if file[-8:] == "alto.xml":
			filePath = rootTranscriptionPath + "/" + bookName + "/" + file
			fileOutputPath = ALTOPath + "/" + file
			if not os.path.exists(fileOutputPath):
				shutil.copyfile(filePath, fileOutputPath)

if __name__ == '__main__': 

	(rootTranscriptionPath,rootImagePath,rootOutputPath) = sys.argv[1:]
	packageFiles(rootTranscriptionPath,rootImagePath,rootOutputPath)

#copy ALTO files.












