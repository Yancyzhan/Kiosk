from django.urls import path
from django.conf.urls import include, url 
from Subsystem import views

urlpatterns = [
    # url(r'biometrics/(?P<bioId>[0-9]+)/(?P<userId>[0-9]+)/$', views.biometrics)
    url(r'api/biometrics/(?P<bioId>[0-9]+)/(?P<userId>[0-9]+)/$', views.connectSystem),
    url(r'api/biometricsInit/(?P<bioId>[0-9]+)/$', views.initSystem),
    url(r'api/biometricsStop/(?P<bioId>[0-9]+)/$', views.stopSystem),
    url(r'subsystemAddEdit/(?P<bioId>[0-9]+)/$', views.bioSystemAddEdit),
    url(r'subsystemDelete/(?P<bioId>[0-9]+)/$', views.bioSystemDelete),
    path('', views.openSubsystemAdmin),
    path('downloadTemplate/', views.downloadTemplate),
    path('log/<str:bioId>/', views.openSubsystemLog)
]