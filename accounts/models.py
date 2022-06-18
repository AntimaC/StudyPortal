from datetime import datetime
from django.db import models
from email.mime import image
from email.policy import default
from pyexpat import model
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
# Create your models here.
class Register(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    branch= models.CharField(max_length=100,verbose_name="")
    def __str__(self):
       return self.user.username

class Profile(models.Model):
    user = models.OneToOneField(User,default="1", on_delete=models.CASCADE, related_name="profile")
    image = models.ImageField(upload_to="images",default="default/user.png",verbose_name="")
    def __str__(self):
       return f'{self.user} profile'

   