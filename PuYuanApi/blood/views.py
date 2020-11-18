from django.shortcuts import render
from django.http import JsonResponse
from django.contrib import auth
from django.contrib.sessions.models import Session
from Denru.models import *
from blood.forms import *
# Create your views here.
def a1c(request):
	result = {'status':'1'}#預設失敗
	if 1:
	#try:
		if request.method == 'GET':
			#從DD那抓出information
			session_key = request.headers.get('Authorization')[7:]#從header抓出session key
			authuser = Session.objects.get(session_key=session_key).get_decoded()['_auth_user_id']#把跟session key合的user授權抓出來解碼
			user = patient.objects.get(id = authuser)#把資訊從資料庫拉出來
			a = user.bloodinfo_set.all()
			#result = {'status':'0','a1cs':{'id':1,'user_id':1,'a1c':user.blood_set.a1c,'recorded_at':'','created_at':user.created_at,'update_at':user.update_at}}#成功
			result = {'status':'0'}#成功
			result['a1cs'] = []
			for item in a:
				record = {}
				record["id"] = item.id
				record['user_id'] = user.id
				record['a1c'] = str(item.a1c)
				if item.recorded_at:
					record['recorded_at'] = item.recorded_at.strftime("%Y-%m-%d %H:%M:%S")
				if item.created_at:
					record['created_at'] = item.created_at.strftime("%Y-%m-%d %H:%M:%S")
				if item.update_at:
					record['updated_at'] = item.update_at.strftime("%Y-%m-%d %H:%M:%S")
				result["a1cs"].append(record)
		if request.method == 'POST':
			session_key = request.headers.get('Authorization')[7:]#從header抓出session key
			authuser = Session.objects.get(session_key=session_key).get_decoded()['_auth_user_id']#把跟session key合的user授權抓出來解碼
			user = patient.objects.get(id = authuser)#把資訊從資料庫拉出來

			blood123 = bloodinfo.objects.create(patient = user)#建立新表單
			form = BloodForm(request.POST)#填入表單
			print(request.POST)
			if form.is_valid():#檢查forms.py中的格式
				data = form.cleaned_data#接form裡面丟出來的資料
				print('-'*50)
			a1c = form.cleaned_data['a1c']
			recorded_at = form.cleaned_data['recorded_at']
			blood123.a1c = a1c
			blood123.recorded_at = recorded_at
			blood123.save()
			result = {'status':'0'}
		if request.method == 'DELETE':
			session_key = request.headers.get('Authorization')[7:]#從header抓出session key
			authuser = Session.objects.get(session_key=session_key).get_decoded()['_auth_user_id']#把跟session key合的user授權抓出來解碼
			user = patient.objects.get(id = authuser)#把資訊從資料庫拉出來
			a = user.bloodinfo_set.all()
			print(a)
			print(request.get_full_path())
			data = request.get_full_path()
			data = data.split('?')[1]
			data = data.replace('%5B%5D%5B%5D=',"")
			data = data.split("&")
			for i in range(len(data)):
				data[i] = data[i].replace("ids","")
			print(data)
			for i in range(len(data)):
				num = data[i]
				a.get(id = num).delete()
			# data = request.get_full_path()
			# data = data.split('=')[1][1:-1]
			# data = data.split(',')
			# print(data)
			# for i in data:
			# 	a.get(id = int(i)).delete()
			result = {'status':'0'}
	#except:
		#pass
		print(result)
	return JsonResponse(result)

def medicine(request):
	result = {'status':'1'}#預設失敗
	if 1:
	#try:
		if request.method == 'GET':
			#從DD那抓出information
			session_key = request.headers.get('Authorization')[7:]#從header抓出session key
			authuser = Session.objects.get(session_key=session_key).get_decoded()['_auth_user_id']#把跟session key合的user授權抓出來解碼
			user = patient.objects.get(id = authuser)#把資訊從資料庫拉出來
			a = user.medi_set.all()
			#result = {'status':'0','a1cs':{'id':1,'user_id':1,'a1c':user.blood_set.a1c,'recorded_at':'','created_at':user.created_at,'update_at':user.update_at}}#成功
			result = {'status':'0'}#成功
			result['drug_useds'] = []
			for item in a:
				record = {}
				record["id"] = item.id
				record['user_id'] = user.id
				record['typee'] = item.typee
				record['name'] = item.hospitalname
				if item.recorded_at:
					record['recorded_at'] = item.recorded_at.strftime("%Y-%m-%d %H:%M:%S")
				result["drug_useds"].append(record)
		if request.method == 'POST':
			session_key = request.headers.get('Authorization')[7:]#從header抓出session key
			authuser = Session.objects.get(session_key=session_key).get_decoded()['_auth_user_id']#把跟session key合的user授權抓出來解碼
			user = patient.objects.get(id = authuser)#把資訊從資料庫拉出來

			med = medi.objects.create(patient = user)#建立新表單
			form = mediForm(request.POST)#填入表單
			print(request.POST)
			if form.is_valid():#檢查forms.py中的格式
				data = form.cleaned_data#接form裡面丟出來的資料
				print('-'*50)
			typee = form.cleaned_data['typee']
			recorded_at = form.cleaned_data['recorded_at']
			hospitalname = form.cleaned_data['hospitalname']
			med.recorded_at = recorded_at
			med.typee = typee
			med.hospitalname = hospitalname
			med.save()
			result = {'status':'0'}
		if request.method == 'DELETE':
			session_key = request.headers.get('Authorization')[7:]#從header抓出session key
			authuser = Session.objects.get(session_key=session_key).get_decoded()['_auth_user_id']#把跟session key合的user授權抓出來解碼
			user = patient.objects.get(id = authuser)#把資訊從資料庫拉出來
			a = user.medi_set.all()
			print(request.get_full_path())
			data = request.get_full_path()
			data = data.split('?')[1]
			data = data.replace('%5B%5D%5B%5D=',"")
			data = data.split("&")
			print(data)
			for i in range(len(data)):
				data[i] = data[i].replace("ids","")
			print(data)
			for i in range(len(data)):
				num = data[i]
				a.get(id = num).delete()
			result = {'status':'0'}
	#except:
		#pass
	return JsonResponse(result)
def mediinfo(request):
	result = {'status':'1'}#預設失敗
	if 1:
	#try:
		if request.method == 'PATCH':
			session_key = request.headers.get('Authorization')[7:]#從header抓出session key
			authuser = Session.objects.get(session_key=session_key).get_decoded()['_auth_user_id']#把跟session key合的user授權抓出來解碼
			user = patient.objects.get(id = authuser)#把資訊從資料庫拉出來
			print(user)

			raw = request.body.decode('UTF-8')
			table = {'%40': '@'}#alter
			for char in table:#把長串資料用&分開
				raw = raw.replace(char, table[char])
			rawlist = raw.split('&')

			data = {var.split('=')[0] : var.split('=')[1] for var in rawlist if var.split('=')[1]}#分開後用=轉成dict
			form = diabeteForm(data)
			if form.is_valid():
				data = form.cleaned_data
				print(data)
				for index in data:
					if data[index]:
						setattr(user.diabete, index, data[index])
				user.diabete.save()#save
				result = {'status':'0'}

		if request.method == 'GET':
			session_key = request.headers.get('Authorization')[7:]#從header抓出session key
			authuser = Session.objects.get(session_key=session_key).get_decoded()['_auth_user_id']#把跟session key合的user授權抓出來解碼
			user = patient.objects.get(id = authuser)#把資訊從資料庫拉出來
			if user.diabete.diabetes_type:
				user.diabete.diabetes_type = user.diabete.diabetes_type
			else:
				user.diabete.diabetes_type = 1
			if user.diabete.oad:
				user.diabete.oad = int(user.diabete.oad)
			else:
				user.diabete.oad = 1
			if user.diabete.insulin:
				user.diabete.insulin = int(user.diabete.insulin)
			else:
				user.diabete.insulin = 1
			if user.diabete.anti_hypertensives:
				user.diabete.anti_hypertensives = int(user.diabete.anti_hypertensives)
			else:
				user.diabete.anti_hypertensives = 1
			result = {
			"status": "0",
			"medical_info": {
				"id": int(user.id),
				"user_id": int(user.id),
				"diabetes_type": int(user.diabete.diabetes_type),
				"oad": int(user.diabete.oad),
				"insulin": int(user.diabete.insulin),
				"anti_hypertensives": int(user.diabete.anti_hypertensives),
				"created_at": user.created_at.strftime("%Y-%m-%d %H:%M:%S"),
				"updated_at": user.diabete.update_at.strftime("%Y-%m-%d %H:%M:%S")
							}
					}#成功
	#except:
		#pass
	return JsonResponse(result)

def news(request):
	result = {'status':'1'}#預設失敗
	if 1:
	#try:
		if request.method == 'GET':
			result = {'status':'0',
			"news":[]
			}#成功
	#except:
		#pass
	return JsonResponse(result)
def bage(request):
	result = {'status':'1'}#預設失敗
	if 1:
	#try:
		if request.method == 'PUT':
			session_key = request.headers.get('Authorization')[7:]#從header抓出session key
			authuser = Session.objects.get(session_key=session_key).get_decoded()['_auth_user_id']#把跟session key合的user授權抓出來解碼
			user = patient.objects.get(id = authuser)#把資訊從資料庫拉出來
			print(user)
			# if request.body['badge']:
			print(request.body)
			raw = request.body.decode('UTF-8')
			table = {'%40': '@'}#alter
			for char in table:#把長串資料用&分開
				raw = raw.replace(char, table[char])
			rawlist = raw.split('&')

			data = {var.split('=')[0] : var.split('=')[1] for var in rawlist if var.split('=')[1]}#分開後用=轉成dict
			user.badge = data["badge"]
			user.save()
			print(user.badge)
			result = {'status':'0'}#成功
	#except:
		#pass
	return JsonResponse(result)
# def a1c(request):
# 	result = {'status':'1'}#預設失敗
# 	if 1:
# 	#try:
# 		if request.method == 'DELETE':
# 			session_key = request.headers.get('Authorization')[7:]#從header抓出session key
# 			authuser = Session.objects.get(session_key=session_key).get_decoded()['_auth_user_id']#把跟session key合的user授權抓出來解碼
# 			user = patient.objects.get(id = authuser)#把資訊從資料庫拉出來
# 			a = user.bloodinfo_set.all()
# 			#idsinbloodinfo.ids = request.body['ids']
# 			print(request.body.decode("utf8"))
# 			raw = request.body.decode("utf8")
# 			table = {'%40': '@', '%5B': '', '%2C': ',', '%5D': ''}#alter
# 			for char in table:#把長串資料用&分開
# 				raw = raw.replace(char, table[char])
# 			rawlist = raw.split('&')

# 			data = {var.split('=')[0] : var.split('=')[1] for var in rawlist if var.split('=')[1]}#分開後用=轉成dict
# 			data = list(map(lambda x: int(x), data['ids'].split(',')))
# 			print(data)
# 			print(request.get_full_path())
# 			for i in data:
# 				user.bloodinfo_set.get(id=i).delete()
# 			result = {'status':'0'}
# 	#except:
# 		#pass
# 	return JsonResponse(result)