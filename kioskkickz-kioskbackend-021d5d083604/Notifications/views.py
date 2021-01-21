from django.shortcuts import render
from rest_framework import permissions, viewsets, generics
from rest_framework.decorators import permission_classes

from .models import Notification
from.serializers import NotificationSerializer

import datetime

def goToNotifications(request):
    return render(request, 'notification.html')

@permission_classes((permissions.IsAuthenticated,))
class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()

    def get_queryset(self): 
        queryset = self.queryset
        query_set=queryset.filter(user=self.request.user)
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        if start_date and end_date:
            start_date_datetime = datetime.datetime.strptime(start_date, "%Y/%m/%d")
            end_date_datetime = datetime.datetime.strptime(end_date, "%Y/%m/%d") + datetime.timedelta(days=1)
            query_set = query_set.filter(created_at__range=(start_date_datetime, end_date_datetime))
        return query_set
