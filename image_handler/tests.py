import os
import urllib.request

from django.contrib.auth.models import User
from django.core.files import File
from django.test import TestCase

from image_handler.models import Image
from image_uploader.settings import MEDIA_ROOT, BASE_DIR
from users.models import Tier, ApiUser


class TestImage(TestCase):

    def test_image_saving_and_retrieval(self):

        user = User.objects.create(username='username')
        tier = Tier.objects.create(name='role', thumbnail_sizes=[200], can_get_original=True)
        apiuser = ApiUser.objects.create(user=user, tier=tier)

        with open(os.path.join(BASE_DIR, 'media', 'test', 'python.png'), errors='ignore') as f:
            image_from_disk = File(f)

            image = Image.objects.create(name='Python', image=image_from_disk, owner=apiuser)

            image_from_db = Image.objects.first()

        self.assertEqual(image.image, image_from_db.image)
