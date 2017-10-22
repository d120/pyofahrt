"""
This is the settings file used in production.
First, it imports all default settings, then overrides respective ones.
Secrets are stored in and imported from an additional file, not set under version control.
"""

from pyofahrt.settings import *
import pyofahrt.settings_secrets as secrets

SECRET_KEY = secrets.SECRET_KEY

#BANK_ACCOUNT = secrets.BANK_ACCOUNT
BANK_ACCOUNT = """Empfänger: Vorstand des D120 e.V.
IBAN: DE91 5089 0000 0064 0851 07
BIC: GENODEF1VBD
"""

DEBUG = False

ALLOWED_HOSTS = ['.fachschaft.informatik.tu-darmstadt.de', '.d120.de']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'localhost',
        'NAME': 'pyofahrt',
        'USER': 'pyofahrt',
        'PASSWORD': secrets.DB_PASSWORD,
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
        }
    }
}

STATIC_URL = '/ofahrt/static/'
LOGIN_REDIRECT_URL = '/ofahrt/'
LOGIN_URL = '/ofahrt/staff/login/'

ADMINS = (('Ofahrt-Dev', 'ofahrt-dev@fachschaft.informatik.tu-darmstadt.de'), )

SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'mail.d120.de'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'pyofahrt'
EMAIL_HOST_PASSWORD = secrets.MAIL_PASSWORD
