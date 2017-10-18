"""
Django settings for pyofahrt project.

Generated by 'django-admin startproject' using Django 1.9.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '8hb0nmhm&hwlq6)*(@95092dw-$lp$v*yp+9yib459h82*penf'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bootstrap3',
    'ofahrtbase',
    'members',
    'staff',
    'faq',
    'workshops',
    'tasks',
    'wiki',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'pyofahrt.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'pyofahrt.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'de'

TIME_ZONE = 'Europe/Berlin'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = 'static'

LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/staff/login'

SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True

CSRF_COOKIE_HTTPONLY = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

SERVER_EMAIL = "ofahrt-leitung@fachschaft.informatik.tu-darmstadt.de"
DEFAULT_FROM_EMAIL = SERVER_EMAIL

MAIL_PREFIX = "[Ofahrt-Info]" + " "

# Mail settings
MAIL_MEMBERSIGNUP_QUEUE_SUBJECT = MAIL_PREFIX + "Anmeldung zur Ofahrt im Wintersemester %d"
MAIL_MEMBERSIGNUP_QUEUE_TEXT = """Hallo %s,

wir haben deine Anmeldung für die Ofahrt für Bachelor-Erstsemester im WiSe %d erfolgreich gespeichert.
Bis zum Eingang des Teilnahmebetrags von 20€ stehst du lediglich auf der vorläufigen Teilnehmer*innenliste. Bitte überweise den Teilnahmebetrag schnellstmöglich an die unten genannten Kontodaten. Wähle als Verwendungszweck bitte "Informatik Erstsemesterfahrt - VORNAME NACHNAME" damit wir die Überweisung deiner Anmeldung zuordnen können. Solltest du keinen Zugriff auf ein Bankkonto oder eine andere Möglichkeit der Überweisung haben, kontaktiere uns bitte unter ofahrt-leitung@d120.de. In diesem Fall finden wir eine Regelung für eine Barzahlung im Fachschaftsraum.

Sobald wir den Teilnahmebetrag erhalten haben setzen wir dich schnellstmöglich auf die feste Teilnahmeliste. Alle weiteren Infos erhälst du dann per Email.

Liebe Grüße,
die Ofahrt-Leitung

-------------------------------

Kontodaten:
%s"""

MAIL_MEMBER_MOVETOQUEUE_SUBJECT = MAIL_PREFIX + "Deine Anmeldung zur Ofahrt"
MAIL_MEMBER_MOVETOQUEUE_TEXT = """Hallo %s,

du wurdest soeben aus der Warteschlange auf die vorläufige Anmeldeliste gesetzt. Um auf die feste Anmeldeliste übernommen zu werden überweise bitte innerhalb von sieben Tagen den Teilnahmebeitrag von 20,00€ auf die unten angegebenen Kontodaten. Wähle als Verwendungszweck bitte "Erstsemesterfahrt Informatik - VORNAME NACHNAME" damit wir die Überweisung deiner Anmeldung zuordnen können. Solltest du keinen Zugriff auf ein Bankkonto oder eine andere Möglichkeit der Überweisung haben, kontaktiere uns bitte unter ofahrt-leitung@d120.de. In diesem Fall finden wir eine Regelung für eine Barzahlung im Fachschaftsraum.

Sobald wir den Teilnahmebeitrag erhalten haben, setzen wir dich schnellstmöglich auf die feste Teilnahmeliste. Alle weiteren Infos erhälst du dann per E-Mail.

Liebe Grüße
die Ofahrt-Leitung

-------------------------------

Kontodaten:
%s"""

MAIL_MEMBERSIGNUP_SUBJECT = MAIL_PREFIX + "Anmeldung zur Ofahrt im Wintersemester %d"
MAIL_MEMBERSIGNUP_TEXT = """Hallo %s,

wir haben deine Anmeldung für die Ofahrt für Bachelor-Erstsemester im WiSe %d erfolgreich gespeichert.
Da derzeit alle Plätze belegt sind bist du aktuell noch in der Warteschlange. Sollte bei den bereits angemeldeten Teilnehmer*innen der Teilnahmebeitrag nach einer Woche nicht bei uns eingegangen sein werden wir aus der Warteschlange auffüllen. Du erhälst in diesem Fall eine Email.

Liebe Grüße,
die Ofahrt-Leitung

-------------------------------

Kontodaten:
%s"""


MAIL_MEMBERSIGNUP_REMINDER_SUBJECT = MAIL_PREFIX + "Erinnerung Teilnahmegebühr, Ofahrt Wintersemester %d"
MAIL_MEMBERSIGNUP_REMINDER_TEXT = """Hallo %s,

danke noch einmal für deine Anmeldung! Seit X Tagen stehst du bereits auf der vorläufigen Anmeldeliste, so weit, so gut. Wir konnten allerdings noch keinen Geldeingang verbuchen. Bitte überweise den Teilnahmebeitrag in Höhe von 50€ auf das unten angegebene Konto, um an der Ofahrt fest teilnehmen zu können.

Wenn du das Geld bereits überwiesen hast, dann scheint die Bank einfach etwas langsam zu sein.

Falls du deine Anmeldung stornieren möchtest, schreibe uns eine Mail, damit wir dich von der Liste entfernen können und Platz für andere Anmeldungen frei wird.

Sollte jedoch bis in Y Tagen bei uns der Beitrag nicht eingegangen sein, wird deine Anmeldung automatisch aus dem System entfernt.

Liebe Grüße,
die Ofahrt-Leitung

-------------------------------

Kontodaten:
%s"""


BANK_ACCOUNT = "folgt separat"  # wird in secret_settings überschrieben

MAIL_WORKSHOPSIGNUP_SUBJECT = MAIL_PREFIX + "Willkommen als Workshopanbieter bei der Ofahrt!"
MAIL_WORKSHOPSIGNUP_TEXT = """Hallo %(name)s,

willkommen als Workshopanbieter der Ofahrt! Mit dem Erhalt dieser Email wurde dein Account in pyofahrt, unserem Verwaltungstool zur Planung uns Strukturierung der OFahrt, freigeschaltet. Im folgenden findest du deine Logindaten.

pyofahrt: http://d120.de/ofahrt
Name: %(username)s
Passwort: %(password)s

Im Adminmenü kannst du dein Passwort jederzeit ändern. Du solltest desweiteren zeitnah auf unsere Mailingliste ofahrt-workshops@d120.de hinzugefügt werden. Nach dem Login kannst du deine(n) Workshop(s) verwalten. Solltest du irgendwelche weiteren Fragen haben melde dich einfach bei uns unter ofahrt-leitung@d120.de.

Mit freundlichen Grüßen,
(okay, das ist eine automatische Mail)"""

MAIL_ORGASIGNUP_SUBJECT = MAIL_PREFIX + "Willkommen im Orgateam der Ofahrt!"
MAIL_ORGASIGNUP_TEXT = """Hallo %(name)s,

willkommen im Orgateam der Ofahrt! Mit dem Erhalt dieser Email wurde dein Account in pyofahrt, unserem Verwaltungstool zur Planung und Strukturierung der Ofahrt, freigeschaltet. Im Folgenden findest du deine Logindaten.

pyofahrt: http://d120.de/ofahrt
Name: %(username)s
Passwort: %(password)s

Im Adminmenü kannst du dein Passwort jederzeit ändern. Du solltest des Weiteren zeitnah auf unsere Orgaliste ofahrt@d120.de hinzugefügt werden. Solltest du irgendwelche weiteren Fragen haben, melde dich einfach bei uns unter ofahrt-leitung@d120.de.

Mit freundlichen Grüßen,
(okay, das ist eine automatische Mail)"""

MAIL_CONTACTFORM_SUBJECT = MAIL_PREFIX + "Ofahrt Kontaktformular"
MAIL_CONTACTFORM_TEXT = """Ofahrt Kontaktformular (Anfrage von %(sender)s)


%(text)s
"""

MAIL_SUPERUSER_SUCCESS_SUBJECT = MAIL_PREFIX + "SuperUser neu angelegt"
MAIL_SUPERUSER_SUCCESS_TEXT = """
Der Superuseraccount "leitung" wurde in pyofahrt neu angelegt.

Die Zugangsdaten findest du unter mnt/media/ofahrt/pw.txt
"""

MAIL_SUPERUSER_ERROR_SUBJECT = MAIL_PREFIX + "SuperUser konnte nicht neu angelegt werden"
MAIL_SUPERUSER_ERROR_TEXT = """
Es wurde beantragt den Superuseraccount \"leitung\" in pyofahrt neu anzulegen. Da der Account allerdings nicht gelöscht wurde, wurde das Passwort zurückgesetzt.

Die Zugangsdaten findest du unter mnt/media/ofahrt/pw.txt
"""

MAIL_NEW_ORGA_SUBJECT = MAIL_PREFIX + "pyofahrt: Neuer Orga-Eintrag"
MAIL_NEW_ORGA_TEXT = """
Eine neue Orga-Bewerbung ist eingegangen. Bitte zeitnah bearbeiten.

Vorname: %(firstname)s
Nachname: %(lastname)s
"""

MAIL_NEW_WORKSHOP_SUBJECT = MAIL_PREFIX + "pyofahrt: Neuer Orga-Eintrag"
MAIL_NEW_WORKSHOP_TEXT = """
Eine neue Workshop-Bewerbung ist eingegangen. Bitte zeitnah bearbeiten.

Vorname: %(firstname)s
Nachname: %(lastname)s
"""

MAIL_TICKETEDIT_SUBJECT = MAIL_PREFIX + "Ticket #%(id)d bearbeitet"
MAIL_TICKETEDIT_TEXT = """
Hallo,
diese Mail soll dich informieren, dass das Ticket #%(id)d "%(subject)s" in der für dich freigegebenen Aufgabenkategorie "%(cat)s" soeben von %(name)s bearbeitet wurde.

Du kannst das Ticket unter folgendem Link einsehen:
%(link)s

Diese Mail wurde automatisch generiert und ist daher auch ohne Unterschrift gültig.
"""

MAIL_TICKETASSIGN_SUBJECT = MAIL_PREFIX + "Ticket #%(id)d neu zugewiesen"
MAIL_TICKETASSIGN_TEXT = """
Hallo,
diese Mail soll dich informieren, dass die Bearbeiterzuweisung für das Ticket #%(id)d "%(subject)s" in der für dich freigegebenen Aufgabenkategorie "%(cat)s" soeben von %(name)s verändert wurde.

Die folgenden Benutzer sind nun für die Bearbeitung zuständig: %(editors)s

Du kannst das Ticket unter folgendem Link einsehen:
%(link)s

Diese Mail wurde automatisch generiert und ist daher auch ohne Unterschrift gültig.
"""

MAIL_TICKETPUSH_SUBJECT = MAIL_PREFIX + "PUSH: Ticket #%(id)d"
MAIL_TICKETPUSH_TEXT = """
Hallo,
diese Mail soll dich informieren, dass das Ticket #%(id)d "%(subject)s" in der für dich freigegebenen Aufgabenkategorie "%(cat)s" soeben von %(name)s einen Push! erhalten hat.

Dies bedeutet, dass %(name)s der Ansicht ist, dass dieses Ticket weitere Aufmerksamkeit benötigt.


Du kannst das Ticket unter folgendem Link einsehen:
%(link)s

Diese Mail wurde automatisch generiert und ist daher auch ohne Unterschrift gültig.
"""

MAIL_TICKETNEWCOMMENT_SUBJECT = MAIL_PREFIX + "Neuer Kommentar im Ticket #%(id)d"
MAIL_TICKETNEWCOMMENT_TEXT = """
Hallo,
diese Mail soll dich informieren, dass %(name)s im Ticket #%(id)d "%(subject)s" in der für dich freigegebenen Aufgabenkategorie "%(cat)s" soeben einen neuen Kommentar hinterlassen hat.

Du kannst das Ticket unter folgendem Link einsehen:
%(link)s

Diese Mail wurde automatisch generiert und ist daher auch ohne Unterschrift gültig.
"""

MAIL_TICKETNEW_SUBJECT = MAIL_PREFIX + "Neues Ticket in der Kategorie %(cat)s"
MAIL_TICKETNEW_TEXT = """
Hallo,
diese Mail soll dich informieren, dass %(name)s soeben in der für dich freigegebenen Aufgabenkategorie "%(cat)s" ein neues Ticket (#%(id)d -  "%(subject)s") angelegt hat.

Du kannst das Ticket unter folgendem Link einsehen:
%(link)s

Diese Mail wurde automatisch generiert und ist daher auch ohne Unterschrift gültig.
"""

BANK_ACCOUNT = """
Vorstand des Fördervereins der Fachschaft Informatik an der TU Darmstadt e.V.
Raum D120
Hochschulstraße 10
64289 Darmstadt
"""
