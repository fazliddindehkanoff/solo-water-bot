import os
import hashlib
import environ

from pathlib import Path
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


env = environ.Env()

BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, ".env"), overwrite=True)

SECRET_KEY = env("SECRET_KEY")
DEBUG = env("DEBUG") == "1"

API_TOKEN = env("API_TOKEN")
WEB_DOMAIN = env("WEB_DOMAIN")
DEBUG = env("DEBUG")
WEBHOOK_PATH = "tgbot/" + hashlib.md5(API_TOKEN.encode()).hexdigest()
WEBHOOK_URL = f"{WEB_DOMAIN}/{WEBHOOK_PATH}"

# ____________________________________________________

ALLOWED_HOSTS = ["*"]
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
    # external apps
    "django_lifecycle_checks",
    # local apps
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
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "src.context_processors.custom_context",
            ],
        },
    },
]

WSGI_APPLICATION = "src.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("POSTGRES_DB"),
        "USER": env("POSTGRES_USER"),
        "PASSWORD": env("POSTGRES_PASSWORD"),
        "HOST": "db",
        "PORT": "5432",
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

LANGUAGE_CODE = "uz"

TIME_ZONE = "Asia/Tashkent"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
CSRF_TRUSTED_ORIGINS = ["https://bot.solowater.uz"]

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
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Buyurtmalar ro'yxati"),
                        "icon": "format_list_bulleted",
                        "link": reverse_lazy("admin:tgbot_order_changelist"),
                    },
                    {
                        "title": _("Kirim-Chiqim"),
                        "icon": "swap_vert",
                        "link": reverse_lazy("admin:tgbot_inoutcome_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Xisoblar"),
                        "icon": "account_balance_wallet",
                        "link": reverse_lazy("admin:tgbot_account_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Telegram bot foydalanuvchilari"),
                        "icon": "person",
                        "link": reverse_lazy("admin:tgbot_telegramuser_changelist"),
                    },
                    {
                        "title": _("Maxsulot aylanmasi"),
                        "icon": "bloodtype",
                        "link": reverse_lazy("admin:tgbot_productinout_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Maxsulotlar"),
                        "icon": "box",
                        "link": reverse_lazy("admin:tgbot_producttemplate_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Ta'riflar"),
                        "icon": "subscriptions",
                        "link": reverse_lazy("admin:tgbot_subscription_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Promotionlar"),
                        "icon": "list",
                        "link": reverse_lazy("admin:tgbot_promotion_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Bonus ball"),
                        "icon": "list",
                        "link": reverse_lazy("admin:tgbot_bonusexchange_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Operatorlar"),
                        "icon": "support_agent",
                        "link": reverse_lazy("admin:auth_user_changelist"),
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Kuriyerlar"),
                        "icon": "directions_run",
                        "link": reverse_lazy("admin:tgbot_curier_changelist"),
                    },
                ],
            },
        ],
    },
}
