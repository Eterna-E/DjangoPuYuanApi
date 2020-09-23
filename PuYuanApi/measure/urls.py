from django.urls import path
from . import views


urlpatterns = [
    path('',views.index),
    path('pressure/',views.pressure_create_view),
]