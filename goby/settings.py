# import os
from django.utils.timezone import timedelta
import pytz
from pathlib import Path
from os.path import join

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-k@vh#dx&%l962#oyj34w3^+#47f^burd%4x26ak2(h=lxs(s2i"
FERNET_KEY = "RWqdn6hhVjsKBqvuzDo7Z16uhI-oXElWn1W0nfipo6E="
# SECRET_KEY = os.environ["SECRET_KEY"]
DEBUG = True

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
        'jazzmin' ,
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
        "DIRS": ["templates"],
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

import os


# settings.py

JAZZMIN_SETTINGS = {
    # Title on the brand (19 chars max)
    "site_title": "GOBY Admin",
    
    # Title on the login screen (19 chars max)
    "site_header": "GOBY",
    
    # Logo to use for your site
    "site_logo": "logo.jpg",
    
    # Welcome text on the login screen
    "welcome_sign": "Welcome to GOBY Administration",
    
    # Copyright on the footer
    "copyright": "GOBY Ltd",
    
    # Field name on user model that contains avatar/image
    "user_avatar": None,
    
    # UI Tweaks
    "show_ui_builder": True,
    
    # Menu icons
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "accounts.User": "fas fa-user-cog",
        "accounts.Nationality": "fas fa-globe",
        "accounts.MaritalStatus": "fas fa-heart",
        "accounts.EmployeeType": "fas fa-briefcase",
        "accounts.City": "fas fa-city",
        "accounts.CityDistrict": "fas fa-map-marker-alt",
        "accounts.Employee": "fas fa-user-tie",
        "accounts.Moderator": "fas fa-user-shield",
        "clients.Client": "fas fa-user",
        "delivery.Delivery": "fas fa-truck",
        "delivery.LocationHistory": "fas fa-map-marker-alt",
        "delivery.Credits": "fas fa-coins",
        "restaurant.MenuCategory": "fas fa-utensils",
        "restaurant.Restaurant": "fas fa-store",
        "restaurant.SliderItem": "fas fa-images",
        "restaurant.MenuItem": "fas fa-hamburger",
        "restaurant.Order": "fas fa-receipt",
        "restaurant.OrderItem": "fas fa-list-ol",
    },
    
    # Menu ordering
    "order_with_respect_to": [
        "accounts",
        "clients",
        "restaurant",
        "delivery",
        "auth",
    ],
    
    # Custom links to append to app groups
    "custom_links": {
        "restaurant": [{
            "name": "Make Announcement", 
            "url": "make_announcement",
            "icon": "fas fa-bullhorn",
            "permissions": ["restaurant.view_restaurant"]
        }]
    },
    
    # Custom admin site title
    "site_brand": "GOBY Administration",
    
    # Whether to display the side menu
    "show_sidebar": True,
    
    # Whether to aut expand the menu
    "navigation_expanded": True,
    
    # Hide these apps when generating side menu
    "hide_apps": [],
    
    # Hide these models when generating side menu
    "hide_models": ["auth.group"],
    
    # List of apps to base side menu ordering off of
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    
    # Related modal configuration
    "related_modal_active": True,
    
    # Custom CSS for admin site
    "custom_css": None,
    
    # Custom JS for admin site
    "custom_js": None,
    
    # Whether to show UI customizer on the sidebar
    "show_ui_builder": True,
    
    # Change view template overrides
    "changeform_format": "horizontal_tabs",
    
    # override change forms on a per modeladmin basis
    "changeform_format_overrides": {
        "auth.user": "collapsible", 
        "auth.group": "vertical_tabs"
    },
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-indigo",
    "accent": "accent-olive",
    "navbar": "navbar-white navbar-light",
    "no_navbar_border": False,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-indigo",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": True,
    "sidebar_nav_child_indent": False,
    "sidebar_nav_compact_style": True,
    "sidebar_nav_legacy_style": True,
    "sidebar_nav_flat_style": False,
    "theme": "litera",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-outline-primary",
        "secondary": "btn-outline-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    },
    "actions_sticky_top": True
}