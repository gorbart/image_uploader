import os
import uuid
from io import BytesIO

import PIL
from django.core.files import File
from django.core.files.images import ImageFile
from django.utils import timezone
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from image_api.serializers import ImageSerializer
from image_handler.models import Image

POSSIBLE_IMAGE_FORMATS = ['jpg', 'png']

IMAGE_NOT_FOUND_ERROR_MESSAGE = 'Image not found'
WRONG_TIER_ERROR_MESSAGE = "Your account tier won't allow this operation"
WRONG_FORMAT_ERROR_MESSAGE = 'Only possible image formats are: {}'.format(POSSIBLE_IMAGE_FORMATS)
INVALID_EXPIRY_TIME_ERROR_MESSAGE = 'Expiry time should be from interval [300, 30000]'
INTERNAL_SERVER_ERROR_MESSAGE = 'Internal server error'

MIN_EXPIRY_TIME = 300
MAX_EXPIRY_TIME = 30000


def get_api_user(request):
    token = request.auth
    user = Token.objects.get(key=token).user
    apiuser = user.apiuser
    return apiuser


def create_thumbnail(image, thumbnail_height):
    image_height = image.image.height
    thumbnail_width = image.image.width / (image_height / thumbnail_height)
    image_path = image.image.path
    pil_image = PIL.Image.open(image_path)
    pil_image.load()
    pil_image.thumbnail((thumbnail_width, thumbnail_height))
    extension = image_path.split('.')[-1]
    blob = BytesIO()
    pil_image.save(blob, extension.upper())
    blob.seek(0)
    return blob, extension


def retrieve_image(apiuser, thumbnail_name):
    try:
        thumbnail = apiuser.image_set.get(name=thumbnail_name)
    except Image.DoesNotExist:
        thumbnail = None
    return thumbnail


def get_possible_thumbnail_heights(apiuser):
    possible_thumbnail_heights = [int(s) for s in apiuser.tier.thumbnail_sizes.split(',')]
    return possible_thumbnail_heights


class UploadImageView(APIView):

    def post(self, request):
        apiuser = get_api_user(request)
        data = request.data
        data['owner'] = apiuser.pk

        extension = data['image'].name.split('.')[-1]

        if extension not in POSSIBLE_IMAGE_FORMATS:
            return Response({'error': WRONG_FORMAT_ERROR_MESSAGE}, status=status.HTTP_406_NOT_ACCEPTABLE)

        serializer = ImageSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListImagesView(APIView):

    def get(self, request):
        apiuser = get_api_user(request)

        images = [(image.name, image.upload_date) for image in apiuser.image_set.all()]

        return Response(data={'images': images}, status=status.HTTP_200_OK)


class ImageLinkView(APIView):

    def get(self, request):
        apiuser = get_api_user(request)

        if not apiuser.tier.can_get_original:
            return Response({'error': WRONG_TIER_ERROR_MESSAGE}, status=status.HTTP_403_FORBIDDEN)

        try:
            image = apiuser.image_set.get(name=request.query_params['name'])
        except Image.DoesNotExist:
            image = None

        if image:
            serializer = ImageSerializer(image)
            return Response(data={'image': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'error': IMAGE_NOT_FOUND_ERROR_MESSAGE}, status=status.HTTP_404_NOT_FOUND)


class ThumbnailLinkView(APIView):

    def get(self, request):
        apiuser = get_api_user(request)
        possible_thumbnail_heights = get_possible_thumbnail_heights(apiuser)

        image_name = request.query_params['name']

        thumbnail_height = int(request.query_params['size'])
        thumbnail_name = image_name + '.' + str(thumbnail_height) + 'px'

        if thumbnail_height not in possible_thumbnail_heights:
            return Response({'error': WRONG_TIER_ERROR_MESSAGE}, status=status.HTTP_403_FORBIDDEN)

        thumbnail = retrieve_image(apiuser, thumbnail_name)

        if thumbnail:
            serializer = ImageSerializer(thumbnail)
            return Response(data={'thumbnail': serializer.data}, status=status.HTTP_200_OK)

        image = retrieve_image(apiuser, image_name)

        if image:
            blob, extension = create_thumbnail(image, thumbnail_height)

            data = {'name': thumbnail_name, 'owner': apiuser.pk,
                    'image': ImageFile(blob, name=thumbnail_name + '.' + extension)}

            serializer = ImageSerializer(data=data)

            if not serializer.is_valid():
                return Response({'error': INTERNAL_SERVER_ERROR_MESSAGE}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            serializer.save()
            return Response(data={'thumbnail': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'error': IMAGE_NOT_FOUND_ERROR_MESSAGE}, status=status.HTTP_404_NOT_FOUND)


class ExpiringLinksView(APIView):

    def get(self, request):
        apiuser = get_api_user(request)

        if not apiuser.tier.can_generate_expiring_links:
            return Response({'error': WRONG_TIER_ERROR_MESSAGE}, status=status.HTTP_403_FORBIDDEN)

        expiry_time = int(request.query_params['expirytime'])

        if not MIN_EXPIRY_TIME <= expiry_time <= MAX_EXPIRY_TIME:
            return Response({'error': INVALID_EXPIRY_TIME_ERROR_MESSAGE}, status=status.HTTP_406_NOT_ACCEPTABLE)

        try:
            image = apiuser.image_set.get(name=request.query_params['name'])
        except Image.DoesNotExist:
            image = None

        if image:
            image.pk = None
            image.name = image.name + str(expiry_time) + 's' + str(uuid.uuid4())[:8]
            image.upload_time = timezone.now()
            image.expiry_time = timezone.now() + timezone.timedelta(seconds=expiry_time)

            with open(image.image.file.name, 'rb') as f:
                image_from_disk = File(f)
                image.image = image_from_disk
                image.save()

                serializer = ImageSerializer(image)

                return Response(data={'image': serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'error': IMAGE_NOT_FOUND_ERROR_MESSAGE}, status=status.HTTP_404_NOT_FOUND)
