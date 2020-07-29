import os
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, 'common/'))
sys.path.insert(0, os.path.join(BASE_DIR, 'apps/'))
sys.path.insert(0, os.path.join(BASE_DIR, 'utils/'))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'cc$r)t8$x=ry3w(gpw4nr@n466@^)xns&t49&($gl&62gmd#&e'

# RT WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"] if DEBUG else ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_celery_results',  # celery异步任务结果
    'django_celery_beat',  # celery定时任务结果
    'rest_framework',
    'corsheaders',
    'djorm_pool'
]

MIDDLEWARE = [
    'common.middleware.CheckSignMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
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


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'djmq',
        'USER': 'dbuser',
        'PASSWORD': 'python',
        'HOST': 'localhost',
        'PORT': 5432,
        'CONN_MAX_AGE': 100,  # 最长链接时间，具体需要dba测试，没有标准
    }
}
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
# 时区设置
LANGUAGE_CODE = 'zh-Hans'
TIME_ZONE = 'Asia/Shanghai'  # 上海时区
USE_I18N = True
USE_L10N = True
USE_TZ = False
STATIC_URL = '/static/'
# pro环境下手机静态文件
if not DEBUG:
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# celery 基本配置
CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'  # celery消息中间键(broker)
# CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/1'  # celery结果返回，可用于跟踪结果
CELERY_RESULT_BACKEND = 'django-db'  # celery执行结果保存在db中
CELERY_ACCEPT_CONTENT = ['application/json', ]  # celery内容等消息的格式设置
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Shanghai'  # celery时区设置，使用settings中TIME_ZONE同样的时区

# 　签名token相关配置
API_TOKEN_URL = "redis://127.0.0.1:6379/1"  # token保存地址
API_TOKEN_EXPIRE = 60  # token有效期，默认60s

# drf认证相关配置
REST_FRAMEWORK = {
    # 　认证方式
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',  # 后台cookie方式
        'rest_framework.authentication.BasicAuthentication',  # 单独提供账号密码
    ),
    # 默认接口权限无
    'DEFAULT_PERMISSION_CLASSES': (
        # 'rest_framework.permissions.IsAuthenticatedOrReadOnly',
        'rest_framework.permissions.AllowAny',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    # 文档功能
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.AutoSchema',
    # 错误返回自定义
    'EXCEPTION_HANDLER': 'common.exception.custom_exception_handler'
}

if not DEBUG:
    # 正式环境的时候需配置返回为jons渲染器，不然会暴露drf样式 html给用户
    REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = ['rest_framework.renderers.JSONRenderer']

# 同源策略解决该方案配置
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'POST',
    'PUT',
)
CORS_ALLOW_HEADERS = (
    'Access-Control-Allow-Origin',
    'XMLHttpRequest',
    'X_FILENAME',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'Pragma',
)

# 基于djorm_pool包的django连接池配置 https://github.com/djangonauts/djorm-ext-pool
DJORM_POOL_OPTIONS = {
    "pool_size": 20,  # 连接池
    "max_overflow": 0,  # 最大连接数
    "recycle": 3600
}
