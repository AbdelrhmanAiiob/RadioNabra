from django import forms
from .models import Article, Comment

class ArticleForm(forms.ModelForm):
  class Meta:
    model= Article
    fields= [
      'title',
      'content',
      'image',
      'seo_description',
      'is_published'
    ]

    widgets= {
      'title': forms.TextInput(attrs={
        'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5',
        'placeholder': 'عنوان المقال...'
      }),
      
      'content': forms.Textarea(attrs={
        'class': 'block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500',
        'placeholder': 'اكتب محتوى المقال هنا...',
        'rows': 6
      }),
      
      'image': forms.ClearableFileInput(attrs={
        'class': 'block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 focus:outline-none'
      }),
      
      'seo_description': forms.TextInput(attrs={
        'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5',
        'placeholder': 'وصف قصير لمحركات البحث...'
      }),
      
      'is_published': forms.CheckboxInput(attrs={
        'class': 'w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500'
      
      }),
    }

class CommentForm(forms.ModelForm):
  class Meta:
    model= Comment
    fields= [
      'username',
      'comment'
    ]
    
    widgets= {
        'username': forms.TextInput(attrs={
        'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5',
        'placeholder': 'اسمك (لو سيبته فاضي هيبقى Unknown)...'
      }),

      'comment': forms.Textarea(attrs={
        'class': 'block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-blue-500 focus:border-blue-500',
        'placeholder': 'اكتب تعليقك هنا...',
        'rows': 4
      }),
    }