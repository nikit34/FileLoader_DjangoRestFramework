from django.db import models

class Doc(models.Model):
    upload = models.ImageField(upload_to='images/')

    def __str__(self):
        return str(self.pk)