from django.contrib.sitemaps import Sitemap
from articles.models import Article
from podcasts.models import Podcast

class ArticleSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Article.objects.all()

    def lastmod(self, obj):
        return getattr(obj, 'created_at', None)

class PodcastSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.9

    def items(self):
        return Podcast.objects.all()

    def lastmod(self, obj):
        return getattr(obj, 'created_at', None)