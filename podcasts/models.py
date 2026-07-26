"""
Database models for the Podcasts application.
Handles metadata, media files, and relationships for podcast episodes and user comments.
"""

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
import datetime

class Podcast(models.Model):
    """
    Represents a single podcast episode.
    Supports both internal audio file hosting and external URLs.
    """
    title = models.CharField(max_length=200, verbose_name="عنوان الحلقة")
    slug = models.SlugField(max_length=200, unique=True, verbose_name="الرابط (Slug)")
    
    description = models.TextField(verbose_name="وصف الحلقة (Show Notes)")
    
    # Organizes uploaded audio files dynamically by date
    audio_file = models.FileField(
        upload_to='podcasts/audio/%Y/%m/%d/',
        blank=True,
        null=True,
        verbose_name="ملف الصوت (MP3/WAV)"
    )
    
    # Fallback/Alternative: Link to externally hosted audio (e.g., SoundCloud, Spotify)
    audio_url = models.URLField(
        blank=True,
        null=True,
        verbose_name="رابط صوت خارجي (اختياري)"
    )
    
    cover_image = models.ImageField(
        upload_to='podcasts/covers/%Y/%m/%d/',
        verbose_name="غلاف الحلقة (Cover)"
    )
    
    # TODO: In future iterations, use a library like `mutagen` to automatically calculate audio duration on save.
    duration = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="مثال: 45:20",
        verbose_name="مدة الحلقة"
    )
    
    is_published = models.BooleanField(default=True, verbose_name="أنشر؟")
    
    seo_description = models.CharField(
        max_length=160,
        blank=True,
        null=True,
        verbose_name="وصف لمحركات البحث (SEO)"
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ الإضافة")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="تاريخ التعديل")
    
    host = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="المقدم / المضيف")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "حلقة بودكاست"
        verbose_name_plural = "حلقات البودكاست"

    @property
    def is_new(self): 
        """
        Determines if the podcast is considered 'new' (published within the last 7 days).
        Useful for UI badging.
        """
        return self.created_at >= timezone.now() - datetime.timedelta(days=7)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """
        Returns the canonical URL for the podcast detail page.
        """
        return reverse('podcasts:detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        """
        Overrides the default save behavior to sanitize text fields (strip whitespaces).
        """
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
    """
    Represents user feedback/comments on specific podcast episodes.
    """
    username = models.CharField(max_length=50, default='غير معروف', verbose_name="الاسم")
    email = models.EmailField(blank=True, null=True, verbose_name="البريد الإلكتروني")
    comment = models.TextField(max_length=500, default='غير معروف', verbose_name="التعليق")
    
    active = models.BooleanField(default=True, verbose_name="نشط")
    
    # Explicit related_name ('comments') allows efficient reverse querying from the Podcast model
    podcast = models.ForeignKey(
        Podcast,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    
    comment_date = models.DateTimeField(auto_now_add=True, verbose_name="تاريخ التعليق")

    class Meta:
        verbose_name = "تعليق بودكاست"
        verbose_name_plural = "تعليقات البودكاست"
        ordering = ['-comment_date']

    def __str__(self):
        return f"Comment by {self.username} on {self.podcast.title}"