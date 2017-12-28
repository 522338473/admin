import json
from django.conf.urls import url
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.shortcuts import render,HttpResponse,redirect
from django.db.models import Q
import datetime
from django.forms import ModelForm
from django.db import transaction
from utils import message

from stark.service import v1
from crm import models

class SingleModelForm(ModelForm):
    class Meta:
        model = models.Customer
        exclude = ["consultant","status","recv_date","last_consult_date"]




class CustomerConfig(v1.StarkConfig):
    order_by = ['-status']

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
            url(r'^public/$',self.wrap(self.public_view),name="%s_%s_public"%app_model_name),
            url(r'^user/$',self.wrap(self.user_view),name="%s_%s_user"%app_model_name),
            url(r'^(\d+)/competition/$',self.wrap(self.competition_view),name="%s_%s_competition"%app_model_name),
            url(r'^single/$', self.wrap(self.single_view), name="%s_%s_single" % app_model_name),

        ]
        return patterns

    list_display = ["id","qq","name",display_gender,display_work_status,display_status,display_course,display_record_consult]
    edit_link = ["name"]
    show_search_form = True

    def public_view(self,request):
        # 条件：未报名 并且 （15天内未成单（当前时间-15）>接客时间） or 3天未跟进（当天时间-3天>最后跟进时间）
        import datetime
        current_user_id = 11
        ctime = datetime.datetime.now().date()
        no_deal = ctime - datetime.timedelta(days=15)
        no_follow = ctime - datetime.timedelta(days=3)

        customer_list = models.Customer.objects.filter(Q(recv_date__lt=no_deal)|Q(last_consult_date__lt=no_follow),status=2)
        return render(request,"public_view.html",{"customer_list":customer_list,"current_user_id":current_user_id})

    def user_view(self,request):
        current_user_id = 11
        customers = models.CustomerDistrbution.objects.filter(user_id=current_user_id).order_by("status")

        return render(request,"user_view.html",{"customers":customers})

    def competition_view(self,request,cid):
        current_user_id = 11
        ctime = datetime.datetime.now().date()
        no_deal = ctime - datetime.timedelta(days=15)
        no_follow = ctime - datetime.timedelta(days=3)
        row_count = models.Customer.objects.filter(Q(recv_date__lt=no_deal) | Q(last_consult_date__lt=no_follow), status=2,id=cid).exclude(consultant_id=current_user_id).update(recv_date=ctime,last_consult_date=ctime,consultant_id=current_user_id)
        if not row_count:
            return HttpResponse("抢单失败")
        models.CustomerDistrbution.objects.create(user_id=current_user_id,customer_id=cid,ctime=ctime)
        return HttpResponse("抢单成功")


    def single_view(self,request):
        if request.method == "GET":
            # message.send_message('1239225096@qq.com', '放哨', '你别走了', '三个月工资太多了')
            forms = SingleModelForm()

            return render(request,"single_view.html",{"forms":forms})
        else:
            # 这里是添加客户的处理机智
            from qndy import CNM

            forms = SingleModelForm(request.POST)
            if forms.is_valid():
                sale_id = CNM.get_sale_id()           #获取销售ID
                ctime = datetime.datetime.now().date()      #获取到当前时间
                if not sale_id:
                    return HttpResponse("你没有资格添加")
                try:
                    with transaction.atomic():
                        forms.instance.consultant_id = sale_id
                        forms.instance.recv_date = ctime
                        forms.instance.last_consult_date = ctime
                        new_form = forms.save()
                        models.CustomerDistrbution.objects.create(user_id=sale_id,customer=new_form,ctime=ctime)

                        # 要发送的目标地址
                        message.send_message('1239225096@qq.com','放哨','你别走了','三个月工资太多了')

                except Exception:
                    return HttpResponse("添加数据异常")

                return redirect(self.get_list_url())
        return render(request, "single_view.html", {"forms": forms})




v1.site.register(models.Customer,CustomerConfig)