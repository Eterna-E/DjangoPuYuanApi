from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib import auth
from .models import *
# from user.models import *
from datetime import date, datetime
from django.views.decorators.csrf import csrf_exempt
import json
from Denru.models import patient
from measure.models import *
from django.contrib.sessions.models import Session
import json


@csrf_exempt
def friend_code(request):  # 16.獲取控糖團邀請碼
    session_key = request.headers.get('Authorization')[
        7:]  # 從header抓出session key
    authuser = Session.objects.get(session_key=session_key).get_decoded()[
        '_auth_user_id']  # 把跟session key合的user授權抓出來解碼，取得user id
    uid = authuser
    try:
        user_friend = Friend.objects.get(uid=uid)
    except:
        output = {"status": "1"}
    else:
        output = {"status": "0", "invite_code": user_friend.invite_code}
    return JsonResponse(output, safe=False)


@csrf_exempt
def friend_list(request):  # 17.控糖團列表
    session_key = request.headers.get('Authorization')[
        7:]  # 從header抓出session key
    authuser = Session.objects.get(session_key=session_key).get_decoded()[
        '_auth_user_id']  # 把跟session key合的user授權抓出來解碼，取得user id
    uid = authuser
    if request.method == 'GET':
        if Friend_data.objects.filter(uid=uid, status=1):
            friends = []
            friends_list = Friend_data.objects.filter(uid=uid, status=1)
            print(friend_list)
            for friend in friends_list:
                print(friend.relation_id)
                user_pro = patient.objects.get(id=uid)
                relation = patient.objects.get(id=uid)
                # user_pro = patient.objects.get(id=friend.relation_id)
                # relation = patient.objects.get(id=user_pro.uid)
                r = {
                    "id": user_pro.id,
                    "name": relation.name,
                    "account": relation.email,
                    "email": relation.email,
                    "phone": relation.phone,
                    "fb_id": "null",
                    "status": relation.status,
                    "group": relation.group,
                    "birthday": str(relation.birthday),
                    "height": relation.height,
                    "gender": relation.gender,
                    "verified": 1,
                    "privacy_policy": relation.privacy_policy,
                    "must_change_password": relation.must_change_password,
                    "badge": relation.badge,
                    "created_at": "2017-10-23 14:39:06",
                    "updated_at": "2017-10-23 14:39:06",
                    "relation_type": friend.friend_type
                }
                friends.append(r)
            output = {"status": "0", "friends": friends}
        else:
            output = {"status": "1"}
    return JsonResponse(output)


@csrf_exempt
def friend_requests(request):  # 18.獲取控糖團邀請
    session_key = request.headers.get('Authorization')[
        7:]  # 從header抓出session key
    authuser = Session.objects.get(session_key=session_key).get_decoded()[
        '_auth_user_id']  # 把跟session key合的user授權抓出來解碼，取得user id
    uid = authuser
    try:
        requests_list = Friend_data.objects.filter(relation_id=uid, status=0)
    except:
        output = {"status": "1"}
    else:
        requests = []
        for request in requests_list:
            user = patient.objects.get(id=2)
            created_at_friendata = datetime.strftime(
                request.created_at, '%Y-%m-%d %H:%M:%S')
            updated_at_friendata = datetime.strftime(
                request.updated_at, '%Y-%m-%d %H:%M:%S')
            r = {
                "id": request.id,
                "user_id": request.uid,
                "relation_id": request.relation_id,
                "type": request.friend_type,
                "status": request.status,
                "created_at": created_at_friendata,
                "updated_at": updated_at_friendata,
                "user": {
                    "id": user.id,
                    "name": user.name,
                    "account": user.email,
                    "email": user.email,
                    "phone": user.phone,
                    "fb_id": "null",
                    "status": user.status,
                    "group": user.group,
                    "birthday": str(user.birthday),
                    "height": user.height,
                    "gender": user.gender,
                    "verified": user.email_verfied,
                    "privacy_policy": user.privacy_policy,
                    "must_change_password": user.must_change_password,
                    "badge": user.badge,
                    "created_at": "2017-10-20 15:43:47",
                    "updated_at": "2017-10-20 15:43:54"
                }
            }
            requests.append(r)
        output = {"status": "0", "requests": requests}
    return JsonResponse(output)


@csrf_exempt
def friend_send(request):  # 19.送出控糖團邀請
    session_key = request.headers.get('Authorization')[
        7:]  # 從header抓出session key
    authuser = Session.objects.get(session_key=session_key).get_decoded()[
        '_auth_user_id']  # 把跟session key合的user授權抓出來解碼，取得user id
    uid = authuser
    if request.method == 'POST':
        nowtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(request.body)
        data = str(request.body).replace('b', '').replace(
            "\\r\\n", '').replace('\'', '')
        print(data)
        data = data.split('&')
        print(data)
        friend_type = data[1].replace('type=', '')
        invite_code = int(data[0].replace('invite_code=', ''))
        # data = json.loads(data)
        # friend_type = data['type']
        # invite_code = data['invite_code']
        # print(friend_type)
        # print(invite_code)
        try:
            user_friend = Friend.objects.get(invite_code=invite_code)
            friend_uid = user_friend.uid
        except:
            output = {"status": "1"}  # 1: 邀請碼無效
            print(123)
        else:
            try:
                Friend_data.objects.get(uid=uid, relation_id=friend_uid)
            except:
                try:
                    Friend_data.objects.create(
                        uid=uid, relation_id=friend_uid, status=0, friend_type=friend_type, updated_at=nowtime)
                except:
                    output = {"status": "1"}
                else:
                    output = {"status": "0"}
            else:
                output = {"status": "2"}  # 2: 已經成為好友
        return JsonResponse(output, safe=False)


@csrf_exempt
def friend_accept(request, friend_data_id):  # 20.接受控糖團邀請
    session_key = request.headers.get('Authorization')[
        7:]  # 從header抓出session key
    authuser = Session.objects.get(session_key=session_key).get_decoded()[
        '_auth_user_id']  # 把跟session key合的user授權抓出來解碼，取得user id
    uid = authuser
    nowtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(1234)
    try:
        check = Friend_data.objects.get(id=friend_data_id, status=0)
        Friend_data.objects.create(uid=uid, relation_id=check.uid, status=1, read=True,
                                   imread=True, friend_type=check.friend_type, updated_at=nowtime)
        check.read = True
        check.status = 1
        check.updated_at = nowtime
        check.save()
    except:
        output = {"status": "1"}
    else:
        output = {"status": "0"}
    return JsonResponse(output, safe=False)


@csrf_exempt
def friend_refuse(request, friend_data_id):  # 21.拒絕控糖團邀請
    # uid = request.user.id
    nowtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        check = Friend_data.objects.get(id=friend_data_id, status=0)
        check.read = True
        check.status = 2
        check.updated_at = nowtime
        check.save()
    except:
        output = {"status": "1"}
    else:
        output = {"status": "0"}
    return JsonResponse(output, safe=False)


@csrf_exempt
def friend_remove(request, friend_data_id):  # 22.刪除控糖團邀請
    # uid = request.user.id
    if request.method == 'GET':
        try:
            Friend_data.objects.filter(id=friend_data_id, status=0).delete()
        except:
            output = {"status": "1"}
        else:
            output = {"status": "0"}
        return JsonResponse(output, safe=False)


@csrf_exempt
def friend_results(request):  # 26.控糖團結果
    session_key = request.headers.get('Authorization')[
        7:]  # 從header抓出session key
    authuser = Session.objects.get(session_key=session_key).get_decoded()[
        '_auth_user_id']  # 把跟session key合的user授權抓出來解碼，取得user id
    uid = authuser
    if request.method == 'GET':
        if Friend_data.objects.filter(uid=uid, read=True, imread=False):
            results = []
            result = Friend_data.objects.filter(
                uid=uid, read=True, imread=False).latest('updated_at')
            user_pro = patient.objects.get(id=result.relation_id)
            relation = patient.objects.get(id=user_pro.id)
            created_at_friendata = datetime.strftime(
                result.created_at, '%Y-%m-%d %H:%M:%S')
            updated_at_friendata = datetime.strftime(
                result.updated_at, '%Y-%m-%d %H:%M:%S')
            created_at_userfile = datetime.strftime(
                relation.created_at, '%Y-%m-%d %H:%M:%S')
            updated_at_userfile = datetime.strftime(
                relation.updated_at, '%Y-%m-%d %H:%M:%S')
            print(results)
            r = {
                "id": result.id,
                "user_id": result.uid,
                "relation_id": result.relation_id,
                "type": result.friend_type,
                "status": int(result.status),
                "read": result.read,
                "created_at": created_at_friendata,
                "updated_at": updated_at_friendata,
                "relation":
                {
                    "id": user_pro.id,
                    "name": relation.name,
                    "account": relation.email,
                    "email": relation.email,
                    "phone": relation.phone,
                    "fb_id": "null",
                    "status": relation.status,
                    "group": relation.group,
                    "birthday": str(relation.birthday),
                    "height": relation.height,
                    "gender": relation.gender,
                    "verified": relation.email_verfied,
                    "privacy_policy": relation.privacy_policy,
                    "must_change_password": relation.must_change_password,
                    "badge": relation.badge,
                    "created_at": created_at_userfile,
                    "updated_at": updated_at_userfile
                }
            }
            result.imread = True
            result.save()
            results.append(r)
            output = {"status": "0", "results": results}
        else:
            output = {"status": "1"}
    return JsonResponse(output)


@csrf_exempt
def friend_remove_more(request):  # 37.刪除更多好友
    session_key = request.headers.get('Authorization')[
        7:]  # 從header抓出session key
    authuser = Session.objects.get(session_key=session_key).get_decoded()[
        '_auth_user_id']  # 把跟session key合的user授權抓出來解碼，取得user id
    uid = authuser
    if request.method == 'DELETE':
        ids_list = request.GET.getlist("ids[]")
        try:
            for ids in ids_list:
                try:
                    Friend_data.objects.get(
                        uid=ids, relation_id=uid, status=1).delete()
                except:
                    pass
                try:
                    Friend_data.objects.get(
                        uid=uid, relation_id=ids, status=1).delete()
                except:
                    pass
        except:
            output = {"status": "0"}
        else:
            output = {"status": "0"}
    else:
        output = {"status": "1"}
    return JsonResponse(output)


@csrf_exempt
def notification(request):  # 36.親友團通知
    session_key = request.headers.get('Authorization')[
        7:]  # 從header抓出session key
    authuser = Session.objects.get(session_key=session_key).get_decoded()[
        '_auth_user_id']  # 把跟session key合的user授權抓出來解碼，取得user id
    uid = authuser
    if request.method == 'POST':
        nowtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(request.body)
        data = str(request.body, encoding="utf-8").replace('b',
                                                           '').replace("\\r\\n", '').replace('\'', '')
        print(data)
        data = json.loads(data)
        message = data['message']
        try:
            friend_list = Friend_data.objects.filter(
                uid=uid, friend_type=0, status=1)
            for friend in friend_list:
                Notification.objects.create(
                    uid=uid, member_id=1, reply_id=friend.relation_id, message=message, updated_at=nowtime)
        except:
            output = {"status": "1"}
        else:
            output = {"status": "0"}
        return JsonResponse(output, safe=False)


@csrf_exempt
def share(request):  # 23.分享
    session_key = request.headers.get('Authorization')[
        7:]  # 從header抓出session key
    authuser = Session.objects.get(session_key=session_key).get_decoded()[
        '_auth_user_id']  # 把跟session key合的user授權抓出來解碼，取得user id
    uid = authuser
    if request.method == 'POST':
        output = {"status": "1"}
        try:
            print(request.body)
            data = str(request.body).replace('b', '').replace(
                "\\r\\n", '').replace('\'', '')
            print(data)
            data = data.split('&')
            print(data)
            share_id = data[0].replace('id=', '')
            data_type = data[2].replace('type=', '')
            relation_type = data[1].replace('relation_type=', '')
            print(share_id, data_type, relation_type)
            # data = str(request.body, encoding="utf-8").replace('b','').replace("\\r\\n",'').replace('\'','')
            # print(data)
            # data = json.loads(data)
            # share_id = data['id']
            # data_type = data['type']
            # relation_type = data['relation_type']
            try:
                Share.objects.create(
                    uid=uid, fid=share_id, data_type=data_type, relation_type=relation_type)
            except:
                output = {"status": "1"}
            else:
                output = {"status": "0"}
            # output = {"status": "0"}
        except:
            pass
        return JsonResponse(output, safe=False)


@csrf_exempt
def share_check(request, relation_type):  # 24.查看分享（含自己分享出去的）
    session_key = request.headers.get('Authorization')[
        7:]  # 從header抓出session key
    authuser = Session.objects.get(session_key=session_key).get_decoded()[
        '_auth_user_id']  # 把跟session key合的user授權抓出來解碼，取得user id
    uid = authuser
    print('relation_type:', relation_type)
    if request.method == 'GET':
        if Share.objects.filter(relation_type=relation_type):
            share_checks = Share.objects.filter(relation_type=relation_type)
            datas = []
            for share_check in share_checks:
                print(share_check.uid)
                print('data type:', share_check.data_type)
                user = patient.objects.get(id=uid)
                r = None
                if share_check.data_type == '0':
                    share_data = Pressure.objects.get(
                        uid=share_check.uid, id=share_check.fid)
                    created_at = datetime.strftime(
                        share_data.created_at, '%Y-%m-%d %H:%M:%S')
                    recorded_at = datetime.strftime(
                        share_data.recorded_at, '%Y-%m-%d %H:%M:%S')
                    created_at_userfile = datetime.strftime(
                        user.created_at, '%Y-%m-%d %H:%M:%S')
                    updated_at_userfile = datetime.strftime(
                        user.updated_at, '%Y-%m-%d %H:%M:%S')
                    r = {
                        "id": share_data.id,
                        "user_id": share_data.uid,
                        "systolic": share_data.systolic,
                        "diastolic": share_data.diastolic,
                        "pulse": share_data.pulse,
                        "recorded_at": recorded_at,
                        "created_at": created_at,
                        "type": 0,
                        "user": {
                            "id": user.id,
                            "name": user.name,
                            "account": user.email,
                            "email": user.email,
                            "phone": user.phone,
                            "fb_id": None,
                            "status": user.status,
                            "group": user.group,
                            "birthday": user.birthday.strftime('%Y-%m-%d'),
                            "height": user.height,
                            "gender": user.gender,
                            "verified": user.email_verfied,
                            "privacy_policy": user.privacy_policy,
                            "must_change_password": user.must_change_password,
                            "badge": user.badge,
                            "created_at": created_at_userfile,
                            "updated_at": updated_at_userfile
                        }
                    }
                if share_check.data_type == '1':
                    try:
                        share_data = Weight.objects.get(
                            uid=share_check.uid, id=share_check.fid)
                        created_at = datetime.strftime(
                            share_data.created_at, '%Y-%m-%d %H:%M:%S')
                        recorded_at = datetime.strftime(
                            share_data.recorded_at, '%Y-%m-%d %H:%M:%S')
                        created_at_userfile = datetime.strftime(
                            user.created_at, '%Y-%m-%d %H:%M:%S')
                        updated_at_userfile = datetime.strftime(
                            user.updated_at, '%Y-%m-%d %H:%M:%S')
                        r = {
                            "id": share_data.id,
                            "user_id": share_data.uid,
                            "weight": float(share_data.weight),
                            "body_fat": float(share_data.body_fat),
                            "bmi": float(share_data.bmi),
                            "recorded_at": recorded_at,
                            "created_at": created_at,
                            "type": 1,
                            "user": {
                                "id": user.id,
                                "name": user.name,
                                "account": user.email,
                                "email": user.email,
                                "phone": user.phone,
                                "fb_id": None,
                                "status": user.status,
                                "group": user.group,
                                "birthday": user.birthday.strftime('%Y-%m-%d'),
                                "height": user.height,
                                "gender": user.gender,
                                "verified": user.email_verfied,
                                "privacy_policy": user.privacy_policy,
                                "must_change_password": user.must_change_password,
                                "badge": user.badge,
                                "created_at": created_at_userfile,
                                "updated_at": updated_at_userfile
                            }
                        }
                    except:
                        r = None
                if share_check.data_type == '2':
                    share_data = Sugar.objects.get(
                        uid=share_check.uid, id=share_check.fid)
                    created_at = datetime.strftime(
                        share_data.created_at, '%Y-%m-%d %H:%M:%S')
                    recorded_at = datetime.strftime(
                        share_data.recorded_at, '%Y-%m-%d %H:%M:%S')
                    created_at_userfile = datetime.strftime(
                        user.created_at, '%Y-%m-%d %H:%M:%S')
                    updated_at_userfile = datetime.strftime(
                        user.updated_at, '%Y-%m-%d %H:%M:%S')
                    r = {
                        "id": share_data.id,
                        "user_id": share_data.uid,
                        "sugar": float(share_data.sugar),
                        "timeperiod": int(share_data.timeperiod),
                        "recorded_at": recorded_at,
                        "created_at": created_at,
                        "type": 2,
                        "user": {
                            "id": user.id,
                            "name": user.name,
                            "account": user.email,
                            "email": user.email,
                            "phone": user.phone,
                            "fb_id": None,
                            "status": user.status,
                            "group": user.group,
                            "birthday": user.birthday.strftime('%Y-%m-%d') if user.birthday.strftime('%Y-%m-%d') else None,
                            "height": user.height,
                            "gender": user.gender,
                            "verified": user.email_verfied,
                            "privacy_policy": user.privacy_policy,
                            "must_change_password": user.must_change_password,
                            "badge": user.badge,
                            "created_at": created_at_userfile,
                            "updated_at": updated_at_userfile
                        }
                    }
                if share_check.data_type == '3':
                    share_data = Diary_diet.objects.get(
                        uid=share_check.uid, id=share_check.fid)
                    created_at = datetime.strftime(
                        share_data.created_at, '%Y-%m-%d %H:%M:%S')
                    recorded_at = datetime.strftime(
                        share_data.recorded_at, '%Y-%m-%d %H:%M:%S')
                    created_at_userfile = datetime.strftime(
                        user.created_at, '%Y-%m-%d %H:%M:%S')
                    updated_at_userfile = datetime.strftime(
                        user.updated_at, '%Y-%m-%d %H:%M:%S')
                    image_count = str(share_data.image_count)
                    r = {
                        "id": share_data.id,
                        "user_id": share_data.uid,
                        "description": share_data.description,
                        "meal": int(share_data.meal),
                        "tag": share_data.tag,
                        # "image":str(image),
                        "image_count": share_data.image_count,
                        "lat": share_data.lat,
                        "lng": share_data.lng,
                        "recorded_at": recorded_at,
                        "created_at": created_at,
                        "type": 3,
                        "user": {
                            "id": user.id,
                            "name": user.name,
                            "account": user.email,
                            "email": user.email,
                            "phone": user.phone,
                            "fb_id": None,
                            "status": user.status,
                            "group": user.group,
                            "birthday": user.birthday.strftime('%Y-%m-%d'),
                            "height": user.height,
                            "gender": user.gender,
                            "verified": user.email_verfied,
                            "privacy_policy": user.privacy_policy,
                            "must_change_password": user.must_change_password,
                            "badge": user.badge,
                            "created_at": created_at_userfile,
                            "updated_at": updated_at_userfile
                        }
                    }
                if r != None:
                    datas.append(r)
            output = {"status": "0", "records": datas}
            print(output)
        else:
            output = {"status": "1"}
        output = {"status": "0"}
        return JsonResponse(output)
