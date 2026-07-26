"""
Admin configuration for the Articles application.
Integrates with Django Unfold for a modern, Tailwind-based UI.
Manages permissions, custom querysets, and automatic field population.
"""

from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Article, Comment

@admin.register(Article)
class ArticleAdmin(ModelAdmin):
    """
    Admin interface for the Article model.
    Restricts authors to only manage their own articles while allowing superusers full access.
    """
    list_display = ('title', 'author', 'is_published', 'created_at')
    
    # Auto-generate the slug based on the title for better SEO and UX.
    prepopulated_fields = {'slug': ('title',)}
    
    # Hide the author field; it will be automatically set in the save_model method.
    exclude = ('author',)

    # TODO: Consider adding 'search_fields' and 'list_filter' (e.g., by date or status) for easier navigation when articles grow.

    def get_queryset(self, request):
        """
        Override the default queryset to implement row-level permissions.
        Superusers view all records; standard staff view only their own records.
        """
        qs = super().get_queryset(request)
        
        if request.user.is_superuser:
            return qs
        
        return qs.filter(author=request.user)

    def save_model(self, request, obj, form, change):
        """
        Override the save behavior to automatically assign the logged-in user 
        as the author of the article upon creation.
        """
        if not obj.pk:  # Check if this is a new article being created
            obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(Comment)
class CommentAdmin(ModelAdmin):
    """
    Admin interface for the Comment model.
    Ensures authors can only moderate comments related to their own articles.
    """
    list_display = ('username', 'article', 'comment_date') 
    list_filter = ('comment_date', 'article')              
    search_fields = ('username', 'comment')                

    def get_queryset(self, request):
        """
        Filter comments based on user role. 
        Superusers see all; authors see comments attached to their specific articles.
        """
        qs = super().get_queryset(request)
        
        if request.user.is_superuser:
            return qs
        
        # Traverse the relationship: Comment -> Article -> Author
        return qs.filter(article__author=request.user)