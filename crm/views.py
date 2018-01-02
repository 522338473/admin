from django.shortcuts import render,HttpResponse,redirect
# from crm import models
from rbac import models
from rbac.service.init_permission import init_permission

# Create your views here.


def login(request):
    if request.method == "GET":
        return render(request,"login.html")
    else:
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = models.User.objects.filter(username=username,password=password).first()
        if user:
            # print(user.id,user.userinfo.id,user.userinfo.name)
            request.session['user_info'] = {'user_id': user.id, 'uid': user.userinfo.id, 'name': user.userinfo.name}
            init_permission(user,request)
            return redirect("/index/")
        return render(request,"login.html")




def index(request):
    return render(request,"index.html")


