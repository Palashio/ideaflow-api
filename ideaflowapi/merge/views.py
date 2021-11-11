from django.shortcuts import render
from rest_framework.decorators import api_view
import os
from django.core.files.storage import default_storage
from django.http import JsonResponse, HttpResponse
from google.cloud import vision
import cv2
import io
import json

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]= "app_creds.json"


@api_view(['GET'])
def merge_images(request):
    files = request.FILES.keys()
    #
    if 'one' not in files or 'two' not in files:
        return JsonResponse({"MESSAGE": "BOTH IMAGES NOT PROVIDED"})

    first_file, second_file = request.FILES['one'], request.FILES['two']

    IMG_NAME_1 = 'buffer/first_image.png'
    IMG_NAME_2 = 'buffer/second_image.png'

    default_storage.save(IMG_NAME_1, first_file)
    default_storage.save(IMG_NAME_2, second_file)

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

    os.remove(IMG_NAME_1)
    os.remove(IMG_NAME_2)

    return JsonResponse(json.dumps(OCR_RESULTS), safe=False, status=200)


