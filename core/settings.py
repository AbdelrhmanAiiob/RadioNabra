from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-!%eu+_*ma-(+%k=a-dw(qy#75$pae5*hc%l$*x)*-zbmu$je&^'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '192.168.1.6']


# Application definition
INSTALLED_APPS = [
  
    # for adminPanel edit
    'unfold',
    'unfold.contrib.filters',
    'unfold.contrib.forms',
    
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # ParentAPPs
    'home.apps.HomeConfig',
    'articles.apps.ArticlesConfig',
    'podcasts.apps.PodcastsConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
LANGUAGE_CODE = 'ar'
TIME_ZONE = 'Africa/Cairo'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_ROOT= os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_DIRS = [
  os.path.join(BASE_DIR, 'static')
]

# Media files
MEDIA_ROOT= os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# ==========================================
# UNFOLD ADMIN PANEL SETTINGS
# ==========================================
from django.templatetags.static import static

UNFOLD = {
    "SITE_TITLE": "إدارة راديو نبرة",
    "SITE_HEADER": "راديو نبرة",
    "SITE_URL": "/",
    "SITE_ICON": {
        "light": lambda request: static("images/main_logo.webp"),
        "dark": lambda request: static("images/main_logo.webp"),
    },
    "SITE_LOGO": {
        "light": lambda request: static("images/main_logo.webp"),
        "dark": lambda request: static("images/main_logo.webp"),
    },
    "STYLES": [
        lambda request: static("css/admin_custom.css"),
    ],
    
    "COLORS": {
        "primary": {
            "50": "#fbf8f1",
            "100": "#f5eedd",
            "200": "#ebdcb0",
            "300": "#e0c57f",
            "400": "#d4af37",
            "500": "#cba358", # لونك الأساسي
            "600": "#b8914b",
            "700": "#9a763c",
            "800": "#7f6235",
            "900": "#68502f",
        },
    },
    "TABS": [
        {
            "models": [
                "articles.article",
                "articles.comment",
            ],
            "items": [
                {"title": "المقالات", "link": "/admin/articles/article/"},
                {"title": "التعليقات", "link": "/admin/articles/comment/"},
            ],
        },
    ],
}