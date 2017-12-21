# -*- coding: utf-8 -*-

from stark.service import v1
from app04 import models
from django.forms import ModelForm,fields,widgets


class UserInfoForm(ModelForm):
    class Meta:
        model = models.UserInfo
        fields = "__all__"
        widgets = {
            "name":widgets.TextInput(attrs={"class":"form-control"}),
            "email":widgets.EmailInput(attrs={"class":"form-control"}),
            "gender":widgets.Select(attrs={"class":"form-control"}),
            "depart":widgets.Select(attrs={"class":"form-control"}),
            "roles":widgets.SelectMultiple(attrs={"class":"form-control"})

        }


class UserInfoConfig(v1.StarkConfig):
    def displsy_gender(self,obj=None,is_header=False):
        if is_header:
            return "性别"
        return obj.get_gender_display()

    def display_depart(self,obj=None,is_header=False):
        if is_header:
            return "部门"
        return obj.depart.caption

    def display_roles(self,obj=None,is_header=False):
        result = []
        if is_header:
            return "角色"
        for i in obj.roles.all():
            result.append(i.title)
        return "__".join(result)

    # model_form_class = UserInfoForm


    list_display = ["id","name","email",displsy_gender,display_depart,display_roles]

    comb_filter = [
        v1.FilterOption("gender",is_choice=True),
        v1.FilterOption("depart",condition={"id__gt":1}),
        v1.FilterOption("roles",True)
    ]


v1.site.register(models.UserInfo,UserInfoConfig)





class DepartmentConfig(v1.StarkConfig):
    list_display = ["id","caption"]

v1.site.register(models.Department,DepartmentConfig)




class RoleConfig(v1.StarkConfig):
    list_display = ["id","title"]

v1.site.register(models.Role,RoleConfig)



