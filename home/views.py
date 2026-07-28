"""
Views for the Home application.
Responsible for rendering the main landing page and aggregating data from other apps (Articles, Podcasts).
"""

from django.shortcuts import render
from django.views.generic import TemplateView
from django.core.cache import cache 
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
        Utilizes Django's low-level cache API to optimize database queries.
        """
        context = super().get_context_data(**kwargs)
        
        latest_articles = cache.get('homepage_latest_articles')
        
        if not latest_articles:
            latest_articles = Article.objects.select_related('author').filter(
                is_published=True
            ).order_by('-created_at')[:3]
            
            cache.set('homepage_latest_articles', latest_articles, 60 * 15)
            
        context['latest_articles'] = latest_articles
        
        
        latest_podcasts = cache.get('homepage_latest_podcasts')
        
        if not latest_podcasts:
            latest_podcasts = Podcast.objects.select_related('host').filter(
                is_published=True
            ).order_by('-created_at')[:4]
            
            cache.set('homepage_latest_podcasts', latest_podcasts, 60 * 15)
            
        context['latest_podcasts'] = latest_podcasts
        
        return context


def global_search(request):
    """
    Handles global search queries across both Articles and Podcasts.
    Returns results to a unified search results page.
    """
    query = request.GET.get('q', '').strip()
    articles = []
    podcasts = []

    if query:
        # articles
        articles = Article.objects.filter(title__icontains=query, is_published=True).order_by('-created_at')
        # podcasts
        podcasts = Podcast.objects.filter(title__icontains=query, is_published=True).order_by('-created_at')

    context = {
        'query': query,
        'articles': articles,
        'podcasts': podcasts,
    }
    return render(request, 'home/search_results.html', context)


def coming_soon(request):
    return render(request, 'home/coming_soon.html')