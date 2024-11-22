from django.urls import path
from . import views 

urlpatterns = [
    path('', views.parties_list, name='parties_list'),
]
