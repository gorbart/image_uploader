import os

from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.utils import timezone

from users.models import ApiUser


def upload_to(instance, filename):
    extension = filename.split('.')[-1]
    hashed_filename = hash(instance.owner.user.username) + hash(instance.upload_date) + hash(filename)
    return os.path.join(str(hashed_filename) + '.' + extension)


class Image(models.Model):
    name = models.CharField(max_length=50, unique=True)
    upload_date = models.DateTimeField(default=timezone.now)
    owner = models.ForeignKey(ApiUser, on_delete=models.CASCADE)

    image = models.ImageField(upload_to=upload_to, max_length=255)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f'{self.owner.user.username}-{self.name}'


@receiver(pre_delete, sender=Image)
def mymodel_delete(sender, instance, **kwargs):
    instance.image.delete(False)
