from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.register, name='register'),
    path('login/',views.login_view, name='login'),
    path('dashboard/',views.dashboard, name='dashboard'),
    path('meeting/',views.videocall, name='meeting'),
    path('logout/',views.logout_view, name='logout'),
    path('join/',views.join_room, name='join_room'),
    path('',views.index, name='index'),
    path('join/leave_room/', views.leave_room, name='leave_room'),
    path('view_report/', views.view_report, name='view_report'),
    path('create_sec/', views.create_sec, name='create_sec'),
]