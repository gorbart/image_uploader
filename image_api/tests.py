import io
import os

from django.conf.global_settings import MEDIA_ROOT
from django.contrib.auth.models import User
from django.core.files import File
from django.test import SimpleTestCase
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer

from image_api.serializers import ImageSerializer
from image_handler.models import Image
from image_uploader.settings import BASE_DIR
from users.models import Tier, ApiUser


class TestImageSerializer(SimpleTestCase):

    def test_image_serialize_and_deserialize(self):

        thumbnail_sizes = [200]

        user = User(username='username', password='password')
        tier = Tier(name='tier', thumbnail_sizes=thumbnail_sizes, can_get_original=True)
        apiuser = ApiUser(user=user, tier=tier)

        with open(os.path.join(BASE_DIR, 'media', 'test', 'python.png')) as f:
            image_from_disk = File(f)

        image = Image(name='Python', image=image_from_disk, owner=apiuser)

        pre_serializer = ImageSerializer(data=image)
        pre_serializer.is_valid()

        json = JSONRenderer().render(pre_serializer.data)

        stream = io.BytesIO(json)
        data = JSONParser().parse(stream)

        post_serializer = ImageSerializer(data=data)
        post_serializer.is_valid()

        self.assertEqual(pre_serializer.data, post_serializer.data)
