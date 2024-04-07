from django.shortcuts import render

from .forms import SearchByKeywordViewForm, ShowChartViewForm
from .tasks import tech_church_search_by_keyword_task
from .charts import number_of_articles_per_authors_chart, number_of_articles_per_tags_chart


# Create your views here.
def search_by_keyword_view(request):
    if request.method == 'POST':
        form = SearchByKeywordViewForm(request.POST)
        # Validate the form
        if form.is_valid():
            result = tech_church_search_by_keyword_task.delay(
                keyword=form.cleaned_data['keyword'],
                page_count=form.cleaned_data['page_count'],
            )
            print('tech_church_search_by_keyword_task results:', result)
    else:
        form = SearchByKeywordViewForm()

    return render(request, 'techchurch/search_by_keyword_view.html', {'form': form})


def show_chart_view(request):
    if request.method == 'POST':
        form = ShowChartViewForm(request.POST)
        # Validate the form
        if form.is_valid():
            choice = form.cleaned_data['chart']
            if choice == 'number_of_articles_per_authors':
                number_of_articles_per_authors_chart()
            elif choice == 'number_of_articles_per_tags':
                number_of_articles_per_tags_chart()

    else:
        form = ShowChartViewForm()

    return render(request, 'techchurch/show_chart_view.html', {'form': form})
