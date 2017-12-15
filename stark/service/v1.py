# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.shortcuts import HttpResponse,render,redirect
from django.utils.safestring import mark_safe
from django.urls import reverse


class StarkConfig(object):
    '''
        function:   Overwrite when an existing style is not satisfied
        自定义显示的列：checkbox;edit;delete =======================    list_display = [checkbox,edit,delete];默认显示
        是否显示增加按钮：show_add_btn=True    ===============    默认显示
        默认显示的无效果表单：model_form_class = None   -===========  ModelForm      =====get_model_form_class
        请求处理的方法：changelist_view();add_view();delete_view();change_view:
        URL相关：urls;   ------->  get_urls      (extra_url:可以扩展的url插件)
        URL反向生成相关：get_change_url();get_list_url();get_add_url();get_delete_url();
    '''

    def __init__(self, model_class, site):
        '''
        :param model_class: <class 'django.db.models.base.ModelBase'>     model对象
        :param site:<class 'stark.service.v1.StarkSite'>               starksite对象
        '''
        self.model_class = model_class
        self.site = site


    #自定义列表显示的列
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
        return mark_safe('<a href="%s">编辑</a>' %(self.get_change_url(obj.id)))

    def delete(self,obj=None,is_header=False):
        if is_header:
            return "删除"
        return mark_safe('<a href="%s">删除</a>' %(self.get_delete_url(obj.id)))


    #展示的列表的列数据
    list_display = []
    def get_list_display(self):
        '''
        list_display:['id', 'name']
        get_list_display:[<function StarkConfig.checkbox at 0x035A2420>, 'id', 'name', <function StarkConfig.edit at 0x035A2468>, <function StarkConfig.delete at 0x035A24B0>]
        :return:gongneng is gei list_display add some method
        '''
        data = []
        if self.list_display:
            print('====list_display',self.list_display)
            data.extend(self.list_display)
            data.append(StarkConfig.edit)
            data.append(StarkConfig.delete)
            data.insert(0,StarkConfig.checkbox)
        print('========data',data)
        return data


    #是否显示添加按钮
    show_add_btn = True
    def get_show_add_btn(self):
        return self.show_add_btn


    #自定义展示的表单样式
    model_form_class = None
    def get_model_form_class(self):
        '''
        :return: 自定义生成model
        '''
        if self.model_form_class:
            return self.model_form_class
        from django.forms import ModelForm
        # class TestModelForm(ModelForm):
        #     class Meta:
        #         model = self.model_form_class
        #         fields = "__all__"
        meta = type("Meta",(object,),{'model':self.model_class,"fields":"__all__"})
        TestModelForm = type("TestModelForm",(ModelForm,),{"Meta":meta})
        return TestModelForm



##########################请求处理的方法######视图相关########################################################
    def changelist_view(self, request, *args, **kwargs):
        head_list = []
        '''
            all the header information
        '''
        for field_name in self.get_list_display():

            if isinstance(field_name,str):
                '''
                    If it is a field in the database 
                '''
                verbose_name = self.model_class._meta.get_field(field_name).verbose_name
            else:
                '''
                    If it is a constum 
                '''
                verbose_name = field_name(self,is_header=True)
            head_list.append(verbose_name)


        data_list = self.model_class.objects.all()
        '''
            data_list：Get all the model objects that are passed in 
        '''

        new_data_list = []
        '''
            this is all of function list
        '''
        for row in data_list:
            '''
                Traversing each model object 
            '''
            temp = []
            '''
                this is each of row
            '''
            for field_name in self.get_list_display():
                if isinstance(field_name,str):
                    val = getattr(row,field_name)
                else:
                    val = field_name(self,row)
                temp.append(val)
            new_data_list.append(temp)


        return render(request,'stark/changelist.html',{"data_list":new_data_list,"head_list":head_list,"add_url":self.get_add_url(),"show_add_btn":self.get_show_add_btn()})

    def add_view(self, request, *args, **kwargs):
        '''
        :param model_form_class:默认情况下model_form_class使用self.get_model_form_class()如果有特殊需求可以自己定制
        :return:
        '''
        model_form_class = self.get_model_form_class()
        if request.method == "GET":
            form = model_form_class()
            return render(request, "stark/change_add.html",{"form":form})
        else:
            form = model_form_class(request.POST)
            if form.is_valid():
                form.save()
                return redirect(self.get_list_url())
            return render(request,"stark/change_add.html",{"form":form})

    def delete_view(self, request, nid, *args, **kwargs):
        self.model_class.objects.filter(pk=nid).delete()
        return redirect(self.get_list_url())

    def change_view(self, request, nid, *args, **kwargs):
        obj = self.model_class.objects.filter(pk=nid).first()
        if not obj:
            return redirect(self.get_list_url())
        model_form_class = self.get_model_form_class()
        if request.method == "GET":
            form = model_form_class(instance=obj)
            return render(request,"stark/change_edit.html",{"form":form})
        else:
            form = model_form_class(instance=obj,data=request.POST)
            if form.is_valid:
                form.save()
                return redirect(self.get_list_url())
            return render(request,"stark/change_edit.html",{"form":form})



###########################URL##############相关##########################################################
    def get_urls(self):
        '''
        model_class._meta.app_label:应用名
        model_class._meta.model_name：表名
        app_model_name：一个元组(应用，表)
        :return:返回的结果是一个url列表
        '''
        app_model_name = (self.model_class._meta.app_label, self.model_class._meta.model_name,)

        url_patterns = [
            url(r'^$', self.changelist_view, name='%s_%s_changelist' % app_model_name),
            url(r'^add/$', self.add_view, name='%s_%s_add' % app_model_name),
            url(r'^(\d+)/delete/$', self.delete_view, name='%s_%s_delete' % app_model_name),
            url(r'^(\d+)/change/$', self.change_view, name='%s_%s_change' % app_model_name)
        ]
        print("=========哈哈")
        url_patterns.extend(self.extra_url())
        '''
            url_patterns:扩展功能
        '''
        return url_patterns

    def extra_url(self):
        '''
        :return:扩展功能
        '''
        return []

    @property
    def urls(self):
        return self.get_urls()

#####################################URL反向处理相关#####################################
    def get_change_url(self,nid):
        '''
        name：路径拼接：app_name/model_name/。。。
        :param nid:
        :return: 反向生成后的url；
        '''
        name = "stark:%s_%s_change"%(self.model_class._meta.app_label,self.model_class._meta.model_name)
        edit_url = reverse(name,args=(nid,))
        return edit_url

    def get_list_url(self):
        name = "stark:%s_%s_changelist"%(self.model_class._meta.app_label,self.model_class._meta.model_name)
        list_url = reverse(name)
        return list_url

    def get_add_url(self):
        name = "stark:%s_%s_add"%(self.model_class._meta.app_label,self.model_class._meta.model_name)
        add_url = reverse(name)
        return add_url

    def get_delete_url(self,nid):
        name = "stark:%s_%s_delete"%(self.model_class._meta.app_label,self.model_class._meta.model_name)
        del_url = reverse(name,args=(nid,))
        return del_url



###########################URL########################################相关##########################################

class StarkSite(object):
    '''
    初始化执行的类；
    '''
    def __init__(self):
        '''
        初始化的时候生成一个字典_registry{
            model_class:stark_config_class(model_class)
        }
        '''
        self._registry = {}

    def register(self, model_class, stark_config_class=None):
        print(stark_config_class,'=====草拟大爷')
        '''
        这个函数在注册的时候执行：v1.site.register(model.UserInfo,UserInfoConfig)
        :param model_class:  <class 'django.db.models.base.ModelBase'>: 指的是当前传进来的对象
        :param stark_config_class: <class 'type'>  没有的话继承StarkConfig
        :return:
        '''
        if not stark_config_class:
            print("==========这里好像执行不到？")
            '''
                stark_config_class = StarkConfig;这里和上边的StarkConfig关联起来
            '''
            stark_config_class = StarkConfig

        self._registry[model_class] = stark_config_class(model_class,self)


        '''
        有的话添加到第一次初始化的字典中
            Some words are added to the first initialized dictionary ：_registry = {
                            <class'app01.models.UserInfo'>: <app01.stark.UserInfoConfigobjectat0x03587A10>,
                            model_class:stark_config_class(model_class,self)}     
        '''

    def get_urls(self):
        '''
        function: The function of this function is to deal with URL
        :return: this function returned a list   =======>example for [xxx,xxx,xxx]
        '''
        url_pattern = []
        for model_class,stark_config_obj in self._registry.items():
            '''
                <class 'app01.models.UserInfo'> <app01.stark.UserInfoConfig object at 0x03587A10>
                app_name:app name
                model_name:model name
            '''
            app_name = model_class._meta.app_label
            model_name = model_class._meta.model_name
            print("========下一个笑起来")
            curd_url = url(r'^%s/%s/'%(app_name,model_name,),(stark_config_obj.urls,None,None))
            print("=========笑完了来这里吗？")
            '''
                stark_config_obj.urls === include(stark_config_obj.urls)
                curd_url:The path of application and table splicing 
                stark_config_obj.urls：这个会跳转到startConfig下边的urls
            '''
            url_pattern.append(curd_url)
        return url_pattern

    @property
    def urls(self):
        '''
        :return: stark参数在反向生成url的时候会用到的
        '''
        return (self.get_urls(), None, "stark")


site = StarkSite()
