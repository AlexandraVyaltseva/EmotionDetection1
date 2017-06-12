from django.db import models
from jsonfield import JSONField

class Image(models.Model):
    image = models.ImageField()

    def __str__(self):
        return str(self.id)

class SubImage(models.Model):
    image = models.ForeignKey(Image, on_delete=models.CASCADE)
    sub_image = models.ImageField()
    scores = JSONField()

    def __str__(self):
        return str(self.image.pk) +'-'+ self.sub_image.name