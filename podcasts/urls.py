from django.urls import path
from . import views

app_name = 'podcasts'
urlpatterns = [
  path('', views.PodcastListView.as_view(), name='list'),
  path('create/', views.PodcastCreateView.as_view(), name='create'),
  path('<slug:slug>/', views.PodcastDetailView.as_view(), name='detail'),
]