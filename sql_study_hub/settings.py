"""Django settings for sql_study_hub project."""

import os
from pathlib import Path

import dj_database_url
from django.core.exceptions import ImproperlyConfigured

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/

def get_bool_env(name, default=False):
    value = os.getenv(name)
    if value is None:
        return default
    value = normalize_env_value(value)
    return value.strip().lower() in {"1", "true", "yes", "on"}


def get_list_env(name, default=""):
    raw_value = normalize_env_value(os.getenv(name, default))
    return [item.strip() for item in raw_value.split(",") if item.strip()]


def normalize_env_value(value):
    if value is None:
        return ""

    normalized = value.strip()
    if len(normalized) >= 2 and normalized[0] == normalized[-1] and normalized[0] in {'"', "'"}:
        return normalized[1:-1].strip()

    return normalized


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-local-dev-key")
SECRET_KEY = normalize_env_value(SECRET_KEY)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = get_bool_env("DEBUG", default=True)

ALLOWED_HOSTS = get_list_env("ALLOWED_HOSTS", "127.0.0.1,localhost")

railway_public_domain = os.getenv("RAILWAY_PUBLIC_DOMAIN")
railway_public_domain = normalize_env_value(railway_public_domain)
if railway_public_domain and railway_public_domain not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append(railway_public_domain)

CSRF_TRUSTED_ORIGINS = get_list_env("CSRF_TRUSTED_ORIGINS")
if railway_public_domain:
    railway_origin = f"https://{railway_public_domain}"
    if railway_origin not in CSRF_TRUSTED_ORIGINS:
        CSRF_TRUSTED_ORIGINS.append(railway_origin)


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "study_hub",
    'crispy_forms',
    'crispy_bootstrap5',
]

AUTH_USER_MODEL = "study_hub.User"

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

ROOT_URLCONF = "sql_study_hub.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "sql_study_hub.wsgi.application"


# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
        conn_health_checks=True,
    )
}


# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

#Login and Logout redirect
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

# Emails BackEnd
EMAIL_BACKEND = os.getenv("EMAIL_BACKEND", "django.core.mail.backends.smtp.EmailBackend")
EMAIL_BACKEND = normalize_env_value(EMAIL_BACKEND)
EMAIL_HOST = normalize_env_value(os.getenv("EMAIL_HOST", "smtp.gmail.com"))
EMAIL_PORT = int(normalize_env_value(os.getenv("EMAIL_PORT", "587")))
EMAIL_USE_TLS = get_bool_env("EMAIL_USE_TLS", default=EMAIL_PORT == 587)
EMAIL_USE_SSL = get_bool_env("EMAIL_USE_SSL", default=EMAIL_PORT == 465)
EMAIL_HOST_USER = normalize_env_value(os.getenv("EMAIL_HOST_USER", ""))
EMAIL_HOST_PASSWORD = normalize_env_value(os.getenv("EMAIL_HOST_PASSWORD", ""))
EMAIL_TIMEOUT = int(normalize_env_value(os.getenv("EMAIL_TIMEOUT", "30")))
DEFAULT_FROM_EMAIL = normalize_env_value(os.getenv("DEFAULT_FROM_EMAIL", EMAIL_HOST_USER or "noreply@example.com"))
SERVER_EMAIL = normalize_env_value(os.getenv("SERVER_EMAIL", DEFAULT_FROM_EMAIL))

if EMAIL_USE_TLS and EMAIL_USE_SSL:
    raise ImproperlyConfigured("EMAIL_USE_TLS and EMAIL_USE_SSL cannot both be True.")

#Apps Config
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"