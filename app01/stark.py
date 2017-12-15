# -*- coding: utf-8 -*-
print("=======app01========")
from stark.service import v1
from app01 import models
from django.utils.safestring import mark_safe
from django.conf.urls import url
from django.shortcuts import HttpResponse
from django.forms import ModelForm
from django.forms import widgets

class UserInfoForm(ModelForm):
    class Meta:
        model = models.UserInfo
        fields = "__all__"
        error_messages = {
            "name":{"required":"字段不能为空"}
        }
        widgets = {
            "name":widgets.TextInput(attrs={"class":"form-control"}),
            "email":widgets.EmailInput(attrs={"class":"form-control"}),
            "ut":widgets.Select(attrs={"class":"form-control"}),
        }

class UserInfoConfig(v1.StarkConfig):
    '''
    方法重构，自身有执行自身，没有去找基类
    '''
    model_form_class = UserInfoForm          #这里的UserInfoForm应该是一个类，不可以是对象

    list_display = ["id","name","email","ut"]         #要显示的列

v1.site.register(models.UserInfo,UserInfoConfig)






class RoleConfig(v1.StarkConfig):
    list_display = ["id","caption",]

v1.site.register(models.Role,RoleConfig)






class UserTypeConfig(v1.StarkConfig):
    list_display = ["id","title"]
v1.site.register(models.UserType,UserTypeConfig)









