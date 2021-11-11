from django.urls import path
from .views import merge_images

urlpatterns = [
    path('', merge_images)
]