from django.views.generic import TemplateView
from django.http import HttpResponse
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from home.views import coming_soon
from django.contrib.sitemaps.views import sitemap
from core.sitemaps import ArticleSitemap, PodcastSitemap

sitemaps = {
    'articles': ArticleSitemap,
    'podcasts': PodcastSitemap,
}

urlpatterns = [
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('googled0a8a8e73a7d08e9.html', lambda request: HttpResponse("google-site-verification: googled0a8a8e73a7d08e9.html")),
  
    path('nabra-control-admin', admin.site.urls),
    path('coming_soon', coming_soon, name='coming_soon'),
    path('', include('home.urls'), name='home'),
    path('articles/', include('articles.urls'), name='articles'),
    path('podcasts/', include('podcasts.urls'), name='podcasts'),
]



# debug= Ture(local)
if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)