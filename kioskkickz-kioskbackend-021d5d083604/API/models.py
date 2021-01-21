from django.db import models
from django.utils import timezone

class ImageModel(models.Model):
    # file will be uploaded to MEDIA_ROOT/img
    created = models.DateTimeField(default = timezone.now)
    title = models.CharField(max_length=100, blank=True, default='')
    image = models.FileField(upload_to='img/')

    def __str__(self):
    	return str(self.title)