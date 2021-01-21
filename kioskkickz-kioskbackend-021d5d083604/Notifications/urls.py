from django.urls import path
from django.conf.urls import include, url 
from Notifications import views
from rest_framework import routers 

router = routers.DefaultRouter()
router.register('notifications', views.NotificationViewSet,'notifications')

urlpatterns = [
    url(r'api/', include(router.urls)),
    url(r'notificationView/', views.goToNotifications),
]