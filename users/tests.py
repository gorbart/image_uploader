from django.contrib.auth.models import User
from django.test import TestCase

from users.models import Role, ApiUser


class ApiUserTest(TestCase):

    def test_apiuser_with_role(self):
        thumbnail_sizes = [200]

        user = User.objects.create(username='username', password='password')
        role = Role.objects.create(name='role', thumbnail_sizes=thumbnail_sizes, can_get_original=True)
        ApiUser.objects.create(user=user, role=role)

        self.assertEqual(ApiUser.objects.first().role.thumbnail_sizes, f'{thumbnail_sizes}')
