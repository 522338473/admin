# -*- coding: utf-8 -*-
print("=======app01========")
from stark.service import v1
from app01 import models
from django.utils.safestring import mark_safe
from django.conf.urls import url
from django.shortcuts import HttpResponse,render,redirect
from django.forms import ModelForm
from django.forms import widgets
from adm import pager





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
    list_display = ["id", "name", "email", "ut"]  # 要显示的列
    show_add_btn = True

    # model_form_class = UserInfoForm          #这里的UserInfoForm应该是一个类，不可以是对象

    show_search_form = True
    search_fields = ["name__contains","email__contains"]

    show_actions = True
    def multi_del(self,request):
        pk_list = request.POST.getlist("pk")
        self.model_class.objects.filter(id__in=pk_list).delete()
        return redirect(self.get_list_url())
    multi_del.short_desc = "批量删除"

    def multi_init(self,request):
        pk_list = request.POST.getlist("pk")
        return redirect(self.get_list_url())
    multi_init.short_desc = "初始化"
    actions = [multi_del,multi_init]






v1.site.register(models.UserInfo,UserInfoConfig)






class RoleConfig(v1.StarkConfig):
    list_display = ["id","caption",]

v1.site.register(models.Role,RoleConfig)






class UserTypeConfig(v1.StarkConfig):
    list_display = ["id","title"]
v1.site.register(models.UserType,UserTypeConfig)




class IportForm(ModelForm):
    class Meta:
        model = models.Iport
        fields = "__all__"
        widgets = {
            "hostname":widgets.TextInput(attrs={"class":"form-control"}),
            "ip":widgets.TextInput(attrs={"class":"form-control"}),
            "port":widgets.NumberInput(attrs={"class":"form-control"}),
            "creat_time":widgets.DateTimeInput(attrs={"class":"form-control"})
        }

class IportConfig(v1.StarkConfig):
    def ip_port(self,obj=None,is_header=False):
        if is_header:
            return "IP：端口"
        return "%s:%s"%(obj.ip,obj.port)
    model_form_class = IportForm
    list_display = ["id","hostname","ip","port","creat_time",ip_port]
    show_add_btn = True

    def report_view(self,request):
        return redirect(self.get_list_url())

    def extra_url(self):
        urls = [
            url(r'^report/$',self.report_view)
        ]
        return urls

    def delete_view(self, request, nid, *args, **kwargs):
        '''
        :param request:为了防止误删设置二次确认
        :param nid:要删除的id
        :return:跳转
        '''
        if request.method == "GET":
            return render(request,"my_delete.html")
        else:
            self.model_class.objects.filter(pk=nid).delete()
            return redirect(self.get_list_url())



v1.site.register(models.Iport,IportConfig)



