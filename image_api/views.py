from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from image_api.serializers import ImageSerializer
from image_handler.models import Image

IMAGE_NOT_FOUND_ERROR_MESSAGE = 'Image not found'
WRONG_TIER_ERROR_MESSAGE = "Your account tier won't allow this operation"


def get_api_user(request):
    token = request.auth
    user = Token.objects.get(key=token).user
    apiuser = user.apiuser
    return apiuser


class UploadImageView(APIView):

    def post(self, request):
        apiuser = get_api_user(request)
        data = request.data
        data['owner'] = apiuser.pk

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
