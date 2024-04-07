from django.urls import path
from .views import search_by_keyword_view, show_chart_view


urlpatterns = [
    path('search_by_keyword_view/', search_by_keyword_view),
    path('show_chart_view/', show_chart_view),
]
