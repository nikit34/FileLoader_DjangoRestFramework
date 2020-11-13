from django.db import models
from account.models import Account


class Doc(models.Model):
    upload = models.FileField(upload_to='images')
    author = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.pk)