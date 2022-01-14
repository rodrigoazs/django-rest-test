import os

import dj_database_url

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

POSTGRES_URL = "HEROKU_POSTGRESQL_d92levl26fuku6_URL"
DATABASES = {"default": dj_database_url.config(default=os.environ[POSTGRES_URL])}
