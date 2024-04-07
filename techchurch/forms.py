from django import forms
from django.conf import settings


class SearchByKeywordViewForm(forms.Form):
    keyword = forms.CharField(label='Keyword', max_length=250)
    page_count = forms.IntegerField(
        label='Page Count',
        min_value=1,
        max_value=settings.MAXIMUM_PAGE_COUNT,
        initial=settings.DEFAULT_PAGE_COUNT,
    )


class ShowChartViewForm(forms.Form):
    CHART_CHOICES = (
        ('number_of_articles_per_authors', 'Number of Articles Per Authors'),
        ('number_of_articles_per_tags', 'Number of Articles Per Tags')
    )

    chart = forms.CharField(
        label='Chart',
        widget=forms.Select(choices=CHART_CHOICES),
        initial=settings.DEFAULT_CHART_CHOICE
    )
