from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from .forms import UserLoginForm,UserRegisterForm
from django.contrib.auth.models import User
#引入验证登录的装饰器
from django.contrib.auth.decorators import login_required

from .forms import ProfileForm
from .models import Profile

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

# 用户注册
def user_register(request):
    if request.method == 'POST':
        user_register_form = UserRegisterForm(data=request.POST)
        if user_register_form.is_valid():
            new_user = user_register_form.save(commit=False)
            # 设置密码
            new_user.set_password(user_register_form.cleaned_data['password'])
            new_user.save()
            # 保存好数据后立即登录并返回博客列表页面
            login(request, new_user)
            return redirect("article:article_list")
        else:
            return HttpResponse("注册表单输入有误。请重新输入~")
    elif request.method == 'GET':
        user_register_form = UserRegisterForm()
        context = { 'form': user_register_form }
        return render(request, 'userprofile/register.html', context)
    else:
        return HttpResponse("请使用GET或POST请求数据")


#删除用户数据
@login_required(login_url='/userprofile/login/')
def user_delete(request,id):
    if request.method == "POST":
        user = User.objects.get(id=id)
        #验证登录用户，待删除用户是否相同
        print(request.user,"111111111111111111111")
        if request.user == user:
            #退出登录，删除数据并返回
            logout(request)
            user.delete()
            return  redirect("article:article_list")
        else:
            return HttpResponse("你没有删除操作的权限")
    else:
        return HttpResponse('仅接受POST请求')


#编辑用户信息
@login_required(login_url="/userprofile/login/")
def profile_edit(request,id):
    user = User.objects.get(id=id)
    #user_id是OneToOneField 自动生成的字段
    profile = Profile.objects.get(user_id=id)
    if request.method == "POST":
        #验证修改数据者，是否为用户本人
        if request.user != user:
            return HttpResponse("你没有权限修改信息")
        profile_form = ProfileForm(data=request.POST)
        if profile_form.is_valid():
            #取得清洗后的数据
            profile_cd = profile_form.cleaned_data
            profile.phone = profile_cd["phone"]
            profile.bio = profile_cd["bio"]
            profile.save()
            #带参数的redirect()
            return redirect('userprofile:edit',id=id)
        else:
            return HttpResponse("输入有误")

    elif request.method == "GET":
        profile_form = ProfileForm()
        context = {"profile_form":profile_form,"profile":profile,"user":user}
        return render(request,"userprofile/edit.html",context)