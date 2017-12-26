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


    list_display = ["id","username","emergency_contract","company",]

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

    def extra_url(self):
        app_model_name = (self.model_class._meta.app_label,self.model_class._meta.model_name)
        url_list = [
            url(r'^(\d+)/score_list$',self.wrap(self.score_list),name="%s_%s_score_list"%(app_model_name))
        ]
        return url_list

    def score_list(self,request,record_id):
        if request.method == "GET":
            from django.forms import Form,fields,widgets
            data = []
            study_record_list = models.StudyRecord.objects.filter(course_record_id=record_id)
            for obj in study_record_list:
                TempForm = type("TempForm",(Form,),{
                    "score_%s"%obj.pk:fields.ChoiceField(choices=models.StudyRecord.score_choices,widget=widgets.Select(attrs={"class":"form-control",})),
                    "homework_note_%s"%obj.pk:fields.ChoiceField(widget=widgets.TextInput(attrs={"class":"form-control"}))
                })
                data.append({'obj':obj,'form':TempForm(initial={'score_%s' %obj.pk:obj.score,'homework_note_%s' %obj.pk:obj.homework_note})})
            return render(request,"score_list.html",{"data":data})
        else:
            data_dict = {}
            for key,value in request.POST.items():
                if key == "csrfmiddlewaretoken":
                    continue
                name,nid = key.rsplit("_",1)
                if nid in data_dict:
                    data_dict[nid][name] = value
                else:
                    data_dict[nid] = {name:value}

            for nid,update_dict in data_dict.items():
                models.StudyRecord.objects.filter(id=nid).update(**update_dict)
            return redirect(request.path_info)


    def kaoqin(self,obj=None,is_header=False):
        if is_header:
            return "考勤"
        return mark_safe("<a href='/stark/crm/studyrecord/?course_record=%s'>考勤管理</a>" %obj.pk)
    def score_input(self,obj=None,is_header=False):
        if is_header:
            return "成绩录入"
        from django.urls import reverse
        rurl = reverse("stark:crm_courserecord_score_list",args=(obj.pk,))
        return mark_safe("<a href='%s'>成绩录入</a>"%rurl)

    list_display = ["class_obj","day_num",kaoqin,score_input]

    show_search_form = True

    show_actions = True

    def mul_init(self,request):
        pk_list = request.POST.getlist("pk")
        record_list = models.CourseRecord.objects.filter(id__in=pk_list)
        for record in record_list:
            exists = models.StudyRecord.objects.filter(course_record=record).exists()
            if exists:
                continue
            student_list = models.Student.objects.filter(class_list=record.class_obj)
            bulk_list = []
            for student in student_list:
                bulk_list.append(models.StudyRecord(student=student,course_record=record))
            models.StudyRecord.objects.bulk_create(bulk_list)

    mul_init.short_desc = "学生初始化"

    actions = [mul_init,]


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
    def display_record(self,obj=None,is_header=False):
        if is_header:
            return "出勤"
        return obj.get_record_display()

    list_display = ["course_record","student",display_record]
    comb_filter = [
        v1.FilterOption("course_record")
    ]
    def action_checked(self,request):
        pk_list = request.POST.getlist("pk")
        models.StudyRecord.objects.filter(id__in=pk_list).update(record="checked")
    action_checked.short_desc = "签到"
    def action_vacate(self,request):
        pk_list = request.POST.getlist("pk")
        models.StudyRecord.objects.filter(id__in=pk_list).update(record="vacate")
    action_vacate.short_desc = "请假"
    def action_late(self,request):
        pk_list = request.POST.getlist("pk")
        models.StudyRecord.objects.filter(id__in=pk_list).update(record="late")
    action_late.short_desc = "迟到"
    def action_leave_early(self,request):
        pk_list = request.POST.getlist("pk")
        models.StudyRecord.objects.filter(id__in=pk_list).update(record="leave_early")
    action_leave_early.short_desc = "早退"
    def action_noshow(self,request):
        pk_list = request.POST.getlist("pk")
        models.StudyRecord.objects.filter(id__in=pk_list).update(record="noshow")
    action_noshow.short_desc = "缺勤"

    actions = [action_checked,action_vacate,action_late,action_leave_early,action_noshow]
    show_add_btn = False
    show_actions = True




v1.site.register(models.StudyRecord,StudyRecordConfig)









