'''
Created on September 27, 2017

Runs Google API ocr on a directory of files.

    python google_vision_api.py imageDirectoryPath outputPath

    python google_vision_api.py /Users/halperta/GitHub/ahpn-ocr/data /Users/halperta/GitHub/ahpn-ocr/output

Where all paths are of form `/Users/halperta/GitHub/ahpn-ocr/'

@author: halperta
'''

import sys
import io
import os
import glob
import codecs

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

# Instantiates a client
client = vision.ImageAnnotatorClient()

def make_request_from_file(filepath):
  # Loads the image into memory
  with io.open(filepath, 'rb') as image_file:
    content = image_file.read()
  image = types.Image(content=content)

  # response = client.document_text_detection(image=image)
  request = dict(
    image = image,
    features = [
      dict(type='DOCUMENT_TEXT_DETECTION'),
      # Add more entries here if more types are desired.
    ],
    image_context = dict(
      language_hints=['es']  # optional
    ),
  )
  return request


def ocrFiles(imageDirectoryPath, outputPath, max_images):
  requests = []
  filenames = []
  filepaths_list = glob.glob("%(imageDirectoryPath)s/*.jpg" % {"imageDirectoryPath": imageDirectoryPath}) 
  for filepath in filepaths_list[:max_images]:
    request = make_request_from_file(filepath)
    requests.append(request)
    filenames.append(os.path.basename(filepath))

  batch_response = client.batch_annotate_images(requests)
  print("responses.size = ", sum(1 for _ in batch_response.responses))
  for (response, filename) in zip(batch_response.responses, filenames):
    text_annotations = response.text_annotations

    with codecs.open('%(outputPath)s/%(filename)s-ocr.txt' % {"outputPath": outputPath,"filename": filename},'w',"utf-8") as f:
      for entity_annotation in text_annotations:
        f.write('language: %(language)s\n' % {"language": entity_annotation.locale})
        f.write("text:\n %(text)s\n" % {"text": entity_annotation.description})

if __name__ == '__main__': 

  (imageDirectoryPath, outputPath) = sys.argv[1:]
  ocrFiles(imageDirectoryPath, outputPath, max_images = 16)


# The name of the image file to annotate
# filename = os.path.join(
#     os.path.dirname(__file__),
#     'cirma_inforpress_0079_002.jpg')

#haa 9-26: create list of all files and filepaths

# def getAllfilenames(directoryPath, fileExtension):
#   filepaths_list = glob.glob("%(directoryPath)s/*.jpg" % {"directoryPath": directoryPath}) 
#   filenames_list = list()
#   for filepath in filepaths_list:
#     filenameWithExt = os.path.basename(filepath)
#     filename = filenameWithExt.replace(fileExtension,"")
#     filenames_list.append(filename)
#   return filenames_list, filepaths_list

#haa 9-26: modified to create capacity for multiple files.
# filepath_root = '/Users/halperta/GitHub/ahpn-ocr/'
# filename = 'cirma_inforpress_0079_002.jpg'
# filepath = filepath_root + filename

# Performs label detection on the image file
# response = client.label_detection(image=image)
# labels = response.label_annotations

# print('Labels:')
# for label in labels:
#     print(label.description)



# full_text_annotations = response.full_text_annotation









