from django.contrib import admin
from .models import Article

# AdminSite

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
  list_display= ('title', 'is_published', 'created_at')


