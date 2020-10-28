from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
# Create your models here.

class patient(User):
	phone = models.CharField(max_length = 20,null = True)
	name = models.CharField(max_length = 20,null = True)
	birthday = models.DateField(null = True)#yyyy-mm-dd
	height = models.CharField(max_length = 20,null = True)
	gender = models.BooleanField(max_length = 10,null = True)#0/1(Flase/True)
	fcm_id = models.CharField(max_length = 10,null = True)
	address = models.CharField(max_length = 100,null = True)
	weight = models.CharField(max_length = 20,null = True)
	#others
	status = models.CharField(max_length = 20,default = 'normal')#登入狀態
	group = models.CharField(max_length = 20,null = True)#群組設定 預設空
	unread_records1 = models.CharField(max_length = 20,null = True)#不知道是啥
	unread_records2 = models.CharField(max_length = 20,null = True)
	unread_records3 = models.CharField(max_length = 20,null = True)
	email_verfied = models.BooleanField(max_length = 10,null = True,default = False)#信箱驗證
	privacy_policy = models.BooleanField(max_length = 10,null = True,default = True)#pp
	must_change_password = models.BooleanField(max_length = 10,default = False)#當更改完密碼就設為1 其他時候以及預設是0
	badge = models.CharField(max_length = 20,null = True)#徽章?! 不知道是啥
	login_times = models.CharField(max_length = 100,default = 0)#登入幾次 每按一次login+1
	created_at = models.DateTimeField(null = True,auto_now_add = True)#可以用auth.User.date_joined屬性找到
	updated_at = models.DateTimeField(null = True,auto_now = True)# 每次有更動就更新 應該就是在其他api加更改現在時間的設定
	after_recording = models.CharField(max_length = 20,null = True)
	no_recording_for_a_day = models.CharField(max_length = 20,null = True)
	over_max_or_under_min = models.CharField(max_length = 20,null = True)
	after_meal = models.CharField(max_length = 20,null = True)
	unit_of_sugar = models.CharField(max_length = 20,null = True)
	unit_of_weight = models.CharField(max_length = 20,null = True)
	unit_of_height = models.CharField(max_length = 20,null = True)
	invite_code = models.CharField(max_length=100,null=True)
	# def __str__(self):
	# 	return self.username
class checkcode(models.Model):
	email = models.EmailField(max_length = 100)
	code = models.CharField(max_length = 20)
	# def __str__(self):
	# 	return self.phone
class sugarinfo(models.Model):
	sugar_delta_max = models.DecimalField(max_digits = 20,decimal_places = 5,default = 0)
	sugar_delta_min = models.DecimalField(max_digits = 20,decimal_places = 5,default = 0)
	sugar_morning_max = models.DecimalField(max_digits = 20,decimal_places = 5,default = 0)
	sugar_morning_min = models.DecimalField(max_digits = 20,decimal_places = 5,default = 0)
	sugar_evening_max = models.DecimalField(max_digits = 20,decimal_places = 5,default = 0)
	sugar_evening_min = models.DecimalField(max_digits = 20,decimal_places = 5,default = 0)
	sugar_before_max = models.DecimalField(max_digits = 20,decimal_places = 5,default = 0)
	sugar_before_min = models.DecimalField(max_digits = 20,decimal_places = 5,default = 0)
	sugar_after_max = models.DecimalField(max_digits = 20,decimal_places = 5,default = 0)
	sugar_after_min = models.DecimalField(max_digits = 20,decimal_places = 5,default = 0)
	systolic_max = models.DecimalField(max_digits = 20,decimal_places = 5,default = 0)
	systolic_min = models.DecimalField(max_digits = 20,decimal_places = 5,default = 0)
	diastolic_max = models.DecimalField(max_digits = 20,decimal_places = 5,default = 0)
	diastolic_min = models.DecimalField(max_digits = 20,decimal_places = 5,default = 0)
	pulse_max = models.DecimalField(max_digits = 20,decimal_places = 5,default = 0)
	pulse_min = models.DecimalField(max_digits = 20,decimal_places = 5,default = 0)
	weight_max = models.DecimalField(max_digits = 20,decimal_places = 5,default = 0)
	weight_min = models.DecimalField(max_digits = 20,decimal_places = 5,default = 0)
	bmi_max = models.DecimalField(max_digits = 20,decimal_places = 5,default = 0)
	bmi_min = models.DecimalField(max_digits = 20,decimal_places = 5,default = 0)
	body_fat_max = models.DecimalField(max_digits = 20,decimal_places = 5,default = 0)
	body_fat_min = models.DecimalField(max_digits = 20,decimal_places = 5,default = 0)
	patient = models.OneToOneField(patient, on_delete = models.CASCADE,default = True)
	# def __str__(self):
	# 	return self.sugar_delta_max
class bloodinfo(models.Model):
	a1c = models.DecimalField(max_digits = 20,decimal_places = 5,default = 0)
	recorded_at = models.DateTimeField(null = True)
	patient = models.ForeignKey(patient, on_delete = models.CASCADE,default = True)
	created_at = models.DateTimeField(null = True,auto_now_add = True)#可以用auth.User.date_joined屬性找到
	update_at = models.DateTimeField(null = True,auto_now = True)
	# def __str__(self):
	# 	return str(self.a1c)
class medi(models.Model):
	typee = models.CharField(max_length = 20,null = True)
	hospitalname = models.CharField(max_length = 20,null = True)
	recorded_at = models.DateTimeField(null = True)
	patient = models.ForeignKey(patient, on_delete = models.CASCADE,default = True)
	# def __str__(self):
	# 	return str(self.a1c)
class diabete(models.Model):
	diabetes_type = models.CharField(max_length = 20,null = True)
	insulin = models.CharField(max_length = 20,null = True)
	anti_hypertensives = models.CharField(max_length = 20,null = True)
	oad = models.CharField(max_length = 20,null = True)
	patient = models.OneToOneField(patient, on_delete = models.CASCADE,default = True)
	# def __str__(self):
	# 	return str(self.diabetes_type)

@admin.register(patient)
class patientAdmin(admin.ModelAdmin):
    list_display = [field.name for field in patient._meta.fields]

@admin.register(checkcode)
class checkcodeAdmin(admin.ModelAdmin):
    list_display = [field.name for field in checkcode._meta.fields]

@admin.register(sugarinfo)
class sugarinfoAdmin(admin.ModelAdmin):
    list_display = [field.name for field in sugarinfo._meta.fields]

@admin.register(bloodinfo)
class bloodinfoAdmin(admin.ModelAdmin):
    list_display = [field.name for field in bloodinfo._meta.fields]

@admin.register(medi)
class mediAdmin(admin.ModelAdmin):
    list_display = [field.name for field in medi._meta.fields]

@admin.register(diabete)
class diabeteAdmin(admin.ModelAdmin):
    list_display = [field.name for field in diabete._meta.fields]
