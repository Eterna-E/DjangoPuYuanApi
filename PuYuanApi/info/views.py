from django.shortcuts import render
from django.http import JsonResponse
from django.contrib import auth
from django.contrib.sessions.models import Session
from Denru.models import *
from info.forms import *

from django.views.decorators.csrf import csrf_exempt

# Create your views here.
@csrf_exempt
def information(request):
	
	#if 1:
	try:
		if request.method == 'PATCH':
			result = {'status': '1'}#重設失敗
			session_key = request.headers.get('Authorization')#從header抓出session key
			authuser = Session.objects.get(session_key=session_key).get_decoded()['_auth_user_id']#把跟session key合的user授權抓出來解碼
			user = patient.objects.get(id = authuser)#把資訊從資料庫拉出來
			print(user)
			print(request.body.decode('UTF-8'))
			raw = request.body.decode('UTF-8')
			table = {'%40': '@'}#alter
			for char in table:#把長串資料用&分開
				raw = raw.replace(char, table[char])
			rawlist = raw.split('&')

			data = {var.split('=')[0] : var.split('=')[1] for var in rawlist if var.split('=')[1]}#分開後用=轉成dict
			print(data)
			print(123)
			form = infoForm(data)
			if form.is_valid():
				data = form.cleaned_data
				print(data)
				for index in data:
					if data[index]:
						setattr(user, index, data[index])
				user.save()#save
				result = {'status': '0'}#重設成功
	except:
		pass

	if 1:
	#try:
		if request.method == 'GET':
			result = {'status': '1'}#設定失敗
			session_key = request.headers.get('Authorization')#從header抓出session key
			authuser = Session.objects.get(session_key=session_key).get_decoded()['_auth_user_id']#把跟session key合的user授權抓出來解碼
			user = patient.objects.get(id = authuser)#把資訊從資料庫拉出來
			#轉性別
			gender = user.gender
			if gender == True:
				gender = 'female'
			else:
				gender = 'male'
			#轉email
			verfy = user.email_verfied
			if verfy == True:
				verfy = 1
			else:
				verfy = 0
			#轉pp
			pp = user.privacy_policy
			if pp == True:
				pp = 1
			else:
				pp = 0
			#轉password
			password = user.password
			if password == True:
				password = 1
			else:
				password = 0
			result = {'status': '0', 
			#user
			'user':{
			'id':int(user.id),
			'name':user.name,
			'account':'test',
			'email':user.email,
			'phone':user.phone,
			'fb_id':'null' ,
			'statusUser' :user.status,
			'group':'null',
			'birthday': user.birthday,
			'height': user.height,
			'weight':user.weight,
			'gender':gender,
			'address':user.address,
			'unread_records':[
			user.unread_records1 if user.unread_records1 is None else int(user.unread_records1),
			str(user.unread_records2),
			user.unread_records3 if user.unread_records3 is None else int(user.unread_records3)],
			'verfied':verfy,
			'privacy_policy':pp,
			'must_change_password':password,
			'fcm_id':user.fcm_id,
			'badge':user.badge if user.badge is None else int(user.badge),
			'login_times':user.login_times if user.login_times is None else int(user.login_times),
			'created_at':user.date_joined.strftime("%Y-%m-%d %H:%M:%S"),
			'update_at':user.update_at}.strftime("%Y-%m-%d %H:%M:%S"),
			#default
			'default':{
			'id':int(1),
			'user_id':int(user.id),
			'sugar_delta_min':user.sugarinfo.sugar_delta_min if user.sugarinfo.sugar_delta_min is None else int(user.sugarinfo.sugar_delta_min),
			'sugar_morning_max':user.sugarinfo.sugar_morning_max if user.sugarinfo.sugar_morning_max is None else int(user.sugarinfo.sugar_morning_max),
			'sugar_morning_min':user.sugarinfo.sugar_morning_min if user.sugarinfo.sugar_morning_min is None else int(user.sugarinfo.sugar_morning_min),
			'sugar_evening_max':user.sugarinfo.sugar_evening_max if user.sugarinfo.sugar_evening_max is None else int(user.sugarinfo.sugar_evening_max),
			'sugar_evening_min':user.sugarinfo.sugar_evening_min if user.sugarinfo.sugar_evening_min is None else int(user.sugarinfo.sugar_evening_min),
			'sugar_before_max':user.sugarinfo.sugar_before_max if user.sugarinfo.sugar_before_max is None else int(user.sugarinfo.sugar_before_max),
			'sugar_before_min':user.sugarinfo.sugar_before_min if user.sugarinfo.sugar_before_min is None else int(user.sugarinfo.sugar_before_min),
			'sugar_after_max':user.sugarinfo.sugar_after_max if user.sugarinfo.sugar_after_max is None else int(user.sugarinfo.sugar_after_max),
			'sugar_after_min':user.sugarinfo.sugar_after_min if user.sugarinfo.sugar_after_min is None else int(user.sugarinfo.sugar_after_min),
			'systolic_max':user.sugarinfo.systolic_max if user.sugarinfo.systolic_max is None else int(user.sugarinfo.systolic_max),
			'systolic_min':user.sugarinfo.systolic_min if user.sugarinfo.systolic_min is None else int(user.sugarinfo.systolic_min),
			'diastolic_max':user.sugarinfo.diastolic_max if user.sugarinfo.diastolic_max is None else int(user.sugarinfo.diastolic_max),
			'diastolic_min':user.sugarinfo.diastolic_min if user.sugarinfo.diastolic_min is None else int(user.sugarinfo.diastolic_min),
			'pulse_max':user.sugarinfo.pulse_max if user.sugarinfo.pulse_max is None else int(user.sugarinfo.pulse_max),
			'pulse_min':user.sugarinfo.pulse_min if user.sugarinfo.pulse_min is None else int(user.sugarinfo.pulse_min),
			'weight_max':user.sugarinfo.weight_max if user.sugarinfo.weight_max is None else int(user.sugarinfo.weight_max),
			'bmi_max':user.sugarinfo.bmi_max if user.sugarinfo.bmi_max is None else int(user.sugarinfo.bmi_max),
			'bmi_min':user.sugarinfo.bmi_min if user.sugarinfo.bmi_min is None else int(user.sugarinfo.bmi_min),
			'body_fat_max':user.sugarinfo.body_fat_max if user.sugarinfo.body_fat_max is None else int(user.sugarinfo.body_fat_max),
			'body_fat_min':user.sugarinfo.body_fat_min if user.sugarinfo.body_fat_min is None else int(user.sugarinfo.body_fat_min),
			'created_at':user.date_joined.strftime("%Y-%m-%d %H:%M:%S"),
			'update_at':user.update_at}.strftime("%Y-%m-%d %H:%M:%S"),
			#settings
			'setting':{
			'id':int(1),
			'user_id':int(user.id),
			'after_recording':int(user.after_recording),
			'no_recording_for_a_day':int(user.no_recording_for),
			'over_max_or_under_min':int(user.over_max_or_under_min),
			'after_meal':int(user.after_meal),
			'unit_of_sugar':int(user.unit_of_sugar),
			'unit_of_weight':int(user.unit_of_weight),
			'unit_of_height':int(user.unit_of_height),
			'created_at':user.date_joined.strftime("%Y-%m-%d %H:%M:%S"),
			'update_at':user.update_at.strftime("%Y-%m-%d %H:%M:%S")

			}
			}
			#print info
	#except:
		
		#pass
	return JsonResponse(result)

@csrf_exempt
def individualdefault(request):
	if request.method == 'PATCH':
		#if 1:
		result = {'status': '1'}#設定失敗
		try:
			
			session_key = request.headers.get('Authorization')#從header抓出session key
			authuser = Session.objects.get(session_key=session_key).get_decoded()['_auth_user_id']#把跟session key合的user授權抓出來解碼
			user = patient.objects.get(id = authuser)#把資訊從資料庫拉出來
			
			print(user)
			raw = request.body.decode('UTF-8')
			table = {'%40': '@'}#alter
			for char in table:#把長串資料用&分開
				raw = raw.replace(char, table[char])
			rawlist = raw.split('&')

			data = {var.split('=')[0] : var.split('=')[1] for var in rawlist if var.split('=')[1]}#分開後用=轉成dict
			form = sugarinfoForm(data)
			
			print(data)
			if form.is_valid():
				data = form.cleaned_data
				print(data)
				for index in data:
					if data[index]:
						setattr(user.sugarinfo, index, data[index])
				user.sugarinfo.save()#save
				result = {'status': '0'}#設定成功
		except:
			pass
	return JsonResponse(result)

# def printinfo(request):
# 	if request.method == 'GET':
# 		#if 1:
# 		result = {'status': '1'}#設定失敗
# 		try:
# 			session_key = request.headers.get('Authorization')#從header抓出session key
# 			authuser = Session.objects.get(session_key=session_key).get_decoded()['_auth_user_id']#把跟session key合的user授權抓出來解碼
# 			user = patient.objects.get(id = authuser)#把資訊從資料庫拉出來

# 			print(user.objects.all())
# 			result = {'status': '0'}#設定成功
# 		except:
# 			pass
# 	return JsonResponse(result)