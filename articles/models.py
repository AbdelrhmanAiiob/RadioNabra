"""
Database models for the Articles application.
Defines the schema for Articles and associated Comments.
"""

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
import datetime

class Article(models.Model):
    """
    Represents a blog post or news article.
    Includes SEO fields and publishing status.
    """
    title = models.CharField(
      max_length=200,
      verbose_name="عنوان المقال"
    )

    # A URL-friendly string used in routing instead of the database ID for better SEO.
    slug = models.SlugField(
      max_length=200,
      unique=True,
      verbose_name="الرابط (Slug)"
    )
    
    content = models.TextField(verbose_name="محتوى المقال")
    
    # Images are organized dynamically by upload date (Year/Month/Day)
    image = models.ImageField(upload_to='articles/%Y/%m/%d/', verbose_name="صورة المقال")
    
    is_published = models.BooleanField(default=True, verbose_name="أنشر؟")

    # Custom field to store a short summary for Search Engine Optimization (Meta Description).
    seo_description = models.CharField(
        max_length=160, 
        blank=True, 
        null=True, 
        verbose_name="وصف لمحركات البحث (SEO)"
    )

    created_at = models.DateTimeField(
      auto_now_add=True,
      verbose_name="تاريخ الإضافة"
    )
    updated_at = models.DateTimeField(
      auto_now=True,
      verbose_name="تاريخ التعديل"
    )

    # Foreign key linking the article to its author (User model)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="الكاتب")

    # TODO: Add a 'views_count' PositiveIntegerField to track popular articles.

    class Meta:
        ordering = ['-created_at'] # Default ordering: newest first
        verbose_name = "مقال"
        verbose_name_plural = "المقالات"

    @property
    def is_new(self):
        """
        Checks if the article was published within the last 7 days.
        Useful for rendering 'New' badges in the frontend templates.
        """
        return self.created_at >= timezone.now() - datetime.timedelta(days=7)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """
        Returns the canonical URL for this object.
        Enables the 'View on site' button in the Django admin panel.
        """
        return reverse('articles:detail', kwargs={'slug': self.slug})
  
    def save(self, *args, **kwargs):
        """
        Overrides the save method to perform data sanitization before committing to the DB.
        """
        if self.content:
            self.content = self.content.strip() # Remove leading/trailing whitespaces
        super().save(*args, **kwargs)


class Comment(models.Model):
    """
    Represents a user comment attached to a specific Article.
    """
    username = models.CharField(
      max_length=50,
      default='غير معروف'
    )
    email = models.EmailField(
      blank=True,
      null=True
    )
    comment = models.TextField(
      max_length=500,
      default='غير معروف'
    )
    
    # Soft delete capability: allows hiding comments without deleting them from the database
    active = models.BooleanField(default=True)
    
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    comment_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "تعليق المقال"
        verbose_name_plural = "تعليقات المقالات"
  
    def __str__(self):
        return f"Comment by {self.username} on {self.article.title}"