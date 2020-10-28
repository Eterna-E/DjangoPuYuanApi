from django.db import models
from django.contrib import admin

# Create your models here.

class Friend(models.Model):
    uid = models.CharField(max_length = 100,blank=True)
    invite_code = models.CharField(max_length = 100,blank=True) # 邀請碼
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True, blank=True)
    date = models.DateField(auto_now=False, auto_now_add=True, blank=True, null=True)

class Friend_data(models.Model):
    uid = models.CharField(max_length = 100,blank=True)
    relation_id = models.CharField(max_length = 100,blank=True)
    friend_type = models.IntegerField(blank=True)
    status = models.CharField(max_length = 100,blank=True)
    read = models.BooleanField(blank=True,default=False)
    imread = models.BooleanField(blank=True,default=False)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now=False, auto_now_add=False, blank=True)
    date = models.DateField(auto_now=False, auto_now_add=True, blank=True, null=True)

class Notification(models.Model):
    uid = models.CharField(max_length = 100,blank=True)
    member_id = models.CharField(max_length = 100,blank=True)
    reply_id = models.CharField(max_length = 100,blank=True)
    message = models.CharField(max_length = 100,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Share(models.Model):
    uid = models.CharField(max_length = 100,blank=True)
    fid = models.CharField(max_length = 100,blank=True)
    data_type = models.CharField(max_length = 100,blank=True)
    relation_type = models.CharField(max_length = 100,blank=True)

@admin.register(Friend)
class FriendAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Friend._meta.fields]

@admin.register(Friend_data)
class Friend_dataAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Friend_data._meta.fields]

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Notification._meta.fields]

@admin.register(Share)
class ShareAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Share._meta.fields]
