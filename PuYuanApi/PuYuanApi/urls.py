"""PuYuanApi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf.urls import include
from django.views.generic import RedirectView
from measure.views import pressure_create_view,index,weight_create_view,sugar_create_view
from Denru.views import *
from info.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('measure.urls')),
    path('', RedirectView.as_view(url='/halo/')),
    path('halo/',index),
    path('api/friend/',include('friend.urls')),

    #Denru
    path('api/register/check/', RegCheck), #可
    path('api/user/privacy-policy/', pp), #可
    path('api/register/', Reg), #可
    path('api/auth/', login), #可
    path('api/verification/send/', sendcode), #可
    path('api/verification/check/', codechecking), #可
    path('api/password/forgot/', forget), #可
    path('api/password/reset/', reset), #可
    #info
    path('api/user/', information), #可
    path('api/user/default/', individualdefault), #可
    # path('api/user/a1c', a1c),
]
