from django.db import models
from django.contrib import admin

# Create your models here.
class Pressure(models.Model):#8.上傳血壓測量結果
    systolic = models.FloatField()
    diastolic = models.FloatField()
    pulse = models.DecimalField(max_digits = 10, decimal_places=0)
    recorded_at = models.DateTimeField()
    # recorded_at = models.DateTimeField(auto_now_add=True)
    # print(systolic,diastolic,pulse,recorded_at)

class Weight(models.Model): #9.上傳體重測量結果
    weight = models.FloatField()
    body_fat = models.FloatField()
    bmi = models.FloatField()
    recorded_at = models.DateTimeField()

class Sugar(models.Model): #10.上傳血糖
    sugar = models.DecimalField(max_digits = 10, decimal_places=0)
    timeperiod = models.DecimalField(max_digits = 10, decimal_places=0)
    recorded_at = models.DateTimeField()

class Diet(models.Model): #10.上傳血糖
    sugar = models.DecimalField(max_digits = 10, decimal_places=0)
    timeperiod = models.DecimalField(max_digits = 10, decimal_places=0)
    recorded_at = models.DateTimeField()

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