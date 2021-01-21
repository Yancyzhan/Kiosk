from rest_framework import serializers
from Subsystem.models import RecordModel

class RecordModelSerializer(serializers.ModelSerializer):
    imageUrl = serializers.CharField(read_only=True, source="image.image.url")

    class Meta:
         model = RecordModel
         fields = ['created','user','image', 'biometricSystem', 'result', 'processTime', 'imageUrl', 'isAccepted']