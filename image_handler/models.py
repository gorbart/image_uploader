from django.db import models
from django.utils import timezone

from users.models import ApiUser


def upload_to(instance, filename):
    return '{user_id}/{year}/{month}/{day}/{filename}'.format(user_id=instance.owner_id, year=instance.upload_date.year,
                                                              month=instance.upload_date.month,
                                                              day=instance.upload_date.day, filename=filename)


class Image(models.Model):
    name = models.CharField(max_length=50)
    upload_date = models.DateTimeField(default=timezone.now())
    owner = models.ForeignKey(ApiUser, on_delete=models.CASCADE)

    image = models.ImageField(upload_to=upload_to, max_length=255)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return f'user {self.owner_id}-{self.name}'
