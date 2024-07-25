import os
import sys
import django
import environ
import logging
from datetime import datetime, timedelta
from django.utils.translation import gettext

from utils import config

# ---------- 系统配置 ----------
# 项目根目录
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 项目主要代码目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)
# APP 代码目录
APPS_DIR = os.path.join(BASE_DIR, 'apps')
sys.path.insert(1, APPS_DIR)

# 环境变量
APP_ENV = os.environ.get('APP_ENV', 'prod')
env = environ.Env()
env_file = '.env.%s' % APP_ENV
env.read_env(env_file=os.path.join(ROOT_DIR, env_file))

SECRET_KEY = 'bhv6!c4#u%r#&=ls&$gfic@7_yi5(eeql=6)ttdj!ai2lg4l%('
DEBUG = env('DEBUG', default=False)
ROOT_URLCONF = 'project.urls'

ALLOWED_HOSTS = ["*"]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'django_celery_beat',

    'game',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'djangorestframework_camel_case.middleware.CamelCaseMiddleWare'
]

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

TIME_FORMAT = '%Y-%m-%d %H:%M:%S'
DATE_TIME_FORMAT = '%Y-%m-%d'

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True
USE_L10N = True
USE_TZ = False

# 前端静态资源实际访问 URL前缀
STATIC_URL = '/build/'

# 静态资源打包目录
STATIC_ROOT = os.path.join(ROOT_DIR, 'build')

# ---------- 跨域配置 ----------
# 全部允许配置
CORS_ORIGIN_ALLOW_ALL = True
# 允许cookie
CORS_ALLOW_CREDENTIALS = True  # 指明在跨域访问中，后端是否支持对cookie的操作

# ---------- DRF配置 ----------
if DEBUG:
    DEFAULT_RENDERER_CLASSES = (
        'djangorestframework_camel_case.render.CamelCaseJSONRenderer',
        'djangorestframework_camel_case.render.CamelCaseBrowsableAPIRenderer',
    )
else:
    DEFAULT_RENDERER_CLASSES = (
        'djangorestframework_camel_case.render.CamelCaseJSONRenderer',
    )
REST_FRAMEWORK = {
    # 时间格式配置
    "DATETIME_FORMAT": "%Y-%m-%d %H:%M:%S",
    # 日期格式配置
    "DATE_FORMAT": "%Y-%m-%d",
    # 默认筛选器
    "DEFAULT_FILTER_BACKENDS": (
        'django_filters.rest_framework.DjangoFilterBackend',
        'utils.ordering.CamelCaseOrderingFilter'
    ),
    # 默认分页器
    "DEFAULT_PAGINATION_CLASS": "utils.pagination.APIPageNumberPagination",
    # 渲染器
    'DEFAULT_RENDERER_CLASSES': DEFAULT_RENDERER_CLASSES,
    # 解析器
    'DEFAULT_PARSER_CLASSES': (
        'djangorestframework_camel_case.parser.CamelCaseFormParser',
        'djangorestframework_camel_case.parser.CamelCaseMultiPartParser',
        'djangorestframework_camel_case.parser.CamelCaseJSONParser'
    ),
    'JSON_UNDERSCOREIZE': {
        'no_underscore_before_number': True,
    }
}

REST_FRAMEWORK_EXTENSIONS = {
    # 默认缓存时间
    'DEFAULT_CACHE_RESPONSE_TIMEOUT': 60 * 5,
    # 默认缓存方式
    'DEFAULT_USE_CACHE': 'default',
}

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        "NAME": config.MYSQL_DB,
        "HOST": "127.0.0.1",
        "PORT": "3306",
        "USER": "root",
        "PASSWORD": env('MYSQL_PASSWORD'),
        'OPTIONS': {'charset': 'utf8mb4'}
    }
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/" + str(config.CACHE_REDIS_DB),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# ---------- 环境变量导出 ----------
AUTH_TOKEN = config.AUTH_TOKEN
CACHE_REDIS_DB = config.CACHE_REDIS_DB

# ---------- 日志配置 ----------
logger = logging.getLogger(__name__)
LOG_DIR = os.path.join(ROOT_DIR, 'logs')
if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(levelname)s %(asctime)s %(module)s %(lineno)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(module)s %(lineno)d %(message)s'
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            # 日志级别
            'level': 'WARNING',
            # 日志类别
            'class': 'logging.handlers.RotatingFileHandler',
            # 日志位置,日志文件名,日志保存目录必须手动创建
            'filename': os.path.join(LOG_DIR, "django.log"),
            # 日志文件的最大值(KB) 设置 50M
            'maxBytes': 50 * 1024 * 1024,
            # 日志文件最大数量 设置 10 个
            'backupCount': 10,
            # 日志格式: 详细格式
            'formatter': 'standard',
            # 文件内容编码
            'encoding': 'utf-8'
        }
    },
    # 日志对象
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'propagate': True,  # 是否让日志信息继续冒泡给其他的日志处理系统
        },
    }
}
