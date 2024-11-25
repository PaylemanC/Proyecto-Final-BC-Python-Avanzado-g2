from django.shortcuts import render
# from graphics.views import generate_chart
from data.models import Members, Bills
from django.db.models import Count
from graphics.views import generate_project_type_chart


def dashboard(request):
    members_count = Members.objects.count()
    bills_by_type = Bills.objects.values('type').annotate(total=Count('type')) # [{'type': 'S', 'total': 50}, {'type': 'HR', 'total': 60}, {'type': 'SRES', 'total': 90}]
    laws_count = Bills.objects.filter(action_text__startswith="Became Public Law No:").count()    
    bill_type_chart = generate_project_type_chart(bills_by_type)
    last_bills = Bills.objects.all().order_by('-action_date')[:10]
    
    return render(request, 'dashboard.html', {
        'members_count': members_count,
        'bills_by_type': bills_by_type,
        'laws_count': laws_count,
        'bill_type_chart': bill_type_chart,
        'last_bills': last_bills
        })  


def member_list(request):
    members = Members.objects.all()
    members_count = Members.objects.count()
    
    return render(request, 'member_list.html', {
        'members': members,
        'members_count': members_count
    })
