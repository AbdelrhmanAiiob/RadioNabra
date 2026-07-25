from django.views.generic import TemplateView
from articles.models import Article
from podcasts.models import Podcast

class IndexView(TemplateView):
  template_name = 'home/index.html'

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['latest_articles'] = Article.objects.filter(is_published=True).order_by('-created_at')[:3]
    context['latest_podcasts'] = Podcast.objects.filter(is_published=True).order_by('-created_at')[:4]
    return context