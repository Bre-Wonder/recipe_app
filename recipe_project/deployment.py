import os
from .settings import *
from .settings import BASE_DIR

# Only use deployment settings if we're in Azure (environment variables exist)
if 'WEBSITE_HOSTNAME' in os.environ:
    SECRET_KEY = os.environ['SECRET']
    ALLOWED_HOSTS = [
        os.environ['WEBSITE_HOSTNAME']
    ]
    CSRF_TRUSTED_ORIGINS = ['https://' + os.environ['WEBSITE_HOSTNAME']]
    DEBUG = False
else:
    # Fall back to development settings for build process
    from .settings import SECRET_KEY, ALLOWED_HOSTS, DEBUG

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Add logging configuration for better error tracking
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Only configure database if we're in Azure
if 'AZURE_POSTGRESQL_CONNECTIONSTRING' in os.environ:
    # Parse connection string more robustly
    connection_string = os.environ['AZURE_POSTGRESQL_CONNECTIONSTRING']
    parameters = {}
    for pair in connection_string.split(' '):
        if '=' in pair:
            key, value = pair.split('=', 1)
            parameters[key] = value

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': parameters.get('dbname', ''),
            'HOST': parameters.get('host', ''),
            'USER': parameters.get('user', ''),
            'PASSWORD': parameters.get('password', ''),
            'PORT': parameters.get('port', '5432'),
            'OPTIONS': {
                'sslmode': 'require',
            },
        }
    }
else:
    # Fall back to development database for build process
    from .settings import DATABASES
