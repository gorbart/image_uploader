import urllib.request

from django.contrib.auth.models import User
from django.core.files import File
from django.test import TestCase

from image_handler.models import Image
from users.models import Tier, ApiUser


class TestImage(TestCase):

    def test_image_saving_and_retrieval(self):
        image_url = 'https://applover.pl/wp-content/uploads/2020/01/kisspng-python-computer-icons-programming-' \
                    'language-executa-5d0f0aa7c78fb3.0414836115612668558174-1024x1024.png'

        user = User.objects.create(username='username', password='password')
        tier = Tier.objects.create(name='role', thumbnail_sizes=[200], can_get_original=True)
        apiuser = ApiUser.objects.create(user=user, tier=tier)

        image_from_web = File(urllib.request.urlretrieve(image_url))

        image = Image.objects.create(name='Python', image=image_from_web, owner=apiuser)

        self.assertEqual(image_from_web, image.image)
