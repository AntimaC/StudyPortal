from datetime import datetime
from django.db import models
from ckeditor.fields import RichTextField
# Create your models here.
from email.mime import image
from email.policy import default
from pyexpat import model
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from dashboard.validators import validate_file

# Create your models here.


class Notes(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=200)
    description = RichTextField(blank=True,null=True)
  
    class Meta:
        verbose_name = "notes"
        verbose_name_plural="notes"
    def __str__(self):
        return self.title


   

class Post(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    post_id = models.AutoField
    post_content = models.TextField(max_length=5000,verbose_name="")
    timestamp= models.DateTimeField(default=now)
    branch=models.CharField(default='',max_length=200)
    image = models.ImageField(upload_to="images",default="")
    def __str__(self):
       return f'{self.user1} Post'


class Replie(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    reply_id = models.AutoField
    reply_content = models.TextField(max_length=5000,verbose_name="")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, default='')
    timestamp= models.DateTimeField(default=now)
    image = models.ImageField(upload_to="images",default="")
    def __str__(self):
       return f'{self.user} Post'



class Task(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,default=1)
    content = models.CharField(max_length=50)
    date_created = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
   
    def __str__(self):
        return f'{self.content}'

    class Meta:
        ordering = ['-date_created']

import os
from django.core.exceptions import ValidationError


def validate_file_extension(value):
  ext = os.path.splitext(value.name)[1]   
  valid_extensions = ('.pdf', '.ppt', '.doc')  
  if not ext.lower() in valid_extensions:
    raise ValidationError('Unsupported file.')

class Upload_Notes(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    uploadingdate = models.CharField(max_length=30)
    branch = models.CharField(max_length=30)
    subject = models.CharField(max_length=50)
    notesfile = models.FileField(null=True,validators=(validate_file_extension, ))
    filetype = models.CharField(max_length=30)
    description = models.CharField(max_length=200, null=True)
    status = models.CharField(max_length=15)

    def __str__(self):
          return f'{self.user} notes'
