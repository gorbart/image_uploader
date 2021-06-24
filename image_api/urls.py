from django.urls import path

from image_api.views import *

app_name = 'image_api'

urlpatterns = [
    path('upload/', UploadImageView.as_view(), name='uploadimage'),
    path('list/', ListImagesView.as_view(), name='listimages'),
    path('link/', ImageLinkView.as_view(), name='imagelink'),
]
