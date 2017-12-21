# -*- coding: utf-8 -*-
from crm import models
from stark.service import v1

class UserInfoConfig(v1.StarkConfig):
    def display_depart(self,obj=None,is_header=False):
        if is_header:
            return "部门"
        return obj.depart.title
    list_display = ["id","name","username","password","email",display_depart]
    comb_filter = [
        v1.FilterOption("depart")
    ]
    show_search_form = True

    show_actions = True

v1.site.register(models.UserInfo,UserInfoConfig)




class DepartmentConfig(v1.StarkConfig):
    list_display = ["id","title","code"]
    show_search_form = True

    show_actions = True

v1.site.register(models.Department,DepartmentConfig)




class ClassListConfig(v1.StarkConfig):
    def display_school(self,obj=None,is_header=False):
        if is_header:
            return "校区"
        return obj.school.title
    def display_course(self,obj=None,is_header=False):
        if is_header:
            return "课程名称"
        return obj.course.name
    def display_teachers(self,obj=None,is_header=False):
        result = []
        if is_header:
            return "任课老师"
        for i in obj.teachers.all():
            result.append(i.name)
        return "__".join(result)
    def display_tutor(self,obj=None,is_header=False):
        if is_header:
            return "班主任"
        return obj.tutor.name
    list_display = ["id",display_school,display_course,"semester","price","start_date","memo",display_teachers,display_tutor]
    comb_filter = [
        v1.FilterOption("school"),
        v1.FilterOption("course"),
    ]
    show_search_form = True

    show_actions = True


v1.site.register(models.ClassList,ClassListConfig)




class StudentConfig(v1.StarkConfig):
    def display_class_list(self,obj=None,is_header=False):
        result = []
        if is_header:
            return "已报班级"
        for i in obj.class_list.all():
            result.append(i.semester)
        return "__".join(result)

    list_display = ["id","customer","username","password","emergency_contract",display_class_list,"company","location","position","salary","welfare","date","memo"]
    comb_filter = [
        v1.FilterOption("class_list")
    ]
    show_search_form = True

    show_actions = True

v1.site.register(models.Student,StudentConfig)




class CourseConfig(v1.StarkConfig):
    list_display = ["id","name"]
    show_search_form = True

    show_actions = True

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
    comb_filter = [
        v1.FilterOption("consultant"),
        v1.FilterOption("customer"),
    ]
    show_search_form = True

    show_actions = True

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
    def display_referral_from(self,obj=None,is_header=False):
        if is_header:
            return "转介绍学员"
        return obj.referral_from.name
    def display_course(self,obj=None,is_header=False):
        result = []
        if is_header:
            return "角色"
        for i in obj.course.all():
            result.append(i.name)
        return "__".join(result)
    def display_consultant(self,obj=None,is_header=False):
        if is_header:
            return "课程顾问"
        return obj.consultant.name
    list_display = ["id","qq","name","gender","education","graduation_school","major","experience","work_status","company","salary","source",display_referral_from,display_course,display_consultant,"status","date","last_consult_date"]
    comb_filter = [
        v1.FilterOption("course"),
    ]
    show_search_form = True

    show_actions = True

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
    comb_filter = [
        v1.FilterOption("class_list"),
        v1.FilterOption("consultant"),
    ]
    show_search_form = True

    show_actions = True

v1.site.register(models.PaymentRecord,PaymentRecordConfig)




class SchoolConfig(v1.StarkConfig):
    list_display = ["id","title"]
    show_search_form = True

    show_actions = True

v1.site.register(models.School,SchoolConfig)





class StudyRecordConfig(v1.StarkConfig):
    def display_course_record(self,obj=None,is_header=False):
        if is_header:
            return "第几天课程"
        return obj.course_record.date
    def display_student(self,obj=None,is_header=False):
        if is_header:
            return "学员"
        return obj.student.username
    list_display = ["id",display_course_record,display_student,"record","score","homework_note","note","homework","stu_memo","date"]
    show_search_form = True

    show_actions = True


v1.site.register(models.StudyRecord,StudyRecordConfig)









