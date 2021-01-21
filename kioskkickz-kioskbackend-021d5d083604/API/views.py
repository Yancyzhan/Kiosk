from rest_framework import permissions, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import ImageSerializer

from .models import ImageModel

         

def HelloWorld(r):
	print('Hello World!')
	return HttpResponse("Hello World!")

# Image rest apis are not used any more. 
# they are only used for testing at the very beginning
@permission_classes((permissions.IsAuthenticated,))
class imageUploadView(viewsets.ModelViewSet):
	queryset = ImageModel.objects.all()
	serializer_class = ImageSerializer
		