from django.contrib import admin
from app01 import models
from django.utils.safestring import mark_safe

# Register your models here.
#######################自定义的admin样式#################################################
# class UserTypeConfig(admin.ModelAdmin):
#     class UserInfoInline(admin.StackedInline):      #外键关联
#         extra = 0
#         model = models.UserInfo             #被关联的外键类
#     inlines = [UserInfoInline]
#     filter_horizontal = ["roles"]
#
# admin.site.register(models.UserType,UserTypeConfig)
#
#
#
# from django.forms import ModelForm
# from django.forms import fields
# class MyForm(ModelForm):
#     class Meta:
#         model = models.UserInfo
#         fields = "__all__"
#         error_messages = {
#             "name":{
#                 "required":"用户名不可以为空"
#             }
#         }
# class UserInfoConfig(admin.ModelAdmin):
#     def diy(self,obj):
#         return obj.name + "最可爱"
#     def more(self,obj):
#         return mark_safe("<a href='http://www.xiaohuar.com'>点击查看高无码</a>")
#     list_display = ["id","name","email","diy","ut","more"]         #自定义显示列
#     list_display_links = ["email"]                  #可跳转链接地址
#     list_filter = ["name"]                    #分类
#     list_editable = ["name"]               #可编辑框，不可以和链接框处在同一位置    跟多个参数表示或
#     search_fields = ["name"]                       #搜索框
#     # raw_id_fields = ["ut"]                         #外键字段用input框显示
#     # fields = ["name"]                     #值显示这个字段
#     # exclude = ["name"]                    #排除的字段
#     # readonly_fields = ["name"]               #只读
#     ordering = ["id"]
#     # radio_fields = {"ut":admin.VERTICAL}          #radio框FK
#     form = MyForm                     #自定义显示错误信息
#
# admin.site.register(models.UserInfo,UserInfoConfig)
#
#
#
# class RoleConfig(admin.ModelAdmin):
#     def func(self):
#         pass
#     def view_on_site(self,obj):              #自定义按钮
#         return "http://www.xiaohuar.com"
#     func.short_description = "自定义的action按钮"
#     actions = [func,]
#     change_list_template = ""            #自定义显示自己的模板
#
# admin.site.register(models.Role,RoleConfig)
# #######################自定义的admin样式#################################################

















