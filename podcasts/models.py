from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
import datetime

class Podcast(models.Model):
  title = models.CharField(
    max_length=200,
    verbose_name="عنوان الحلقة"
  )
  
  slug = models.SlugField(
    max_length=200,
    unique=True,
    verbose_name="الرابط (Slug)"
  )
  
  description = models.TextField(
    verbose_name="وصف الحلقة (Show Notes)"
  )
  
  # حقل لرفع الملف الصوتي مباشرة على السيرفر
  audio_file = models.FileField(
    upload_to='podcasts/audio/%Y/%m/%d/',
    blank=True,
    null=True,
    verbose_name="ملف الصوت (MP3/WAV)"
  )
  
  # if the podcast on other place
  audio_url = models.URLField(
    blank=True,
    null=True,
    verbose_name="رابط صوت خارجي (اختياري)"
  )
  
  cover_image = models.ImageField(
    upload_to='podcasts/covers/%Y/%m/%d/',
    verbose_name="غلاف الحلقة (Cover)"
  )
  
  duration = models.CharField(
    max_length=20,
    blank=True,
    null=True,
    help_text="مثال: 45:20",
    verbose_name="مدة الحلقة"
  )
  
  is_published = models.BooleanField(
    default=True,
    verbose_name="أنشر؟"
  )
  
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
  
  host = models.ForeignKey(
    User,
    on_delete=models.CASCADE,
    verbose_name="المقدم / المضيف"
  )

  class Meta:
    ordering = ['-created_at']
    verbose_name = "حلقة بودكاست"
    verbose_name_plural = "حلقات البودكاست"

  @property
  def is_new(self): # for 7days new
    return self.created_at >= timezone.now() - datetime.timedelta(days=7)

  def __str__(self):
    return self.title

  def get_absolute_url(self):
    return reverse('podcasts:detail', kwargs={'slug': self.slug})

  def save(self, *args, **kwargs):
    # Clean whitespaces before saving to database
    if self.title:
      self.title = self.title.strip()
    if self.description:
      self.description = self.description.strip()
    if self.seo_description:
      self.seo_description = self.seo_description.strip()
    if self.duration:
      self.duration = self.duration.strip()

    super().save(*args, **kwargs)


class PodcastComment(models.Model):
  username = models.CharField(
    max_length=50,
    default='غير معروف',
    verbose_name="الاسم"
  )
  email = models.EmailField(
    blank=True,
    null=True,
    verbose_name="البريد الإلكتروني"
  )
  comment = models.TextField(
    max_length=500,
    default='غير معروف',
    verbose_name="التعليق"
  )
  active = models.BooleanField(
    default=True,
    verbose_name="نشط"
  )
  podcast = models.ForeignKey(
    Podcast,
    on_delete=models.CASCADE,
    related_name='comments'
  )
  comment_date = models.DateTimeField(
    auto_now_add=True,
    verbose_name="تاريخ التعليق"
  )

  class Meta:
    verbose_name = "تعليق بودكاست"
    verbose_name_plural = "تعليقات البودكاست"
    ordering = ['-comment_date']

  def __str__(self):
    return f"Comment by {self.username} on {self.podcast.title}"