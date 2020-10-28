from django.urls import path
from .views import *


urlpatterns = [
    path('send/', friend_send), #可
    path('code/', friend_code), #可
    path('list/', friend_list), #可，未合併
    path('requests/', friend_requests), #可，未合併
    path('<int:friend_data_id>/accept/', friend_accept), #可
    path('<int:friend_data_id>/refuse/', friend_refuse), #可
    path('<int:friend_data_id>/remove/', friend_remove), #可
    path('results/', friend_results), #可
    path('remove/', friend_remove_more), #可

]