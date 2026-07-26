"""
Django settings for the Radio Nabra project.
Configures environments, databases, security protocols, and third-party integrations (e.g., Unfold).
Follows industry best practices by utilizing environment variables (.env) for sensitive data.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from a .env file into the system's environment
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ==========================================
# SECURITY & CORE SETTINGS
# ==========================================

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
# Parses the string 'True'/'False' from the .env file into a Python boolean
DEBUG = os.getenv('DEBUG', 'False') == 'True'

# Defines which host/domain names this Django site can serve
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '127.0.0.1').split(',')


# ==========================================
# APPLICATIONS & MIDDLEWARE
# ==========================================

INSTALLED_APPS = [
    # --- Third-Party Apps ---
    # Unfold: A modern, Tailwind CSS-based admin interface
    'unfold',
    'unfold.contrib.filters',
    'unfold.contrib.forms',
    
    # --- Django Core Apps ---
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # --- Local Apps ---
    'home.apps.HomeConfig',
    'articles.apps.ArticlesConfig',
    'podcasts.apps.PodcastsConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # TODO: Add 'whitenoise.middleware.WhiteNoiseMiddleware' here later for efficient static files serving in production.
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


# ==========================================
# DATABASE CONFIGURATION
# ==========================================
# Uses PostgreSQL for robust, production-ready data management.
# Credentials are securely fetched from environment variables.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST', 'localhost'),
        'PORT': os.getenv('DB_PORT', '5432'),
    }
}


# ==========================================
# PASSWORD VALIDATION & INTERNATIONALIZATION
# ==========================================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'ar'
TIME_ZONE = 'Africa/Cairo'
USE_I18N = True
USE_TZ = True


# ==========================================
# STATIC & MEDIA FILES
# ==========================================
# Static files (CSS, JS, Images) used by the application
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

# User-uploaded files (e.g., Article images, Podcast audio)
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
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
            "500": "#cba358", # Brand primary color (Gold)
            "600": "#b8914b",
            "700": "#9a763c",
            "800": "#7f6235",
            "900": "#68502f",
        },
    },
    "TABS": [
        {
            "models": ["articles.article", "articles.comment"],
            "items": [
                {"title": "المقالات", "link": "/admin/articles/article/"},
                {"title": "التعليقات", "link": "/admin/articles/comment/"},
            ],
        },
    ],
}


# ==========================================
# PRODUCTION SECURITY SETTINGS
# ==========================================
# TODO: Uncomment 'SECURE_SSL_REDIRECT = True' when deploying to production with an active SSL certificate. (DONE)

# Ensures cookies are only sent over HTTPS
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Enables the browser's built-in XSS protection
SECURE_BROWSER_XSS_FILTER = True

# Prevents the site from being rendered inside an iframe (Clickjacking protection)
X_FRAME_OPTIONS = 'DENY' 

# HTTP Strict Transport Security (HSTS): Forces browsers to use HTTPS for the specified duration (1 year)
SECURE_HSTS_SECONDS = 31536000 
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True