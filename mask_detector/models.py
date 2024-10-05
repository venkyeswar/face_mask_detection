from django.db import models

class MaskImage(models.Model):
    image = models.ImageField(upload_to='images/')
    label = models.CharField(max_length=100)
    confidence = models.FloatField()

    def __str__(self):
        return self.label
