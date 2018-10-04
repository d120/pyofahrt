"""
This is the settings file used in production.
First, it imports all default settings, then overrides respective ones.
Secrets are stored in and imported from an additional file, not set under version control.
"""
import ldap
from django_auth_ldap.config import LDAPSearch, LDAPGroupQuery, GroupOfNamesType

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

ADMINS = (('pyofahrt-Dev', 'pyofahrt-dev@fachschaft.informatik.tu-darmstadt.de'), )

SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'mail.d120.de'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'pyofahrt'
EMAIL_HOST_PASSWORD = secrets.MAIL_PASSWORD

# Authentication Backends
AUTHENTICATION_BACKENDS = [
        'django.contrib.auth.backends.ModelBackend',
        'django_auth_ldap.backend.LDAPBackend',
        ]

# LDAP Config
AUTH_LDAP_SERVER_URI = "ldap://ldap.d120.de"
AUTH_LDAP_BIND_DN = "cn=pyofahrt,ou=Services,dc=fachschaft,dc=informatik,dc=tu-darmstadt,dc=de"
AUTH_LDAP_BIND_PASSWORD = secrets.AUTH_LDAP_BIND_PASSWORD
AUTH_LDAP_USER_SEARCH = LDAPSearch("ou=People,dc=fachschaft,dc=informatik,dc=tu-darmstadt,dc=de",
    ldap.SCOPE_SUBTREE, "(uid=%(user)s)")
AUTH_LDAP_GROUP_SEARCH = LDAPSearch("ou=Groups,dc=fachschaft,dc=com",
    ldap.SCOPE_SUBTREE, "(objectClass=groupOfNames)"
)
AUTH_LDAP_GROUP_TYPE = GroupOfNamesType()

AUTH_LDAP_USER_ATTR_MAP = {"first_name": "givenName", "last_name": "sn",
        "email": "mail"}

AUTH_LDAP_USER_FLAGS_BY_GROUP = {
        "is_staff": "cn=fachschaft,ou=Group,dc=fachschaft,dc=informatik,dc=tu-darmstadt,dc=de",
        "is_superuser": (LDAPGroupQuery("cn=ofahrtleitung,ou=Group,dc=fachschaft,dc=informatik,dc=tu-darmstadt,dc=de") |
                        LDAPGroupQuery("cn=developers,ou=Group,dc=fachschaft,dc=informatik,dc=tu-darmstadt,dc=de") |
                        LDAPGroupQuery("cn=fss,ou=Group,dc=fachschaft,dc=informatik,dc=tu-darmstadt,dc=de"))
        }
