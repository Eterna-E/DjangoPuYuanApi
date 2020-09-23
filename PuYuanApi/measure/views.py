from django.shortcuts import render
from .forms import PressureForm,WeightForm,SugarForm
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

# Create your views here.
def index(request):
    return render(request,'hello.html',{
        'data': "Hello Django ",
    })

@csrf_exempt
def pressure_create_view(request):
    form = PressureForm(request.POST or None)
    if form.is_valid():
        form.save()
        return JsonResponse({"status": "0",},safe=False)
    else:
        return JsonResponse({"status": "1",},safe=False)

@csrf_exempt
def weight_create_view(request):
    form = WeightForm(request.POST or None)
    if form.is_valid():
        form.save()
        return JsonResponse({"status": "0",},safe=False)
    else:
        return JsonResponse({"status": "1",},safe=False)

@csrf_exempt
def sugar_create_view(request):
    form = SugarForm(request.POST or None)
    if form.is_valid():
        form.save()
        return JsonResponse({"status": "0",},safe=False)
    else:
        return JsonResponse({"status": "1",},safe=False)