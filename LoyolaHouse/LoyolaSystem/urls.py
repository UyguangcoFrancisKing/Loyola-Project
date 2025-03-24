from django.urls import path
from . import views


app_name = 'loyola'

urlpatterns = [
    path('profiles/', views.profiles_view, name='profiles'),
    path('logout/', views.log_out, name='logout'),
    path('dashboard/', views.email_view, name='dashboard'),
    path('create-announcement/', views.create_announcement, name='newAnnouncement'),
]   
