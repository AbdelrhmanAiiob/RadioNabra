from django.contrib import admin
from .models import Article, Comment

# main article
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
  list_display= ('title', 'author', 'is_published', 'created_at')

  # Automatically fills the 'slug' field based on what you type in the 'title' field.
  prepopulated_fields= {'slug': ('title',)}

  # Hides the specified fields from the admin add/change form.
  exclude= ('author',)

  def get_queryset(self, request):
    """
      Overrides the default queryset to restrict access.
      Superusers can see all records, while regular staff (authors) 
      can only see and manage their own records.
    """
  
    qs= super().get_queryset(request)
    
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

# commentSide
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
  list_display = ('username', 'article', 'comment_date') # appear fields
  list_filter = ('comment_date', 'article')              # fields filter
  search_fields = ('username', 'comment')                # fields search

  def get_queryset(self, request):
    """
      Super user=> can see all,
      norma user=> just see he's comments or related to he's articles
    """
    qs = super().get_queryset(request)
    
    # if superUser
    if request.user.is_superuser:
      return qs
    
    # if normalUser filter the related comments and get the article author
    return qs.filter(article__author=request.user)