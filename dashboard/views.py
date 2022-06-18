from datetime import date
from itertools import count

from multiprocessing import context
from random import choices
from django.shortcuts import get_object_or_404, redirect, render , HttpResponseRedirect
from . forms  import *
from django.contrib.auth import views 
from django.contrib import messages
from django.views import View, generic
from django.contrib.auth  import authenticate,  login, logout
from django.contrib.auth.decorators import login_required
import requests
from django.contrib.auth.models import User
from .models import Post, Replie 
from accounts.models import  Profile, Register
from tkinter import *
from gtts import gTTS
from googletrans import Translator
import  PyPDF4
from .models import Task ,Upload_Notes
from dashboard.forms import TaskForm, UpdateTaskForm,UpdateNoteForm,PostContent,ReplyContent
import io
from io import BytesIO
from django.http import HttpResponse, JsonResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.db.models import Q
from django.db.models import Count
from django.urls import reverse

# Create your views here.
def index(request):
    return render(request,"index.html")

@login_required(login_url = 'login')
def admin_home(request):
    pending_notes = Upload_Notes.objects.filter(status="pending").count()
    accepted_notes = Upload_Notes.objects.filter(status="Accept").count()
    rejected_notes = Upload_Notes.objects.filter(status="Reject").count()
    all_notes = Upload_Notes.objects.all().count()
    
   # data = Profile.objects.filter(Q(user__is_superuser=False), Q(user__is_staff=False)).order_by('-user__last_login')[:10]
    data = Profile.objects.filter(Q(user__is_superuser=False), Q(user__is_staff=False), Q(user__last_login__isnull=False)).order_by('-user__last_login')
    user= User.objects.values_list('last_login')
    context={
        'pending_notes':pending_notes,
        'accepted_notes':accepted_notes,
        'rejected_notes':rejected_notes,
        'all_notes':all_notes,
        'data':data,
        'user':user
    }
    return render(request,"instructor/admin_home.html",context)


@login_required
def show_all_users(request):
    data = Profile.objects.filter(Q(user__is_superuser=False), Q(user__is_staff=False))
    #user = User.objects.get(id=request.user.id)
    #data1 = Register.objects.get(user = data)
    users = Register.objects.all()
    return render(request, "instructor/showallusers.html", {'users': users,'dt':data})
   

@login_required
def delete_post(request, pk=None):
    post = Post.objects.filter(id=pk)
    post.delete()
    return redirect('/forum_a')

@login_required
# def delete_reply(request, pk=None):

#     reply = Replie.objects.filter(id=pk)
#     reply.delete()
#     return redirect(reverse('dashboard:discussion', args=[reply.post.id]))   
def delete_reply(request, pk=None):
    reply = Replie.objects.filter(id=pk)
    reply_instance = get_object_or_404(Replie,id=pk)
    post_pk=reply_instance.post.id
    reply.delete()
    return redirect(reverse('dashboard:discussion', args=[post_pk])) 

@login_required
def user_home(request):
    return render(request,"user/user_home.html")

@login_required
def delete_user(request,pk=None):
        User.objects.get(id=pk).delete()
        return redirect("/showallusers")
@login_required
def forum_a(request):
    user = request.user
    posts = Post.objects.filter().order_by('-timestamp')
    
    profile = Profile.objects.all()
    if request.method=="POST":   
          user = request.user
          image = request.user.profile.image
          content = request.POST.get('content','')
          branch = request.POST.get('branch','')
          post = Post(user1=user, post_content=content, image=image,branch=branch)
          post.save()
          return redirect('/forum_a') 
    posts = Post.objects.filter().order_by('-timestamp')
    
    context={
        'posts':posts,
        
    }
    return render(request, "forum.html",context)




@login_required
# def forum(request):
#     user = request.user
#     profile = Profile.objects.all()
#     user = User.objects.get(id=request.user.id)
#     data = Register.objects.get(user = user)
#     user_posts = Post.objects.filter(branch=data.branch).count()
#     if request.method=="POST": 
#        # form=PostContent(request.POST)
#         #if form.is_valid():  
#           user = request.user
#           image = request.user.profile.image
#           content = request.POST.get('content','')
#           branch = request.POST.get('branch','')
          
#           post = Post(user1=user, post_content=content, image=image,branch=branch)
#           post.save()
#           messages.success(request, f'Your Question has been posted successfully!!')
#           return redirect('/forum')
#        # else:
#            # form=PostContent()  
         
#     posts = Post.objects.filter(branch=data.branch).order_by('-timestamp')
#    # form= PostContent()
    # print(data.branch)
    # context={
    #     'posts':posts,
    #     'branch':data.branch,
    #     'user_posts':user_posts
    # }
    # return render(request, "forum.html",context)
def forum(request):
    user = request.user
    profile = Profile.objects.all()
    user = User.objects.get(id=request.user.id)
    data = Register.objects.get(user = user)
    user_posts = Post.objects.filter(branch=data.branch).count()
    if request.method=="POST": 
       # form=PostContent(request.POST)
        #if form.is_valid():  
          user = request.user
          image = request.user.profile.image
          content = request.POST.get('content','')
          branch = request.POST.get('branch','')
          post = Post(user1=user, post_content=content, image=image,branch=branch)
          post.save()
          messages.success(request, f'Your Question has been posted successfully!!')
          return redirect('/forum')
       # else:
           # form=PostContent()  
       
    posts = Post.objects.filter(branch=data.branch,).order_by('-timestamp')
   # form= PostContent()
    print(data.branch)
    context={
        'posts':posts,
        'branch':data.branch,
        'user_posts':user_posts
    }
    return render(request, "forum.html",context)





def edit_post(request, pk):
    post = Post.objects.get(id=pk)
    if request.method == 'POST':
        form = UpdatePostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Post updated successfully!")
            return redirect(reverse('dashboard:discussion', args=[post.id]))
    else:
        form = UpdatePostForm(instance=post)
    context = {
        'form': form
    }
    return render(request, 'edit_post.html', context)

def computer_science(request): 
    post = Post.objects.all()
    posts = Post.objects.filter(branch="Computer Science").order_by('-timestamp')
    return render(request, 'instructor/computer_science.html', {'posts':posts})   

def edit_reply(request, pk):
    reply = Replie.objects.get(id=pk)

    if request.method == 'POST':
        form = UpdateReplyForm(request.POST, instance=reply)
        if form.is_valid():
            form.save()
            messages.success(request, "Reply updated successfully!")
            return redirect(reverse('dashboard:discussion', args=[reply.post.id]))
    else:
        form = UpdateReplyForm(instance=reply)
    context = {
        'form': form
    }
    return render(request, 'edit_reply.html', context)
@login_required(login_url = 'login')   
def discussion(request, myid):
    post = Post.objects.filter(id=myid).first()
    replies = Replie.objects.filter(post=post)
    if request.method=="POST":
        form=ReplyContent(request.POST)
        if form.is_valid():  
          user = request.user
          image = request.user.profile.image
          desc = request.POST.get('reply_content','')
          post_id =request.POST.get('post_id','')
          reply = Replie(user = user, reply_content = desc, post=post, image=image)
          reply.save()
          messages.success(request, f'Your Reply has been posted successfully!!')
          return redirect(f'/discussion/{post_id}')
        else:
            form=ReplyContent()
    form= ReplyContent()
             
    return render(request, "discussion.html", {'post':post, 'replies':replies,'form':form})    


# notes views
@login_required(login_url = 'login')
def notes(request):
    if request.method=="POST":
         form=NotesForm(request.POST)
         if form.is_valid():
             notes=Notes(user=request.user,title=request.POST['title'],description=request.POST['description'])
             notes.save()
             messages.success(request,f"Notes added successfully!")
         else:
            form=NotesForm()     
    form=NotesForm()     
    notes = Notes.objects.filter(user = request.user)
    context={'notes':notes,'form':form}
    return render(request,'user/notes.html',context)

@login_required(login_url = 'login') 
def delete_note(request,pk=None):
        Notes.objects.get(id=pk).delete()
        return redirect("/notes")


class NotesDetailView(generic.DetailView):
        model=Notes 
        template_name = 'user/notes_detail.html' 

def update_notes(request, pk):
    note = Notes.objects.get(id=pk)
    if request.method == 'POST':
        form = UpdateNoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            messages.success(request,"Notes updated successfully!")
            return redirect('/notes')
    else:
        form = UpdateNoteForm(instance=note)
    context = {
        'form': form
    }
    return render(request, 'user/update_notes.html', context)

# Download pdf For notes

def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


class DownloadPdf(View):
    def get(self, request, pk, *args, **kwargs):
        try:
            note = Notes.objects.get(id = pk, user = request.user)     
        except:
            return HttpResponse("505 Not Found")
        data = {
            'id':note.id,
            'title':note.title,
            'description':note.description
            
        }
        pdf = render_to_pdf('user/pdf.html', data)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "notes_%s.pdf" %(data['id'])
            content = "inline; filename='%s'" %(filename)
            #download = request.GET.get("download")
            #if download:
            content = " attachment; filename=%s" %(filename)
            response['Content-Disposition'] = content
            print(note.title)
            
            return response
            
        return HttpResponse("Not found")

# pdf=======


#todo views
@login_required
def todo(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            todo=Task(user=request.user,content=request.POST['content'])
            todo.save()
            # form.save()
            return redirect('/todo')
    else:
        form = TaskForm()
    todo=Task.objects.filter(user=request.user)
    count_todos = todo.count()

    completed_todo = Task.objects.filter(complete=True,user=request.user)
    count_completed_todo = completed_todo.count()

    uncompleted = count_todos - count_completed_todo    
    context = {
        'todos': todo,
        'form': form,
        'count_todos': count_todos,
        'count_completed_todo': count_completed_todo,
        'uncompleted': uncompleted,
    }
    return render(request, 'user/todo.html', context)

@login_required
def update(request, pk):
    task = Task.objects.get(id=pk)
    if request.method == 'POST':
        form = UpdateTaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('/todo')
    else:
        form = UpdateTaskForm(instance=task)
    todo=Task.objects.filter(user=request.user)
    count_todos = todo.count()

    completed_todo = Task.objects.filter(complete=True,user=request.user)
    count_completed_todo = completed_todo.count()

    uncompleted = count_todos - count_completed_todo    
      
    context = {
        'todos': todo,
        'form': form,
        'count_todos': count_todos,
        'count_completed_todo': count_completed_todo,
        'uncompleted': uncompleted,
    }
    return render(request, 'user/update_task.html', context)

@login_required
def delete(request, pk):
    task = Task.objects.get(id=pk)
    if request.method == 'POST':
        task.delete()
        return redirect('/todo')
    todo=Task.objects.filter(user=request.user)
    count_todos = todo.count()

    completed_todo = Task.objects.filter(complete=True,user=request.user)
    count_completed_todo = completed_todo.count()

    uncompleted = count_todos - count_completed_todo    
     
    context = {
        'todos': todo,
        'count_todos': count_todos,
        'count_completed_todo': count_completed_todo,
        'uncompleted': uncompleted,
    }    
    return render(request, 'user/delete_task.html',context)



   
#book views

@login_required
def books(request):
   error=''
   if request.method == "POST":
      try:
        form=DashboardFom(request.POST)
        text=request.POST['text']
        url="https://www.googleapis.com/books/v1/volumes?q="+text
        r=requests.get(url)
        answer=r.json()

        result_list=[]
        for i in range(10):

            result_dict = {
            'title':answer['items'][i]['volumeInfo']['title'],
            'subtitle':answer['items'][i]['volumeInfo'].get('subtitle'),
            'description':answer['items'][i]['volumeInfo'].get('description'),
            'count':answer['items'][i]['volumeInfo'].get('pageCount'),
            'categories':answer['items'][i]['volumeInfo'].get('categories'),
            'rating':answer['items'][i]['volumeInfo'].get('pageRating'),
            'thumbnail':answer['items'][i]['volumeInfo'].get('imageLinks').get('thumbnail'),
            'preview':answer['items'][i]['volumeInfo'].get('previewLink')
             }

            result_list.append(result_dict) 
            context={'form':form,
            'results':result_list}      
        return render(request,"user/books.html",context)
      except Exception as e:
            error="please Enter a correct book name"
   else:
        form=DashboardFom()
   context={'form':form,'error':error}
   return render(request,"user/books.html",context)   



#tranlator views

def texttotxt(request):
     music = ''
     result=''
     
     if request.method == "POST":
        try:
          lang = request.POST.get("lang", None)
          text = request.POST.get("text", None)
          value={
              'text':text,
              'lang':lang
          }
          print(value)
          translator = Translator()
          tr = translator.translate(text, dest=lang)
          result=tr.text 
          object = gTTS(text=result, lang=lang,slow=False)
          object.save("static/speech.mp3")
          music = "ok"
          context={
            'music':music,
            'result':result,
            'value':value
         }
          return render(request,'user/texttotxt.html',context)
        except Exception as e:
            messages.success(request, 'Something Went Wrong Try Again')
     else:
        pass
     context={
        'music':music,
        'result':result,
       
    }
     return render(request,"user/texttotxt.html",context)
    





def texttospeech(request):
    
    music = ''
    if request.method =='POST' and request.FILES['pdf']:
        try:
           text = request.POST.get('text')
           lang =request.POST.get('lang')
           pdf = request.FILES['pdf'].read()
           value={
               'pdf':pdf
           }
           print(value)
           if pdf:
            pdfReader = PyPDF4.PdfFileReader(io.BytesIO(pdf))
            content = ''
            for i in range(int(pdfReader.numPages)):
              content += pdfReader.getPage(i).extractText()+"\n"
            text =content
            translator = Translator()
            tr = translator.translate(text, dest=lang)
            result=tr.text 
            object = gTTS(text=result, lang=lang,slow=False)
            object.save("static/speech.mp3")
            music = "ok"
            context={
            'music':music,
            'value':value
            }
            return render(request,'user/texttospeech.html',context) 
        except Exception as e:
            messages.success(request, 'Something Went Wrong Try Again!')             
    else:
        pass
    context={
        'music':music,
    }
    return render(request,"user/texttospeech.html",context)

@login_required
def upload_notes(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user = User.objects.get(id=request.user.id)
    data = Register.objects.get(user = user)    
    if request.method=='POST':
        branch = request.POST['branch']
        subject = request.POST['subject']
        notes = request.FILES['notesfile']
        filetype = request.POST['filetype']
        description = request.POST['description']

        user = User.objects.filter(username=request.user.username).first()
        Upload_Notes.objects.create(user=user,uploadingdate=date.today(),branch=branch,subject=subject,notesfile=notes,
                                 filetype=filetype,description=description,status='pending')
        messages.success(request,f"Notes uploaded from {request.user.username} successfully!")
        return redirect('/view_mynotes')
    return render(request,'user/upload_notes.html',{'branch':data.branch})

@login_required
def view_mynotes(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user = User.objects.get(id=request.user.id)

    notes = Upload_Notes.objects.filter(user = user)

    context = {'notes':notes}
    return render(request,'user/view_mynotes.html',context)

@login_required 
def delete_mynotes(request,pk=None):
    notes = Upload_Notes.objects.get(id=pk)
    notes.delete()
    return redirect("/view_mynotes")

@login_required
def pending_notes(request):
    pnotes = Upload_Notes.objects.filter(status = "pending")

    context = {'pnotes':pnotes}
    return render(request,'instructor/pending_notes.html',context)
@login_required
def assign_status(request, pk=None):
    notes = Upload_Notes.objects.get(id=pk)
    if request.method=='POST':
        status = request.POST['status']
        try:
            notes.status = status
            notes.save()
            messages.success(request,f" assign status to Notes successfully!")
            return redirect("/all_notes")
        except:
         messages.error(request, 'Something went wrong, Try Again')
    context = {'notes':notes,}
    return render(request,'instructor/assign_status.html',context)


def accepted_notes(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    notes = Upload_Notes.objects.filter(status = "Accept")
    context = {'notes':notes}
    return render(request, 'instructor/accepted_notes.html',context)

def rejected_notes(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    notes = Upload_Notes.objects.filter(status = "Reject")
    context = {'notes':notes}
    return render(request, 'instructor/rejected_notes.html',context)

def all_notes(request):
    if not request.user.is_authenticated:
        return redirect('login_admin')
    notes = Upload_Notes.objects.all()
    context = {'notes':notes}
    return render(request, 'instructor/all_notes.html',context)

def delete_notes(request, pk=None):
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('login')
        print(request.POST.get('notesid'))
        notes = Upload_Notes.objects.get(id=int(request.POST.get('notesid')))
        notes.delete()
        return JsonResponse({'msg': 'Notes deleted successfully !'})

@login_required
def delete_notess(request,pk=None):
    notes = Upload_Notes.objects.get(id=pk)
    notes.delete()
    messages.success(request,f"  Notes  delated  successfully!")
    return  redirect('/all_notes')
#def delete_notess(request, pk=None):
#     if request.method == 'POST':
#         if not request.user.is_authenticated:
#             return redirect('login')
#         print(request.POST.get('notesid'))
#         notes = Upload_Notes.objects.get(id=int(request.POST.get('notesid')))
#         notes.delete()
#         return JsonResponse({'msg': 'Notes deleted successfully !'})

def view_allnotes(request):
    if not request.user.is_authenticated:
        return redirect('login')
    user = User.objects.get(id=request.user.id)
    data = Register.objects.get(user = user)
     
    print(data.branch)  
    notes = Upload_Notes.objects.filter(status='Accept',branch=data.branch)
   
    context = {'notes':notes}
    return render(request, 'user/view_allnotes.html',context)    


def notessharing(request):
    user = User.objects.get(id=request.user.id)
    data = Register.objects.get(user = user)
    mynotes = Upload_Notes.objects.filter(user = user).count()
    allnotes = Upload_Notes.objects.filter(status='Accept',branch=data.branch).count()
    context={
        'mynotes':mynotes,
        'allnotes':allnotes
    }
    return render(request,"user/notessharing.html",context)