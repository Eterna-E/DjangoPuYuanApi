from django.shortcuts import render
# from .forms import PressureForm,WeightForm,SugarForm
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from datetime import date,datetime
import json
from .models import Pressure,Weight,Sugar,Diary_diet,UserCare
from friend.models import Friend_data
from django.contrib.sessions.models import Session

# Create your views here.
def index(request):
    return render(request,'hello.html',{
        'data': "Hello Django ",
    })

@csrf_exempt
def pressure_create_view(request): # 8.上傳血壓測量結果
    session_key = request.headers.get('Authorization')[7:]#從header抓出session key
    authuser = Session.objects.get(session_key=session_key).get_decoded()['_auth_user_id']#把跟session key合的user授權抓出來解碼，取得user id
    output = {"status":"1"}
    if request.method == "POST":
        try:
            print(request.body)
            data = str(request.body).replace('b','').replace("\\r\\n",'').replace('\'','')
            print(data)
            table = {'%40': '@','%20' : ' ',"%3A" : ':'}#alter
            for char in table:#把長串資料用&分開
                data = data.replace(char, table[char])
            data = data.split('&')
            print(data)
            diastolic = data[0].replace('diastolic=','')
            pulse = data[1].replace('pulse=','')
            recorded_at = data[2].replace('recorded_at=','')
            systolic = data[3].replace('systolic=','')
            # data = json.loads(data)
            # systolic = data['systolic']
            # diastolic = data['diastolic']
            # pulse = data['pulse']
            # recorded_at = data['recorded_at']
            try:
                Pressure.objects.create(uid=uid, systolic=systolic, diastolic=diastolic, pulse=pulse, recorded_at=recorded_at)
            except:
                output = {"status":"0"}
        except:
            pass
    return JsonResponse(output)

@csrf_exempt
def weight_create_view(request): # 9.上傳體重測量結果
    session_key = request.headers.get('Authorization')[7:]#從header抓出session key
    authuser = Session.objects.get(session_key=session_key).get_decoded()['_auth_user_id']#把跟session key合的user授權抓出來解碼，取得user id
    output = {"status":"1"}
    if request.method == "POST":
        try:
            print(request.body)
            data = str(request.body).replace('b','',1).replace("\\r\\n",'').replace('\'','')
            print(data)
            table = {'%40': '@','%20' : ' ',"%3A" : ':'}#alter
            for char in table:#把長串資料用&分開
                data = data.replace(char, table[char])
            data = data.split('&')
            print(data)
            bmi = data[0].replace('bmi=','')
            body_fat = data[1].replace('body_fat=','')
            recorded_at = data[2].replace('recorded_at=','')
            weight = data[3].replace('weight=','')
            # data = json.loads(data)

            # weight = data['weight']
            # body_fat = data['body_fat']
            # bmi = data['bmi']
            # recorded_at = data['recorded_at']
            try:
                Weight.objects.create(uid=uid, weight=weight, body_fat=body_fat, bmi=bmi, recorded_at=recorded_at)
            except:
                output = {"status":"0"}
        except:
            pass
    return JsonResponse(output)

@csrf_exempt
def sugar_create_view(request): # 10.上傳血糖測量結果
    session_key = request.headers.get('Authorization')[7:]#從header抓出session key
    authuser = Session.objects.get(session_key=session_key).get_decoded()['_auth_user_id']#把跟session key合的user授權抓出來解碼，取得user id
    uid = authuser
    output = {"status":"1"}
    if request.method == "POST":
        try:
            print(request.body)
            data = str(request.body).replace('b','',1).replace("\\r\\n",'').replace('\'','')
            print(data)
            table = {'%40': '@','%20' : ' ',"%3A" : ':'}#alter
            for char in table:#把長串資料用&分開
                data = data.replace(char, table[char])

            data = data.split('&')
            print(data)
            drug = data[0].replace('drug=','')
            exercise = data[1].replace('exercise=','')
            recorded_at = data[2].replace('recorded_at=','')
            sugar = data[3].replace('sugar=','')
            timeperiod = data[4].replace('timeperiod=','')
            if drug == '1':
                drug == True
            elif drug == '0':
                drug == False
            if exercise == '1':
                exercise == True
            elif exercise == '0':
                exercise == False
            print(drug,exercise,recorded_at,sugar,timeperiod)
            # table = {'%40': '@'}#alter
            # for char in table:#把長串資料用&分開
            #     raw = raw.replace(char, table[char])
            #   rawlist = raw.split('&')
            # data = json.loads(data)

            # sugar = data['sugar']
            # timeperiod = data['timeperiod']
            # recorded_at = data['recorded_at']
            output = {"status":"0"}
            try:
                Sugar.objects.create(uid=uid, exercise = exercise,drug = drug,sugar=sugar, timeperiod=timeperiod, recorded_at=recorded_at)
            except:
                pass
        except:
            pass
    return JsonResponse(output)

@csrf_exempt
def diary_diet_create_view(request): # 15.飲食日記
    session_key = request.headers.get('Authorization')[7:]#從header抓出session key
    authuser = Session.objects.get(session_key=session_key).get_decoded()['_auth_user_id']#把跟session key合的user授權抓出來解碼，取得user id
    uid = authuser
    output = {"status":"1"}
    if request.method == "POST":
        try:
            print(request.body)
            data = str(request.body, encoding="utf-8").replace('b','',1).replace("\\r\\n",'').replace('\'','').replace("\\","\\\\")
            print(data)
            table = {'%40': '@','%20' : ' ',"%3A" : ':',"%5B%5D%5B%5D" : ""}#alter
            for char in table:#把長串資料用&分開
                data = data.replace(char, table[char])
            rawlist = data.split('&')
            data = {var.split('=')[0] : var.split('=')[1] for var in rawlist if var.split('=')[1]}
            print(data)
            form = DietForm(data)
            if form.is_valid():
                data = form.cleaned_data
                print(data)
                d = Diary_diet.objects.create(uid=uid)
                for index in data:
                    if data[index]:
                        setattr(d, index, data[index])
                output = {"status":"0", "image_url":"http://211.23.17.100:3001/diet_1_2020-08-17_11:11:11_0"}

            # data = json.loads(data)

            # description = data['description']
            # meal = data['meal']
            # tag = str(data['tag'])
            # image_count = data['image']
            # lat = data['lat']
            # lng = data['lng']
            # recorded_at = data['recorded_at']
            # try:
            #     print('-'*50)
            # except Exception:
            #     print(Exception)
            #     output = {"status":"1"}
        except:
            pass
    return JsonResponse(output,safe=False)

@csrf_exempt
def last_upload(request): # 25.最後上傳時間
    session_key = request.headers.get('Authorization')[7:]#從header抓出session key
    authuser = Session.objects.get(session_key=session_key).get_decoded()['_auth_user_id']#把跟session key合的user授權抓出來解碼，取得user id
    uid = authuser
    upload = []
    if request.method == 'GET':
        if Pressure.objects.filter(uid=uid):
            pre = Pressure.objects.filter(uid=uid).latest('recorded_at')
            pre = str(pre.recorded_at)
            upload.append({"blood_pressure":pre})
        if Weight.objects.filter(uid=uid):
            wei = Weight.objects.filter(uid=uid).latest('recorded_at')
            wei = str(wei.recorded_at)
            upload.append({"weight":wei})
        if Sugar.objects.filter(uid=uid):
            sug = Sugar.objects.filter(uid=uid).latest('recorded_at')
            sug = str(sug.recorded_at)
            upload.append({"blood_sugar":sug})
        if Diary_diet.objects.filter(uid=uid):
            die = Diary_diet.objects.filter(uid=uid).latest('recorded_at')
            die = str(die.recorded_at)
            upload.append({"diet":die})
        output = {
            "status":"0",
            "last_upload":upload
        }
    else:
        output = {"status":"1"}
    return JsonResponse(output)

@csrf_exempt
def records(request): # 40.刪除日記記錄
    
    output = {"status":"1"}
    if request.method == 'DELETE':
        # data = request.get_full_path()
        # data = data.split('?')[1]
        # data = data.replace('%5B%5D',"")
        # data = data.split("&")
        # print(data)
        # if request.GET.getlist("blood_pressures[]"):
        #     data_list = request.GET.getlist("blood_pressures[]")
        #     for data in data_list:
        #         Pressure.objects.get(id=data).delete()
        # if request.GET.getlist("weights[]"):
        #     data_list = request.GET.getlist("weights[]")
        #     for data in data_list:
        #         Weight.objects.get(id=data).delete()
        # if request.GET.getlist("blood_sugars[]"):
        #     data_list = request.GET.getlist("blood_sugars[]")
        #     for data in data_list:
        #         Sugar.objects.get(id=data).delete()
        # if request.GET.getlist("diets[]"):
        #     data_list = request.GET.getlist("diets[]")
        #     for data in data_list:
        #         Diary_diet.objects.get(id=data).delete()
        url = request.get_full_path().split("?")[1]
        url_list = url.split("&")
        print(url_list)
        for item in url_list:
            if item.startswith("blood_pressures"):
                print(item.split("=")[1])
                Pressure.objects.get(id = int(item.split("=")[1])).delete()
            elif item.startswith("diets"):
                print(item.split("=")[1])
                Diary_diet.objects.get(id = int(item.split("=")[1])).delete()
            elif item.startswith("weights"):
                print(item.split("=")[1])
                Weight.objects.get(id = int(item.split("=")[1])).delete()
            elif item.startswith("blood_sugars"):
                print(item.split("=")[1])
                Sugar.objects.get(id = int(item.split("=")[1])).delete()
        output = {"status":"0"}
    return JsonResponse(output)

@csrf_exempt
def diary_list(request): # 14.日記列表資料
    session_key = request.headers.get('Authorization')[7:]#從header抓出session key
    authuser = Session.objects.get(session_key=session_key).get_decoded()['_auth_user_id']#把跟session key合的user授權抓出來解碼，取得user id
    if request.method == 'GET':
        date = request.GET.get("date")
        print(date)
        diary = []
        if date:
            if Pressure.objects.filter( date=date):
                blood_pressures = Pressure.objects.filter( date=date)
                for blood_pressure in blood_pressures:
                    r = {
                            "id":blood_pressure.id,
                            "user_id":blood_pressure.uid,
                            "systolic":blood_pressure.systolic,
                            "diastolic":blood_pressure.diastolic,
                            "pulse":blood_pressure.pulse,
                            "recorded_at":blood_pressure.recorded_at.strftime("%Y-%m-%d %H:%M:%S"),
                            "type":"blood_pressure"
                        }
                    diary.append(r)
            if Weight.objects.filter( date=date):
                weights = Weight.objects.filter( date=date)
                for weight in weights:
                    r = {
                            "id":weight.id,
                            "user_id":weight.uid,
                            "weight":weight.weight,
                            "body_fat":weight.body_fat,
                            "bmi":weight.bmi,
                            "recorded_at":weight.recorded_at.strftime("%Y-%m-%d %H:%M:%S"),
                            "type":"weight"
                        }
                    diary.append(r)
            if Sugar.objects.filter( date=date):
                blood_sugars = Sugar.objects.filter( date=date)
                for blood_sugar in blood_sugars:
                    r = {
                            "id":blood_sugar.id,
                            "user_id":blood_sugar.uid,
                            "sugar":int(blood_sugar.sugar),
                            "timeperiod":int(blood_sugar.timeperiod),
                            "recorded_at":blood_sugar.recorded_at.strftime("%Y-%m-%d %H:%M:%S"),
                            "type":"blood_sugar"
                        }
                    diary.append(r)
            if Diary_diet.objects.filter( date=date):
                diary_diets = Diary_diet.objects.filter( date=date)
                for diary_diet in diary_diets:
                    if UserCare.objects.filter( date=date):
                        reply = UserCare.objects.filter(member_id=0, date=date).latest('updated_at')
                        r = {
                                "id":int(diary_diet.id),
                                "user_id":int(diary_diet.uid),
                                "description":diary_diet.description,
                                "meal":int(diary_diet.meal),
                                "tag":diary_diet.tag,
                                "image":diary_diet.image_count,
                                "type":"diet",
                                "location":
                                    {
                                        "lat":diary_diet.lat,
                                        "lng":diary_diet.lng
                                    },
                                "recorded_at":diary_diet.recorded_at.strftime("%Y-%m-%d %H:%M:%S"),
                                "reply":reply.message
                            }
                    else:
                        r = {
                                "id":int(diary_diet.id),
                                "user_id":int(diary_diet.uid),
                                "description":diary_diet.description,
                                "meal":int(diary_diet.meal),
                                "tag":diary_diet.tag,
                                "image":diary_diet.image_count,
                                "type":"diet",
                                "location":
                                    {
                                        "lat":diary_diet.lat,
                                        "lng":diary_diet.lng
                                    },
                                "recorded_at":str(diary_diet.recorded_at),
                            }
                    diary.append(r)
            output = {"status":"0", "diary":diary}
        else:
            output = {"status":"1"}
        # print(json.dumps(output))
    return JsonResponse(output)

@csrf_exempt
def care(request): # 28.送出關懷諮詢!+27.獲取關懷諮詢!
    session_key = request.headers.get('Authorization')[7:]#從header抓出session key
    authuser = Session.objects.get(session_key=session_key).get_decoded()['_auth_user_id']#把跟session key合的user授權抓出來解碼，取得user id
    uid = authuser
    
    output = {"status":"1"}
    if request.method == 'POST':
        print(request.body)
        data = str(request.body).replace('b','',1).replace("\\r\\n",'').replace('\'','')
        print(data)
        data = json.loads(data)
        message = data['message']
        recorded_at = data['recorded_at']
        recorded_at = recorded_at.replace("%20", " ")
        recorded_at = recorded_at.replace("%3A", ":")
        friend_list = Friend_data.objects.filter(uid=uid, status=1)
        for friend_data in friend_list:
            UserCare.objects.create(uid=uid, member_id=friend_data.friend_type, reply_id=friend_data.relation_id, message=message, updated_at=recorded_at)
        output = {"status":"0"}
    if request.method == 'GET':
        usercares = UserCare.objects.filter(reply_id=uid)
        cares = []
        for usercare in usercares:
            r = {
                    "id":usercare.id,
                    "user_id":usercare.uid,
                    "member_id":usercare.member_id,
                    "reply_id":usercare.reply_id,
                    "message":usercare.message,
                    "created_at":usercare.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    "updated_at":usercare.updated_at.strftime("%Y-%m-%d %H:%M:%S")
                }
            cares.append(r)
        output = {"status":"0", "cares":cares}
    return JsonResponse(output)