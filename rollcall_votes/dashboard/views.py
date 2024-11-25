from django.shortcuts import render
from data.models import Members, Bills
from django.db.models import Count
from graphics.views import generate_project_type_chart, generate_law_conversion_line_chart
from datetime import datetime


def dashboard(request):
    members_count = Members.objects.count()
    bills_by_type = Bills.objects.values('type').annotate(total=Count('type')) # [{'type': 'S', 'total': 50}, {'type': 'HR', 'total': 60}, {'type': 'SRES', 'total': 90}]
    laws_count = Bills.objects.filter(action_text__startswith="Became Public Law No:").count()    
    bill_type_chart = generate_project_type_chart(bills_by_type)
    last_bills = Bills.objects.all().order_by('-action_date')[:10]
    
    law_conversion_data = convert_date('action_date')
    law_conversion_chart = generate_law_conversion_line_chart(law_conversion_data)
    
    return render(request, 'dashboard.html', {
        'members_count': members_count,
        'bills_by_type': bills_by_type,
        'laws_count': laws_count,
        'bill_type_chart': bill_type_chart,
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

def convert_date(date):
    from datetime import datetime
    from django.db.models import F

    # Filtrar proyectos que se convirtieron en ley
    laws = Bills.objects.filter(action_text__startswith="Became Public Law No:")

    # Crear una lista procesada donde `action_date` se convierte a tipo `date`
    laws_by_date = []
    for law in laws:
        if law.action_date:  # Asegurarse de que `action_date` no sea None
            try:
                action_date_parsed = datetime.strptime(law.action_date, '%Y-%m-%d').date()
                laws_by_date.append({'action_date': action_date_parsed, 'id': law.bill_id})
            except ValueError:
                continue  # Ignorar fechas inválidas

    # Agrupar por `action_date` y contar los registros
    grouped_data = {}
    for entry in laws_by_date:
        date = entry['action_date']
        if date in grouped_data:
            grouped_data[date] += 1
        else:
            grouped_data[date] = 1

    # Convertir a lista para pandas, transformando la fecha a cadena
    data_for_chart = [{'action_date': date.strftime('%Y-%m-%d'), 'total': total} for date, total in grouped_data.items()]
    data_for_chart.sort(key=lambda x: x['action_date'])

    return data_for_chart
