'''
Created on September 27, 2017

Runs Google API ocr on a directory of files.

    python google_vision_api.py imageDirectoryPath outputPath

    python google_vision_api.py /Users/halperta/GitHub/ahpn-ocr/data /Users/halperta/GitHub//ahpn-ocr/output

Where all paths are of form `/Users/halperta/GitHub/ahpn-ocr/'

@author: halperta
'''


import io
import os
import glob

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

# Instantiates a client
client = vision.ImageAnnotatorClient()

def ocrFiles(imageDirectoryPath, outputPath):
	filePaths_list = glob.glob("%(imageDirectoryPath)s/*.jpg" % {"imageDirectoryPath": imageDirectoryPath}) 
	for filePath in filePaths_list:
		fileName = os.path.basename(filePath)

		# Loads the image into memory
		with io.open(filePath, 'rb') as image_file:
			content = image_file.read()
		image = types.Image(content=content)

		response = client.document_text_detection(image=image)

		text_annotations = response.text_annotations

		f = open('%(outputPath)s/%(fileName)s-ocr.txt' % {"outputPath": outputPath,"fileName": fileName},'w')
		for entity_annotation in text_annotations:
		  f.write("language: ", entity_annotation.locale)
		  f.write("text:\n", entity_annotation.description)
		f.close()

if __name__ == '__main__': 

  (imageDirectoryPath, outputPath) = sys.argv[1:]
  ocrFiles(imageDirectoryPath, outputPath)  


# The name of the image file to annotate
# file_name = os.path.join(
#     os.path.dirname(__file__),
#     'cirma_inforpress_0079_002.jpg')

#haa 9-26: create list of all files and filepaths

# def getAllFileNames(directoryPath, fileExtension):
# 	filePaths_list = glob.glob("%(directoryPath)s/*.jpg" % {"directoryPath": directoryPath}) 
# 	fileNames_list = list()
# 	for filePath in filePaths_list:
# 	  fileNameWithExt = os.path.basename(filePath)
# 	  fileName = fileNameWithExt.replace(fileExtension,"")
# 	  fileNames_list.append(fileName)
# 	return fileNames_list, filePaths_list

#haa 9-26: modified to create capacity for multiple files.
# file_path_root = '/Users/halperta/GitHub/ahpn-ocr/'
# file_name = 'cirma_inforpress_0079_002.jpg'
# file_path = file_path_root + file_name

# Performs label detection on the image file
# response = client.label_detection(image=image)
# labels = response.label_annotations

# print('Labels:')
# for label in labels:
#     print(label.description)



# full_text_annotations = response.full_text_annotation









