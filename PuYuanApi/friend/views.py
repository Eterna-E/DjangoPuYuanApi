from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.contrib import auth
from .models import *
# from user.models import *
from datetime import date,datetime
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def friend_code(request): # 16.獲取控糖團邀請碼
    uid = request.user.id
    uid = 123
    try:
        user_friend = Friend.objects.get(uid=uid)
    except:
        output = {"status":"1"}
    else:
        output = {"status":"0", "invite_code":user_friend.invite_code}
    return JsonResponse(output,safe=False)

@csrf_exempt
def friend_list(request): # 17.控糖團列表
    uid = request.user.id
    uid = 123
    if request.method == 'GET':
        if Friend_data.objects.filter(uid=uid, status=0):
            friends = []
            friends_list = Friend_data.objects.filter(uid=uid, status=0)
            for friend in friends_list:
                r = {
                        "id": 2,
                        "name": "QQ",
                        "account": "fb_1",
                        "email": "null",
                        "phone": "null",
                        "fb_id": "1",
                        "status": "Normal",
                        "group": "null",
                        "birthday": "1995-10-10",
                        "height": 171,
                        "gender": "男",
                        "verified": 1,
                        "privacy_policy": 1,
                        "must_change_password": 0,
                        "badge": 87,
                        "created_at": "2017-10-23 14:39:06",
                        "updated_at": "2017-10-23 19:41:53",
                        "relation_type": 1
                }
                friends.append(r)
            output = {"status":"0", "friends":friends}
        else:
            output = {"status":"1"}
    return JsonResponse(output)

@csrf_exempt
def friend_requests(request): # 18.獲取控糖團邀請
    uid = request.user.id
    uid = 123
    try:
        requests_list = Friend_data.objects.filter(relation_id=uid, status=0)
    except:
        output = {"status":"1"}
    else:
        requests = []
        for request in requests_list:
            created_at_friendata = datetime.strftime(request.created_at, '%Y-%m-%d %H:%M:%S')
            updated_at_friendata = datetime.strftime(request.updated_at, '%Y-%m-%d %H:%M:%S')
            r = {
                "id":request.id,
                "user_id":request.uid,
                "relation_id":request.relation_id,
                "type":request.friend_type,
                "status":request.status,
                "created_at":created_at_friendata,
                "updated_at":updated_at_friendata,
                "user":{
                            "id": 2,
                            "name": "null",
                            "account": "fb_2",
                            "email": "null",
                            "phone": "null",
                            "fb_id": "2",
                            "status": "Normal",
                            "group": "null",
                            "birthday": "null",
                            "height": "null",
                            "gender": "null",
                            "verified": 1,
                            "privacy_policy": 1,
                            "must_change_password": 0,
                            "badge": 87,
                            "created_at": "2017-10-20 15:43:47",
                            "updated_at": "2017-10-20 15:43:54"
                        }
                    }
            requests.append(r)
        output = {"status":"0", "requests":requests}
    return JsonResponse(output)

@csrf_exempt
def friend_send(request): # 19.送出控糖團邀請
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
