#coding:utf-8
from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.models import User
from django.db import connection 
from django.contrib.auth.decorators import login_required  
from . import common 
import json
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
# python 不要带分号 注意缩进  if for while 等语句块用冒号

@login_required(login_url='/login/login')
def newFileView(request):
    pass

def getTokenView(request):
    a = common.get_upload_token(request.user.username,request.POST['path'],request.POST['filename'])
    if a == False:
        a = '文件名或者路径名不合法'
    return render(request,'fileapi/test.html',{'content':a})

@csrf_exempt
def callbackView(request):  # 七牛新建或者修改文件的回调
    
    a = common.new_or_modify_file(request)
    if a == False:
        a = '文件名或者路径名不合法'
        data = {'success':False,"name":request.POST['fname']}
    else:
        data = {'success':True,"name":request.POST['fname']}

    return HttpResponse(json.dumps(data), content_type="application/json")  
    return render(request,'fileapi/test.html',{'content':a})

def newDirView(request):
    a = 'ok'
    if common.new_dir(request) == False:
        a = '路径名已存在或者路径名不合法'
    return render(request,'fileapi/test.html',{'content':a})
    
def moveFileView(request):
    result = common.move_file(request, request.POST['path'], request.POST['filename'], request.POST['newpath'], request.POST['newfilename'])
    if result == False:
        a = "文件名或者文件夹名不存在 或者 文件名或者路径名不合法"
    else:
        a = "ok"
    return render(request,'fileapi/test.html',{'content':a})

def listFileView(request):
    a = common.list_file(request,request.POST['path'])
    return render(request,'fileapi/test.html',{'content':a})

def removeFileView(request):
    result = common.remove_file(request,request.POST['path'],request.POST['filename'])
    if result == False :
        result = "文件名或者文件夹名不存在 或者 文件名或者路径名不合法"
    else:
        reuslt = "ok"
    return render(request,'fileapi/test.html',{'content':result})

