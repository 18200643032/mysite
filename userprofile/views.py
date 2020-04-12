from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from .forms import UserLoginForm


#用户登录

def user_login(request):
    if request.method == "POST":
        user_login_form = UserLoginForm(data=request.POST)
        if user_login_form.is_valid():
            #清洗合法数据
            data = user_login_form.cleaned_data
            user = authenticate(username=data["username"],password=data["password"])
            if user:
                #保存到session中
                login(request,user)
                return redirect("article:article_list")
            else:
                return HttpResponse("账号或密码有误，请重新输入")
        else:
            return HttpResponse("账号或密码输入有误")

    elif request.method == "GET":
        user_login_form = UserLoginForm()
        context= {"form":user_login_form}
        return render(request,"userprofile/login.html",context)
    else:
        return HttpResponse("请求错误")


#用户退出
def user_logout(request):
    logout(request)
    return redirect("article:article_list")