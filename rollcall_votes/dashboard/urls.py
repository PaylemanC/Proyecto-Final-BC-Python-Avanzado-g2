from django.urls import path
from . import views


urlpatterns = [
    path('', views.dashboard, name='dashboard'),  
    path('rollcall_list/', views.rollcall_list, name="rollcall_list"),
    path('legislators', views.member_list, name="member_list"),
    path('rollcall/', views.rollcall, name='rollcall'),  
]
