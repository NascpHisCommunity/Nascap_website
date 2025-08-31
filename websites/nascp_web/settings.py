"""
nascp_web/settings.py
Cleaned for Django 5.1.6 + django-summernote
"""

from pathlib import Path
import os

# ---- critical routing vars ----
ROOT_URLCONF = "nascp_web.urls"           # ← ensure this matches your project name
WSGI_APPLICATION = "nascp_web.wsgi.application"
# ---------------------------------------------------------------------
# Core paths
# ---------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------
# Security & debug
# ---------------------------------------------------------------------
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-only-key")          # 🔒 override in prod
DEBUG      = os.getenv("DJANGO_DEBUG", "1") == "1"
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]                           # 🔒 add your domain in prod

# HTTPS / HSTS (enable only when DEBUG == False)
SECURE_SSL_REDIRECT          = not DEBUG                             # 🔒
SECURE_HSTS_SECONDS          = 31_536_000 if not DEBUG else 0        # 🔒 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = not DEBUG                           # 🔒
SECURE_HSTS_PRELOAD          = not DEBUG                             # 🔒
SECURE_CONTENT_TYPE_NOSNIFF  = True
SECURE_BROWSER_XSS_FILTER    = True
X_FRAME_OPTIONS              = "DENY"

# ---------------------------------------------------------------------
# Content-Security Policy – relaxed for Summernote in dev
# ---------------------------------------------------------------------
CSP_DEFAULT_SRC = ("'self'",)
CSP_STYLE_SRC   = ("'self'", "'unsafe-inline'", "https://fonts.googleapis.com")
CSP_SCRIPT_SRC  = ("'self'", "'unsafe-inline'", "https://ajax.googleapis.com")
CSP_FONT_SRC    = ("'self'", "https://fonts.gstatic.com")

# ---------------------------------------------------------------------
# Authentication
# ---------------------------------------------------------------------
AUTH_USER_MODEL = "users.CustomUser"

# ---------------------------------------------------------------------
# Installed apps
# ---------------------------------------------------------------------
INSTALLED_APPS = [
    # Django core
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third-party
    "crispy_forms",
    "django_filters",
    "django_tables2",
    "rest_framework",
    "django_summernote",             # keep above custom apps for template precedence
    "csp",

    # Local apps
    "apps.users",
    "apps.file_manager",
    "apps.api",
    "apps.content_creator",
    "apps.audit.apps.AuditConfig",
]

CRISPY_TEMPLATE_PACK = "bootstrap5"

# Summernote tweaks (optional)
SUMMERNOTE_CONFIG = {
    "summernote": {
        "width": "100%",
        "height": 400,
        # "toolbar": [ ... ]          # customise if desired
    },
}

# ---------------------------------------------------------------------
# Middleware
# ---------------------------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "apps.audit.middleware.AuditMiddleware",
    "csp.middleware.CSPMiddleware",
]

# ---------------------------------------------------------------------
# Templates
# ---------------------------------------------------------------------
TEMPLATES = [{
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
}]

# ---------------------------------------------------------------------
# Database
# ---------------------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME":     "nascp_web",
        "USER":     "postgres",
        "PASSWORD": "%%%%%%%",
        "HOST":     "localhost",
        "PORT":     "1111",
    }
}

# ---------------------------------------------------------------------
# REST Framework
# ---------------------------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
}

# ---------------------------------------------------------------------
# Static & media files
# ---------------------------------------------------------------------
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]      # project-level assets (dev)
STATIC_ROOT     = BASE_DIR / "staticfiles"    # `collectstatic` target

MEDIA_URL  = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ---------------------------------------------------------------------
# Internationalisation
# ---------------------------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE     = "UTC"
USE_I18N      = True
USE_TZ        = True

# ---------------------------------------------------------------------
# Misc
# ---------------------------------------------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
