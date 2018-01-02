# -*- coding: utf-8 -*-
import copy
import json

from django.conf.urls import url
from django.db.models import Q
from django.http import QueryDict
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.safestring import mark_safe

from utils.pager import Pagination


# from adm import pager


class FilterOption(object):
    def __init__(self,field_name,multi=False,condition=None,is_choice=False,text_func_name=None,val_func_name=None):
        '''
        :param field_name: 字段名
        :param multi: 是否多选
        :param condition: 显示数据的筛选条件
        :param is_choice: 是否是choice
        '''
        self.field_name = field_name
        self.multi = multi
        self.is_choice = is_choice
        self.condition = condition
        self.text_func_name = text_func_name
        self.val_func_name = val_func_name
    def get_queryset(self,_field):
        if self.condition:
            return _field.rel.to.objects.filter(**self.condition)
        return _field.rel.to.objects.all()

    def get_choices(self,_field):
        return _field.choices



class FilterRow(object):
    def __init__(self,option,data,request):
        '''组合搜索类
        :param option: 字段名
        :param data:
        :param request: request请求的数据
        '''
        self.data = data
        self.option = option
        self.request = request
    def __iter__(self):
        params = copy.deepcopy(self.request.GET)
        params._mutable = True
        current_id = params.get(self.option.field_name)
        current_id_list = params.getlist(self.option.field_name)

        if self.option.field_name in params:
            print("params",params)
            origin_list = params.pop(self.option.field_name)
            url = "{0}?{1}".format(self.request.path_info,params.urlencode())
            yield mark_safe("<a href='{0}'>全部</a>".format(url))
            params.setlist(self.option.field_name,origin_list)
        else:
            url = "{0}?{1}".format(self.request.path_info,params.urlencode())
            yield mark_safe("<a class='active' href='{0}'>全部</a>".format(url))

        for val in self.data:
            if self.option.is_choice:
                pk, text = str(val[0]), val[1]
            else:
                pk, text = str(val.pk), str(val)
            if not self.option.multi:
                params[self.option.field_name] = pk

                url = "{0}?{1}".format(self.request.path_info, params.urlencode())
                if current_id == pk:
                    yield mark_safe("<a class='active' href='{0}'>{1}</a>".format(url,text))
                else:
                    yield mark_safe("<a href='{0}'>{1}</a>".format(url,text))
            else:
                _params = copy.deepcopy(params)
                id_list = _params.getlist(self.option.field_name)
                if pk in current_id_list:
                    id_list.remove(pk)
                    _params.setlist(self.option.field_name,id_list)
                    url = "{0}?{1}".format(self.request.path_info,_params.urlencode())
                    yield mark_safe("<a class='active' href='{0}'>{1}</a>".format(url,text))
                else:
                    id_list.append(pk)
                    _params.setlist(self.option.field_name,id_list)
                    url = "{0}?{1}".format(self.request.path_info,_params.urlencode())
                    yield mark_safe("<a href='{0}'>{1}</a>".format(url,text))






class ChangeList(object):
    '''
        self.config <app01.stark.UserInfoConfig object at 0x035909D0>
        self.list_display [<function StarkConfig.checkbox at 0x035A10C0>, 'id', 'name', 'email', 'ut', <function StarkConfig.edit at 0x035A1108>, <function StarkConfig.delete at 0x035A1150>]
        self.model_class <class 'app01.models.UserInfo'>
        self.request <WSGIRequest: GET '/stark/app01/userinfo/?page=4'>
        self.show_add_btn True
        self.actions [<function UserInfoConfig.multi_del at 0x035A1858>, <function UserInfoConfig.multi_init at 0x035A18A0>]
        self.show_actions True
        self.show_search_form True
        self.search_form_val （搜索关键词）
        self.Params 普通：<QueryDict: {'page': ['4']}>   搜索：<QueryDict: {'_q': ['你好啊']}>
    '''
    def __init__(self,config,queryset):
        self.config = config
        self.list_display = config.get_list_display()
        self.model_class = config.model_class
        self.request = config.request
        self.show_add_btn = config.get_show_add_btn()
        self.actions = config.get_actions()
        self.show_actions = config.get_show_actions()
        self.comb_filter = config.get_comb_filter()
        self.show_comb_filter = config.get_show_comb_filter()
        self.edit_link = config.get_edit_link()
        self.show_search_form = config.get_show_search_form()
        self.search_form_val = config.request.GET.get(config.search_key,"")


        # 分页处理相关
        current_page = self.request.GET.get("page",1)
        total_count = queryset.count()
        page_obj = Pagination(current_page,total_count,self.request.path_info,self.request.GET)
        self.page_obj = page_obj

        self.data_list = queryset[page_obj.start:page_obj.end]


    def modify_actions(self):
        result = []
        for func in self.actions:
            temp = {"name":func.__name__,"text":func.short_desc}
            result.append(temp)
        return result


    def add_url(self):
        return self.config.get_add_url()


    def head_list(self):
        '''
        :return: 要显示的表头部分
        '''
        result = []
        for field_name in self.list_display:
            if isinstance(field_name,str):
                verbose_name = self.model_class._meta.get_field(field_name).verbose_name
            else:
                verbose_name = field_name(self.config,is_header=True)
                print("self_config",self.config)
            result.append(verbose_name)
        return result


    def body_list(self):
        '''
        :return: body体部分，主要数据;data_list:所有数据
        '''
        data_list = self.data_list
        new_data_list = []
        for row in data_list:
            temp = []
            for field_name in self.list_display:
                if isinstance(field_name,str):
                    val = getattr(row,field_name)
                    # 自定义编辑列
                    if field_name in self.edit_link:
                        val = self.edit_link_tag(row.pk,val)
                else:
                    val = field_name(self.config,row)
                temp.append(val)
            new_data_list.append(temp)
        return new_data_list


    def gen_comb_filter(self):
        from django.db.models import ForeignKey, ManyToManyField

        for option in self.comb_filter:

            _field = self.model_class._meta.get_field(option.field_name)

            if isinstance(_field,ForeignKey):       #外键
                # data_list.append(_field.rel.to.objects.all())
                row = FilterRow(option,option.get_queryset(_field),self.request)
            elif isinstance(_field,ManyToManyField):    #多对多
                # data_list.append(_field.rel.to.objects.all())
                row = FilterRow(option, option.get_queryset(_field), self.request)
            else:          #单选
                # data_list.append(_field.choices)
                row = FilterRow(option,option.get_choices(_field),self.request)
            yield row


    def edit_link_tag(self,pk,text):
        '''
        此函数的作用是返回一个可以点击的标签
        :param pk:
        :param text:
        :return: 返回一个标签，
        '''
        query_str = self.request.GET.urlencode()
        print("query_str",query_str)
        params = QueryDict(mutable=True)

        params[self.config._query_param_key] = query_str
        print("params", params)
        print("params_urlencode",params.urlencode())
        return mark_safe('<a href="%s?%s">%s</a>' % (self.config.get_change_url(pk), params.urlencode(), text,))




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
        类中经常用到的字段封装到构造方法中
        :param model_class: <class 'django.db.models.base.ModelBase'>     model对象
        :param site:<class 'stark.service.v1.StarkSite'>               starksite对象
        '''
        self.model_class = model_class
        self.site = site
        self.request = None
        self._query_param_key ="_listfilter"
        self.search_key = "_q"



    # 自定义列表显示的列
    def checkbox(self, obj=None, is_header=False):
        '''
        自定义按钮显示
        :param obj:
        :return:
        '''
        if is_header:
            return "选择"
        return mark_safe('<input type="checkbox" name="pk" value="%s">' % (obj.id,))

    def edit(self, obj=None, is_header=False):
        if is_header:
            return "编辑"
        query_str = self.request.GET.urlencode()
        print("self.request.GET.urlencode()",self.request.GET.urlencode())
        # query_str : 前端获取到的页码
        if query_str:
            print("============>")
            params = QueryDict(mutable=True)                 # 设置可以被修改
            params[self._query_param_key] = query_str
            # self.get_change_url(obj.id)?params.urlencode():拼接后的URL（具有记忆功能）
            return mark_safe("<a href='%s?%s'>编辑</a>"%(self.get_change_url(obj.id),params.urlencode(),))
        return mark_safe('<a href="%s">编辑</a>' % (self.get_change_url(obj.id),))

    def delete(self, obj=None, is_header=False):
        if is_header:
            return "删除"
        return mark_safe('<a href="%s">删除</a>' % (self.get_delete_url(obj.id)))

    # 展示的列表的列数据
    list_display = []
    def get_list_display(self):
        '''
        list_display:['id', 'name']
        get_list_display:[<function StarkConfig.checkbox at 0x035A2420>, 'id', 'name', <function StarkConfig.edit at 0x035A2468>, <function StarkConfig.delete at 0x035A24B0>]
        :return:gongneng is gei list_display add some method
        '''
        data = []
        if self.list_display:

            data.extend(self.list_display)
            # data.append(StarkConfig.edit)
            data.append(StarkConfig.delete)
            data.insert(0, StarkConfig.checkbox)
        return data

    # 可编辑按钮
    edit_link = []
    def get_edit_link(self):
        result = []
        if self.edit_link:
            result.extend(self.edit_link)
        return result

    # 是否显示添加按钮
    show_add_btn = True
    def get_show_add_btn(self):
        return self.show_add_btn

    # 自定义展示的表单样式
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
        meta = type("Meta", (object,), {'model': self.model_class, "fields": "__all__"})
        TestModelForm = type("TestModelForm", (ModelForm,), {"Meta": meta})
        return TestModelForm


    # 关键字搜索
    show_search_form = False
    def get_show_search_form(self):
        return self.show_search_form


    search_fields = []
    def get_search_fields(self):
        result = []
        if self.search_fields:
            result.extend(self.search_fields)
        return result


    def get_search_condition(self):
        key_word = self.request.GET.get(self.search_key)
        # key_word:获取到的关键字
        search_fields = self.get_search_fields()
        # search_fields:过滤条件
        condition = Q()
        condition.connector = "or"
        if key_word and self.get_show_search_form():
            for field_name in search_fields:
                print("field_name",field_name,search_fields)
                condition.children.append((field_name,key_word))
        return condition


    # actions
    show_actions = False
    def get_show_actions(self):
        return self.show_actions


    actions = []      #添加函数.short_desc显示在actions
    def get_actions(self):
        result = []
        if self.actions:
            result.extend(self.actions)
        return result


    # 组合搜索
    comb_filter = []
    def get_comb_filter(self):
        result = []
        if self.comb_filter:
            result.extend(self.comb_filter)
        return result

    show_comb_filter = False
    def get_show_comb_filter(self):
        return self.show_comb_filter








    ##########################请求处理的方法######视图相关########################################################
    def changelist_view(self, request, *args, **kwargs):

        if request.method == "POST" and self.get_show_actions():
            func_name_str = request.POST.get("list_action")
            action_func = getattr(self,func_name_str)
            ret = action_func(request)
            if ret:
                return ret

        comb_condition = {}
        # 搜索相关的处理
        option_list = self.get_comb_filter()
        print("option_list",option_list)
        for key in request.GET.keys():
            value_list = request.GET.getlist(key)
            print("value_list",value_list)

            flag = False
            for option in option_list:
                if option.field_name == key:
                    flag = True
                    break
            if flag:
                comb_condition["%s__in"%key] = value_list     #filter需要的格式是a=b的格式，所以用__in{"cond__in":[x,y,z]}=====>cond__in=[x,y,z]  ===>cond=x;cond=y;cond=z;
        queryset = self.model_class.objects.filter(self.get_search_condition()).filter(**comb_condition).distinct()

        cl = ChangeList(self,queryset)
        return render(request,"stark/changelist.html",{"cl":cl})


    def add_view(self, request, *args, **kwargs):
        '''
        :param model_form_class:默认情况下model_form_class使用self.get_model_form_class()如果有特殊需求可以自己定制
        :return:
        '''
        model_form_class = self.get_model_form_class()
        _popbackid = request.GET.get("_popbackid")
        print("_prpbackid",_popbackid)
        if request.method == "GET":
            form = model_form_class()
            return render(request, "stark/change_add.html", {"form": form,'config':self})

        else:
            form = model_form_class(request.POST)
            if form.is_valid():
                new_obj = form.save()
                if _popbackid:
                    from django.db.models.fields.reverse_related import ManyToOneRel

                    # _popbackid:popup框
                    result = {"status":False,"id":None,"text":None,"popbackid":_popbackid}
                    # result:result {'id': 8, 'text': '后勤部', 'popbackid': 'id_depart'}
                    model_name = request.GET.get("model_name")
                    related_name = request.GET.get("related_name")
                    for related_object in new_obj._meta.related_objects:
                        _model_name = related_object.field.model._meta.model_name
                        _related_name = related_object.related_name
                        if (type(related_object)== ManyToOneRel):
                            _field_name = related_object.field_name
                        else:
                            _field_name = "pk"
                        _limit_choices_to = related_object.limit_choices_to
                        if model_name == _model_name and related_name == str(_related_name):
                            is_exists = self.model_class.objects.filter(**_limit_choices_to,pk=new_obj.pk).exists()
                            if is_exists:
                                result["status"] = True
                                result["text"] = str(new_obj)
                                result["id"] = getattr(new_obj,_field_name)
                                return render(request,"stark/popup_response.html",{"json_result":json.dumps(result,ensure_ascii=False)})
                    return render(request,"stark/popup_response.html",{"json_result":json.dumps(result,ensure_ascii=False)})
                else:
                    return redirect(self.get_list_url())

            return render(request, "stark/change_add.html", {"form": form,'config':self})


    def change_view(self, request, nid, *args, **kwargs):
        # obj 前端获取到的数据
        obj = self.model_class.objects.filter(pk=nid).first()
        if not obj:
            return redirect(self.get_list_url())
        model_form_class = self.get_model_form_class()
        if request.method == "GET":
            form = model_form_class(instance=obj)

            return render(request, "stark/change_edit.html", {"form": form,'config':self})
        else:
            form = model_form_class(instance=obj, data=request.POST)
            if form.is_valid:
                form.save()
                list_query_str = request.GET.get(self._query_param_key)
                # list_query_str:获取到的当前页码
                list_url = "%s?%s"%(self.get_list_url(),list_query_str)
                # list_url:拼接后的路径,返回的时候具有记忆功能
                return redirect(list_url)
            return render(request, "stark/change_edit.html", {"form": form,'config':self})



            ###########################URL##############相关##########################################################


    def delete_view(self, request, nid, *args, **kwargs):
        if request.method == "GET":
            return render(request, "my_delete.html")
        else:
            self.model_class.objects.filter(pk=nid).delete()
            return redirect(self.get_list_url())




    def wrap(self,view_func):
        def inner(request,*args,**kwargs):
            self.request = request
            return view_func(request,*args,**kwargs)
        return inner


    def get_urls(self):
        '''
        model_class._meta.app_label:应用名
        model_class._meta.model_name：表名
        app_model_name：一个元组(应用，表)
        :return:返回的结果是一个url(app_name,model_name)列表
        '''
        app_model_name = (self.model_class._meta.app_label, self.model_class._meta.model_name,)

        url_patterns = [
            url(r'^$', self.wrap(self.changelist_view), name='%s_%s_changelist' % app_model_name),
            url(r'^add/$', self.wrap(self.add_view), name='%s_%s_add' % app_model_name),
            url(r'^(\d+)/delete/$', self.wrap(self.delete_view), name='%s_%s_delete' % app_model_name),
            url(r'^(\d+)/change/$', self.wrap(self.change_view), name='%s_%s_change' % app_model_name)
        ]

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
    def get_change_url(self, nid):
        '''
        name：路径拼接：app_name/model_name/。。。
        :param nid:
        :return: 反向生成后的url；
        '''
        name = "stark:%s_%s_change" % (self.model_class._meta.app_label, self.model_class._meta.model_name)
        edit_url = reverse(name, args=(nid,))
        # print("====edit", edit_url)
        return edit_url

    def get_list_url(self):
        name = "stark:%s_%s_changelist" % (self.model_class._meta.app_label, self.model_class._meta.model_name)
        list_url = reverse(name)
        return list_url

    def get_add_url(self):
        name = "stark:%s_%s_add" % (self.model_class._meta.app_label, self.model_class._meta.model_name)
        add_url = reverse(name)
        return add_url

    def get_delete_url(self, nid):
        name = "stark:%s_%s_delete" % (self.model_class._meta.app_label, self.model_class._meta.model_name)
        del_url = reverse(name, args=(nid,))
        return del_url

    ###########################URL########################################相关##############




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
        这个函数在注册的时候执行：v1.site.register(model.UserInfo,UserInfoConfig)
        :param model_class:  <class 'django.db.models.base.ModelBase'>: 指的是当前传进来的对象
        :param stark_config_class: <class 'type'>  没有的话继承StarkConfig
        :return:
        '''
        if not stark_config_class:

            '''
                stark_config_class = StarkConfig;这里和上边的StarkConfig关联起来
            '''
            stark_config_class = StarkConfig

        self._registry[model_class] = stark_config_class(model_class, self)

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
        for model_class, stark_config_obj in self._registry.items():
            '''
                <class 'app01.models.UserInfo'> <app01.stark.UserInfoConfig object at 0x03587A10>
                app_name:app name
                model_name:model name 
            '''
            app_name = model_class._meta.app_label
            model_name = model_class._meta.model_name

            curd_url = url(r'^%s/%s/' % (app_name, model_name,), (stark_config_obj.urls, None, None))

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
