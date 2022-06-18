from django.contrib import admin
from dashboard.models import  Notes , Post, Replie,Task,Upload_Notes
# Register your models here.
admin.site.register(Notes)

admin.site.register(Post)
admin.site.register(Replie)
admin.site.register(Task)
admin.site.register(Upload_Notes)