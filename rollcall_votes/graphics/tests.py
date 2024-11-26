"""
Unit tests for chart generation in the Dashboard application.

This module contains tests for the `PartyChart` and `LawConversionLineChart` 
classes, two types of graphs, ensuring that they generate valid 
HTML outputs based on input data.

Test cases:
    - test_law_conversion_line_chart_generation: Verifies the `LawConversionLineChart` 
      class generates valid HTML for line and area charts.
    - test_party_chart_generation: Verifies the `PartyChart` class generates valid HTML 
      for circular bar charts representing party distributions.

To execute the tests, run:
    python manage.py test graphics
"""
from django.test import TestCase
from .views import PartyChart, LawConversionLineChart

class ChartGenerationTests(TestCase):
    def setUp(self):
        self.law_data = [
            {'action_date': '2024-01-01', 'total': 10},
            {'action_date': '2024-02-01', 'total': 20},
            {'action_date': '2024-03-01', 'total': 15},
        ]
        self.party_data = [
            {'party_name': 'Democrat', 'total': 150},
            {'party_name': 'Republican', 'total': 140},
        ]


    def test_law_conversion_line_chart_generation(self):
        """Test LawConversionLineChart generates valid HTML."""
        chart = LawConversionLineChart()
        chart_html = chart.generate_chart(self.law_data)
        self.assertIn('<html>', chart_html)
        self.assertIn('</html>', chart_html)
        self.assertIn('2024-01-01', chart_html)
        self.assertIn('20', chart_html) 
        
        
    def test_party_chart_generation(self):
        """Test PartyChart generates valid HTML."""
        chart = PartyChart()
        chart_html = chart.generate_chart(self.party_data)
        self.assertIn('<html>', chart_html)
        self.assertIn('</html>', chart_html)
        self.assertIn('Democrat', chart_html)
        self.assertIn('Republican', chart_html)
