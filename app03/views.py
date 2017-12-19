from django.shortcuts import render,HttpResponse
from adm.pager import Pagination
from app01 import models
# Create your views here.

# HOST_LIST = []
# for i in range(1,1014):
#     HOST_LIST.append("c%s.com"%i)

def hosts(request):
    HOST_LIST = models.UserInfo.objects.all()
    """
    自定义分页组件的使用方法：
        pager_obj = Pagination(request.GET.get('page',1),len(HOST_LIST),request.path_info)
        host_list = HOST_LIST[pager_obj.start:pager_obj.end]
        html = pager_obj.page_html()
        return render(request,'hosts.html',{'host_list':host_list,"page_html":html})
    """
    pager_obj = Pagination(request.GET.get("page",1),len(HOST_LIST),request.path_info)
    host_list = HOST_LIST[pager_obj.start:pager_obj.end]
    html = pager_obj.page_html()
    return render(request,"host.html",{"host_list":host_list,"page_html":html})





# def hosts(request):
#     current_page = int(request.GET.get("page"))           #获取到当前的页码
#     per_page_count = 10             #每页显示的条数
#     start = (current_page - 1) * per_page_count    #截取的开始部分
#     end = current_page * per_page_count         #截取的结束部分
#     host_list = HOST_LIST[start:end]       #每页要显示的条数
#
#     total_cont = len(HOST_LIST)            #总长度
#     max_page_num,div = divmod(total_cont,per_page_count)
#     # max_page_num:整数页码     div剩下的页码
#     if div:         #如果有剩余，最大的整数页码+1
#         max_page_num +=1
#     page_html_list = []
#     for i in range(1,max_page_num + 1):      #顾头不顾尾，加一
#         if i == current_page:  #当前页面的按钮链接
#             temp = "<a class='active' href='/host/?page=%s'>%s</a>"%(i,i)
#         else:          #不是当前页面的按钮链接
#             temp = "<a href='/host/?page=%s'>%s</a>"%(i,i)
#         page_html_list.append(temp)
#     print(type(page_html_list),'====================asf')
#     page_html = "".join(page_html_list)          #生成一个新的字符串
#     print(type(page_html))
#     return render(request,"host.html",{"host_list":host_list,"page_html":page_html})



# from app01 import models
# model_list = []
# for i in range(100):
#     mode = models.Role(caption=i)
#     model_list.append(mode)
# models.Role.objects.bulk_create(model_list)




























