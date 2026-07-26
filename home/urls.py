"""
URL configurations for the Home application.
Handles the routing for the landing page and static-informational pages (About, Contact).
"""

from django.urls import path
from django.views.generic import TemplateView
from . import views

app_name = 'home'

urlpatterns = [
    # Main landing page displaying the latest aggregated content
    path('', views.IndexView.as_view(), name='index'),

    # OPTIMIZATION: Using TemplateView directly in urlpatterns for static pages.
    # This is a best practice to keep views.py clean when no complex context logic or form handling is needed.
    path('about/', TemplateView.as_view(template_name='home/about.html'), name='about'),
    path('contact/', TemplateView.as_view(template_name='home/contact.html'), name='contact'),
    
    # TODO: If the Contact page later requires form handling (e.g., sending emails via a contact form), 
    # move it to a dedicated FormView or CreateView in views.py.
]