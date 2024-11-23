from django.shortcuts import render
from graphics.views import generate_chart
from data.models import Members


def dashboard(request):
    chart_html = generate_chart()
    members = Members.objects.all()
    members_count = Members.objects.count()
    
    return render(request, 'dashboard.html', {
        'chart_html': chart_html,
        'members': members,
        'members_count': members_count
        })  


def rollcall_list(request):
    return render(request, 'rollcall_list.html')


def rollcall(request):
    return render(request, 'rollcall.html')  


def member_list(request):
    return render(request, 'member_list.html')