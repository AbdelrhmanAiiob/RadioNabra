from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'home'

urlpatterns = [
  path('', views.IndexView.as_view(), name='index'),
  path('about/', TemplateView.as_view(template_name='home/about.html'), name='about'),
  path('contact/', TemplateView.as_view(template_name='home/contact.html'), name='contact'),
]