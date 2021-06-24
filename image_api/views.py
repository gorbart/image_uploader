from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from image_api.serializers import ImageSerializer


class UploadImageView(APIView):

    def post(self, request):
        token = request.auth

        user = Token.objects.get(key=token).user

        apiuser = user.apiuser

        data = request.data

        data['owner'] = apiuser.pk

        serializer = ImageSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
