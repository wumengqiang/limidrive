#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.generic import FormView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from django.db import connection 
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required  
from django.forms import ModelForm
# Create your views here.
# python 不要带分号 注意缩进  if for while 等语句块用冒号

def registerView(request):
    if request.method == 'GET':
        return render(request,'login/register.html')
    username = request.POST['username']
    passwd = request.POST['passwd']
    passwd_repeat = request.POST['passwd_repeat']
    if passwd_repeat != passwd or not username or not passwd:
        return HttpResponseRedirect('/login/register')
    # cursor = connection.cursor()  # 数据库操作
    # cursor.excute("select username from auth_user where username=%"%username)
    res = User.objects.filter(username=username)
    if len(res) == 0:
        user = User.objects.create_user(username=username,password=passwd)
        user.save()
        return HttpResponseRedirect('/login/login')
    else:
        return HttpResponseRedirect('/login/register')
def loginView(request):
    if request.user.is_authenticated():

        return render(request,'fileapi/getfiledetail.html')
        #return render(request,'fileapi/uploadfile.html')
        #return render(request,'fileapi/gettoken.html')
        #return render(request,'fileapi/newfile.html')
        return render(request,'fileapi/listfile.html')
        return render(request,'fileapi/removefile.html')
        return render(request,'fileapi/movefile.html')
        return render(request,'fileapi/newdir.html')
        return render(request,'fileapi/newfile.html')
    if request.method == 'GET':
        return render(request,'login/login.html')
        
    if request.user.is_authenticated():
        return render(request,'fileapi/gettoken.html')
        return HttpResponseRedirect('/login/space')
    else:
        uname = request.POST['username']
        passwd = request.POST['passwd']
        print("%s %s"%(uname,passwd))
        user = authenticate(username=uname, password=passwd)
        if user is not None:
            login(request,user)
            return render(request,'fileapi/getfiledetail.html')
            return render(request,'fileapi/uploadfile.html')
            return render(request,'fileapi/gettoken.html')
            return render(request,'fileapi/newfile.html')
           # return render(request,'fileapi/listfile.html')
           # return render(request,'fileapi/removefile.html')
            return render(request,'fileapi/movefile.html')
            return render(request,'fileapi/newdir.html')
            return HttpResponseRedirect('/login/space')
        else:
            # return render(request,'login/welcome.html')
            return HttpResponseRedirect('/login/register')


