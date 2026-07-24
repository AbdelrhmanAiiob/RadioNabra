from django.urls import path
from .views import ArticleListView, ArticleDetailView, ArticleCreateView

app_name = 'articles'

urlpatterns = [
  path('', ArticleListView.as_view(), name='list'), # Index Page For ArticelAPP
  path('add/', ArticleCreateView.as_view(), name='add'),
  path('<slug:slug>/', ArticleDetailView.as_view(), name='detail'),
]