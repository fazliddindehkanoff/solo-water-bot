import os
import hashlib
from pathlib import Path
from environs import Env

from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

env = Env()
if not os.path.exists(".env"):
    print(".env fayli topilmadi!")
    print(".env.example faylidan nusxa ko'chirib shablonni o'zizga moslang.")
    exit(1)


env.read_env()

API_TOKEN = env.str("API_TOKEN")
SECRET_KEY = env.str("SECRET_KEY")
WEB_DOMAIN = env.str("WEB_DOMAIN")
DEBUG = env.bool("DEBUG")

WEBHOOK_PATH = "tgbot/" + hashlib.md5(API_TOKEN.encode()).hexdigest()
WEBHOOK_URL = f"{WEB_DOMAIN}/{WEBHOOK_PATH}"


# ____________________________________________________

BASE_DIR = Path(__file__).resolve().parent.parent


ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    # admins
    "unfold",  # before django.contrib.admin
    "unfold.contrib.filters",  # optional, if special filters are needed
    "unfold.contrib.forms",  # optional, if special form elements are needed
    "unfold.contrib.import_export",  # optional, if django-import-export package is used
    "unfold.contrib.guardian",  # optional, if django-guardian package is used
    "unfold.contrib.simple_history",  # optional, if django-simple-history package is used
    "django.contrib.admin",  # required
    # built-in apps
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "tgbot",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "src.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "src.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
# CSRF_COOKIE_SECURE = False
# CSRF_COOKIE_HTTPONLY = False


# admin settings:

UNFOLD = {
    "SITE_TITLE": "SoloWaterAdmin",
    "SITE_HEADER": "SoloWater",
    "SITE_URL": "/",
    "SITE_SYMBOL": "water_drop",  # symbol from icon set
    "SHOW_HISTORY": True,  # show/hide "History" button, default: True
    "SHOW_VIEW_ON_SITE": True,  # show/hide "View on site" button, default: True
    "SIDEBAR": {
        "show_search": False,  # Search in applications and models names
        "show_all_applications": False,  # Dropdown with all applications and models
        "navigation": [
            {
                "items": [
                    {
                        "title": _("Dashboard"),
                        "icon": "dashboard",
                        "link": reverse_lazy("admin:index"),
                    },
                    {
                        "title": _("Foydalanuvchilar"),
                        "icon": "person",
                        "link": reverse_lazy("admin:tgbot_telegramuser_changelist"),
                    },
                    {
                        "title": _("Maxsulot Sotish"),
                        "icon": "arrow_upward",
                        "link": reverse_lazy("admin:tgbot_productoutcome_changelist"),
                    },
                    {
                        "title": _("Maxsulot sotib olish"),
                        "icon": "arrow_downward",
                        "link": reverse_lazy("admin:tgbot_productincome_changelist"),
                    },
                    {
                        "title": _("Maxsulotlar"),
                        "icon": "box",
                        "link": reverse_lazy("admin:tgbot_producttemplate_changelist"),
                    },
                    {
                        "title": _("Ta'riflar"),
                        "icon": "subscriptions",
                        "link": reverse_lazy("admin:tgbot_subscription_changelist"),
                    },
                    {
                        "title": _("Promotionlar"),
                        "icon": "list",
                        "link": reverse_lazy("admin:tgbot_promotion_changelist"),
                    },
                ],
            },
        ],
    },
}
