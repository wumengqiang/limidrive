#coding=utf-8
from django.db import models
from django.conf import settings
# Create your models here.

class FileInfo(models.Model):
    '''
        文件和目录都会保存在其中，目录的file_type='dir'
    '''
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="owner_set")
    add_by = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="add_set")
    file_id = models.AutoField(primary_key=True)
    file_name = models.CharField(max_length=100)
    file_path = models.CharField(max_length=300)
    file_type = models.CharField(max_length=20)
    size = models.IntegerField()
    last_modify = models.DateField(auto_now=True)
    add_time = models.DateField(auto_now_add=True)
     
