"""
Django settings for djmq project.

Generated by 'django-admin startproject' using Django 2.0.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'cc$r)t8$x=ry3w(gpw4nr@n466@^)xns&t49&($gl&62gmd#&e'

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
    'django_celery_results',
    'django_celery_beat'
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

ROOT_URLCONF = 'djmq.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'djmq.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'djmq',
        'USER': 'root',
        'PASSWORD': 'python',
        'HOST': 'localhost',
        'PORT': 3306,
    }
}
# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

# LANGUAGE_CODE = 'en-us'
#
# TIME_ZONE = 'UTC'
#
# USE_I18N = True
#
# USE_L10N = True
#
# USE_TZ = True
LANGUAGE_CODE = 'zh-Hans'
TIME_ZONE = 'Asia/Shanghai'  # 上海时区
USE_I18N = True
USE_L10N = True
USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'

# celery 基本配置
CELERY_BROKER_URL = 'redis://127.0.0.1:6379/3'  # celery中间人
# CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/1'  # celery结果返回，可用于跟踪结果
CELERY_RESULT_BACKEND = 'django-db'
CELERY_ACCEPT_CONTENT = ['application/json', ]  # celery内容等消息的格式设置
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Shanghai'  # celery时区设置，使用settings中TIME_ZONE同样的时区

# 声明celery定时器
from datetime import timedelta

CELERY_BEAT_SCHEDULE = {
    'celery_test': {
        'task': 'user.tasks.beattestfunc',
        'schedule': timedelta(seconds=3),  # 每隔3秒执行一次
        'args': (16, 16)
    },
}



from kombu import Queue, Exchange

# 声明两个任务队列
CELERY_QUEUES = (
    # Queue("celery",  Exchange('celery', type='direct'), routing_key='celery'),
    Queue("sqllog", Exchange('sqllog', type='direct'), routing_key="sqllog"),
)
#
# CELERY_DEFAULT_QUEUE = 'celery'
# CELERY_DEFAULT_ROUTING_KEY = 'celery'

# 给不同的任务方法放到不一样的队列中去执行
CELERY_ROUTES = {
    "user.tasks.testfunc": {
        "queue": "sqllog",
        "routing_key": "sqllog"
    }
}
from . celery import app
app.conf.update(CELERY_QUEUES=CELERY_QUEUES, CELERY_ROUTES=CELERY_ROUTES)
"""
需要分别跑两个woker 绑定消费队列
celery -A djmq.celery worker -l info -Q celery
celery -A djmq.celery worker -l info -Q sqllog

"""

