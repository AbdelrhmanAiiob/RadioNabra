from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Podcast(models.Model):
  title= models.CharField(
    max_length=200,
    verbose_name="عنوان الحلقة"
  )

  # A URL-friendly string (e.g., 'my-article-title') used in the URL instead of the ID for better SEO.
  slug= models.SlugField(
    max_length=200,
    unique=True,
    verbose_name="الرابط (Slug)"
  )

  description= models.TextField(
    verbose_name="وصف الحلقة"
  )

  audio_file= models.FileField(
    upload_to='podcasts/audio/%Y/%m/%d/',
    verbose_name="الملف الصوتي"
  )

  image= models.ImageField(
    upload_to='podcasts/images/%Y/%m/%d/',
    verbose_name="صورة الغلاف"
  )

  is_published= models.BooleanField(
    default=True,
    verbose_name="منشورة؟"
  )

  created_at= models.DateTimeField(
    auto_now_add=True,
    verbose_name="تاريخ النشر"
  )

  # The podcast author publisher
  author= models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    verbose_name="مقدم الحلقة"
  )

  class Meta:
    ordering= ['-created_at']
    verbose_name= "حلقة بودكاست"
    verbose_name_plural= "حلقات البودكاست"

  def __str__(self):
    return self.title