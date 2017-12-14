# -*- coding: utf-8 -*-
from django.conf.urls import url
from django.shortcuts import HttpResponse,render


class StarkConfig(object):
    list_display = []
    def __init__(self, model_class, site):
        '''
        :param model_class: <class 'django.db.models.base.ModelBase'>     model对象
        :param site:<class 'stark.service.v1.StarkSite'>               starksite对象
        '''
        self.model_class = model_class
        self.site = site


    ##########################请求处理的方法################################
    def changelist_view(self, request, *args, **kwargs):
        head_list = []
        '''
            all the header information
        '''
        for field_name in self.list_display:

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
            for field_name in self.list_display:
                if isinstance(field_name,str):
                    val = getattr(row,field_name)
                else:
                    val = field_name(self,row)
                temp.append(val)
            new_data_list.append(temp)


        return render(request,'stark/changelist.html',{"data_list":new_data_list,"head_list":head_list})

    def add_view(self, request, *args, **kwargs):
        return HttpResponse("添加页面")

    def delete_view(self, request, nid, *args, **kwargs):
        return HttpResponse("删除页面")

    def change_view(self, request, nid, *args, **kwargs):
        return HttpResponse("修改页面")

    def get_urls(self):
        '''
        model_class._meta.app_label:应用名
        model_class._meta.model_name：表名
        app_model_name：一个元组(应用，表)
        :return:返回的结果是一个url列表
        '''
        app_model_name = (self.model_class._meta.app_label, self.model_class._meta.model_name,)

        url_patterns = [
            url(r'^$', self.changelist_view, name='%s_%s_changlist' % app_model_name),
            url(r'^add/$', self.add_view, name='%s_%s_add' % app_model_name),
            url(r'^(\d+)/delete/$', self.delete_view, name='%s_%s_delete' % app_model_name),
            url(r'^(\d+)/change/$', self.change_view, name='%s_%s_change' % app_model_name)
        ]
        return url_patterns

    @property
    def urls(self):
        return self.get_urls()

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
        '''
        :param model_class:  <class 'django.db.models.base.ModelBase'>: 指的是当前传进来的对象
        :param stark_config_class: <class 'type'>  没有的话继承StarkConfig
        :return:
        '''
        if not stark_config_class:
            stark_config_class = StarkConfig

        self._registry[model_class] = stark_config_class(model_class,self)
        '''
        有的话添加到第一次初始化的字典中
            Some words are added to the first initialized dictionary ：_registry = {
                            <class'app01.models.UserInfo'>: <app01.stark.UserInfoConfigobjectat0x03587A10>,
                            model_class:stark_config_class(model_class,self)
                            }
                            
        '''

    def get_urls(self):
        '''
        :return: this function returned a list   =======>example for [xxx,xxx,xxx]
        '''
        url_pattern = []
        for model_class,stark_config_obj in self._registry.items():
            '''
                <class 'app01.models.UserInfo'> <app01.stark.UserInfoConfig object at 0x03587A10>
                app_name:应用名
                model_name:表名
            '''
            app_name = model_class._meta.app_label
            model_name = model_class._meta.model_name
            curd_url = url(r'^%s/%s/'%(app_name,model_name,),(stark_config_obj.urls,None,None))
            '''
                curd_url:应用和表拼接出来的路径
            '''
            url_pattern.append(curd_url)
        return url_pattern

    @property
    def urls(self):
        '''
        :return: 第三个参数反向生成的时候用到
        '''
        return (self.get_urls(), None, "stark")


site = StarkSite()
