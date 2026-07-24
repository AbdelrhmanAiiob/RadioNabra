from django.contrib import admin
from .models import Podcast

@admin.register(Podcast)
class PodcastAdmin(admin.ModelAdmin):
  list_display = ('title', 'author', 'is_published', 'created_at')
  
  # Automatically fills the 'slug' field based on what you type in the 'title' field.
  prepopulated_fields = {'slug': ('title',)}
  
  # Hides the specified fields from the admin add/change form.
  exclude = ('author',)

  def get_queryset(self, request):
    """
      Overrides the default queryset to restrict access.
      Superusers can see all records, while regular staff (authors) 
      can only see and manage their own records.
    """
  
    qs = super().get_queryset(request)
    
    # If user is the admin. 
    if request.user.is_superuser:
      return qs

    # If normal user return he's own articles.
    return qs.filter(author=request.user)

  def save_model(self, request, obj, form, change):
    """
      Overrides the default save behavior.
      Automatically assigns the currently logged-in user as the 'author' 
      when a new record is created.
    """
  
    if not obj.pk: # New article.
      obj.author = request.user
    super().save_model(request, obj, form, change)