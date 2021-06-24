from django.urls import path

from image_api.views import UploadImageView

app_name = 'image_api'

urlpatterns = [
    path('upload/', UploadImageView.as_view(), name='uploadimage')
]
