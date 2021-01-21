from django.urls import path
from django.conf.urls import include, url 
from API import views
from rest_framework import routers 
router = routers.DefaultRouter()
router.register('image', views.imageUploadView, 'image')

urlpatterns = [
    url(r'^', include(router.urls)),
    url(r'hello', views.HelloWorld)
]