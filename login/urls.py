from django.conf.urls import include,url
from django.contrib import admin
from . import views
urlpatterns = [
    url(r'^login$', views.loginView),
    url(r'^register$',views.registerView),
 ]
