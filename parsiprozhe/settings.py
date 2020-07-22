import os
from django.core.exceptions import ImproperlyConfigured
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = True

secret = json.load(open(os.path.join(BASE_DIR, 'secret.json')))
secret_dev = json.load(open(os.path.join(BASE_DIR, 'secret_dev.json')))

def get_secret(setting, secrets=secret, secrets_dev=secret_dev):
    """Get secret setting or fail with ImproperlyConfigured"""
    try:
        if DEBUG:
            return secrets_dev[setting]
        return secrets[setting]
    except KeyError:
        raise ImproperlyConfigured("Set the {} setting".format(setting))

SECRET_KEY = get_secret('SECRET_KEY')

DEFAULT_CHARSET = 'utf-8'

FILE_UPLOAD_MAX_MEMORY_SIZE = 15242880

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'www.parsiprozhe.ir', 'parsiprozhe.ir']


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'debug_toolbar',
    'shop'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'debug_toolbar.middleware.DebugToolbarMiddleware'
]

ROOT_URLCONF = 'parsiprozhe.urls'

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/registration/login/'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'shop.context_processors.cart'
            ],
        },
    },
]

WSGI_APPLICATION = 'parsiprozhe.wsgi.application'

DATABASES = {
     'default': {
        'ENGINE': 'mysql.connector.django',
        'NAME': get_secret('DB_NAME'),
        'USER': get_secret('DB_USERNAME'),
        'PASSWORD': get_secret('DB_PASSWORD')
        'HOST': 'localhost',
        #'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8',
        },

    }
}


AUTH_PASSWORD_VALIDATORS = [

    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    }
]


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Tehran'

USE_I18N = False

USE_L10N = False

USE_TZ = False


STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MEDIA_URL = '/media/'
STATICFILES_DIRS = [ BASE_DIR+"/assets", ]
STATIC_ROOT  ='/home/parsipro/public_html/static'
MEDIA_ROOT  ='/home/parsipro/public_html/media'

CART_SESSION_ID = 'cart'

MERCHANT = get_secret('MERCHANT')


'''
INTERNAL_IPS = ['127.0.0.1']

DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda x: True
}
'''

