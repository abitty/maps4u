"""
Django settings for podarok project.

Generated by 'django-admin startproject' using Django 1.11.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

import json
from django.core.exceptions import ImproperlyConfigured

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(os.path.join(BASE_DIR, 'secrets.json')) as secrets_file:
    secrets = json.load(secrets_file)

def get_secret(setting, secrets=secrets):
    """Get secret setting or fail with ImproperlyConfigured"""
    try:
        return secrets[setting]
    except KeyError:
        raise ImproperlyConfigured("Set the {} setting".format(setting))


# путь до папки media, в общем случае она пуста в начале
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/' # для медии в шаблонах
FILE_UPLOAD_PERMISSIONS = 0o644
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

X_FRAME_OPTIONS = 'SAMEORIGIN'
SUMMERNOTE_THEME = 'bs3'  # Show summernote with Bootstrap4


SUMMERNOTE_CONFIG = {
	# Using SummernoteWidget - iframe mode, default
	'iframe': True,

	# Or, you can set it as False to use SummernoteInplaceWidget by default - no iframe mode
	# In this case, you have to load Bootstrap/jQuery stuff by manually.
	# Use this when you're already using Bootstraip/jQuery based themes.
	#'iframe': False,

	# You can put custom Summernote settings
	'summernote': {
		# As an example, using Summernote Air-mode
		'airMode': False,

		# Change editor size
		'width': '100%',
		'height': '480',

		# Use proper language setting automatically (default)
		'lang': None,
		'styleTags': [
		'p',
		{'title': 'Эпиграф', 'tag': 'blockquote', 'className': 'blockquote text-right epigraph', 'value': 'blockquote' },
		{'title': 'Автор эпиграфа','tag':'footer','className':'blockquote-footer  font-wieght-lighter','value':'footer'},
		'h1','h2','h3','h4','h5',
		'footer','blockquote',
		],
		
		# Toolbar customization
		# https://summernote.org/deep-dive/#custom-toolbar-popover
		'toolbar': [
			['view', ['codeview','fullscreen', 'undo', 'redo']],
			['style', ['style']],
			['font', ['bold', 'italic', 'clear']],
			['fontname', ['Kurale','PT cerif','Segoy UI']],
			['para', ['ul', 'ol', 'paragraph']],
			['insert', ['link', 'picture']],
		],

		# Or, set editor language/locale forcely
		'lang': 'ru-RU',
	},
	# Need authentication while uploading attachments.
	'attachment_require_authentication': False,
}


THUMBNAIL_FORMAT = 'JPEG'


"""
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}
"""


LOGIN_URL = '/login/'

# пустая папка, сюда будет собирать статику collectstatic
#урл для шаблонов
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')


STATICFILES_DIRS = [
	os.path.join(BASE_DIR, "assets"),
	os.path.join(BASE_DIR, "templates"),
#	os.path.join(BASE_DIR, "templates/images/"),
#	os.path.join(BASE_DIR, "templates/css/"),
#	os.path.join(BASE_DIR, "templates/js/"),
]
   

# "Поисковики" статики. Первый ищет статику в STATICFILES_DIRS,
# второй в папках приложений.

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
]

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = get_secret("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

THUMBNAIL_DEBUG = False

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
	'django.contrib.sites',
	'django.contrib.sitemaps',
	'sorl.thumbnail',
	'rest_framework',
	'django_summernote',
    'maps',
]

SITE_ID=1
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'maps4u.urls'

WSGI_APPLICATION = 'maps4u.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
	'NAME': get_secret("MYSQL_DB"),
	'PASSWORD': get_secret("MYSQL_PASSWORD"),
	'USER': get_secret("MYSQL_USER"),
	'CHARSET':'utf8',
	'PORT':get_secret("MYSQL_PORT"),
	'HOST':'127.0.0.1',
	'OPTIONS': {
		#	'read_default_file': os.path.join(BASE_DIR,'podarok_mysql.conf'),
			'init_command': "SET sql_mode='STRICT_TRANS_TABLES,NO_ZERO_DATE,NO_ZERO_IN_DATE'; SET default_storage_engine=INNODB",
	}
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


REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}

# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True
USE_L10N = True
USE_TZ = True


LOGGING = {
	'version': 1,
	'disable_existing_loggers': False,
	'handlers': {
		'file': {
			'level': 'DEBUG',
			'class': 'logging.FileHandler',
			'filename': '/var/log/maps4u/debug.log',
		},
    },
	'loggers': {
		#'django': {
		#	'handlers': ['file'],
		#	'level': 'DEBUG',
		#	'propagate': True,
		#},
		'coins': {
			'handlers': ['file'],
			'level': 'DEBUG',
			'propagate': True,
		},
	},
}


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/"

# secure

SECURE_CONTENT_TYPE_NOSNIFF = True
from .local import *
