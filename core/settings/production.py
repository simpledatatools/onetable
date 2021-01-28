from __future__ import absolute_import, unicode_literals
import os
from .base import *

SECRET_KEY = os.environ['SECRET_KEY']

DEBUG = False

# Heroku: Update database configuration from $DATABASE_URL.
import dj_database_url
DATABASES['default'] =  dj_database_url.config()
#db_from_env = dj_database_url.config(conn_max_age=500)
#DATABASES['default'].update(db_from_env)

ALLOWED_HOSTS = [
    'onetable.herokuapp.com',
    #'www.onetableapp.com',
    '127.0.0.1',
]

# Redirect to https in production
SECURE_SSL_REDIRECT = True
# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

COMPRESS_OFFLINE = True
COMPRESS_CSS_FILTERS = [
    'compressor.filters.css_default.CssAbsoluteFilter',
    'compressor.filters.cssmin.CSSMinFilter',
]
COMPRESS_CSS_HASHING_METHOD = 'content'

# AWS S3: Store production images on an S3 bucket not the django instance
AWS_ACCESS_KEY_ID = 'AKIA2ZUWWWAZVALHY2W3'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'nano-website-uploads'
AWS_S3_REGION_NAME = 'us-east-1'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# Detailed logging using  heroku logs --tail --app simple-data-tools on heroku cli
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'ERROR'),
        },
    },
}

try:
    from .local import *
except ImportError:
    pass
