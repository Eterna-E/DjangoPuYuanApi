from django.http import JsonResponse 
from .forms import *
from django.contrib import auth
from django.contrib.sessions.models import Session
import random
import string

from Denru.models import *
from django.core.mail import send_mail
import smtplib
from django.http import HttpResponse
from friend.models import Friend

# 註冊確認
def RegCheck(request):
	result = {'status': '0'}
	try:
		if request.method == 'GET':
			username = request.GET['account']
			username = username.replace('%40', '@')
			patient.objects.get(email=username)
			result['status'] = '1'
	except:
		pass
	return JsonResponse(result)
# FB
def pp(request):
	result = {'status': '0'}
	return JsonResponse(result)
# 註冊
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
				email = form.cleaned_data['email']#抓電郵
				password = form.cleaned_data['password']#抓密碼
				print(password)
				username = username.replace('%40', '@')#email @ alter
				email = email.replace('%40', '@')
				invite_code = "".join(random.sample('0123456789',6))
				user = patient.objects.create(username=username,email=email ,invite_code=invite_code)#創建使用者
				#新增表單
				sugarinfo.objects.create(patient = user)
				diabete.objects.create(patient = user)
				user.set_password(password)
				print(user.username)
				user.save()
				Friend.objects.create(uid=user.id,invite_code=invite_code)
				result['status'] = '0'#創建成功
		#except:
		#	pass
	return JsonResponse(result)
#登入Session
def login(request):
	if request.method == 'POST':
		# if 1 :
		result = {'status': '1'}#登入失敗
		user = auth.authenticate(username=request.POST['account'], password=request.POST['password'])
		auth.login(request, user)
		try:
			#把資訊從資料庫拉出來
			if user is not None and user.is_active:
				user = patient.objects.get(username = request.POST['account'])
				user.login_times = str(int(user.login_times) + 1)
				user.save()
				result = {'status': '0','token': request.session.session_key}#登入成功		except:
		except:
			pass
	return JsonResponse(result)
#傳驗證碼
def sendcode(request):
	result = {'status': '1'}
	if request.method == 'POST': 
		# if 1:
		try:
			print(request.body)
			email = request.POST['email']#抓POSTemail
			email = email.replace('%40', '@')
			print(email)
			code = ''.join(random.sample(string.ascii_letters + string.digits, 10))#生成10位驗證碼
			userinfo = checkcode.objects.create(code=code,email=email)#把抓到的送進資料庫
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
		print(result)
	return JsonResponse(result)
#檢查驗證碼
def codechecking(request):
	if request.method == 'POST':
		#if 1:
		try:
			if checkcode.objects.get(email=request.POST['email']):#如果phone存在且一樣
				if checkcode.objects.get(code=request.POST['code']):#如果打進來的phone跟code一樣就
					result = {'status': '0'}#驗證成功 
		except:
			result = {'status': '1'}#驗證失敗
	return JsonResponse(result)

#忘記密碼
def forget(request):
	if request.method == 'POST':
		#if 1:
		result = {'status': '1'}#
		try:
			user = patient.objects.get(email=request.POST['email'])#抓出那個人的密碼.email
			email = user.email
			newPW = ''.join(random.sample(string.ascii_letters + string.digits, 10))#生成10位暫時密碼
			user.set_password(newPW)#更改資料庫中的密碼
			user.must_change_password = True
			user.save()#儲存資訊
			#傳更改的新密碼給user
			send_mail(
				'gai mi ma',
				newPW,
				"davidwu5858@gmail.com",
				[email],
				fail_silently=False,
			)
			result = {'status': '0'}#更改成功
		except:
			pass
	return JsonResponse(result)

#重設密碼
def reset(request):
	if request.method == 'POST':
		#if 1:
		try:
			session_key = request.headers.get('Authorization')[7:]#從header抓出session key
			authuser = Session.objects.get(session_key=session_key).get_decoded()['_auth_user_id']#把跟session key合的user授權抓出來解碼
			user = patient.objects.get(id = authuser)#把資訊從資料庫拉出來
			password = request.POST['password']#抓POST_password
			user.set_password(password)#資料庫密碼重設
			user.save()#儲存資訊
			result = {'status': '0'}#重設成功
		except:
			result = {'status': '1'}#重設失敗
	return JsonResponse(result)

