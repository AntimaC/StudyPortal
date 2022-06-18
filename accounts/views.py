
from multiprocessing import context
from random import choices
import re
from django.shortcuts import redirect, render , HttpResponse
from . forms  import *
from django.contrib.auth import views 
from django.contrib import messages
from django.views import generic
from django.contrib.auth  import authenticate,  login, logout
from django.contrib.auth.decorators import login_required
import requests
from accounts.models import  Profile
from accounts.forms import ProfileUpdateForm ,UserUpdateForm,Branch
from django.core.mail import send_mail,BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
import threading
class EmailThread(threading.Thread):
    def __init__(self,emails):
         self.emails = emails
         threading.Thread.__init__(self)
    def run(self):
         self.emails.send(fail_silently=False)


# Create your views here.

def admin_login(request):
    if request.method=="POST":
        try:
          username = request.POST['username']
          password = request.POST['password']
          user = authenticate(username=username, password=password)
          if user.is_staff:
            login(request, user)
            return redirect("/admin_home")
        except Exception as e:
            messages.error(request, "Invalid Credentials")
                 
    return render(request,"instructor/admin_login.html")


def admin_change_password(request):
    user = request.user
    if request.method == "POST":
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        if user.check_password('{}'.format(old_password)) == False:
              messages.success(request, 'please old password was entered incorrectly Please enter it again.')
        else:        
            if  confirm_password == new_password:
               user.set_password( new_password)
               user.save()
               messages.success(request, 'Your password have chanded successfully.')
               return redirect( '/accounts/admin_login')  
              
            else:
                messages.success(request, 'Password did not match.')
    return render(request, "instructor/admin_change_password.html")






def register(request):
    if request.method=="POST":   
        username = request.POST['username']
        email = request.POST['email']
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        branch=request.POST['branch']
        Value = {
               'username':username,
                'firstname':first_name,
                'lastname':last_name,
                'email':email,
                'branch':branch
            }
       
        regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]') 
        atSymbole = email.index('@')
        dot =email.rfind(".")
        error_mess=""
        if User.objects.filter(username=username).exists():
            error_mess ="This User name have been taken Please try other"
        if User.objects.filter(email=email).exists():
            error_mess ="This email id is already exist"
        if len(username) > 15:  
              error_mess = "username should be under 15 charecter" 
        if(regex.search(username) != None):
                 error_mess = "username must be in alphabets"
                  
        if(regex.search(first_name) != None):
            error_mess = "Name must be in alphabets"  
        if password != confirm_password:  
              error_mess = "Passwords do not match."     
        if  dot != -1:  
            if  (dot <= atSymbole + 3): 
                error_mess = " Please check Your typed email, 3 or 4 character  required before dot"    
            if  (dot != len(email)-4 and dot != len(email)-3):
                error_mess = " Please check Your typed email, After dot, 3 or 2 character required"
        else:
            error_mess = "Please check Your typed email, dot is required after  @"
        if not error_mess:
         user = User.objects.create_user(username, email, password)
         Register.objects.create(user=user,branch=branch)
         user.first_name = first_name
         user.last_name = last_name
         user.save()
         return render(request, 'user_login.html')  

        else:
            context={
                'error':error_mess,
                'values':Value
              } 
            return render(request,"users/register.html",context)       
    return render(request,"users/register.html")




def user_login(request):
    if request.method=="POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect("/user_home")
        else:
            messages.error(request, "Invalid Credentials")
                 
    return render(request,"user_login.html")

@login_required
def admin_profile(request):
    user = User.objects.get(id=request.user.id)  
    profile = Profile.objects.filter(user=user).get()  
    instance = profile
    return render(request, "instructor/admin_profile.html")


@login_required
def user_profile(request):
    user = User.objects.get(id=request.user.id)
    data = Register.objects.get(user = user)
    return render(request, "users/user_profile.html",{'data':data})


@login_required
def user_editprofile(request):
    if request.method == 'POST':
       
        b_form = Branch(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        u_form = UserUpdateForm(request.POST, instance=request.user)                           
        if p_form.is_valid() and u_form.is_valid() and b_form.is_valid():
            p_form.save()
            u_form.save()
            u_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('/accounts/user_editprofile')

    else:
        p_form = ProfileUpdateForm(instance=request.user.profile)
        u_form = UserUpdateForm(instance=request.user)
        b_form = Branch(instance=request.user)
       
    context = {
        
        'p_form': p_form,
        'u_form': u_form,
        'b_form': b_form,
    }
    return render(request, 'users/user_editprofile.html',context)





@login_required(login_url = 'login')
def admin_editprofile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        b_form = Branch(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('/accounts/admin_editprofile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        
    }
    return render(request, "instructor/admin_editprofile.html",context)
    
@login_required
def Logout(request):
    logout(request)
    messages.success(request, 'logout successfully.')
    return redirect('/')
#register and login complted===========================
def change_password_after_login(request):
   
    if request.method=='POST':
        old_password = request.POST['old_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        user = User.objects.get(username__exact = request.user.username)
        if user.check_password('{}'.format(old_password)) == False:
              messages.success(request, 'please old password was entered incorrectly Please enter it again.')
        else:        
            if  confirm_password == new_password:
               user.set_password( new_password)
               user.save()
               messages.success(request, 'Your password have chanded successfully.')
               return redirect( '/accounts/user_login')  
              
            else:
                messages.success(request, 'Password did not match.')

    return render(request,'users/change_password_after_login.html')




