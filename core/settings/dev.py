# You could make another 'dev_custom.py' for Database & Email config. Then run with the 'dev_custom' environment like this:
# ./manage.py runserver --settings=core.settings.dev_custom

from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'p6_izlna_zfupnk57int)z2cew$qs7=q(hkm)f^1xhc%5pyurr'

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*']

# Database Config: provide your own local or remote postgresql
# DATABASES = {
#       'default': {
#           'ENGINE': 'django.db.backends.postgresql',
#           'NAME': 'one-table-local',
#           'USER': 'postgres',
#           'PASSWORD': 'postgres',
#           'HOST': 'localhost',
#           'PORT': '5432',
#       }
# }

# Sending Email Config: Just use the real smptp server.
# If you are going to use Gmail. Do not forget to turn on this flag: https://www.google.com/settings/security/lesssecureapps
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_PORT = '587'
# EMAIL_HOST_USER = 'yourGmail@gmail.com'
# EMAIL_HOST_PASSWORD = 'yourGmailPassword'
# EMAIL_USE_TLS = True

# The INTERNAL_IPS trick is enable checking if the env is debug or not in the template files
INTERNAL_IPS = (
    '127.0.0.1',
    'localhost',
)

try:
    from .local import *
except ImportError:
    pass
