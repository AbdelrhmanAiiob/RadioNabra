"""
Views for the Home application.
Responsible for rendering the main landing page and aggregating data from other apps (Articles, Podcasts).
"""

from django.views.generic import TemplateView
from articles.models import Article
from podcasts.models import Podcast

class IndexView(TemplateView):
    """
    Renders the main homepage of Radio Nabra.
    Aggregates the most recent published articles and podcasts to display as highlights/hero sections.
    """
    template_name = 'home/index.html'

    def get_context_data(self, **kwargs):
        """
        Injects the latest active articles and podcasts into the template context.
        """
        context = super().get_context_data(**kwargs)
        
        # Fetch the latest 3 published articles.
        # OPTIMIZATION: Added select_related('author') to prevent N+1 database queries 
        # in case the author's name is rendered on the homepage cards.
        context['latest_articles'] = Article.objects.select_related('author').filter(
            is_published=True
        ).order_by('-created_at')[:3]
        
        # Fetch the latest 4 published podcasts.
        # OPTIMIZATION: Added select_related('host') for the same N+1 prevention reason.
        context['latest_podcasts'] = Podcast.objects.select_related('host').filter(
            is_published=True
        ).order_by('-created_at')[:4]
        
        # TODO: Implement Django's cache framework (e.g., low-level cache API or template fragment caching) 
        # here in the future. The homepage is highly trafficked, and caching these read-heavy queries 
        # will significantly reduce database load and improve response time.
        
        return context