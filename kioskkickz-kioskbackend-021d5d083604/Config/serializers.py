from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Config,UseType
from Subsystem.models import BiometricSystemModel


class ConfigSerializer(serializers.HyperlinkedModelSerializer):
    userId = serializers.IntegerField(read_only=True, source="user.id")
    userName = serializers.CharField(read_only=True, source="user.username")
    useType = serializers.CharField(read_only=True, source="useType.name")
    biometricSystem = serializers.IntegerField(read_only=True, source="biometricSystem.id")
    needImage = serializers.BooleanField(read_only=True, source="biometricSystem.needImage")
    needName = serializers.BooleanField(read_only=True, source="biometricSystem.needName")

    class Meta:
        model = Config
        fields = ['userId', 'userName','useType','biometricSystem','needImage', 'needName', 'maxTrialTime', 'headerTitle']
