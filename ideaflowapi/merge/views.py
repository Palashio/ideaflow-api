from django.shortcuts import render
from rest_framework.decorators import api_view
import os
from django.core.files.storage import default_storage
from django.http import JsonResponse, HttpResponse
from google.cloud import vision
import cv2
import io
import json
import numpy as np

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]= "app_creds.json"


@api_view(['POST'])
def merge_images(request):
    files = request.FILES.keys()
    data = request.data.keys()
    #
    if 'one' not in files or 'two' not in files:
        return JsonResponse({"MESSAGE": "BOTH IMAGES NOT PROVIDED"})

    first_file, second_file = request.FILES['one'], request.FILES['two']

    IMG_NAME_1 = 'buffer/first_image.png'
    # IMG_NAME_2 = 'buffer/second_image.png'

    default_storage.save(IMG_NAME_1, first_file)
    default_storage.save(IMG_NAME_1, second_file)

    img1 = cv2.imread(IMG_NAME_1)
    img2 = cv2.imread(IMG_NAME_1)

    img1_rotation = get_rotation()

    if 'vertical' in data:
        im_v = cv2.hconcat([img1, img2])
    else:
        im_v = cv2.vconcat([img1, img2])

    client = vision.ImageAnnotatorClient()

    with io.open(IMG_NAME_1, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations

    OCR_RESULTS = ""
    for text in texts:
        OCR_RESULTS += str(text.description) + "\n"

    os.remove(IMG_NAME_1)

    return JsonResponse(json.dumps(OCR_RESULTS), safe=False, status=200)

def process_image(incoming_image, rotation):
    if rotation == 0:
        return incoming_image
    elif rotation == 90:
        return cv2.rotate(incoming_image, cv2.cv2.ROTATE_90_CLOCKWISE)
    elif rotation == 180:
        return cv2.rotate(incoming_image, cv2.ROTATE_180)
    else:
        return cv2.rotate(incoming_image, cv2.ROTATE_90_COUNTERCLOCKWISE)

def get_rotation(response):
    import pprint
    texts = response.text_annotations

    current = texts[0].bounding_poly.vertices
    c_x, c_y = 0, 0

    for i in range(4):
        c_x += current[i].x
        c_y += current[i].y

    c_x = c_x / 4
    c_y = c_y / 4

    x_0 = current[0].x
    y_0 = current[0].y


    if x_0 < c_x:
        if y_0 < c_y:
            return 0
        else:
            return 270
    else:
        if y_0 < c_y:
            return 90
        else:
            return 180

        
