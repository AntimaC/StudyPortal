from django import forms
from django.db.models import fields
from django.forms import widgets
from numpy import number
from .models import *
from django.contrib.auth.forms import UserCreationForm 
from .models import Task ,Post,Replie


class NotesForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = ['title','description']
        widgets={
            'title':forms.TextInput(attrs={'class':'form-control'}),
             'description':forms.Textarea(attrs={'class':'form-control'}),
        }


class UpdateNoteForm(forms.ModelForm):
    class Meta:
        model = Notes
        fields = [ 'title','description']



class DateInput(forms.DateInput):
       input_type ='date'
       
           

class DashboardFom(forms.Form):
    text=forms.CharField(max_length=100,label="Enter your search:") 
  

class TaskForm(forms.ModelForm):
    content = forms.CharField(
        label='', widget=forms.TextInput(attrs={'placeholder': 'Add Task here...'}))
   

    class Meta:
        model = Task
        fields = ['content']


class UpdateTaskForm(forms.ModelForm):
    content = forms.CharField(
        label='Edit Task', widget=forms.TextInput(attrs={}))

    class Meta:
        model = Task
        fields=['content','complete']
       

class PostContent(forms.ModelForm):
    class Meta:
        model=Post
        fields = ['post_content']
        widgets={
            'post_content':forms.Textarea(attrs={'rows':4, 'cols':15}),
        }
        
class ReplyContent(forms.ModelForm):
    class Meta:
        model = Replie
        fields = ['reply_content']
        widgets={
            'reply_content':forms.Textarea(attrs={'rows':4, 'cols':15}),
        }
class UpdatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [ 'post_content']
        widgets={
            'reply_content':forms.Textarea(attrs={'rows':10, 'cols':3}),
        }

class UpdateReplyForm(forms.ModelForm):
    class Meta:
        model = Replie
        fields = [ 'reply_content']
        widgets={
            'reply_content':forms.Textarea(attrs={'rows':10, 'cols':3}),
        }