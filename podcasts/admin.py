"""
Admin configuration for the Podcasts application.
Integrates with Django Unfold and manages role-based access for podcast hosts.
"""

from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Podcast, PodcastComment

@admin.register(Podcast)
class PodcastAdmin(ModelAdmin):
    """
    Admin interface for the Podcast model.
    Ensures that regular hosts can only see and edit their own podcasts,
    while superusers maintain full control.
    """
    list_display = ('title', 'host', 'is_published', 'created_at')

    # Automatically fills the 'slug' field based on what is typed in the 'title' field for SEO optimization.
    prepopulated_fields = {'slug': ('title',)}

    # Exclude the host field as it is automatically populated based on the logged-in user.
    exclude = ('host',)
    
    # TODO: Add 'list_filter' (e.g., 'is_published', 'created_at') and 'search_fields' for better scalability.

    def get_queryset(self, request):
        """
        Overrides the default queryset to restrict access.
        """
        qs = super().get_queryset(request)
        
        if request.user.is_superuser:
            return qs
            
        return qs.filter(host=request.user)

    def save_model(self, request, obj, form, change):
        """
        Automatically assigns the currently logged-in user as the 'host' 
        when a new podcast record is created.
        """
        if not obj.pk:  # Check if this is a new object
            obj.host = request.user
        super().save_model(request, obj, form, change)


@admin.register(PodcastComment)
class PodcastCommentAdmin(ModelAdmin):
    """
    Admin interface for the PodcastComment model.
    Hosts can only view and manage comments associated with their own podcasts.
    """
    list_display = ('username', 'podcast', 'comment_date') 
    list_filter = ('comment_date', 'podcast')              
    search_fields = ('username', 'comment')                

    def get_queryset(self, request):
        """
        Filter comments based on user role using relationship spanning.
        """
        qs = super().get_queryset(request)
        
        if request.user.is_superuser:
            return qs
            
        return qs.filter(podcast__host=request.user)