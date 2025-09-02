"""
nascp_web/settings.py
Django 5.1.6 • CKEditor configured (uploads enabled)
"""

from pathlib import Path
import os

# ---------------------------------------------------------------------
# Core paths
# ---------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------
# Routing (project module names)
# ---------------------------------------------------------------------
ROOT_URLCONF = "nascp_web.urls"
WSGI_APPLICATION = "nascp_web.wsgi.application"

# ---------------------------------------------------------------------
# Security & debug
# ---------------------------------------------------------------------
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-only-key")   # 🔒 override in prod
DEBUG = os.getenv("DJANGO_DEBUG", "1") == "1"
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]                    # 🔒 add your domain in prod

# HTTPS / HSTS (enable only when DEBUG == False)
SECURE_SSL_REDIRECT = not DEBUG
SECURE_HSTS_SECONDS = 31_536_000 if not DEBUG else 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = not DEBUG
SECURE_HSTS_PRELOAD = not DEBUG
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
# X_FRAME_OPTIONS = "SAMEORIGIN"  # CKEditor doesn't require iframes; default is OK

# ---------------------------------------------------------------------
# Content Security Policy (CSP) – friendly defaults for CKEditor
# ---------------------------------------------------------------------
# Using django-csp middleware only (no 'csp' in INSTALLED_APPS required)
CSP_SCRIPT_SRC = ("'self'", "'unsafe-inline'")
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'", "https://fonts.googleapis.com")
CSP_IMG_SRC = ("'self'", "data:", "blob:")
CSP_FRAME_ANCESTORS = ("'self'",)

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
    "crispy_bootstrap5",                      # ▶ CKEDITOR: ensure crispy uses bootstrap5 correctly
    "django_filters",
    "django_tables2",
    "rest_framework",
    "ckeditor",                               # ▶ CKEDITOR: add
    "ckeditor_uploader",                      # ▶ CKEDITOR: add (enables uploads)

    # Local apps
    "apps.users",
    "apps.file_manager",
    "apps.api",
    "apps.content_creator",
    "apps.audit.apps.AuditConfig",
]

# Crispy Forms (Bootstrap 5)
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"  # ▶ CKEDITOR: added
CRISPY_TEMPLATE_PACK = "bootstrap5"

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
    "csp.middleware.CSPMiddleware",          # uses CSP_* settings above
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
# Database (dev example)
# ---------------------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "nascp_web",
        "USER": "postgres",
        "PASSWORD": "vvvvvvvv",
        "HOST": "localhost",
        "PORT": "1111",
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
STATICFILES_DIRS = [BASE_DIR / "static"]     # source assets (dev)
STATIC_ROOT = BASE_DIR / "staticfiles"       # collectstatic target

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ---------------------------------------------------------------------
# CKEditor configuration
# ---------------------------------------------------------------------
CKEDITOR_UPLOAD_PATH = "uploads/"            # ▶ CKEDITOR: adds /media/uploads/...
CKEDITOR_IMAGE_BACKEND = "pillow"            # ▶ CKEDITOR

CKEDITOR_CONFIGS = {                         # ▶ CKEDITOR: toolbar/features
    "default": {
        "toolbar": "full",                   # or 'basic'
        "height": 400,
        "width": "100%",
        "extraPlugins": ",".join([
            "uploadimage", "image2", "autolink", "embed", "codesnippet", "justify"
        ]),
        "removePlugins": "stylesheetparser",
    }
}

# ---------------------------------------------------------------------
# Internationalisation
# ---------------------------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ---------------------------------------------------------------------
# Misc
# ---------------------------------------------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
