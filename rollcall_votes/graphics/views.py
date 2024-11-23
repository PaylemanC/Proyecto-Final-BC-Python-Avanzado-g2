import altair as alt
import pandas as pd


def generate_chart():
    data = pd.DataFrame({
        'category': ['A', 'B', 'C', 'D', 'E'],
        'value': [30, 20, 50, 40, 60]
    })
    
    chart = alt.Chart(data).mark_bar().encode(
        x='category',
        y='value',
        tooltip=['category', 'value'] 
    )
    
    return chart.to_html()
