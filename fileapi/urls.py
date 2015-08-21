from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^newFile',views.newFileView),
    url(r'^getToken',views.getTokenView),
    url(r'^callback', views.callbackView),           
    url(r'^newDir', views.newDirView),        
    url(r'^moveFile', views.moveFileView),
    url(r'^listFile', views.listFileView),
    url(r'^removeFile', views.removeFileView),
    url(r'^getFileDetail', views.getFileDetailView),
]
