#coding:utf-8
from django.conf import settings
from qiniu import Auth,put_file,BucketManager
import qiniu.config
import json
from .models import FileInfo
from django.contrib.auth.models import User
import re

def get_upload_token(username,path,filename):  # 返回上传凭证
    Auth(settings.QINIU_ACCESS_KEY, settings.QINIU_SECRET_KEY)  # 授权
    
    key = ''.join(username, path, '/', filename)     # key值 
    print key  # python2.7
    callbackBody = "fname=$(fname)&fsize=$(fsize)&key=$(key)&bucket=$(bucket)"  # key中有username
    token = q.upload_token(settings.QINIU_BUCKET_NAME, key, 3600, {'callbackUrl':QINIU_UPLOAD_CALLBACK_URL, 'callbackBody':callbackBody})
    data = {'key':key,'upload_token':token }
    return json.dumps(data,ensure_ascii=False,encoding="utf-8")


def get_private_url(username, path,filename):
    q = Auth(settings.QINIU_ACCESS_KEY, settings.QINIU_SECRET_KEY)  # 授权
    base_url = ''.join(settings.QINIU_DOMAIN,username, path, '/', filename)
    return q.private_download_url(base_url, expires=3600)

def new_or_modify_file(request):  #  七牛回调url view
    key = request.POST['key']
    fsize = int(request.POST['fsize'])
    fname = request.POST['fname']
    username = re.match(r"([^/])+", key, re.UNICODE).group(0)
    path = key[len(username):-len(fname)-1]  # 去除username和file_name
    user = User.objects.filter(username = username)[0]
    if files = FileInfo.objects.filter(owner=username,file_path=path,file_name=fname):
        files[0].file_size = fsize
        files[0].save()
        return
    filetype = re.search(r"\.(\S+)",fname, re.UNICODE).group(1)
    file1 = FileInfo(owner=user, add_by=user, file_name=fname, file_path=path, file_type=filetype, size=fsize)
    file1.save()

def new_dir(reuqest):  # 从浏览器发来的request
    file1 = FileInfo(owner=reuqest.user, add_by=request.user, file_name=request.POST['filename'], file_path=request.POST['path'],file_type='dir',size=0)
    file1.save()

def move_file(request,path,filename,newpath,newfilename,bucket=None):  # bucket即bucketmanager path='/dir/dir' 可用于重命名文件,移动文件,移动目录，重命名目录
    if bucket == None:
        q = Auth(settings.QINIU_ACCESS_KEY, settings.QINIU_SECRET_KEY)  # 授权
        bucket = BucketManager(q)

    # 数据库操作
    file1 = FileInfo.objects.filter(owner=request.user,file_name=filename,file_path=path)[0]
    file1.file_path = newpath
    file1.file_name = newfilename
    file1.save()

    if file1.file_type == 'dir': 
        subpath = ''.join(path,'/',filename)
        files = FileInfo.objects.filter(owner=request.user,file_path=subpath)
        subpath2 = ''.join(newpath,'/',newfilename)
        for f in files:
            if f.file_type != 'dir':
                f.file_path = subpath2
                f.save()
                key = ''.join(request.user.username, subpath , '/', f.file_name)
                key2 = ''.join(request.user.username, subpath2, '/', f.file_name)
                ret, info = bucket.move(settings.QINIU_BUCKET_NAME, key, settings.QINIU_BUCKET_NAME, key2)
                print(info)
                assert ret={}
            else :
                move_file(request,subpath,f.file_name,subpath2,f.file_name,bucket)
    else:
        key = ''.join(request.user.username, path, '/', filename)
        key2 = ''.join(request.user.username, newpath, '/', newfilename)
        ret, info = bucket.move(settings.QINIU_BUCKET_NAME, key, settings.QINIU_BUCKET_NAME, key2)
        print(info)
        assert ret == {}

def remove_file(request,path,filename,bucket=None):  # 删除文件 删除目录
    if bucket == None:
        q = Auth(settings.QINIU_ACCESS_KEY, settings.QINIU_SECRET_KEY)  # 授权
        bucket = BucketManager(q)

    file1 =FileInfo.objects.filter(owner=request.user,file_name=filename,file_path=path)[0]
    file_type = file1.file_type
    file1.delete()
    if file_type == 'dir':
        subpath = ''.join(path,'/',filename)
        files = FileInfo.objects.filter(owner=request.user,file_path=subpath)
        for f in files:
            if f.file_type != 'dir':
                f.delete()
                key = ''.join(request.user.username, subpath , '/', f.file_name)
                ret, info = bucket.delete(settings.QINIU_BUCKET_NAME, key)
                print(info)
                assert ret is None
                assert info.status_code == 612
            else:
                filename =f.file_name
                f.delete()
                remove_file(request,subpath,filename,bucket)
    else:
        key = ''.join(request.user.username, path, '/', filename)
        ret, info = bucket.delete(settings.QINIU_BUCKET_NAME, key)
        print(info)
        assert ret is None
        assert info.status_code == 612

def list_file(request, path):
    q = Auth(settings.QINIU_ACCESS_KEY, settings.QINIU_SECRET_KEY)  # 授权
    files = FileInfo.objects.filter(owner=request.user,file_path=path)
    filelist = {}
    for f in files:
        if f.file_type == 'dir':  # 文件夹不需要下载 ，但可以设置另外的子目录获取的url，待定
            filelist[f.file_name] = ""
            continue
        base_url = ''.join(settings.QINIU_DOMAIN,request.user.username, path, '/', f.filename)
        filelist[f.file_name] =  q.private_download_url(base_url, expires=3600)
    return json.dumps(filelist,ensure_ascii=False,encoding="utf-8",sort_keys=True)


