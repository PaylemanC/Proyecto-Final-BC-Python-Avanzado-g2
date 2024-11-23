from django.shortcuts import render


def dashboard(request):
    return render(request, 'dashboard.html')  


def rollcall(request):
    return render(request, 'rollcall.html')  
