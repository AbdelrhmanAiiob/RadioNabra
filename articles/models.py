from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
import datetime

class Article(models.Model):
  title= models.CharField(
    max_length=200,
    verbose_name="عنوان المقال"
  )

  # A URL-friendly string (e.g., 'my-article-title') used in the URL instead of the ID for better SEO.
  slug= models.SlugField(
    max_length=200,
    unique=True,
    verbose_name="الرابط (Slug)"
  )

  content= models.TextField(
    verbose_name="محتوى المقال"
  )

  image= models.ImageField(
    upload_to='articles/%Y/%m/%d/',
    verbose_name="صورة المقال"
  )

  is_published= models.BooleanField(
    default=True,
    verbose_name="أنشر؟"
  )

  # Custom field to store a short summary for search engines (Meta Description).
  seo_description= models.CharField(
    max_length=160,
    blank=True,
    null=True,
    verbose_name="وصف لمحركات البحث (SEO)"
  )

  created_at= models.DateTimeField(
    auto_now_add=True,
    verbose_name="تاريخ الإضافة"
  )
  updated_at= models.DateTimeField(
    auto_now=True,
    verbose_name="تاريخ التعديل"
  )

  # The articles author publisher
  author= models.ForeignKey(
    User,
    on_delete= models.CASCADE,
    verbose_name="الكاتب"
  )

  class Meta:
    ordering= ['-created_at']
    verbose_name= "مقال"
    verbose_name_plural= "المقالات"

  @property
  def is_new(self):
    return self.created_at >= timezone.now() - datetime.timedelta(days=7)

  def __str__(self):
    return self.title

  # 
  def get_absolute_url(self):
    """
      Returns the canonical URL for this object,
      used in templates and to enable the "View on site" button in the admin panel.
    """
    return reverse('articles:detail', kwargs={'slug': self.slug})

class Comment(models.Model):
  username= models.CharField(
    max_length=50,
    default='unknown' 
  )
  email = models.EmailField(
    blank=True,
    null=True
  )
  comment= models.TextField(
    max_length=500,
    default= 'Unknown'
  )
  active = models.BooleanField(
    default=True
  )
  article= models.ForeignKey(
    Article,
    on_delete=models.CASCADE,
  )
  
  comment_date= models.DateTimeField(
    auto_now_add=True
  )

  class Meta:
    verbose_name= "تعليق"
    verbose_name_plural= "التعليقات"
  
  def __str__(self):
    return f"Comment by {self.username} on {self.article.title}"
