# -*- coding: utf-8 -*-
print("=============app01========")
from stark.service import v1
from app01 import models
from django.utils.safestring import mark_safe
from django.shortcuts import HttpResponse

class UserInfoConfig(v1.StarkConfig):
    '''
    方法重构，自身有执行自身，没有去找基类
    '''
    def checkbox(self,obj=None,is_header=False):
        '''
        自定义按钮显示
        :param obj:
        :return:
        '''
        if is_header:
            return "选择"
        return mark_safe('<input type="checkbox" name="pk" value="%s">' %(obj.id,))
    def edit(self,obj=None,is_header=False):
        if is_header:
            return "编辑"
        return mark_safe('<a href="/edit/%s">编辑</a>' %(obj.id,))
    list_display = [checkbox,"id","name",edit]         #要显示的列


v1.site.register(models.UserInfo,UserInfoConfig)


class RoleConfig(v1.StarkConfig):
    list_display = ["name",]

v1.site.register(models.Role,RoleConfig)




class UserTypeConfig(v1.StarkConfig):
    list_display = ["id","title"]
v1.site.register(models.UserType,UserTypeConfig)









