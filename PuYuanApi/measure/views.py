from django.shortcuts import render
# from .forms import PressureForm,WeightForm,SugarForm
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .models import Pressure,Weight,Sugar

# Create your views here.
def index(request):
    return render(request,'hello.html',{
        'data': "Hello Django ",
    })

@csrf_exempt
def pressure_create_view(request):
    if request.method == "POST":
        print(request.body)
        data = str(request.body).replace('b','').replace("\\r\\n",'').replace('\'','')
        print(data)
        data = json.loads(data)
        systolic = data['systolic']
        diastolic = data['diastolic']
        pulse = data['pulse']
        recorded_at = data['recorded_at']
        Pressure.objects.create(systolic=systolic,diastolic=diastolic,pulse=pulse,recorded_at=recorded_at)
        return JsonResponse({"status": "0",},safe=False)
    else:
        return JsonResponse({"status": "1",},safe=False)

@csrf_exempt
def weight_create_view(request):
    if request.method == "POST":
        print(request.body)
        data = str(request.body).replace('b','',1).replace("\\r\\n",'').replace('\'','')
        print(data)
        data = json.loads(data)
        weight = data['weight']
        body_fat = data['body_fat']
        bmi = data['bmi']
        recorded_at = data['recorded_at']
        Weight.objects.create(weight=weight,body_fat=body_fat,bmi=bmi,recorded_at=recorded_at)
        return JsonResponse({"status": "0",},safe=False)
    else:
        return JsonResponse({"status": "1",},safe=False)

@csrf_exempt
def sugar_create_view(request):
    if request.method == "POST":
        print(request.body)
        data = str(request.body).replace('b','',1).replace("\\r\\n",'').replace('\'','')
        print(data)
        data = json.loads(data)
        sugar = data['sugar']
        timeperiod = data['timeperiod']
        recorded_at = data['recorded_at']
        Sugar.objects.create(sugar=sugar,timeperiod=timeperiod,recorded_at=recorded_at)
        return JsonResponse({"status": "0",},safe=False)
    else:
        return JsonResponse({"status": "1",},safe=False)

@csrf_exempt
def diary_diet_create_view(request): # 飲食日記!
    # uid = request.user.id
    if request.method == 'POST':
        data = request.body
        data = str(data, encoding="utf-8")
        data = {
            i.split('=')[0]: i.split('=')[1]
            for i in data.replace("%40","@").split('&') if i.split('=')[1]
        }
        tag = request.POST.getlist("tag[][]")
        description = data['description']
        image = request.POST.get("image")
        lat = data['lat']
        lng = data['lng']
        # meal_list = ['早餐', '午餐', '晚餐']
        meal = data['meal']
        recorded_at = data['recorded_at']
        recorded_at = recorded_at.replace("%20", " ")
        recorded_at = recorded_at.replace("%3A", ":")
        try:
            Diary_diet.objects.create( description=description, meal=meal, tag=tag, image_count=image, lat=lat, lng=lng, recorded_at=recorded_at)
        except:
            output = {"status":"1"}
        else:
            output = {"status":"0", "image_url":"http://211.23.17.100:3001/diet_1_2020-08-17_11:11:11_0"}
    return JsonResponse(output,safe=False)