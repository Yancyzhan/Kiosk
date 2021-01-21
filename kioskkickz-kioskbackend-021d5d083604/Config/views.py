from django.forms.models import model_to_dict
from django.shortcuts import render
from rest_framework import permissions, viewsets, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Config
from .models import ConfigForm
from.serializers import ConfigSerializer

from django.shortcuts import get_object_or_404

# Create your views here.
def changeconfig(request):
    message = ''
    if request.method == "POST":
        try:
            instance = Config.objects.get(user_id=request.user)
        except Config.DoesNotExist:
            instance = None
        form = ConfigForm(request.POST, instance=instance)
        if form.is_valid():
            config = form.save(commit=False)
            config.user = request.user
            config.save()
            message = 'The config is saved successfully!'
    else:
        try:
            config = Config.objects.get(user_id=request.user)
        except Config.DoesNotExist:
            config = Config(user_id=request.user)
        form = ConfigForm(initial=model_to_dict(config))
    
    return render(request, 'config.html', {'form': form, 'message': message})
    
class ConfigViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows configurations to be viewed
    """
    queryset = Config.objects.all()
    serializer_class = ConfigSerializer
    

