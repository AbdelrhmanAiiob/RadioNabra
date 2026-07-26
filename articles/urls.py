"""
URL configurations for the Articles application.
Maps URLs to their respective Class-Based Views (CBVs).
"""

from django.urls import path
from .views import ArticleListView, ArticleDetailView, ArticleCreateView

app_name = 'articles'

urlpatterns = [
    # Main article listing page
    path('', ArticleListView.as_view(), name='list'), 
    
    # Endpoint to create a new article from the frontend (if applicable)
    path('add/', ArticleCreateView.as_view(), name='add'),
    
    # Detailed view of a specific article, identified by its slug
    path('<slug:slug>/', ArticleDetailView.as_view(), name='detail'),
]