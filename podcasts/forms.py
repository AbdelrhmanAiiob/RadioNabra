"""
Forms for the Podcasts application.
Utilizes Django ModelForms with injected Tailwind CSS classes for consistent frontend styling.
"""

from django import forms
from .models import Podcast, PodcastComment

class PodcastForm(forms.ModelForm):
    """
    Form for creating and updating Podcasts.
    Includes fields for direct audio uploads or external audio URLs.
    """
    class Meta:
        model = Podcast
        fields = [
            'title',
            'description',
            'audio_file',
            'audio_url',
            'cover_image',
            'duration',
            'seo_description',
            'is_published'
        ]

        # TODO: Implement a `clean()` method to ensure at least one audio source (file OR url) is provided.

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-[#cba358] focus:border-[#cba358] block w-full p-2.5 transition-colors',
                'placeholder': 'عنوان الحلقة...'
            }),
            'description': forms.Textarea(attrs={
                'class': 'block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-[#cba358] focus:border-[#cba358] transition-colors',
                'placeholder': 'اكتب وصف الحلقة (Show Notes) هنا...',
                'rows': 6
            }),
            'audio_file': forms.ClearableFileInput(attrs={
                'class': 'block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 focus:outline-none'
            }),
            'audio_url': forms.URLInput(attrs={
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-[#cba358] focus:border-[#cba358] block w-full p-2.5 transition-colors',
                'placeholder': 'https://example.com/audio.mp3',
                'dir': 'ltr'
            }),
            'cover_image': forms.ClearableFileInput(attrs={
                'class': 'block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 focus:outline-none'
            }),
            'duration': forms.TextInput(attrs={
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-[#cba358] focus:border-[#cba358] block w-full p-2.5 transition-colors',
                'placeholder': 'مثال: 45:20'
            }),
            'seo_description': forms.TextInput(attrs={
                'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-[#cba358] focus:border-[#cba358] block w-full p-2.5 transition-colors',
                'placeholder': 'وصف قصير لمحركات البحث...'
            }),
            'is_published': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-[#cba358] bg-gray-100 border-gray-300 rounded focus:ring-[#cba358]'
            }),
        }


class PodcastCommentForm(forms.ModelForm):
    """
    Form for user comments on podcasts.
    """
    class Meta:
        model = PodcastComment
        fields = [
            'username',
            'comment'
        ]
        
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'w-full bg-white border border-gray-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-[#cba358] focus:border-transparent transition-all',
                'placeholder': 'اكتب اسمك هنا (اختياري)...'
            }),
            'comment': forms.Textarea(attrs={
                'class': 'w-full bg-white border border-gray-200 rounded-xl px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-[#cba358] focus:border-transparent transition-all resize-none',
                'placeholder': 'شاركنا رأيك في الحلقة...',
                'rows': 4
            }),
        }