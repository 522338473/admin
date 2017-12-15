# -*- coding: utf-8 -*-
print("=======app01========")
from stark.service import v1
from app01 import models
from django.utils.safestring import mark_safe
from django.conf.urls import url
from django.shortcuts import HttpResponse

class UserInfoConfig(v1.StarkConfig):
    '''
    方法重构，自身有执行自身，没有去找基类
    '''

    list_display = ["id","name"]         #要显示的列

v1.site.register(models.UserInfo,UserInfoConfig)






class RoleConfig(v1.StarkConfig):
    list_display = ["id","name",]

v1.site.register(models.Role,RoleConfig)






class UserTypeConfig(v1.StarkConfig):
    list_display = ["id","title"]
v1.site.register(models.UserType,UserTypeConfig)









