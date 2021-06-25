import os

from django.contrib.auth.models import User
from django.core.files import File
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIRequestFactory, APIClient

from image_uploader.settings import BASE_DIR
from users.models import Tier, ApiUser

PYTHON_PNG = 'python.png'
BMP_TEST_IMAGE_NAME = 'bmp_test.bmp'
IMAGE_NAME = 'python'


class ViewsTest(APITestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.client = APIClient()

        user = User.objects.create_user(username='username', password='password')
        user.save()
        self.token = Token.objects.get(user_id=user.id)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        thumbnail_sizes = '200, 400'
        tier = Tier.objects.create(name='tier', thumbnail_sizes=thumbnail_sizes, can_get_original=True)
        self.apiuser = ApiUser.objects.create(user=user, tier=tier)

    def test_upload_image(self):
        response = self.upload_image(PYTHON_PNG)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_upload_image_wrong_format(self):
        response = self.upload_image(BMP_TEST_IMAGE_NAME)

        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

    def test_list_images(self):
        self.upload_image(PYTHON_PNG)

        url = reverse('image_api:listimages')
        response = self.client.get(url, format='json')
        self.assertEqual(len(response.data), len(self.apiuser.image_set.all()))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_image_link_correct(self):
        self.upload_image(PYTHON_PNG)

        url = reverse('image_api:imagelink')
        response = self.client.get(url, {'name': IMAGE_NAME}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_image_link_incorrect(self):
        self.upload_image(PYTHON_PNG)

        url = reverse('image_api:imagelink')
        response = self.client.get(url, {'name': IMAGE_NAME + 'XYZ'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_image_link_wrong_tier(self):
        self.apiuser.tier.can_get_original = False
        self.apiuser.tier.save()
        self.apiuser.save()

        self.upload_image(PYTHON_PNG)

        url = reverse('image_api:imagelink')
        response = self.client.get(url, {'name': IMAGE_NAME}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_nonexistent_thumbnail(self):
        self.upload_image(PYTHON_PNG)
        response = self.get_thumbnail()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_existent_thumbnail(self):
        self.upload_image(PYTHON_PNG)
        self.get_thumbnail()
        response = self.get_thumbnail()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(self.apiuser.image_set.all()), 2)

    def get_thumbnail(self):
        url = reverse('image_api:thumbnaillink')
        response = self.client.get(url, {'name': IMAGE_NAME, 'size': 200}, format='json')
        return response

    def upload_image(self, image_name):
        url = reverse('image_api:uploadimage')
        with open(os.path.join(BASE_DIR, 'media', 'test', image_name), 'rb') as f:
            image_from_disk = File(f)
            data = {'name': IMAGE_NAME, 'image': image_from_disk}

            response = self.client.post(url, data, format='multipart')
        return response
