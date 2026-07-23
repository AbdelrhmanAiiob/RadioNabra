from django.contrib import admin
from .models import Article

# AdminSite
class ArticleAdmin(admin.ModelAdmin):
  list_display = ('title', 'is_published', 'created_at')
  prepopulated_fields = {'slug': ('title',)}


admin.site.register(Article)
