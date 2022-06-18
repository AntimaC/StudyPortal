from django import forms
from django.db.models import fields
from django.forms import widgets
from numpy import number
from accounts.models import *
from accounts.models import Profile 



BRANCH =(
    ( "Computer Science","Computer Science"),
    ( "IT","IT"),
    ( "Civil","Civil"),
    ("Electronics","Electronics"),
    ( "Electric", "Electric"),
     ("Mechanical", "Mechanical" ),
    
)
 
# creating a form 
class Branch(forms.ModelForm):
    class Meta:
        model = Register 
        fields = [ 'branch']
        widgets = {
                'branch': forms.Select(choices=BRANCH)
            }
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User 
        fields = [ 'first_name','last_name','email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']