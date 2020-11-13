from django.db import models

from account.models import User


class Doc(models.Model):
    upload = models.FileField(upload_to='images')
    author = models.ManyToManyField(User)

    def __str__(self):
        return str(self.pk)