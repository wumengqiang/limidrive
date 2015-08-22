from django.test import TestCase
from . import common,views
from .models import FileInfo
from django.contrib.auth.models import User

# Create your tests here.

class NewFileTest(TestCase):
    def test_newfile_case1(self): # new file in root dir
        init_database()
        common.new_or_modify_file('xuxing/noway','noway',32)

       # user = User.objects.filter(username="xuxing")
       # file1 = FileInfo.objects.filter(owner=user,file_path='/',file_type="text",size=32)
       # self.assertEqual(bool(file1),True)


def init_database():
    user2 = User.objects.create_user(username="xuxing",password="123456")
    user2.save()
    file1 = FileInfo(file_name='fuck',file_path='/',file_type='dir',size=568,owner=user2,add_by)
    FileInfo.objects.raw("""
    insert into fileapi_fileinfo (file_name,file_path,file_type,size,add_by_id,owner_id) values ('fuck','/','dir',568,2,2);
    insert into fileapi_fileinfo (file_name,file_path,file_type,size,add_by_id,owner_id) values ('hello.py','/fuck','py',100,2,2);
    insert into fileapi_fileinfo (file_name,file_path,file_type,size,add_by_id,owner_id) values ('hello','/fuck','dir',468,2,2);
    insert into fileapi_fileinfo (file_name,file_path,file_type,size,add_by_id,owner_id) values ('hello.py','/fuck/hello','py',111,2,2);
    insert into fileapi_fileinfo (file_name,file_path,file_type,size,add_by_id,owner_id) values ('not_hello','/fuck/hello','dir',357,2,2);
    insert into fileapi_fileinfo (file_name,file_path,file_type,size,add_by_id,owner_id) values ('hello.py','/fuck/hello/not_hello','py',234,2,2);
    insert into fileapi_fileinfo (file_name,file_path,file_type,size,add_by_id,owner_id) values ('novel','/fuck/hello/not_hello','text',123,2,2);
    """)
    users = User.objects.all()
    if not bool(users):
        print "why"
    for  user in users:
        print user.username
    files = FileInfo.objects.all()
    for file1 in files:
        print " ".join([file1.file_name,file1.file_path,file1.size,file1.file_type])

