"""kioskBackend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.http import (
    FileResponse, Http404, HttpResponse, HttpResponseNotModified,
)
from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from django.conf.urls import include, url 
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.views.static import serve
from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test

# @user_passes_test(lambda u: u.is_superuser)



@login_required
def protected_serve(request, path, document_root=None, show_indexes=False):
    if 'img/' in path or request.user.is_superuser:
        return serve(request, path, document_root, show_indexes)
    else:
        return HttpResponse("403 : You can't access this file!")

urlpatterns = [
    url(r'^%s(?P<path>.*)$' % settings.MEDIA_URL[1:], protected_serve, {'document_root': settings.MEDIA_ROOT}),
	path('api/', include('API.urls')),
    path('admin/', admin.site.urls),
    path('subsystem/', include('Subsystem.urls')),
    path('config/', include('Config.urls')),
    path('notifications/', include('Notifications.urls')),
    path('records/', include('Records.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', login_required(TemplateView.as_view(template_name='home.html')), name='home')
] 
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


