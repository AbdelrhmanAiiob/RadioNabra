from django.contrib import admin
from .models import Podcast, PodcastComment

# main podcast
@admin.register(Podcast)
class PodcastAdmin(admin.ModelAdmin):
  list_display = ('title', 'host', 'is_published', 'created_at')

  # Automatically fills the 'slug' field based on what you type in the 'title' field.
  prepopulated_fields = {'slug': ('title',)}

  exclude = ('host',)

  def get_queryset(self, request):
    qs = super().get_queryset(request)
    
    if request.user.is_superuser:
      return qs
    return qs.filter(host=request.user)

  def save_model(self, request, obj, form, change):
    if not obj.pk: 
      obj.host = request.user
    super().save_model(request, obj, form, change)


# commentSide
@admin.register(PodcastComment)
class PodcastCommentAdmin(admin.ModelAdmin):
  list_display = ('username', 'podcast', 'comment_date') 
  list_filter = ('comment_date', 'podcast')              
  search_fields = ('username', 'comment')                

  def get_queryset(self, request):
    qs = super().get_queryset(request)
    
    if request.user.is_superuser:
      return qs
    return qs.filter(podcast__host=request.user)