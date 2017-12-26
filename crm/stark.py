# -*- coding: utf-8 -*-
from crm import models
from django.conf.urls import url
from stark.service import v1
from django.utils.safestring import mark_safe
from django.shortcuts import render,redirect,HttpResponse

class UserInfoConfig(v1.StarkConfig):
    list_display = ["id","name","username","email","depart"]
    show_search_form = True
    search_fields = ["name__contains", "email__contains"]
    edit_link = ["name"]



v1.site.register(models.UserInfo,UserInfoConfig)




class DepartmentConfig(v1.StarkConfig):
    list_display = ["id","title","code"]
    show_search_form = True
    edit_link = ["title",]


v1.site.register(models.Department,DepartmentConfig)




class ClassListConfig(v1.StarkConfig):
    def display_school(self,obj=None,is_header=False):
        if is_header:
            return "校区"
        return obj.school.title
    def display_course(self,obj=None,is_header=False):
        if is_header:
            return "班级"
        return "%s(%s期)"%(obj.course.name,obj.semester)
    def display_student_coutn(self,obj=None,is_header=False):
        if is_header:
            return "班级人数"
        return "77"
    list_display = ["id",display_school,display_course,"memo","start_date",display_student_coutn]

    show_search_form = True



v1.site.register(models.ClassList,ClassListConfig)




class StudentConfig(v1.StarkConfig):
    def display_class_list(self,obj=None,is_header=False):
        result = []
        if is_header:
            return "已报班级"
        for i in obj.class_list.all():
            result.append(i.semester)
        return "__".join(result)

    list_display = ["id","username","emergency_contract",display_class_list,"company",]

    show_search_form = True



v1.site.register(models.Student,StudentConfig)




class CourseConfig(v1.StarkConfig):
    list_display = ["id","name"]
    show_search_form = True



v1.site.register(models.Course,CourseConfig)




class ConsultRecordConfig(v1.StarkConfig):
    def display_customer(self,obj=None,is_header=False):
        if is_header:
            return "所咨询客户"
        return obj.customer.name
    def display_consultant(self,obj=None,is_header=False):
        if is_header:
            return "跟踪人"
        return obj.consultant.name

    list_display = ["id",display_customer,display_consultant,"date","note"]

    show_search_form = True



v1.site.register(models.ConsultRecord,ConsultRecordConfig)




class CourseRecordConfig(v1.StarkConfig):
    def display_class_obj(self,obj=None,is_header=False):
        if is_header:
            return "班级"
        return obj.class_obj.semester
    def display_teacher(self,obj=None,is_header=False):
        if is_header:
            return "讲师"
        return obj.teacher.name
    list_display = ["id",display_class_obj,"day_num",display_teacher,"date","course_title","course_memo","has_homework","homework_title","homework_memo","exam"]
    comb_filter = [
        v1.FilterOption("class_obj"),
        v1.FilterOption("teacher"),
    ]
    show_search_form = True

    show_actions = True


v1.site.register(models.CourseRecord,CourseRecordConfig)




class CustomerConfig(v1.StarkConfig):

    def display_record_consult(self,obj=None,is_header=False):
        if is_header:
            return "跟进记录"
        return mark_safe("<a href='/stark/crm/consultrecord/?customer=%s'>查看跟踪记录</a>"%(obj.pk,))
    def display_status(self,obj=None,is_header=False):
        if is_header:
            return "状态"
        return obj.get_status_display
    def display_work_status(self,obj=None,is_header=False):
        if is_header:
            return "职业状态"
        return obj.get_work_status_display
    def display_gender(self,obj=None,is_header=False):
        if is_header:
            return "性别"
        return obj.get_gender_display
    def display_course(self,obj=None,is_header=False):
        result = []
        if is_header:
            return "咨询课程"
        for i in obj.course.all():
            result.append(i.name)
        return "_".join(result)


    def delete_course(self,request,customer_id,course_id):
        """
        删除当前用户感兴趣的课程
        :param request:
        :param customer_id:
        :param course_id:
        :return:
        """
        customer_obj = self.model_class.objects.filter(pk=customer_id).first()
        customer_obj.course.remove(course_id)
        # 跳转回去时，要保留原来的搜索条件
        return redirect(self.get_list_url())

    def extra_url(self):
        app_model_name = (self.model_class._meta.app_label, self.model_class._meta.model_name,)
        patterns = [
            url(r'^(\d+)/(\d+)/dc/$', self.wrap(self.delete_course), name="%s_%s_dc" % app_model_name),
        ]
        return patterns

    list_display = ["id","qq","name",display_gender,display_work_status,display_status,display_course,display_record_consult]
    edit_link = ["name"]
    show_search_form = True



v1.site.register(models.Customer,CustomerConfig)




class PaymentRecordConfig(v1.StarkConfig):
    def display_customer(self,obj=None,is_header=False):
        if is_header:
            return "客户"
        return obj.customer.name
    def display_class_list(self,obj=None,is_header=False):
        if is_header:
            return "班级"
        return obj.class_list.semester
    def display_consultant(self,obj=None,is_header=False):
        if is_header:
            return "负责老师"
        return obj.consultant.name
    list_display = ["id",display_customer,display_class_list,"pay_type","paid_fee","turnover","quote","note","date",display_consultant]
    show_search_form = True


v1.site.register(models.PaymentRecord,PaymentRecordConfig)




class SchoolConfig(v1.StarkConfig):
    list_display = ["id","title"]
    show_search_form = True


v1.site.register(models.School,SchoolConfig)





class StudyRecordConfig(v1.StarkConfig):
    def display_course_record(self,obj=None,is_header=False):
        if is_header:
            return "第几天课程"
        return obj.get_course_display
    def display_student(self,obj=None,is_header=False):
        if is_header:
            return "学员"
        return obj.student.username
    list_display = ["id",display_course_record,display_student,"record","score","homework_note","note","homework","stu_memo","date"]
    show_search_form = True



v1.site.register(models.StudyRecord,StudyRecordConfig)









