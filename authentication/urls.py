from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
#Urls for Authentication
path('',views.homepage,name="homepage"),
path('register',views.reg_user,name="register"),
path('login',views.log_in,name="login"),
path('signout',views.signout,name="signout"),


]