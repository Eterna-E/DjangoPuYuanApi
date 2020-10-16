from django.http import JsonResponse
from Denru.models import *
from .forms import *
from django.contrib import auth
from django.contrib.sessions.models import Session
import random
import string

from django.core.mail import send_mail
import smtplib
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

# 註冊確認
@csrf_exempt
def RegCheck(request):
	result = {'status': '0'}
	try:
		if request.method == 'GET':
			username = request.GET['account']
			username = username.replace('%40', '@')
			patient.objects.get(username=username)
			result['status'] = '1'
	except:
		pass
	return JsonResponse(result)
# FB
@csrf_exempt
def pp(request):
	result = {'status': '0'}
	return JsonResponse(result)
# 註冊
@csrf_exempt
def Reg(request):
	if request.method == 'POST':
		result = {'status': '1'}#預設失敗
		if 1:
		#try:
			form = PatientForm(request.POST)
			print(request.POST)
			if form.is_valid():#檢查forms.py中的格式
				data = form.cleaned_data#接form裡面丟出來的資料
			username = form.cleaned_data['account']#抓名字
			phone = form.cleaned_data['phone']#抓電話
			email = form.cleaned_data['email']#抓電郵
			password = form.cleaned_data['password']#抓密碼
			username = username.replace('%40', '@')#email @ alter
			email = email.replace('%40', '@')
			user = patient.objects.create(username=username,phone=phone,email=email)#創建使用者
			#新增表單
			sugarinfo.objects.create(patient = user)
			user.set_password(password)
			print(user.username)
			user.save()

			result['status'] = '0'#創建成功
		#except:
		#	pass
	return JsonResponse(result)
#登入Session
@csrf_exempt
def login(request):
	if request.method == 'POST':
		if 1 :
			user = auth.authenticate(username=request.POST['account'], password=request.POST['password'])
			auth.login(request, user)
			#把資訊從資料庫拉出來
		#try:
			if user is not None and user.is_active:
				user = patient.objects.get(username = request.POST['account'])
				user.login_times = str(int(user.login_times) + 1)
				user.save()
				result = {'status': '0','token': request.session.session_key}#登入成功
			else:
				result = {'status': '1'}#登入失敗
		#except:
			#pass
	return JsonResponse(result)
#傳驗證碼
@csrf_exempt
def sendcode(request):
	if request.method == 'POST': 
		#if 1:
		try:
			phone = request.POST['phone']#抓POST號碼
			email = request.POST['email']#抓POSTemail
			code = ''.join(random.sample(string.ascii_letters + string.digits, 10))#生成10位驗證碼
			userinfo = checkcode.objects.create(phone=phone,code=code,email=email)#把抓到的送進資料庫
			send_mail(
				'yanzhenma',
				code,
				'davidwu5858@gmail.com',
				[email],
				fail_silently=False,
			)
			userinfo.save()
			result = {'status': '0'}#傳送成功
		except:
			result = {'status': '1'}#傳送失敗
	return JsonResponse(result)
#檢查驗證碼
@csrf_exempt
def codechecking(request):
	if request.method == 'POST':
		#if 1:
		try:
			print(123)
			print(checkcode.objects.get(phone='0999000111'))
			if checkcode.objects.get(phone=request.POST['phone']):#如果phone存在且一樣
				if checkcode.objects.get(code=request.POST['code']):#如果打進來的phone跟code一樣就
					result = {'status': '0'}#驗證成功
		except:
			result = {'status': '1'}#驗證失敗
	return JsonResponse(result)

#忘記密碼
@csrf_exempt
def forget(request):
	if request.method == 'POST':
		#if 1:
		try:
			user = patient.objects.get(email=request.POST['email'])#抓出那個人的密碼.email
			email = user.email
			newPW = ''.join(random.sample(string.ascii_letters + string.digits, 10))#生成10位暫時密碼
			user.set_password(newPW)#更改資料庫中的密碼
			user.save()#儲存資訊
			#傳更改的新密碼給user
			send_mail(
				'gai mi ma',
				newPW,
				'davidwu5858@gmail.com',
				[email],
				fail_silently=False,
			)
			result = {'status': '0'}#更改成功
		except:
			result = {'status': '1'}#更改失敗
	return JsonResponse(result)

#重設密碼
@csrf_exempt
def reset(request):
	if request.method == 'POST':
		#if 1:
		try:
			session_key = request.headers.get('Authorization')#從header抓出session key
			# print(session_key)
			authuser = Session.objects.get(session_key=session_key).get_decoded()['_auth_user_id']#把跟session key合的user授權抓出來解碼
			user = patient.objects.get(id = authuser)#把資訊從資料庫拉出來
			password = request.POST['password']#抓POST_password
			user.set_password(password)#資料庫密碼重設
			user.save()#儲存資訊
			result = {'status': '0'}#重設成功
		except:
			result = {'status': '1'}#重設失敗
	return JsonResponse(result)

