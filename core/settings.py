from pathlib import Path
import os
from dotenv import load_dotenv
import dj_database_url

# ============================================================
# Base Setup
# ============================================================
BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_BUILD_DIR = BASE_DIR / "frontend_build"
load_dotenv(BASE_DIR / ".env")

# ============================================================
# Security & Environment
# ============================================================
SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret-key")
DEBUG = os.getenv("DEBUG", "True") == "True"

ALLOWED_HOSTS = os.getenv(
    "ALLOWED_HOSTS",
    "6ahotel.com,www.6ahotel.com,sixa-hotel-backend.onrender.com,localhost,127.0.0.1"
).split(",")

# Trust proxy headers (Render)
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

# ============================================================
# Installed Apps
# ============================================================
INSTALLED_APPS = [
    # Django core
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third-party
    "rest_framework",
    "django_filters",
    "corsheaders",

    # Local apps
    "api",
    "hotel",
]

# ============================================================
# Middleware
# ============================================================
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

# ============================================================
# Templates (Frontend Integration)
# ============================================================
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [FRONTEND_BUILD_DIR],
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

WSGI_APPLICATION = "core.wsgi.application"

# ============================================================
# Database
# ============================================================
DATABASES = {
    "default": dj_database_url.config(
        default=os.getenv(
            "DATABASE_URL",
            "postgresql://postgres:password@127.0.0.1:5432/hotel_db"
        ),
        conn_max_age=600,
    )
}

# ============================================================
# Static & Media Files
# ============================================================
STATIC_URL = "/static/"
STATICFILES_DIRS = [FRONTEND_BUILD_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ============================================================
# REST Framework
# ============================================================
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.OrderingFilter",
        "rest_framework.filters.SearchFilter",
    ],
}

# ============================================================
# CORS & CSRF Configuration
# ============================================================
CORS_ALLOWED_ORIGINS = os.getenv(
    "CORS_ALLOWED_ORIGINS",
    "https://6ahotel.com,https://www.6ahotel.com,https://sixa-hotel-backend.onrender.com,http://localhost:3000"
).split(",")

CSRF_TRUSTED_ORIGINS = os.getenv(
    "CSRF_TRUSTED_ORIGINS",
    "https://6ahotel.com,https://www.6ahotel.com,https://sixa-hotel-backend.onrender.com,http://localhost:3000"
).split(",")

CORS_ALLOW_CREDENTIALS = os.getenv("CORS_ALLOW_CREDENTIALS", "True") == "True"

# ============================================================
# Internationalization
# ============================================================
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Africa/Kampala"
USE_I18N = True
USE_TZ = True

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ============================================================
# Production Security
# ============================================================
if not DEBUG:
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

if DEBUG:
    INSTALLED_APPS += ["django_extensions"]

# =========================
# EMAIL CONFIG
# =========================
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "aheebwatim@gmail.com"
EMAIL_HOST_PASSWORD = os.getenv("rmmi fhas wngp azpp")  # use Gmail App Password
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

# === Email (development-friendly) ===
# For dev: console backend prints emails to terminal.
EMAIL_BACKEND = os.environ.get("EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend")
DEFAULT_FROM_EMAIL = os.environ.get("DEFAULT_FROM_EMAIL", "no-reply@6ahotel.local")

# Who receives reservation notifications by email
RESERVATIONS_NOTIFICATION_RECIPIENTS = [
    os.environ.get("RESERVATION_NOTIFY_EMAIL", "aheebwatim@gmail.com"),
]

# === WhatsApp / Twilio (optional) ===
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID", "")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN", "")
# Example: 'whatsapp:+14155238886' from Twilio Sandbox/Business
WHATSAPP_FROM = os.environ.get("WHATSAPP_FROM", "")
# Your number for now:
WHATSAPP_TO = os.environ.get("WHATSAPP_TO", "whatsapp:+256779985109")

# You can also stash your public hotel contact here for future use
HOTEL_PUBLIC_WHATSAPP = os.environ.get("HOTEL_PUBLIC_WHATSAPP", "+256779985109")
HOTEL_PUBLIC_EMAIL = os.environ.get("HOTEL_PUBLIC_EMAIL", "aheebwatim@gmail.com")
