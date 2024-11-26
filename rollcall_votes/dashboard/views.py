from django.shortcuts import render
from data.models import Members, Bills
from django.db.models import Count
from graphics.views import ProjectTypeChart, PartyChart, LawConversionLineChart
from datetime import datetime

def dashboard(request):
    members_count = Members.objects.count()
    laws_count = Bills.objects.filter(action_text__startswith="Became Public Law No:").count()    
    last_bills = Bills.objects.all().order_by('-action_date')[:10]
    
    law_conversion_data = group_laws_by_date()
    law_chart = LawConversionLineChart()
    law_conversion_chart = law_chart.generate_chart(law_conversion_data)
    
    return render(request, 'dashboard.html', {
        'members_count': members_count,
        'laws_count': laws_count,
        'last_bills': last_bills,
        'law_conversion_chart': law_conversion_chart
    })  


def member_list(request):
    members = Members.objects.all()
    members_count = Members.objects.count()
    
    party_distribution = (
        members.values('party_code__name')  
        .annotate(total=Count('member_id'))  
        .order_by('party_code__name') 
    )
    
    chart_data = [{'party_name': entry['party_code__name'], 'total': entry['total']} for entry in party_distribution]
    
    party_chart = PartyChart()
    members_type_chart = party_chart.generate_chart(chart_data)
    
    return render(request, 'member_list.html', {
        'members': members,
        'members_count': members_count,
        'members_type_chart': members_type_chart
    })
    
    
def bill_list(request):
    bills = Bills.objects.all().order_by('-action_date')
    bills_by_type = Bills.objects.values('type').annotate(total=Count('type')) 
    chart_data = [{'type': entry['type'], 'total': entry['total']} for entry in bills_by_type]
    
    project_chart = ProjectTypeChart()
    bill_type_chart = project_chart.generate_chart(chart_data)
    
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
