from django.contrib import admin
from django.urls import path
from . import views

app_name="dashboard"
urlpatterns=[
    path('',views.index,name="index"),
   path('user_home',views.user_home,name="user_home"),
   path('admin_home',views.admin_home,name="admin_home"), 
   path("forum", views.forum, name="forum"),
   path("discussion/<int:myid>", views.discussion, name="discussion"),
   path("showallusers", views.show_all_users, name="showallusers"),
   path('delete_user/<int:pk>',views.delete_user,name="delete_user"),
  path('computer_science',views.computer_science,name="computer_science"),
path('forum_a',views.forum_a,name="forum_a"),

   path('delete_post/<int:pk>',views.delete_post,name="delete_post"),
    path('delete_reply/<int:pk>',views.delete_reply,name="delete_reply"),
   path('notes',views.notes, name="notes"),
   path('delete_note/<int:pk>',views.delete_note,name="delete_note"),
   path('notes_detail/<int:pk>',views.NotesDetailView.as_view(),name="notes-detail"),
   path('update_notes/<int:pk>/', views.update_notes, name='update_notes'),
   path('books',views.books, name="books"),
 path('texttospeech',views.texttospeech, name="texttospeech"),
 path('texttotxt',views.texttotxt, name="texttotxt"), 
 path('todo', views.todo, name='todo'),
 path('update/<int:pk>/', views.update, name='todos-update'),
 path('delete/<int:pk>/', views.delete, name='todos-delete'),
 path('upload_notes', views.upload_notes, name='upload_notes'),
 path('view_mynotes', views.view_mynotes, name='view_mynotes'),
 path('delete_mynotes/<int:pk>/', views.delete_mynotes, name='delete_mynotes'),
 path('pending_notes', views.pending_notes, name='pending_notes'),
path('assign_status/<int:pk>', views.assign_status, name='assign_status'),
path('accepted_notes', views.accepted_notes, name='accepted_notes'),
path('rejected_notes', views.rejected_notes, name='rejected_notes'),
path('all_notes', views.all_notes, name='all_notes'),
path('delete_notes/<int:pk>', views.delete_notess, name='delete_notes'),
 path('delete-records/', views.delete_notes, name='delete_notes'),
path('view_allnotes', views.view_allnotes, name='view_allnotes'),
path('notessharing', views.notessharing, name='notessharing'),
path('download/<int:pk>/', views.DownloadPdf.as_view(), name = 'download'),
path('edit_post/<int:pk>/', views.edit_post, name='edit_post'),
path('edit_reply/<int:pk>/', views.edit_reply, name='edit_reply'),

 ]