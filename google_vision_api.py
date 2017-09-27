import io
import os

# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

# Instantiates a client
client = vision.ImageAnnotatorClient()

# The name of the image file to annotate
# file_name = os.path.join(
#     os.path.dirname(__file__),
#     'cirma_inforpress_0079_002.jpg')

#haa 9-26: create for-loop to work over multiple files
#should open the holding directory

#then import filenames into list of files
#then use that to do the following things for each file


#haa 9-26: modified to create capacity for multiple files.
file_path_root = '/Users/halperta/GitHub/ahpn-ocr/'
file_name = 'cirma_inforpress_0079_002.jpg'
file_path = file_path_root + file_name

# Loads the image into memory
with io.open(file_path, 'rb') as image_file:
    content = image_file.read()

image = types.Image(content=content)

# Performs label detection on the image file
# response = client.label_detection(image=image)
# labels = response.label_annotations

# print('Labels:')
# for label in labels:
#     print(label.description)

response = client.document_text_detection(image=image)


text_annotations = response.text_annotations
for entity_annotation in text_annotations:
  print("language: ", entity_annotation.locale)
  print("text:\n", entity_annotation.description)
  # 

# full_text_annotations = response.full_text_annotation

# print to file
f = open('helloworld.txt','w')
f.write('hello world')
f.close()








