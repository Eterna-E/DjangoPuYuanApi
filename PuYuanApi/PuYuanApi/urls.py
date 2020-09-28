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

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('api/user/blood/pressure/', pressure_create_view),
    # path('api/user/weight/', weight_create_view),
    # path('api/user/blood/sugar/', sugar_create_view),
    path('api/', include('measure.urls')),
    path('api/user/diet/', sugar_create_view),
    path('', RedirectView.as_view(url='/halo/')),
    path('halo/',index),
]
#api/user/records