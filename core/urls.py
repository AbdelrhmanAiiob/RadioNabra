from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from home.views import coming_soon

urlpatterns = [
    path('nabra-control-admin', admin.site.urls),
    path('coming_soon', coming_soon, name='coming_soon'),
    path('', include('home.urls'), name='home'),
    path('articles/', include('articles.urls'), name='articles'),
    path('podcasts/', include('podcasts.urls'), name='podcasts'),
]

# debug= Ture(local)
if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)