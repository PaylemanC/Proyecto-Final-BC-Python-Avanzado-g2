from django.shortcuts import render
from data.models import Members, Bills
from django.db.models import Count
from graphics.views import generate_project_type_chart, generate_law_conversion_line_chart
from datetime import datetime


def dashboard(request):
    members_count = Members.objects.count()
    laws_count = Bills.objects.filter(action_text__startswith="Became Public Law No:").count()    
    last_bills = Bills.objects.all().order_by('-action_date')[:10]
    
    law_conversion_data = group_laws_by_date()
    law_conversion_chart = generate_law_conversion_line_chart(law_conversion_data)
    
    return render(request, 'dashboard.html', {
        'members_count': members_count,
        'laws_count': laws_count,
        'last_bills': last_bills,
        'law_conversion_chart': law_conversion_chart
    })  


def member_list(request):
    members = Members.objects.all()
    members_count = Members.objects.count()
    
    return render(request, 'member_list.html', {
        'members': members,
        'members_count': members_count
    })
    
def bill_list(request):
    bills = Bills.objects.all().order_by('-action_date')
    bills_by_type = Bills.objects.values('type').annotate(total=Count('type')) # [{'type': 'S', 'total': 50}, {'type': 'HR', 'total': 60}, {'type': 'SRES', 'total': 90}]
    bill_type_chart = generate_project_type_chart(bills_by_type)
    
    return render(request, 'bill_list.html', {
        'bills': bills,
        'bill_type_chart': bill_type_chart,
    })

def group_laws_by_date():
    laws = Bills.objects.filter(action_text__startswith="Became Public Law No:")

    laws_with_dates = []
    for law in laws:
        if law.action_date:
            try:
                action_date_parsed = datetime.strptime(law.action_date, '%Y-%m-%d').date()
                laws_with_dates.append({'action_date': action_date_parsed, 'id': law.bill_id})
            except ValueError:
                continue  
            
    laws_grouped_by_date = {}
    for entry in laws_with_dates:
        date = entry['action_date']
        if date in laws_grouped_by_date:
            laws_grouped_by_date[date] += 1
        else:
            laws_grouped_by_date[date] = 1
            
    chart_ready_data = [{'action_date': date.strftime('%Y-%m-%d'), 'total': total}
                        for date, total in laws_grouped_by_date.items()]
    chart_ready_data.sort(key=lambda x: x['action_date'])

    return chart_ready_data
