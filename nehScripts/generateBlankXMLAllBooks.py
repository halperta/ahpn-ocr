'''
Created on April 11, 2017
Automates production of blank dipl. XML files when provided with a path to the the containing folders for XML files and image files.
    cd ocr-auxiliary-data/scripts/
    python generateBlankXMLAllBooks.py imageDirectoryPath xmlDirectoryPath outputPath
    python generateBlankXMLAllBooks.py "/Volumes/My\ Passport/primeros_media" /Users/hra288/Github/neh/testTranscribedBooks /Users/hra288/Github/neh/testOutput 
Where all paths are of form `/Users/halperta/GitHub/ocr-auxiliary-data'
@author: halperta
'''

import sys
import subprocess
import glob
import os
import re #if using replacements on regex

def getAllFileNames(directoryPath, fileExtension):
  # get image file relative paths & strip extensions
  getFilePaths = "%(directoryPath)s/*%(fileExtension)s" % {"directoryPath": directoryPath, "fileExtension": fileExtension} 
  print getFilePaths
  filePaths_list = glob.glob(getFilePaths)
  print filePaths_list
  fileNames_list = list()
  for filePath in filePaths_list:
    fileNameWithExt = os.path.basename(filePath)
    fileName = fileNameWithExt.replace(fileExtension,"")
    fileNames_list.append(fileName)
  return fileNames_list, filePaths_list

def generateBlankXML(imageDirectoryPath, xmlDirectoryPath, outputPath):

  getBookPaths = xmlDirectoryPath + "/*/"
  listOfBookPaths = glob.glob(getBookPaths)
  for bookPath in listOfBookPaths:
    print bookPath
    bookName = re.search(r".*Books/(.*?)/.*", bookPath).group(1)
    bookImageDirectoryPath = imageDirectoryPath + "/%(bookName)s/1000" % {"bookName": bookName}
    bookXMLDirectoryPath = xmlDirectoryPath + "/%(bookName)s/" % {"bookName": bookName}
    bookOutputPath = "%(outputPath)s/%(bookName)s/" % {"outputPath": outputPath, "bookName": bookName}

    imageFileNames_list, imageFilePaths_list = getAllFileNames(bookImageDirectoryPath,".jpg")
    print "imagefilenameslist  \n" 
    print imageFileNames_list
    xmlFileNames_list, xmlFilePaths_list = getAllFileNames(bookXMLDirectoryPath,"_dipl.alto.xml")


  #   imageFilePaths_list = glob.glob("%(imageDirectoryPath)s/*.jpg" % {"imageDirectoryPath": imageDirectoryPath}) 
  #   imageFileNames_list = list()
  #   for imageFilePath in imageFilePaths_list:
  #     imageFileNameWithExt = os.path.basename(imageFilePath)
  #     imageFileName = imageFileNameWithExt.replace(".jpg","")
  #     imageFileNames_list.append(imageFileName)
    #print imageFileNames_list
    
    # get xml files relative paths
  #   xmlFilePaths_list = glob.glob("%(xmlDirectoryPath)s/*_dipl.alto.xml" % {"xmlDirectoryPath": xmlDirectoryPath})
  #   xmlFileNames_list = list()
  #   for xmlFilePath in xmlFilePaths_list:
  #     xmlFileNameWithExt = os.path.basename(xmlFilePath)
  #     xmlFileName = xmlFileNameWithExt.replace("_dipl.alto.xml","")
  #     xmlFileNames_list.append(xmlFileName)
  #   print xmlFileNames_list
     
    #remove files that already exist in xml
    untranscribed_list = list()
    for imageFileName in imageFileNames_list:
      if imageFileName not in xmlFileNames_list:
        untranscribed_list.append(imageFileName)  
    print untranscribed_list
    
    #produce new xml files with the appropriate text.
    for fileName in untranscribed_list:
      shortFileName = fileName.replace("-1000","")
      imageNumber = shortFileName[-5:]
      xmlText = (
        """<?xml version="1.0" encoding="UTF-8"?>""",
        """<alto xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns="http://www.loc.gov/standards/alto/ns-v3#" xsi:schemaLocation="http://www.loc.gov/standards/alto/ns-v3# http://www.loc.gov/standards/alto/v3/alto.xsd" xmlns:emop="http://emop.tamu.edu">""",
        """  <Description>""",
        """    <MeasurementUnit>pixel</MeasurementUnit>""",
        """    <sourceImageInformation>""",
        """      <fileName>%(fileName)s.jpg</fileName>""" % {"fileName": fileName},
        """    </sourceImageInformation>""",
        """  </Description>""",
        """  <Layout>""",
        """    <Page ID="%(shortFileName)s"  PHYSICAL_IMG_NR="%(imageNumber)s"></Page>""" % {"shortFileName": shortFileName, "imageNumber": imageNumber},
        """  </Layout>""",
        """</alto>""")
  #    f = open('%(xmlDirectoryPath)s/%(fileName)s_dipl.alto.xml' % {"xmlDirectoryPath": xmlDirectoryPath,"fileName": fileName},'w') # if you want to print to location of all xml files
      f = open('%(outputPath)s/%(fileName)s_dipl.alto.xml' % {"outputPath": outputPath,"fileName": fileName},'w')
      for line in xmlText:
        f.write("%s\n" % line)
      f.close()

      f = open('%(outputPath)s/%(fileName)s_norm.alto.xml' % {"outputPath": outputPath,"fileName": fileName},'w')
      for line in xmlText:
        f.write("%s\n" % line)
      f.close()
            
if __name__ == '__main__': 

  (imageDirectoryPath, xmlDirectoryPath,outputPath) = sys.argv[1:]
  generateBlankXML(imageDirectoryPath, xmlDirectoryPath, outputPath)  
