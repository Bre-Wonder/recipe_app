import os
from .settings import *
from .settings import BASE_DIR

SECRET_KEY = os.environ['SECRET']
ALLOWED_HOSTS = [
    os.environ['WEBSITE_HOSTNAME']
]
CSRF_TRUSTED_ORIGINS = ['https://' + os.environ['WEBSITE_HOSTNAME']]
DEBUG = False

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

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

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
