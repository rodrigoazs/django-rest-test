import dj_database_url  # noqa
import django_on_heroku

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "ciba",
    }
}

# django_heroku
django_on_heroku.settings(locals())
