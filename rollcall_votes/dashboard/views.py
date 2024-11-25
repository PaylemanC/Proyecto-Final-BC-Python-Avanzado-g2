from django.shortcuts import render
from graphics.views import generate_chart
from data.models import Members


def dashboard(request):
    chart_html = generate_chart()
    
    return render(request, 'dashboard.html', {
        'chart_html': chart_html
        })  


def member_list(request):
    members = Members.objects.all()
    members_count = Members.objects.count()
    
    return render(request, 'member_list.html', {
        'members': members,
        'members_count': members_count
    })
