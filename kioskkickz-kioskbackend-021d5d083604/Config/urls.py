from django.urls import path
from django.conf.urls import include, url 
from Config import views
from rest_framework import routers 

router = routers.DefaultRouter()
router.register('configs', views.ConfigViewSet,'configs')

urlpatterns = [
    url(r'api/', include(router.urls)),
    url(r'configAddEdit/', views.changeconfig),
]