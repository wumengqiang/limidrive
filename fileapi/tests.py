from django.test import TestCase
from . import common,views
from .models import FileInfo
from django.contrib.auth.models import User

# Create your tests here.

class NewFileTest(TestCase):
    def test_newfile_case1(self): # new file in root dir
        init_database()
        common.new_or_modify_file('xuxing/noway','noway',32)
        user = User.objects.filter(username="xuxing")
        file1 = FileInfo.objects.filter(owner=user,file_name='noway',file_path='/',file_type="text",size=32)
        self.assertEqual(bool(file1),True)  

    def test_newfile_case2(self):
        init_database()
        common.new_or_modify_file('xuxing/fuck/hello/not_hello/noway','noway',32)
        user = User.objects.filter(username="xuxing")
        
        file1 = FileInfo.objects.filter(owner=user,file_name='noway',file_path='/fuck/hello/not_hello',file_type="text",size=32)
        self.assertEqual(bool(file1),True)  
        file1 = FileInfo.objects.filter(owner=user,file_name='novel',file_path='/fuck/hello/not_hello',file_type="text",size=123)
        self.assertEqual(bool(file1),True)  
        file1 = FileInfo.objects.filter(owner=user,file_name='hello.py',file_path='/fuck/hello/not_hello',file_type="py",size=234)
        self.assertEqual(bool(file1),True)  
        file1 = FileInfo.objects.filter(owner=user,file_name='not_hello',file_path='/fuck/hello',file_type="dir",size=389)
        self.assertEqual(bool(file1),True)  
        file1 = FileInfo.objects.filter(owner=user,file_name='hello.py',file_path='/fuck/hello',file_type="py",size=111)
        self.assertEqual(bool(file1),True)  
        file1 = FileInfo.objects.filter(owner=user,file_name='hello',file_path='/fuck',file_type="dir",size=500)
        self.assertEqual(bool(file1),True)  
        file1 = FileInfo.objects.filter(owner=user,file_name='hello.py',file_path='/fuck',file_type="py",size=100)
        self.assertEqual(bool(file1),True)  
        file1 = FileInfo.objects.filter(owner=user,file_name='fuck',file_path='/',file_type="dir",size=600)
        self.assertEqual(bool(file1),True)  

def init_database():
    delete_data()
    user2 = User.objects.create_user(username="xuxing",password="123456")
    user2.save()
    file1 = FileInfo(file_name='fuck',file_path='/',file_type='dir',size=568,owner=user2,add_by=user2)
    file1.save()
    file1 = FileInfo(file_name='hello.py',file_path='/fuck',file_type='py',size=100,owner=user2,add_by=user2)
    file1.save()
    file1 = FileInfo(file_name='hello',file_path='/fuck',file_type='dir',size=468,owner=user2,add_by=user2)
    file1.save()
    file1 = FileInfo(file_name='hello.py',file_path='/fuck/hello',file_type='py',size=111,owner=user2,add_by=user2)
    file1.save()
    file1 = FileInfo(file_name='not_hello',file_path='/fuck/hello',file_type='dir',size=357,owner=user2,add_by=user2)
    file1.save()
    file1 = FileInfo(file_name='hello.py',file_path='/fuck/hello/not_hello',file_type='py',size=234,owner=user2,add_by=user2)
    file1.save()
    file1 = FileInfo(file_name='novel',file_path='/fuck/hello/not_hello',file_type='text',size=123,owner=user2,add_by=user2)
    file1.save()

    users = User.objects.all()
    if not bool(users):
        print "why"
    for  user in users:
        print user.username
    files = FileInfo.objects.all()
    for file1 in files:
        print " ".join([file1.file_name,file1.file_path,str(file1.size),file1.file_type])

def delete_data():
    User.objects.all().delete()
    FileInfo.objects.all().delete()
