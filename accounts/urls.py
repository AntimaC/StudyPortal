from django.contrib import admin
from django.urls import path, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views

app_name="accounts"
urlpatterns=[
    
   path('register',views.register,name="register"),
  path('admin_login',views.admin_login,name="admin_login"),
  path('user_login',views.user_login,name="user_login"),
 path('admin_editprofile',views.admin_editprofile, name="admin_editprofile"),
 path('user_editprofile',views.user_editprofile, name="user_editprofile"),
path('admin_profile',views.admin_profile, name="admin_profile"),
path('user_profile',views.user_profile, name="user_profile"), 
path('Logout',views.Logout, name="Logout"), 
path('change_password_after_login' , views.change_password_after_login , name="change_password_after_login"),
path('admin_change_password',views.admin_change_password,name="admin_change_password"),
]