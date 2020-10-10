from django.urls import path
from .views import *


urlpatterns = [
    path('send/', friend_send), #可
    path('code/', friend_code), #可
    path('list/', friend_list), #可，未合併
    path('requests/', friend_requests), #可，未合併
]