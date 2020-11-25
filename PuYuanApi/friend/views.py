from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib import auth
from .models import *
# from user.models import *
from datetime import date, datetime
from django.views.decorators.csrf import csrf_exempt
import json
from Denru.models import patient
from measure.models import *
from django.contrib.sessions.models import Session
import json


@csrf_exempt
def friend_code(request):  # 16.獲取控糖團邀請碼
	session_key = request.headers.get('Authorization')[7:]  # 從header抓出session key
	authuser = Session.objects.get(session_key=session_key).get_decoded()['_auth_user_id']  # 把跟session key合的user授權抓出來解碼，取得user id
	uid = authuser
	if request.method == "GET":
		output = {"status": "1"}#預設失敗
		try:
			print("正在提取使用者資料...")
			get_user = Friend.objects.get(uid=uid)
			print("正在取使用者邀請碼...")
			output = {"status": "0", "invite_code": get_user.invite_code}
		except:
			pass
	return JsonResponse(output, safe=False)


@csrf_exempt
def friend_list(request):  # 17.控糖團列表
	session_key = request.headers.get('Authorization')[7:]  # 從header抓出session key
	authuser = Session.objects.get(session_key=session_key).get_decoded()['_auth_user_id']  # 把跟session key合的user授權抓出來解碼，取得user id
	uid = authuser #4
	print("登入的uid為:"+uid)
	if request.method == 'GET':
		output = {"status": "1"}#預設失敗
		empty_array_for_friends = []#空陣列
		try:
			print("正在提取已加為好友...")
			accepted_friends = Friend_data.objects.filter(uid=uid, status=1)
			for friend in accepted_friends:
				print("已提取的好友uid為:"+friend.relation_id)
				accepter = patient.objects.get(id=friend.relation_id)
				print("正在轉換生日資料型態...")
				if accepter.birthday != None:
					bir = accepter.birthday.strftime("%Y-%m-%d")
				else:
					bir = "1999-01-01"
				if accepter.gender == True:
					gen = "男"
				elif accepter.gender == False:
					gen = "女"
				else:
					gen = "女"
				print("正在建構朋友的基本資料字典...")
				print(friend.friend_type)
				friend_basic_datas = {
					"id": str2int(accepter.id),
					"name": accepter.name,
					"account": accepter.email,
					"email": accepter.email,
					"phone": accepter.phone,
					"fb_id": "1",
					"status": "Normal",
					"group": accepter.group,
					"birthday": bir,
					"height": str2int(accepter.height),
					"gender": gen,
					"verified": boolean2int(accepter.email_verfied),
					"privacy_policy": boolean2int(accepter.privacy_policy),
					"must_change_password": boolean2int(accepter.must_change_password),
					"badge": str2int(accepter.badge),
					"created_at": accepter.created_at.strftime('%Y-%m-%d %H:%M:%S'),
					"updated_at": accepter.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
					"relation_type": int(friend.friend_type)
				}

				#print(friend_basic_datas)
				# friend_basic_datas = {
		  #           "id": 2,
		  #           "name": "baka",
		  #           "account": "fb_1",
		  #           "email": "davidwu5858@gmail.com",
		  #           "phone": "0987654321",
		  #           "fb_id": "1",
		  #           "status": "Normal",
		  #           "group": "0",
		  #           "birthday": "1995-10-10",
		  #           "height": 171,
		  #           "gender": "男",
		  #           "verified": 1,
		  #           "privacy_policy": 1,
		  #           "must_change_password": 0,
		  #           "badge": 87,
		  #           "created_at": "2017-10-23 14:39:06",
		  #           "updated_at": "2017-10-23 19:41:53",
		  #           "relation_type": 2
		  #       }
				print("朋友的基本資料字典已建構完畢...")
				empty_array_for_friends.append(friend_basic_datas)
				print("正在回傳朋友的基本資料字典...")
				output = {"status": "0", "friends": empty_array_for_friends}
				print("朋友的基本資料字典回傳完畢...")
				print(empty_array_for_friends)
		except:
			pass
	return JsonResponse(output)


@csrf_exempt
def friend_requests(request):  # 18.獲取控糖團邀請
	session_key = request.headers.get('Authorization')[7:]  # 從header抓出session key
	authuser = Session.objects.get(session_key=session_key).get_decoded()['_auth_user_id']  # 把跟session key合的user授權抓出來解碼，取得user id
	uid = authuser#5 send to 7 , 7 login , 
	# print(uid)
	if request.method == "GET":
		output = {"status": "1"}
		try:
		# if 1:
			print("正在提取寄給本帳號的邀請...")
			requests_list = Friend_data.objects.filter(relation_id=uid, status=0)
			print("寄給本帳號的邀請提取完畢...")
			requests = []
			for request in requests_list:
				user = patient.objects.get(id = uid)
				created_at_friendata = datetime.strftime(request.created_at, '%Y-%m-%d %H:%M:%S')
				updated_at_friendata = datetime.strftime(request.updated_at, '%Y-%m-%d %H:%M:%S')
				if user.birthday != None:
					bir = user.birthday.strftime('%Y-%m-%d')
				else:
					bir = "1999-01-01"
				r = {
					"id": request.id,
					"user_id": str2int(request.uid),
					"relation_id": str2int(request.uid),
					"type": str2int(request.friend_type),
					"status": str2int(request.status),
					"created_at": created_at_friendata,
					"updated_at": updated_at_friendata,
					"user": {
						"id": user.id,
						"name": user.name,
						"account": user.email,
						"email": user.email,
						"phone": user.phone,
						"fb_id": "1",
						"status": user.status,
						"group": user.group,
						"birthday": bir,
						"height": str2int(user.height),
						"gender": boolean2int(user.gender),
						"verified": boolean2int(user.email_verfied),
						"privacy_policy": boolean2int(user.privacy_policy),
						"must_change_password": boolean2int(user.must_change_password),
						"badge": str2int(user.badge),
						"created_at": "2017-10-20 15:43:47",
						"updated_at": "2017-10-20 15:43:54"
					}
				}
				emptydict = {}
				print(r)
				if r == emptydict:
					raise Exception("r裡面沒東西")
				requests.append(r)
				output = {"status": "0", "requests": requests}
		except:
			print(e)
	return JsonResponse(output)


@csrf_exempt
def friend_send(request):  # 19.送出控糖團邀請
	session_key = request.headers.get('Authorization')[7:]  # 從header抓出session key
	authuser = Session.objects.get(session_key=session_key).get_decoded()['_auth_user_id']  # 把跟session key合的user授權抓出來解碼，取得user id
	uid = authuser
	if request.method == 'POST':
		print(request.body)
		output = {"status": "1"}#預設不成功
		nowtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		data = str(request.body).replace('b', '').replace("\\r\\n", '').replace('\'', '')
		data = data.split('&')
		friend_type = data[1].replace('type=', '')
		invite_code = int(data[0].replace('invite_code=', ''))
		# try:
		# 	user_friend = Friend.objects.get(invite_code=invite_code)
		# 	friend_uid = user_friend.uid
		# except:
		# 	output = {"status": "1"}  # 1: 邀請碼無效
		# 	print(123)
		# else:
		# 	try:
		# 		Friend_data.objects.get(uid=uid, relation_id=friend_uid,friend_type = friend_type)
		# 	except:
		# 		try:
		# 			Friend_data.objects.create(uid=uid, relation_id=friend_uid,read=True, status=0, friend_type=friend_type, updated_at=nowtime)
		# 		except:
		# 			output = {"status": "1"}
		# 		else:
		# 			output = {"status": "0"}
		# 	else:
		# 		output = {"status": "2"}  # 2: 已經發送過邀請
		try:
			print("抓出朋友")
			user_friend = Friend.objects.get(invite_code=invite_code) #抓出朋友
			print("抓出朋友uid")
			friend_uid = user_friend.uid #抓出朋友uid
			print("檢查朋友是否邀請過")
			try: #如果之前有送過邀請
				Friend_data.objects.get(uid = uid, relation_id = friend_uid)
				output = {"status": "2"}#顯示已經寄過邀請
				print("已經寄過邀請囉")
			except: #如果沒有寄過邀請
				Friend_data.objects.create(uid=uid, relation_id=friend_uid,read=True, status=0, friend_type=friend_type, updated_at=nowtime)
				#建立邀請物件
				output = {"status": "0"}
				print("邀請已送出")
				#顯示邀請已寄出
		except:
			print("發生錯誤")
		return JsonResponse(output, safe=False)


@csrf_exempt
def friend_accept(request, friend_data_id):  # 20.接受控糖團邀請
	output = {"status": "1"}
	if request.method == "GET":
		session_key = request.headers.get('Authorization')[ 7:]  # 從header抓出session key
		authuser = Session.objects.get(session_key=session_key).get_decoded()['_auth_user_id']  # 把跟session key合的user授權抓出來解碼，取得user id
		uid = authuser
		nowtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		print(1234)
		try:
			check = Friend_data.objects.get(id=friend_data_id, status=0)
			print(456)
			Friend_data.objects.create(uid=uid, relation_id=check.uid, status=1, read=True,imread=True, friend_type=check.friend_type, updated_at=nowtime)
			check.read = True
			check.status = 1
			check.updated_at = nowtime
			check.save()
			output = {"status": "0"}
		except:
			pass
	return JsonResponse(output, safe=False)


@csrf_exempt
def friend_refuse(request, friend_data_id):  # 21.拒絕控糖團邀請
	# uid = request.user.id
	nowtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	try:
		check = Friend_data.objects.get(id=friend_data_id, status=0)
		check.read = True
		check.imread = True
		check.status = 2
		check.updated_at = nowtime
		check.save()
	except:
		output = {"status": "1"}
	else:
		output = {"status": "0"}
	return JsonResponse(output, safe=False)


@csrf_exempt
def friend_remove(request, friend_data_id):  # 22.刪除控糖團邀請
	# uid = request.user.id
	if request.method == 'GET':
		try:
			Friend_data.objects.filter(id=friend_data_id, status=0).delete()
		except:
			output = {"status": "1"}
		else:
			output = {"status": "0"}
		return JsonResponse(output, safe=False)


@csrf_exempt
def friend_results(request):  # 26.控糖團結果
	session_key = request.headers.get('Authorization')[7:]  # 從header抓出session key
	authuser = Session.objects.get(session_key=session_key).get_decoded()['_auth_user_id']  # 把跟session key合的user授權抓出來解碼，取得user id
	uid = authuser
	output = {"status": "1"}
	if request.method == 'GET':
		results = []
		if Friend_data.objects.filter(uid=uid, read=True,imread = False):
			print("我要進來囉")
			result = Friend_data.objects.filter(uid=uid, read=True ,imread = False)
			print(result)
			for user in result:
				accepter = patient.objects.get(id=user.relation_id)
				relation = patient.objects.get(id=accepter.id)
				created_at_friendata = datetime.strftime(user.created_at, '%Y-%m-%d %H:%M:%S')
				updated_at_friendata = datetime.strftime(user.updated_at, '%Y-%m-%d %H:%M:%S')
				created_at_userfile = datetime.strftime(relation.created_at, '%Y-%m-%d %H:%M:%S')
				updated_at_userfile = datetime.strftime(relation.updated_at, '%Y-%m-%d %H:%M:%S')
				if relation.birthday != None:
					bir = relation.birthday.strftime('%Y-%m-%d')
				else:
					bir = "1999-01-01"
				r = {
					"id": str2int(user.uid),
					"user_id": str2int(user.uid),
					"relation_id": str2int(user.relation_id), 
					"type": str2int(user.friend_type),
					"status": str2int(user.status),
					"read": user.read,
					"created_at": created_at_friendata,
					"updated_at": updated_at_friendata,
					"relation":
					{
						"id": accepter.id,
						"name": relation.name,
						"account": relation.email,
						"email": relation.email,
						"phone": relation.phone,
						"fb_id": "1",
						"status": "Normal",
						"group": relation.group,
						"birthday": bir,
						"height": str2int(relation.height),
						"gender": boolean2int(relation.gender),
						"unread_records": "[0,0,0]",
						"verified": boolean2int(relation.email_verfied),
						"privacy_policy": boolean2int(relation.privacy_policy),
						"must_change_password": boolean2int(relation.must_change_password),
						"badge": str2int(relation.badge),
						"created_at": created_at_userfile,
						"updated_at": updated_at_userfile
					}
				}
				user.imread = True
				user.save()
				results.append(r)
				print(r)
				print("ccccccccccccccccccccccccccccc")
		output = {"status": "0", "results": results}
	return JsonResponse(output)


@csrf_exempt
def friend_remove_more(request):  # 37.刪除更多好友
	session_key = request.headers.get('Authorization')[7:]  # 從header抓出session key
	authuser = Session.objects.get(session_key=session_key).get_decoded()['_auth_user_id']  # 把跟session key合的user授權抓出來解碼，取得user id
	uid = authuser#7
	output = {"status": "1"}
	if request.method == 'DELETE':
		# ids_list = request.GET.getlist("ids[]")
		# print(ids_list)
		data = request.get_full_path().split('?')[1]
		data = data.split('=')[1]
		data = str(data)
		uid = str(uid)
		print(data,uid)
		try:
			Friend_data.objects.get(uid=uid, relation_id=data, status=1).delete()
			Friend_data.objects.get(uid=data, relation_id=uid, status=1).delete()
			output = {"status": "0"}
		except:
			pass
	return JsonResponse(output)


@csrf_exempt
def notification(request):  # 36.親友團通知
	session_key = request.headers.get('Authorization')[
		7:]  # 從header抓出session key
	authuser = Session.objects.get(session_key=session_key).get_decoded()[
		'_auth_user_id']  # 把跟session key合的user授權抓出來解碼，取得user id
	uid = authuser
	if request.method == 'POST':
		nowtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
		print(request.body)
		data = str(request.body, encoding="utf-8").replace('b',
														   '').replace("\\r\\n", '').replace('\'', '')
		print(data)
		data = json.loads(data)
		message = data['message']
		try:
			friend_list = Friend_data.objects.filter(
				uid=uid, friend_type=0, status=1)
			for friend in friend_list:
				Notification.objects.create(
					uid=uid, member_id=1, reply_id=friend.relation_id, message=message, updated_at=nowtime)
		except:
			output = {"status": "1"}
		else:
			output = {"status": "0"}
		return JsonResponse(output, safe=False)


@csrf_exempt
def share(request,type_of = "-1"):  # 23.分享
	session_key = request.headers.get('Authorization')[7:]  # 從header抓出session key
	authuser = Session.objects.get(session_key=session_key).get_decoded()['_auth_user_id']  # 把跟session key合的user授權抓出來解碼，取得user id
	uid = authuser
	if request.method == 'POST':
		output = {"status": "0"}
		try:
			print(request.body)
			data = str(request.body).replace('b', '').replace('%40','@').replace("'","")
			print(data)
			data = data.split('&')
			print(data)
			share_id = data[0].replace('id=', '')
			relation_type = data[1].replace('relation_type=', '')
			data_type = data[2].replace('type=', '')
			# account = data[0].replace("account=","")
			# password = data[1].replace("password=","")
			# phone = data[2].replace("phone=","")
			# invite_code = data[3].replace("invite_code=","")
			# typee = data[4].replace("type=","")
			# print(account,password,phone,invite_code,typee)
			try:
				Share.objects.create(uid=uid, fid=share_id, data_type=data_type, relation_type=relation_type)
				output = {"status": "0"}
			except:
				pass
		except:
			pass
	return JsonResponse(output, safe=False)

def int2str(data):
	if data:
		data = str(data)
	else:
		data = "1"
	return data
def str2int(data):
	if data:
		data = int(data)
	else:
		data = 1
	return data
def boolean2int(data):
	if data == None:
		data = 0
	elif data == True:
		data = 1
	else:
		data = 0
	return data
@csrf_exempt
def share_check(request, relation_type):  # 24.查看分享（含自己分享出去的）
	session_key = request.headers.get('Authorization')[7:]  # 從header抓出session key
	authuser = Session.objects.get(session_key=session_key).get_decoded()['_auth_user_id']  # 把跟session key合的user授權抓出來解碼，取得user id
	uid = authuser
	print('relation_type:', relation_type)
	print(type(relation_type))
	if request.method == 'GET':
		output = {"status": "1"}
		if Share.objects.filter(relation_type=relation_type):
			share_checks = Share.objects.filter(relation_type=relation_type)

			# print("我在這裡啦")
			datas = []
			for share_check in share_checks:
				# print("uid :"+share_check.uid,"fid :"+share_check.fid)
				user = patient.objects.get(id=uid)
				# print("qwerqwerqwerewrqewrqwerwqer")
				if user.birthday != None:
					birthday = user.birthday.strftime('%Y-%m-%d')
				else:
					birthday = "1999-11-01"
				r = None
				if share_check.data_type == '0':
					share_data = Pressure.objects.get(uid=share_check.uid, id=share_check.fid)
					created_at = datetime.strftime(share_data.created_at, '%Y-%m-%d %H:%M:%S')
					recorded_at = datetime.strftime(share_data.recorded_at, '%Y-%m-%d %H:%M:%S')
					created_at_userfile = datetime.strftime(user.created_at, '%Y-%m-%d %H:%M:%S')
					updated_at_userfile = datetime.strftime(user.updated_at, '%Y-%m-%d %H:%M:%S')
					r = {
						"id": share_data.id,
						"user_id": str2int(share_data.uid),
						"systolic": str2int(share_data.systolic),
						"diastolic": str2int(share_data.diastolic),
						"pulse": str2int(share_data.pulse),
						"recorded_at": recorded_at,
						"created_at": created_at,
						"type": 0,
						"user": {
							"id": user.id,
							"name": int2str(user.name),
							"account": user.email,
							"email": user.email,
							"phone": int2str(user.phone),
							"fb_id": "1",
							"status": int2str(user.status),
							"group": user.group,
							"birthday": birthday,
							"height": str2int(user.height),
							"gender": boolean2int(user.gender),
							"verified": boolean2int(user.email_verfied),
							"privacy_policy": str2int(user.privacy_policy),
							"must_change_password": boolean2int(user.must_change_password),
							"badge": str2int(user.badge),
							"created_at": created_at_userfile,
							"updated_at": updated_at_userfile
						}
					}
					# print(r)
				if share_check.data_type == '1':
					try:
						share_data = Weight.objects.get(uid=share_check.uid, id=share_check.fid)
						created_at = datetime.strftime(share_data.created_at, '%Y-%m-%d %H:%M:%S')
						recorded_at = datetime.strftime(share_data.recorded_at, '%Y-%m-%d %H:%M:%S')
						created_at_userfile = datetime.strftime(user.created_at, '%Y-%m-%d %H:%M:%S')
						updated_at_userfile = datetime.strftime(user.updated_at, '%Y-%m-%d %H:%M:%S')
						# print("我又進來囉")
						r = {
							"id": share_data.id,
							"user_id": share_data.uid,
							"weight": float(share_data.weight),
							"body_fat": float(share_data.body_fat),
							"bmi": float(share_data.bmi),
							"recorded_at": recorded_at,
							"created_at": created_at,
							"type": 1,
							"user": {
								"id": user.id,
								"name": user.name,
								"account": user.email,
								"email": user.email,
								"phone": int2str(user.phone),
								"fb_id": None,
								"status": int2str(user.status),
								"group": user.group,
								"birthday": birthday,
								"height": str2int(user.height),
								"gender": boolean2int(user.gender),
								"verified": boolean2int(user.email_verfied),
								"privacy_policy": str2int(user.privacy_policy),
								"must_change_password": boolean2int(user.must_change_password),
								"badge": str2int(user.badge),
								"created_at": created_at_userfile,
								"updated_at": updated_at_userfile
							}
						}
						# print(r)
					except:
						pass
				if share_check.data_type == '2':
					try:
						share_data = Sugar.objects.get(uid=share_check.uid, id=share_check.fid)
						created_at = datetime.strftime(share_data.created_at, '%Y-%m-%d %H:%M:%S')
						recorded_at = datetime.strftime(share_data.recorded_at, '%Y-%m-%d %H:%M:%S')
						created_at_userfile = datetime.strftime(user.created_at, '%Y-%m-%d %H:%M:%S')
						updated_at_userfile = datetime.strftime(user.updated_at, '%Y-%m-%d %H:%M:%S')
						r = {
							"id": share_data.id,
							"user_id": str2int(share_data.uid),
							"sugar": float(share_data.sugar),
							"timeperiod": str2int(share_data.timeperiod),
							"recorded_at": recorded_at,
							"created_at": created_at,
							"type": 2,
							"user": {
								"id": user.id,
								"name": int2str(user.name),
								"account": user.email,
								"email": user.email,
								"phone": int2str(user.phone),
								"fb_id": "1",
								"status": int2str(user.status),
								"group": user.group,
								"birthday": birthday,
								"height": user.height,
								"gender": boolean2int(user.gender),
								"verified": boolean2int(user.email_verfied),
								"privacy_policy": str2int(user.privacy_policy),
								"must_change_password": boolean2int(user.must_change_password),
								"badge": str2int(user.badge),
								"created_at": created_at_userfile,
								"updated_at": updated_at_userfile
							}
						}
						# print(r)
					except:
						pass
				if share_check.data_type == '3':
					try:
						share_data = Diary_diet.objects.get(uid=share_check.uid, id=share_check.fid)
						created_at = datetime.strftime(share_data.created_at, '%Y-%m-%d %H:%M:%S')
						recorded_at = datetime.strftime(share_data.recorded_at, '%Y-%m-%d %H:%M:%S')
						created_at_userfile = datetime.strftime(user.created_at, '%Y-%m-%d %H:%M:%S')
						updated_at_userfile = datetime.strftime(user.updated_at, '%Y-%m-%d %H:%M:%S')
						image_count = str(share_data.image_count)
						r = {
							"id": share_data.id,
							"user_id": str2int(share_data.uid),
							"description": share_data.description,
							"meal": int(share_data.meal),
							"tag": share_data.tag,
							# "image":str(image),
							"image_count": share_data.image_count,
							"lat": share_data.lat,
							"lng": share_data.lng,
							"recorded_at": recorded_at,
							"created_at": created_at,
							"type": 3,
							"user": {
								"id": user.id,
								"name": user.name,
								"account": user.email,
								"email": user.email,
								"phone": int2str(user.phone),
								"fb_id": None,
								"status": user.status,
								"group": user.group,
								"birthday": birthday,
								"height": user.height,
								"gender": user.gender,
								"verified": boolean2int(user.email_verfied),
								"privacy_policy": str2int(user.privacy_policy),
								"must_change_password": boolean2int(user.must_change_password),
								"badge": str2int(user.badge),
								"created_at": created_at_userfile,
								"updated_at": updated_at_userfile
							}
						}
						# print(r)
					except:
						pass
				if r!= None:
					datas.append(r)
		output = {"status": "0", "records": datas}
		print(output)
		return JsonResponse(output)
