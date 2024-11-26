"""
Classes used to generate charts in the application's Dashboard with Vega-Altair, 
designed to represent and generate specific visual charts based on the provided data.

Each class provides a `generate_chart` method that accepts data in the form of 
a list of dictionaries and returns the chart in HTML format.
"""

import altair as alt
import pandas as pd
from abc import ABC, abstractmethod

class ChartGenerator(ABC):
    @abstractmethod
    def generate_chart(self, data) -> str:
        """Generates an HTML representation of a chart."""
        pass
    
class BaseChartGenerator(ChartGenerator):
    """
    Base class with common functionality for chart generation. 

    The class is intended to be extended by other specific chart generator classes
    which will implement their specific charting logic.

    Methods:
        __init__():
            Initializes the base chart generator with an empty DataFrame.
        
        _prepare_data(data: list[dict], percentage_column: str):
            Prepares the data by calculating percentages and sorting the values based on the specified column.
        
        _get_chart_html(chart: alt.Chart) -> str:
            Converts the Altair chart object to HTML format.

    Parameters for `_prepare_data`:
        data (list of dict): A list of dictionaries where each dictionary contains 'type' and 'total' keys.
        percentage_column (str): The column name by which the data will be sorted (e.g., 'percentage').

    """
    def __init__(self):
        self._df = None 
    
    def _prepare_data(self, data: list[dict], percentage_column: str) -> None:
        self._df = pd.DataFrame(data)
        self._df['percentage'] = (self._df['total'] / self._df['total'].sum()) * 100
        self._df['percentage'] = self._df['percentage'].round(2)
        self._df = self._df.sort_values(percentage_column)

    def _get_chart_html(self, chart: alt.Chart) -> str:
        return chart.to_html()

class ProjectTypeChart(BaseChartGenerator):
    """
    Generates a circular bar chart to visualize the percentage distribution of project types.

    Parameters for `generate_chart`:
        data (list of dict): A list of dictionaries with 'type' and 'total' keys.
    """
    def generate_chart(self, data) -> str:
        '''Generates the chart based on the input data, returning it as an HTML string.'''
        self._prepare_data(data, 'percentage')
        chart = alt.Chart(self._df).mark_arc(innerRadius=50).encode(
            theta='percentage:Q',
            color='type:N',
            tooltip=['type:N', 'percentage:Q'],
            text='type:N',
            order=alt.Order('percentage:Q', sort='ascending')
        )
        return self._get_chart_html(chart)
    
    
class PartyChart(BaseChartGenerator):
    """
    Generates a circular bar chart to visualize the percentage distribution of members by party.

    Methods:
        generate_chart(data): Generates the chart based on the input data, returning it as an HTML string.

    Parameters for `generate_chart`:
        data (list of dict): A list of dictionaries with 'party_name' and 'total' keys.
    """
    def generate_chart(self, data) -> str:
        '''Generates the chart based on the input data, returning it as an HTML string.'''
        self._prepare_data(data, 'percentage')
        chart = alt.Chart(self._df).mark_arc(innerRadius=50).encode(
            theta='percentage:Q',
            color='party_name:N',
            tooltip=['party_name:N', 'percentage:Q'],
            order=alt.Order('percentage:Q', sort='ascending')
        )
        return self._get_chart_html(chart)
    
    
class LawConversionLineChart(BaseChartGenerator):
    """
    Generates a line and area chart to visualize the number of laws passed over time.

    Parameters for `generate_chart`:
        data (list of dict): A list of dictionaries with 'action_date' and 'total' keys.
    """
    def generate_chart(self, data) -> str:
        '''Generates the chart based on the input data, returning it as an HTML string.'''
        self._df = pd.DataFrame(data)  
        
        line = alt.Chart(self._df).mark_line(point=alt.OverlayMarkDef(filled=False, fill="white")).encode(
            x=alt.X('action_date:T', title='Date'),
            y=alt.Y('total:Q', title='Number of Laws Passed'),
            strokeWidth=alt.value(2.5),
            color=alt.value('#F8BD7A'),
            tooltip=[
                alt.Tooltip('action_date:T', title='Date'),
                alt.Tooltip('total:Q', title='Laws Passed')
            ]
        )

        area = alt.Chart(self._df).mark_area(
            line={'color': '#F8BD7A'}, 
            color=alt.Gradient(
                gradient='linear',
                stops=[
                    alt.GradientStop(color='white', offset=0),
                    alt.GradientStop(color='#F8BD7A', offset=1)
                ],
                x1=1, x2=1, y1=1, y2=0
            )
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
        return self._get_chart_html(law_line_chart)
