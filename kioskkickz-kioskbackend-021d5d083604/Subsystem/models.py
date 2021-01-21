from django.db import models
from django.forms import ModelForm
from django.utils import timezone
from API.models import ImageModel
from django.contrib.auth.models import User

# Create your models here.

class BiometricSystemModel(models.Model):
    # file will be uploaded to MEDIA_ROOT/biometricSystem
    created = models.DateTimeField(default = timezone.now)
    name = models.CharField(max_length=100, blank=True, default='')
    script = models.FileField(upload_to='biometricSystem/scripts/')
    machineLModel = models.FileField(upload_to='biometricSystem/models/',null=True, blank=True)
    needName = models.BooleanField(default=True)
    needImage = models.BooleanField(default=True)
    portNum = models.IntegerField(null=True)
    isStarted = models.BooleanField(default=False)

    def __str__(self):
    	return str(self.name)

    class Meta:
        verbose_name = 'Biometric System'
        verbose_name_plural = 'Biometric Systems'

class RecordModel(models.Model):
    created = models.DateTimeField(default = timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1, null=True)
    image = models.ForeignKey(ImageModel, on_delete=models.CASCADE)
    biometricSystem = models.ForeignKey(BiometricSystemModel, on_delete=models.CASCADE)
    result = models.CharField(max_length=255, blank=True, default='')
    processTime = models.FloatField(default=0)
    isAccepted = models.BooleanField(default=True)

    def __str__(self):
    	return str(self.created)

    class Meta:
        verbose_name = 'Record'
        verbose_name_plural = 'Records'

class BioSystemForm(ModelForm):
    class Meta:
        model = BiometricSystemModel
        fields = ['name','script','machineLModel','needName', 'needImage', 'portNum']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})
