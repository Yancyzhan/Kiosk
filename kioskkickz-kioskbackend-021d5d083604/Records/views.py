from django.core.paginator import Paginator
from django.shortcuts import render
from rest_framework import permissions, viewsets, generics
from rest_framework.decorators import permission_classes
from Subsystem.models import RecordModel
from.serializers import RecordModelSerializer

import datetime

def listing(request):
    records_list = RecordModel.objects.all()
    paginator = Paginator(records_list, 1) # Show 1 record per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'records.html', {'page_obj': page_obj})
    
@permission_classes((permissions.IsAuthenticated,))
class RecordModelViewSet(viewsets.ModelViewSet):
    serializer_class = RecordModelSerializer
    queryset = RecordModel.objects.all()

    def get_queryset(self): 
        queryset = self.queryset
        query_set=queryset.filter(user=self.request.user)
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        if start_date and end_date:
            start_date_datetime = datetime.datetime.strptime(start_date, "%Y/%m/%d")
            end_date_datetime = datetime.datetime.strptime(end_date, "%Y/%m/%d") + datetime.timedelta(days=1)
            query_set = query_set.filter(created__range=(start_date_datetime, end_date_datetime))
        return query_set