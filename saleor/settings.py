from __future__ import unicode_literals

import ast
import os.path

import dj_database_url
import dj_email_url
from django.contrib.messages import constants as messages
import django_cache_url
import os


DEBUG = ast.literal_eval(os.environ.get('DEBUG', 'True'))

SITE_ID = 1

PROJECT_ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), '..'))

ROOT_URLCONF = 'saleor.urls'

WSGI_APPLICATION = 'saleor.wsgi.application'

ADMINS = (
    (os.getenv('SUPERUSER_NAME'), os.getenv('SUPERUSER_EMAIL')),
)
MANAGERS = ADMINS
INTERNAL_IPS = os.environ.get('INTERNAL_IPS', '127.0.0.1').split()

CACHE_URL = os.environ.get('CACHE_URL',
                           os.environ.get('REDIS_URL', 'locmem://'))
CACHES = {'default': django_cache_url.parse(CACHE_URL)}

#SQLITE_DB_URL = 'sqlite:///' + os.path.join(PROJECT_ROOT, 'dev.sqlite')
#DATABASES = {'default': dj_database_url.config(default=SQLITE_DB_URL)}
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('DB_NAME', 'lwc'),
        'USER': 'lwc',
        'PASSWORD': os.getenv('DB_PASS'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': '3306',
    }
}

SECRET_KEY = os.getenv('DB_PASS')

TIME_ZONE = 'America/Chicago'
LANGUAGE_CODE = 'en-us'
USE_I18N = True
USE_L10N = True
USE_TZ = True


EMAIL_URL = os.environ.get('EMAIL_URL', 'console://')
email_config = dj_email_url.parse(EMAIL_URL)

EMAIL_FILE_PATH = email_config['EMAIL_FILE_PATH']
EMAIL_HOST_USER = email_config['EMAIL_HOST_USER']
EMAIL_HOST_PASSWORD = email_config['EMAIL_HOST_PASSWORD']
EMAIL_HOST = email_config['EMAIL_HOST']
EMAIL_PORT = email_config['EMAIL_PORT']
EMAIL_BACKEND = email_config['EMAIL_BACKEND']
EMAIL_USE_TLS = email_config['EMAIL_USE_TLS']
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')


MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'media')
MEDIA_URL = '/media/'


context_processors = [
    'django.contrib.auth.context_processors.auth',
    'django.template.context_processors.debug',
    'django.template.context_processors.i18n',
    'django.template.context_processors.media',
    'django.template.context_processors.static',
    'django.template.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'django.template.context_processors.request',
    'saleor.core.context_processors.default_currency',
    'saleor.core.context_processors.categories']

loaders = [
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    # TODO: this one is slow, but for now need for mptt?
    'django.template.loaders.eggs.Loader']

if not DEBUG:
    loaders = [('django.template.loaders.cached.Loader', loaders)]

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [os.path.join(PROJECT_ROOT, 'templates')],
    'OPTIONS': {
        'debug': DEBUG,
        'context_processors': context_processors,
        'loaders': loaders,
        'string_if_invalid': '<< MISSING VARIABLE "%s" >>' if DEBUG else ''}}]

MIDDLEWARE_CLASSES = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'babeldjango.middleware.LocaleMiddleware',
    'saleor.cart.middleware.CartMiddleware',
    'saleor.core.middleware.DiscountMiddleware',
    'saleor.core.middleware.GoogleAnalytics',
    'saleor.core.middleware.CountryMiddleware',
    'saleor.core.middleware.CurrencyMiddleware'
]

INSTALLED_APPS = [
    'saleor',
    # External apps that need to go before django's
    'offsite_storage',

    # Django modules
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.sitemaps',
    'django.contrib.sites',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.auth',

    # Local apps
    'saleor.userprofile',
    'saleor.discount',
    'saleor.product',
    'saleor.cart',
    'saleor.checkout',
    'saleor.core',
    'saleor.order',
    'saleor.registration',
    'saleor.dashboard',
    'saleor.shipping',

    # External apps
    'versatileimagefield',
    'babeldjango',
    'bootstrap3',
    'django_prices',
    'emailit',
    'mptt',
    'payments',
    'selectable',
    'materializecssform',
    'rest_framework',
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
            '%(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'filters': ['require_debug_true'],
            'formatter': 'simple'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True
        },
        'saleor': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True
        }
    }
}

AUTHENTICATION_BACKENDS = (
    'saleor.registration.backends.EmailPasswordBackend',
    'saleor.registration.backends.ExternalLoginBackend',
    'saleor.registration.backends.TrivialBackend'
)

AUTH_USER_MODEL = 'userprofile.User'

LOGIN_URL = '/account/login'

DEFAULT_CURRENCY = 'EUR'
AVAILABLE_CURRENCIES = [DEFAULT_CURRENCY]
DEFAULT_WEIGHT = 'kg'

ACCOUNT_ACTIVATION_DAYS = 3

LOGIN_REDIRECT_URL = 'home'

FACEBOOK_APP_ID = os.environ.get('FACEBOOK_APP_ID')
FACEBOOK_SECRET = os.environ.get('FACEBOOK_SECRET')

GOOGLE_ANALYTICS_TRACKING_ID = os.environ.get('GOOGLE_ANALYTICS_TRACKING_ID')
GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')

PAYMENT_MODEL = 'order.Payment'
PAYMENT_HOST = 'u3417ebcb4f4355ace7aa:8080'
PAYMENT_USES_SSL = False
PAYMENT_VARIANTS = {
    'default': ('payments.dummy.DummyProvider', {}),
    'stripe': ('payments.stripe.StripeProvider', {
        'secret_key': os.getenv('STRIPE_SECRET_KEY_TEST'),
        'public_key': os.getenv('STRIPE_PUBLIC_KEY_TEST')
    })
}

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'

CHECKOUT_PAYMENT_CHOICES = [
    # ('default', 'Dummy provider'),
    ('stripe', 'Debit/Credit Card')
]

MESSAGE_TAGS = {
    messages.ERROR: 'danger',
}

LOW_STOCK_THRESHOLD = 5

PAGINATE_BY = 16

TEST_RUNNER = ''

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost').split()

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Amazon S3 configuration
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STATIC_BUCKET_NAME = os.environ.get('AWS_STATIC_BUCKET_NAME')

AWS_MEDIA_ACCESS_KEY_ID = os.environ.get('AWS_MEDIA_ACCESS_KEY_ID')
AWS_MEDIA_SECRET_ACCESS_KEY = os.environ.get('AWS_MEDIA_SECRET_ACCESS_KEY')
AWS_MEDIA_BUCKET_NAME = os.environ.get('AWS_MEDIA_BUCKET_NAME')

if AWS_STATIC_BUCKET_NAME:
    STATICFILES_STORAGE = 'offsite_storage.storages.CachedS3FilesStorage'

if AWS_MEDIA_BUCKET_NAME:
    DEFAULT_FILE_STORAGE = 'offsite_storage.storages.S3MediaStorage'
    THUMBNAIL_DEFAULT_STORAGE = DEFAULT_FILE_STORAGE

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')
STATIC_URL = 'http://s3.amazonaws.com/%s' % AWS_STATIC_BUCKET_NAME
STATICFILES_DIRS = [
    os.path.join(PROJECT_ROOT, 'saleor', 'static')
]
STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder'
]
VERSATILEIMAGEFIELD_RENDITION_KEY_SETS = {
    'defaults': [
        ('list_view', 'crop__100x100'),
        ('dashboard', 'crop__400x400'),
        ('product_page_mobile', 'crop__680x680'),
        ('product_page_big', 'crop__750x750'),
        ('product_page_thumb', 'crop__280x280')
    ]
}
