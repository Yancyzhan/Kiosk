from django.urls import path
from django.conf.urls import include, url 
from Records import views
from rest_framework import routers 
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required


router = routers.DefaultRouter()
router.register('records', views.RecordModelViewSet,'records')

urlpatterns = [
    path('', login_required(TemplateView.as_view(template_name='records.html'))),
    url(r'api/', include(router.urls)),
]