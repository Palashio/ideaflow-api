import cv2
from google.cloud import vision
from google.protobuf.json_format import MessageToDict
import io
import os
import proto

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="app_creds.json"

IMG_NAME_1 = "Screen Shot 2021-11-08 at 1.14.18 PM.png"
IMG_NAME_2 = "Screen Shot 2021-11-09 at 6.37.22 PM.png"

img1 = cv2.imread(IMG_NAME_1)
img2 = cv2.imread(IMG_NAME_2)

im_v = cv2.vconcat([img1, img1])


client = vision.ImageAnnotatorClient()

with io.open(IMG_NAME_1, 'rb') as image_file:
    content = image_file.read()

image = vision.Image(content=content)

response = client.text_detection(image=image)
texts = response.text_annotations

OCR_RESULTS = ""
for text in texts:
    OCR_RESULTS += str(text.description) + "\n"

print(OCR_RESULTS)

ocr_dict = {"result": OCR_RESULTS}
ocr_dict.json()


