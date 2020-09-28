from django.db import models
from django.contrib import admin

# Create your models here.
class Pressure(models.Model):#8.上傳血壓測量結果
    systolic = models.FloatField(null=True)
    diastolic = models.FloatField(null=True)
    pulse = models.DecimalField(max_digits = 10, decimal_places=0,null=True)
    recorded_at = models.DateTimeField(blank=True)
    # recorded_at = models.DateTimeField(auto_now_add=True)
    # print(systolic,diastolic,pulse,recorded_at)

class Weight(models.Model): #9.上傳體重測量結果
    weight = models.FloatField(null=True)
    body_fat = models.FloatField(null=True)
    bmi = models.FloatField(blank=True)
    recorded_at = models.DateTimeField(blank=True)

class Sugar(models.Model): #10.上傳血糖
    sugar = models.DecimalField(max_digits = 10, decimal_places=0, blank=True, null=True)
    timeperiod = models.DecimalField(max_digits = 10, decimal_places=0, blank=True, null=True)
    recorded_at = models.DateTimeField(blank=True)

class Diary_diet(models.Model): #15.飲食日記
    # uid = models.CharField(max_length = 100,blank=True)
    description = models.CharField(max_length=10, blank=True, null=True, default=0)
    meal = models.DecimalField(max_digits=5, decimal_places=0, blank=True, null=True, default=0)
    tag = models.CharField(max_length = 100,blank=True)
    # image = models.ImageField(upload_to = 'diet/diet_%Y-%m-%d_%H:%M:%S',blank=True)
    image_count = models.IntegerField(blank=True)
    lat = models.FloatField(max_length = 100,blank=True)
    lng = models.FloatField(max_length = 100,blank=True)
    recorded_at = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True, blank=True)

@admin.register(Pressure)
class PressureAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Pressure._meta.fields]
	# list_display = ('id', 'systolic')

@admin.register(Weight)
class WeightAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Weight._meta.fields]

@admin.register(Sugar)
class SugarAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Sugar._meta.fields]

@admin.register(Diary_diet)
class Diary_dietAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Diary_diet._meta.fields]