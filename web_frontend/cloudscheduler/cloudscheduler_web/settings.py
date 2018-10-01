"""
Django settings for cloudscheduler project.

Generated by 'django-admin startproject' using Django 1.11.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
from cloudscheduler.lib.csv2_config import Config
config = Config('web_frontend')

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'sa$jy+6m=w$nn=1i*=7_i)=p21ubbw65=(*(ubuo!fhy-zf$$='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Profiling
SILKY_PYTHON_PROFILER = True
SILKY_PYTHON_PROFILER_BINARY = True
SILKY_PYTHON_PROFILER_RESULT_PATH = "/var/www/silkydata/"

ALLOWED_HOSTS = ["csv2.heprc.uvic.ca",
                 "csv2-dev.heprc.uvic.ca",
                 "csv2-dev2.heprc.uvic.ca",
                ]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'formatters': {
        'simple': {
            'format': '[%(asctime)s] %(levelname)s %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'verbose': {
            'format': '[%(asctime)s] %(levelname)s [%(name)s.%(funcName)s:%(lineno)d] %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
    },
    'handlers': {
        'applogfile': {
            'level':'INFO',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': config.log_file,
            'maxBytes': 1024*1024*15, # 15MB
            'backupCount': 10,
            'formatter': 'simple'
        },
    },
    'loggers': {
        'glintv2': {
            'handlers': ['applogfile'],
            'level': 'INFO',
        },
    }
}


# Application definition

INSTALLED_APPS = [
    'silk',
    'csv2.apps.Csv2Config',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
#    'debug_toolbar',
    'mathfilters',
]
if config.enable_glint:
    INSTALLED_APPS.append('glintwebui.apps.GlintwebuiConfig')

INTERNAL_IPS = [
    '142.104.60.114',
    '142.104.60.61',
]

MIDDLEWARE = [
    'silk.middleware.SilkyMiddleware',
#    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.RemoteUserMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
'''
DEBUG_TOOLBAR_PANELS = [
    'debug_toolbar.panels.versions.VersionsPanel',
    'debug_toolbar.panels.timer.TimerPanel',
    'debug_toolbar.panels.settings.SettingsPanel',
    'debug_toolbar.panels.headers.HeadersPanel',
    'debug_toolbar.panels.request.RequestPanel',
    'debug_toolbar.panels.sql.SQLPanel',
    'debug_toolbar.panels.staticfiles.StaticFilesPanel',
    'debug_toolbar.panels.templates.TemplatesPanel',
    'debug_toolbar.panels.cache.CachePanel',
    'debug_toolbar.panels.signals.SignalsPanel',
    'debug_toolbar.panels.logging.LoggingPanel',
    'debug_toolbar.panels.redirects.RedirectsPanel',
]
DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
}
'''
INTERNAL_IPS = [
    '142.104.60.114',
    '142.104.60.61',
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.RemoteUserBackend',
]


ROOT_URLCONF = 'cloudscheduler_web.urls'

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

WSGI_APPLICATION = 'cloudscheduler_web.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config.db_name,
        'USER': config.db_user,
        'PASSWORD': config.db_password,
#        'HOST': '127.0.0.1',
#        'PORT': '3306',
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/Vancouver'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

#STATICFILES_DIRS = (
#    os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/static/',
#)

STATIC_URL = '/static/'
STATIC_ROOT = '/opt/cloudscheduler/web_frontend/cloudscheduler/csv2/static/'

# Celery variables
# not sure if it should be json for sure or not yet.
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Canada/Pacific'
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_DEFAULT_QUEUE = 'celery'
CELERY_DEFAULT_EXCHANGE = "celery"
CELERY_QUEUES = {
    "celery": {"exchange": "celery"},
    "image_collection": {"exchange": "image_collection"},
}
CELERY_ROUTES = {
    'Glintv2.glintv2.tasks.image_collection': {'queue': 'image_collection'},
}
