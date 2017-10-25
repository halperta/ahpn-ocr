import sys
import subprocess
import glob
import os
import re
import shutil


def packageFiles():
	#generate a list of books
	listOfBookPaths = glob.glob("/Users/hra288/Github/neh/testTranscribedBooks/*/")
	#for each book, go through operations:
	for bookPath in listOfBookPaths:

		#generate file names and paths
		bookName = re.search(r".*Books/(.*?)/.*", bookPath).group(1)
		rootDirectory = "Users/hra288/Github/neh"
		TEXTPath = "testOutput/%(bookName)s/TEXT" % {"bookName": bookName}
		ALTOPath = "testOutput/%(bookName)s/ALTO" % {"bookName": bookName}
		allFileNames = os.listdir(bookPath)

		concatenateTextFiles(TEXTPath,allFileNames, bookName)
		# generateBlankXML()
		moveALTOFiles(allFileNames, bookName, ALTOPath)


def concatenateTextFiles(TEXTPath,allFileNames, bookName):
	#concatenate norm and trans text files into new folder.
	if not os.path.exists(TEXTPath):
		os.makedirs(TEXTPath)
	# print bookName

	normTextFileNames = list()
	transTextFileNames = list()
	for file in allFileNames:
		if file[-7:] == "zed.txt":
			filePath = "testTranscribedBooks/" + bookName + "/" + file
			print filePath
			normTextFileNames.append(filePath)
		if file[-7:] == "ion.txt":
			filePath = "testTranscribedBooks/" + bookName + "/" + file
			print filePath
			transTextFileNames.append(filePath)
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

# def generateBlankXML():
# 	#to do this I need to compare xml files against the list of image files which I currently don't have. where to get?


def moveALTOFiles(allFileNames, bookName, ALTOPath):
		#make directory
	if not os.path.exists(ALTOPath):
		os.makedirs(ALTOPath)
	for file in allFileNames:
		if file[-8:] == "alto.xml":
			filePath = "testTranscribedBooks/" + bookName + "/" + file
			fileOutputPath = ALTOPath + "/ALTO/" + file
			print "file output path is" + fileOutputPath
			if not os.path.exists(fileOutputPath):
				os.rename(filePath, fileOutputPath)


	#generate blank xml

if __name__ == '__main__': 
	packageFiles()

#copy ALTO files.












