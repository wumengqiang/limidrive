#coding:utf-8
from django.conf import settings
from qiniu import Auth,put_file,BucketManager
import qiniu.config
import json
from .models import FileInfo
from django.contrib.auth.models import User
import re

def get_upload_token(username,path,filename):  # 返回上传凭证 ok
    if not check_str(path,ispath=True) or not check_str(filename):
        return False
    q = Auth(settings.QINIU_ACCESS_KEY, settings.QINIU_SECRET_KEY)  # 授权
    if path == '/':
        path = ""
    key = ''.join([username, path, '/', filename])     # key值 
    print key  # python2.7
    callbackBody = "fname=$(fname)&fsize=$(fsize)&key=$(key)&bucket=$(bucket)"  # key中有username
    token = q.upload_token(settings.QINIU_BUCKET_NAME, key, 3600, {'callbackUrl':settings.QINIU_UPLOAD_CALLBACK_URL, 'callbackBody':callbackBody})
    data = {'key':key,'upload_token':token }
    return json.dumps(data,ensure_ascii=False,encoding="utf-8")


def get_private_url(username, path,filename):
    q = Auth(settings.QINIU_ACCESS_KEY, settings.QINIU_SECRET_KEY)  # 授权
    base_url = ''.join([settings.QINIU_DOMAIN,username, path, '/', filename])
    return q.private_download_url(base_url, expires=3600)

def new_or_modify_file(request):  # ok 七牛回调url view
    print request.POST['key'],request.POST['fname']
    if not check_str(request.POST['key'],ispath=True) or not check_str(request.POST['fname']):
        return False
    key = request.POST['key']
    fsize = int(request.POST['fsize'])
    fname = request.POST['fname']
    username = re.match(r"([^/])+", key, re.UNICODE)
    if username == None or username.group(0) == "":
        return False
    username = username.group(0)
    path = key[len(username):-len(fname)-1]  # 去除username和file_name
    if path == "":
        path = '/'
    # print ' '.join([key,str(fsize),path,fname,username])
    user = User.objects.filter(username = username)[0]
    files = FileInfo.objects.filter(owner=user,file_path=path,file_name=fname)
    if bool(files):
        files[0].size = fsize
        files[0].save()
        return True
    filetype = re.search(r"\.(\S+)$",fname, re.UNICODE)
    if filetype == None or filetype.group(1) == "":
        filetype = 'text'
    else:
        filetype = filetype.group(1)
    file1 = FileInfo(owner=user, add_by=user, file_name=fname, file_path=path, file_type=filetype, size=fsize)
    file1.save()
    return True

def new_dir(request):  #  ok 从浏览器发来的request
    if check_str(request.POST['filename']) and check_str(request.POST['path'],ispath=True):
        if FileInfo.objects.filter(owner=request.user,file_name=request.POST['filename'],file_path=request.POST['path']):
            return False
        file1 = FileInfo(owner=request.user, add_by=request.user, file_name=request.POST['filename'], file_path=request.POST['path'],file_type='dir',size=0)
        file1.save()
        return True
    return False

def move_file(request,path,filename,newpath,newfilename,bucket=None):  # bucket即bucketmanager path='/dir/dir' 可用于重命名文件,移动文件,移动目录，重命名目录 # ok
    if bucket == None:
        q = Auth(settings.QINIU_ACCESS_KEY, settings.QINIU_SECRET_KEY)  # 授权
        bucket = BucketManager(q)
        if  not check_str(filename) or not check_str(path,ispath=True) or  not check_str(newfilename) or not check_str(newpath,ispath=True):
            return False
            
    # 数据库操作
    file1 = FileInfo.objects.filter(owner=request.user,file_name=filename,file_path=path)
    if bool(file1):
        file1 = file1[0]
    else:
        return False  # 文件名或者文件夹名不存在
    file1.file_path = newpath
    file1.file_name = newfilename
    file1.save()
    if path == '/':
        path = ''
    if newpath == '/':
        newpath = ''
    if file1.file_type == 'dir': 
        subpath = ''.join([path,'/',filename])
        files = FileInfo.objects.filter(owner=request.user,file_path=subpath)
        subpath2 = ''.join([newpath,'/',newfilename])
        for f in files:
            if f.file_type != 'dir':
                f.file_path = subpath2
                f.save()
                key = ''.join([request.user.username, subpath , '/', f.file_name])
                key2 = ''.join([request.user.username, subpath2, '/', f.file_name])
                ret, info = bucket.move(settings.QINIU_BUCKET_NAME, key, settings.QINIU_BUCKET_NAME, key2)
                print info
                # assert ret=={}
            else :
                move_file(request,subpath,f.file_name,subpath2,f.file_name,bucket)
    else:
        key = ''.join([request.user.username, path, '/', filename])
        key2 = ''.join([request.user.username, newpath, '/', newfilename])
        ret, info = bucket.move(settings.QINIU_BUCKET_NAME, key, settings.QINIU_BUCKET_NAME, key2)
        print info
        # assert ret == {}
    return True

def remove_file(request,path,filename,bucket=None):  # 删除文件 删除目录  ok
    if bucket == None:
        q = Auth(settings.QINIU_ACCESS_KEY, settings.QINIU_SECRET_KEY)  # 授权
        bucket = BucketManager(q)
        if  not check_str(filename) or not check_str(path,ispath=True):
            return False
    file1 =FileInfo.objects.filter(owner=request.user,file_name=filename,file_path=path)
    if bool(file1):
        file1 = file1[0]
    else:
        return False
    file_type = file1.file_type
    file1.delete()
    if path == '/':
        path = ''
    if file_type == 'dir':
        subpath = ''.join([path,'/',filename])
        print subpath
        files = FileInfo.objects.filter(owner=request.user,file_path=subpath)
        for f in files:
            print f.file_name,f.file_type
            if f.file_type != 'dir':
                key = ''.join([request.user.username, subpath , '/', f.file_name])
                ret, info = bucket.delete(settings.QINIU_BUCKET_NAME, key)
                f.delete()
                print info
               # assert ret is None
               # assert info.status_code == 612
            else:
                filename =f.file_name
                remove_file(request,subpath,filename,bucket)

    else:
        key = ''.join([request.user.username, path, '/', filename])
        ret, info = bucket.delete(settings.QINIU_BUCKET_NAME, key)
        print info
       # assert ret is None
       # assert info.status_code == 612
    return True

def list_file(request, path): # ok
    q = Auth(settings.QINIU_ACCESS_KEY, settings.QINIU_SECRET_KEY)  # 授权
    files = FileInfo.objects.filter(owner=request.user,file_path=path)
    filelist = {}
    for f in files:
        if f.file_type == 'dir':  # 文件夹不需要下载 ，但可以设置另外的子目录获取的url，待定
            filelist[f.file_name] = ""
            continue
        if path == '/':
            path = ""
        base_url = ''.join([settings.QINIU_DOMAIN,request.user.username, path, '/', f.file_name])
        filelist[f.file_name] =  q.private_download_url(base_url, expires=3600)
    return json.dumps(filelist,ensure_ascii=False,encoding="utf-8",sort_keys=True)

def check_str(str1,ispath=False):
    if ispath:
        a = re.match(r"""[^\Z\\'";:$%^&*+=|{}]+""",str1,re.UNICODE)
    else:
        a = re.match(r"""[^\Z/\\'";:$%^&*+=|{}]+""",str1,re.UNICODE)
    if a != None and a.group(0) == str1:
        return True
    return False
