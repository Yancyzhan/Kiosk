from django.db import models
from django.forms import ModelForm
from django.utils import timezone
from API.models import ImageModel
from Subsystem.models import BiometricSystemModel
from django.contrib.auth.models import User

# Create your models here.
class UseType(models.Model):
    name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.name

class Config(models.Model):
    headerTitle = models.CharField(max_length=255, default='Biometric Kiosk', null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1, primary_key=True)
    useType = models.ForeignKey(UseType, on_delete=models.CASCADE)
    biometricSystem = models.ForeignKey(BiometricSystemModel, on_delete=models.CASCADE)
    maxTrialTime = models.IntegerField()

class HomePageImage(models.Model):
    image = models.ForeignKey(ImageModel, on_delete=models.CASCADE, db_constraint=False)
    config = models.ForeignKey(Config, on_delete=models.CASCADE, db_constraint=False)
    
class ConfigForm(ModelForm):
    class Meta:
        model = Config
        fields = ['headerTitle','useType','biometricSystem','maxTrialTime']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control'})