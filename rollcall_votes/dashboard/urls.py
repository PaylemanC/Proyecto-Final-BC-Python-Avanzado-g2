from django.urls import path
from . import views


urlpatterns = [
    path('', views.dashboard, name='dashboard'), 
    path('legislators', views.member_list, name="member_list")
]
