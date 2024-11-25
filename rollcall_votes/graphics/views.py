import altair as alt
import pandas as pd


def generate_project_type_chart(data):
    df = pd.DataFrame(data)

    df['percentage'] = (df['total'] / df['total'].sum()) * 100
    
    df['percentage'] = df['percentage'].round(2)
    
    df = df.sort_values('percentage')
    
    chart = alt.Chart(df).mark_arc(innerRadius=50).encode(
        theta='percentage:Q',
        color='type:N',
        tooltip=['type:N', 'percentage:Q'],
        text='type:N',
        order=alt.Order('percentage:Q', sort='ascending')
    )
    
    return chart.to_html()
