import altair as alt
import pandas as pd
from django.shortcuts import render


def dashboard(request):
    return render(request, 'dashboard.html')


def rollcall(request):
    return render(request, 'rollcall.html')


def chart_view(request):
    data = pd.DataFrame({
        'category': ['A', 'B', 'C', 'D', 'E'],
        'value': [30, 20, 50, 40, 60]
    })
    
    chart = alt.Chart(data).mark_bar().encode(
        x='category',
        y='value',
        tooltip=['category', 'value'] 
    )
    
    chart_html = chart.to_html()
    
    return render(request, 'chart_template.html', {'chart_html': chart_html})