from django.utils.timezone import timedelta
import pytz
from pathlib import Path
from os.path import join

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-k@vh#dx&%l962#oyj34w3^+#47f^burd%4x26ak2(h=lxs(s2i"
FERNET_KEY = "RWqdn6hhVjsKBqvuzDo7Z16uhI-oXElWn1W0nfipo6E="

DEBUG = True

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Registered Apps
    "users",
    "delivery",
    "clients",
    "restaurants",
    # Third Parties
    "rest_framework",
    "rest_framework_simplejwt",
    "corsheaders",
    "drf_spectacular",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "goby.middlewares.timezone_middleware.GlobalTimezoneMiddleware",
    "goby.middlewares.lang_middleware.LangMiddleware",
    "goby.middlewares.helper_message_middleware.HelperMessageMiddleware",
]

ROOT_URLCONF = "goby.urls"

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

WSGI_APPLICATION = "goby.wsgi.application"

# Database

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db/db.sqlite3",
    }
}

# Password validation

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]

# Internationalization

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Africa/Cairo"
CAIRO_TZ = pytz.timezone("Africa/Cairo")

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)

STATIC_URL = "/static/"
STATIC_ROOT = join(BASE_DIR, "static")

MEDIA_URL = "/media/"
MEDIA_ROOT = join(BASE_DIR, "media")

# Default primary key field type

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "users.User"

# rest_framework settings
REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": "rest_framework.custom_pagination.CustomPagination",
    "PAGE_SIZE": 10,
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.OrderingFilter",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

# simple jwt settings
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=99999),
    "REFRESH_TOKEN_LIFETIME": timedelta(hours=6),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": False,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "Authorization",
}

# cors headers settings
CORS_ALLOW_ALL_ORIGINS = True

# proxy ssl headers
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
USE_X_FORWARDED_HOST = True
