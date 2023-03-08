import os
from pathlib import Path

import dj_database_url
from django.core.management.utils import get_random_secret_key
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/
PYTHON_ENV = os.environ.get("PYTHON_ENV", "production")

IN_PRODUCTION = PYTHON_ENV == "production"

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("SECRET_KEY", default=get_random_secret_key())

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = PYTHON_ENV != "production"

DEBUG_PROPAGATE_EXCEPTIONS = True

ALLOWED_HOSTS = [".chaebot.kvdstudio.app" if IN_PRODUCTION else "*"]

API_PORT = os.environ.get("PORT", "8080")

# Application definition

INSTALLED_APPS = [
    "bot.apps.BotConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
    "django_filters",
    "rest_framework",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "kvisualbot.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "kvisualbot.wsgi.application"

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases


def _get_database_config():
    if IN_PRODUCTION:
        config = dj_database_url.config()
    else:
        username = os.environ.get("POSTGRESQL_USERNAME")
        db = os.environ.get("POSTGRESQL_DATABASE")
        url = f"postgres://{username}@postgres:5432/{db}"
        config = dj_database_url.parse(url)
    return config


DATABASES = {"default": _get_database_config()}


REST_FRAMEWORK = {
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
    ]
}

# Cache

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "TIMEOUT": None,
    }
}

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Seoul"

USE_I18N = True

USE_L10N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = "/static/"

STATIC_ROOT = BASE_DIR / "staticfiles"

STORAGES = {
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}


# Discord

DISCORD_ADMIN_ID = int(os.environ.get("DISCORD_ADMIN_ID", "0"))

DISCORD_TEST_GUILD_ID = int(os.environ.get("DISCORD_TEST_GUILD_ID", "0"))

DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")


# Twitter

TWITTER_CONSUMER_KEY = os.environ.get("TWITTER_CONSUMER_KEY")

TWITTER_CONSUMER_SECRET = os.environ.get("TWITTER_CONSUMER_SECRET")

TWITTER_ACCESS_KEY = os.environ.get("TWITTER_ACCESS_KEY")

TWITTER_ACCESS_SECRET = os.environ.get("TWITTER_ACCESS_SECRET")


# Bot

BOT_PREFIX = "!" if IN_PRODUCTION else "$"
