from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.contrib import auth
from .models import *
# from user.models import *
from datetime import date,datetime
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def friend_send(request): # 送出控糖團邀請!
    uid = request.user.id
    uid = 123
    if request.method == 'POST':
        nowtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(request.body)
        data = str(request.body).replace('b','').replace("\\r\\n",'').replace('\'','')
        print(data)
        data = json.loads(data)
        friend_type = data['type']
        invite_code = data['invite_code']
        try:
            user_friend = Friend.objects.get(invite_code=invite_code)
            friend_uid = user_friend.uid
        except:
            output = {"status":"1"} # 1: 邀請碼無效
        else:
            try:
                Friend_data.objects.get(uid=uid, relation_id=friend_uid)
            except:
                try:
                    Friend_data.objects.create(uid=uid, relation_id=friend_uid, status=0, friend_type=friend_type, updated_at=nowtime)
                except:
                    output = {"status":"1"}
                else:
                    output = {"status":"0"}
            else:
                output = {"status":"2"} # 2: 已經成為好友
        return JsonResponse(output,safe=False)
