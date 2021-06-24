import os

from django.db import models
from django.utils import timezone

from users.models import ApiUser


def upload_to(instance, filename):
    return os.path.join(str(instance.owner_id), str(instance.upload_date.year), str(instance.upload_date.month),
                        str(instance.upload_date.day), filename)


class Image(models.Model):
    name = models.CharField(max_length=50, unique=True)
    upload_date = models.DateTimeField(default=timezone.now)
    owner = models.ForeignKey(ApiUser, on_delete=models.CASCADE)

    image = models.ImageField(upload_to=upload_to, max_length=255)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f'{self.owner.user.username}-{self.name}'
