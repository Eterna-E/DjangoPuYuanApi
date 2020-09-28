from django.urls import path
from .views import *


urlpatterns = [
    path('',index),
    path('user/blood/pressure/', pressure_create_view), #可
    path('user/weight/', weight_create_view),#可
    path('user/blood/sugar/', sugar_create_view),#可
    path('user/diet/', diary_diet_create_view),#可
]