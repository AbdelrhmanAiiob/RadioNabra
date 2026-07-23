from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Article(models.Model):
  title= models.CharField(
    max_length= 200,
    verbose_name="عنوان المقال"
  )
  
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
  
  author= models.ForeignKey(
    User,
    on_delete= models.CASCADE,
    verbose_name="الكاتب"
  )
  
  class Meta:
    ordering = ['-created_at']
    verbose_name = "مقال"
    verbose_name_plural = "المقالات"
  
  def __str__(self):
    return self.title
  
  def get_absolute_url(self):
    return reverse('articles:detail', kwargs={'slug': self.slug})