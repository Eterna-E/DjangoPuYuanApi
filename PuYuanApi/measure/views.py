from django.shortcuts import render
# from .forms import PressureForm,WeightForm,SugarForm
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import Pressure,Weight,Sugar,Diary_diet,UserCare

# Create your views here.
def index(request):
    return render(request,'hello.html',{
        'data': "Hello Django ",
    })

@csrf_exempt
def pressure_create_view(request): # 上傳血壓測量結果
    uid = request.user.id
    uid = 123
    if request.method == "POST":
        print(request.body)
        data = str(request.body).replace('b','').replace("\\r\\n",'').replace('\'','')
        print(data)
        data = json.loads(data)
        systolic = data['systolic']
        diastolic = data['diastolic']
        pulse = data['pulse']
        recorded_at = data['recorded_at']
        try:
            Pressure.objects.create(uid=uid, systolic=systolic, diastolic=diastolic, pulse=pulse, recorded_at=recorded_at)
        except:
            output = {"status":"1"}
        else:
            output = {"status":"0"}
    return JsonResponse(output)

@csrf_exempt
def weight_create_view(request): # 上傳體重測量結果
    uid = request.user.id
    uid = 123
    if request.method == "POST":
        print(request.body)
        data = str(request.body).replace('b','',1).replace("\\r\\n",'').replace('\'','')
        print(data)
        data = json.loads(data)
        weight = data['weight']
        body_fat = data['body_fat']
        bmi = data['bmi']
        recorded_at = data['recorded_at']
        try:
            Weight.objects.create(uid=uid, weight=weight, body_fat=body_fat, bmi=bmi, recorded_at=recorded_at)
        except:
            output = {"status":"1"}
        else:
            output = {"status":"0"}
    return JsonResponse(output)

@csrf_exempt
def sugar_create_view(request): # 上傳血糖測量結果
    uid = request.user.id
    uid = 123
    if request.method == "POST":
        print(request.body)
        data = str(request.body).replace('b','',1).replace("\\r\\n",'').replace('\'','')
        print(data)
        data = json.loads(data)
        sugar = data['sugar']
        timeperiod = data['timeperiod']
        recorded_at = data['recorded_at']
        try:
            Sugar.objects.create(uid=uid, sugar=sugar, timeperiod=timeperiod, recorded_at=recorded_at)
        except:
            output = {"status":"1"}
        else:
            output = {"status":"0"}
    return JsonResponse(output)

@csrf_exempt
def diary_diet_create_view(request): # 飲食日記
    uid = request.user.id
    uid = 123
    if request.method == "POST":
        print(request.body)
        data = str(request.body, encoding="utf-8").replace('b','',1).replace("\\r\\n",'').replace('\'','').replace("\\","\\\\")
        print(data)
        data = json.loads(data)
        description = data['description']
        meal = data['meal']
        tag = str(data['tag'])
        image_count = data['image']
        lat = data['lat']
        lng = data['lng']
        recorded_at = data['recorded_at']
        try:
            Diary_diet.objects.create(uid=uid, description=description, meal=meal, tag=tag, image_count=image_count, lat=lat, lng=lng, recorded_at=recorded_at)
        except:
            output = {"status":"1"}
        else:
            output = {"status":"0", "image_url":"http://211.23.17.100:3001/diet_1_2020-08-17_11:11:11_0"}
    return JsonResponse(output,safe=False)

@csrf_exempt
def last_upload(request): # 最後上傳時間
    uid = request.user.id
    uid = 123
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
def records(request): # 刪除日記記錄
    uid = request.user.id
    uid = 123
    output = {"status":"1"}
    if request.method == 'DELETE':
        if request.GET.getlist("blood_pressures[]"):
            data_list = request.GET.getlist("blood_pressures[]")
            for data in data_list:
                Pressure.objects.get(id=data).delete()
        if request.GET.getlist("weights[]"):
            data_list = request.GET.getlist("weights[]")
            for data in data_list:
                Weight.objects.get(id=data).delete()
        if request.GET.getlist("blood_sugars[]"):
            data_list = request.GET.getlist("blood_sugars[]")
            for data in data_list:
                Sugar.objects.get(id=data).delete()
        if request.GET.getlist("diets[]"):
            data_list = request.GET.getlist("diets[]")
            for data in data_list:
                Diary_diet.objects.get(id=data).delete()
        output = {"status":"0"}
    return JsonResponse(output)

@csrf_exempt
def diary_list(request): # 日記列表資料
    uid = request.user.id
    uid = 123
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
                        "recorded_at":str(blood_pressure.recorded_at),
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
                        "recorded_at":str(weight.recorded_at),
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
                        "recorded_at":str(blood_sugar.recorded_at),
                        "type":"blood_sugar"
                    }
                diary.append(r)
        if Diary_diet.objects.filter( date=date):
            diary_diets = Diary_diet.objects.filter( date=date)
            for diary_diet in diary_diets:
                if UserCare.objects.filter( date=date):
                    reply = UserCare.objects.filter(member_id=0, date=date).latest('updated_at')
                    r = {
                            "id":diary_diet.id,
                            "user_id":diary_diet.uid,
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
                            "reply":reply.message
                        }
                else:
                    r = {
                            "id":diary_diet.id,
                            "user_id":diary_diet.uid,
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