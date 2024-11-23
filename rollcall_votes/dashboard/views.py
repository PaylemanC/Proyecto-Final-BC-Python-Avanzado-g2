from django.shortcuts import render
from graphics.views import generate_chart


def dashboard(request):
    chart_html = generate_chart()
    
    return render(request, 'dashboard.html', {'chart_html': chart_html})  


def rollcall(request):
    return render(request, 'rollcall.html')  
