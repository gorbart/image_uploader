from django.contrib.auth.models import AbstractUser, User, PermissionsMixin
from django.core.validators import int_list_validator
from django.db import models


class Tier(models.Model):

    name = models.CharField(max_length=30)
    thumbnail_sizes = models.TextField(validators=[int_list_validator])
    can_get_original = models.BooleanField(default=False)
    can_generate_expiring_links = models.BooleanField(default=False)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.name


class ApiUser(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tier = models.ForeignKey(Tier, on_delete=models.CASCADE)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return self.user.username
