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

def generate_party_chart(data):
    df = pd.DataFrame(data)
    
    df['percentage'] = (df['total'] / df['total'].sum()) * 100
    df['percentage'] = df['percentage'].round(2)
    
    df = df.sort_values('percentage')
    
    chart = alt.Chart(df).mark_arc(innerRadius=50).encode(
        theta='percentage:Q',
        color='party_name:N',
        tooltip=['Parties:N', 'percentage:Q'],
        order=alt.Order('percentage:Q', sort='ascending')
    )
    
    return chart.to_html()


def generate_law_conversion_line_chart(data):
    df = pd.DataFrame(data)
    line = alt.Chart(df).mark_line(point=alt.OverlayMarkDef(filled=False, fill="white")).encode(
        x=alt.X('action_date:T', title='Date'),
        y=alt.Y('total:Q', title='Number of Laws Passed'),
        strokeWidth=alt.value(2.5),
        color=alt.value('#F8BD7A'),
        tooltip=[
            alt.Tooltip('action_date:T', title='Date'),
            alt.Tooltip('total:Q', title='Laws Passed')
        ]
    )

    area = alt.Chart(df).mark_area(
            line={'color': '#F8BD7A'}, 
            color=alt.Gradient(
                gradient='linear',
                stops=[
                    alt.GradientStop(color='white', offset=0),
                    alt.GradientStop(color='#F8BD7A', offset=1)
                ],
                x1=1, x2=1, y1=1, y2=0 )
            ).encode(
                x='action_date:T',
                y='total:Q',
                tooltip=[
                    alt.Tooltip('action_date:T', title='Date'),
                    alt.Tooltip('total:Q', title='Laws Passed')
                ]
            )

    law_line_chart = (area + line).properties(
        width=700,
        height=300
    )
    
    return law_line_chart.to_html()
