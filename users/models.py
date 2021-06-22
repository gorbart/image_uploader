from django.contrib.auth.models import AbstractUser, User
from django.core.validators import validate_comma_separated_integer_list
from django.db import models


class Role(models.Model):

    name = models.CharField(max_length=30)
    thumbnail_sizes = models.TextField(validators=[validate_comma_separated_integer_list])
    can_get_original = models.BooleanField(default=False)
    can_generate_expiring_links = models.BooleanField(default=False)


class ApiUser(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    def __repr__(self):
        return self.user.username
