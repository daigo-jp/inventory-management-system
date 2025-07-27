"""
Django settings for pro_sotsu project.
"""

import os
from pathlib import Path

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'your-secret-key'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'foods',  # 追加されたアプリケーション
    'menu',
    'disposal',
    'home',
    'sales',
    'work',
    'order',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'disposal.middleware.profiling.ProfilingMiddleware',
]

ROOT_URLCONF = 'pro_sotsu.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'pro_sotsu.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Static files
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
# settings.py
# settings.py に追加
LOGIN_REDIRECT_URL = '/foods/main_page/'  # ログイン後のリダイレクト先

LOGOUT_REDIRECT_URL = '/foods/main_page/'

AUTH_USER_MODEL = 'home.StoreAccount'  # カスタムユーザーモデルのパスを指定

# プライマリキーの自動生成を BigAutoField に設定
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# タイムゾーンを日本標準時に設定
TIME_ZONE = 'Asia/Tokyo'

# UTCを使用するかどうか
USE_TZ = False