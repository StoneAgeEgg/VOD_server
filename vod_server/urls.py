"""vod_server URL Configuration

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
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include

from . import views
from . import videostream
import apps.OD_data.urls as OD_data_urls

admin.site.site_title = '管理后台'
admin.site.site_header = '目标检测管理后台'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/data/', include(OD_data_urls)),
    path('', views.MainPage),
    path('monitor/', videostream.streamhr),
    path('comfirmName/', videostream.tellName),
    path('picsave/', videostream.savingpic),
    url(r'^uploadFiles/', views.upload),
    url(r'^getFileName/', views.GetFileName),
    path('default', views.DefaultPage),
]
