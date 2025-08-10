# backend/settings.py
import os
from pathlib import Path
import environ
from datetime import timedelta

# ─────────────────────────────
# BASE & ENV
# ─────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    DEBUG=(bool, False),
    USE_RENDER_DB=(bool, False),
)

# Load .env if present (do NOT commit .env)
env_file = BASE_DIR / ".env"
if env_file.exists():
    environ.Env.read_env(env_file)

# ─────────────────────────────
# SECURITY
# ─────────────────────────────
SECRET_KEY = env("SECRET_KEY")
DEBUG = env.bool("DEBUG", False)

# ALLOWED_HOSTS: accept comma-separated string in env or fall back to sane defaults
_raw_allowed = env("ALLOWED_HOSTS", default="")
if isinstance(_raw_allowed, (list, tuple)):
    ALLOWED_HOSTS = list(_raw_allowed)
else:
    ALLOWED_HOSTS = [h.strip() for h in str(_raw_allowed).split(",") if h.strip()] or ["localhost", "127.0.0.1"]

# ─────────────────────────────
# APPS / MIDDLEWARE
# ─────────────────────────────
INSTALLED_APPS = [
    "corsheaders",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",

    # Third-party
    "rest_framework",
    "rest_framework_simplejwt.token_blacklist",
    "drf_yasg",

    # Local apps
    "quotes",

    # Static
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # must be high in the stack
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "backend.wsgi.application"

# ─────────────────────────────
# DATABASE
# ─────────────────────────────
if env.bool("USE_RENDER_DB", False):
    DATABASES = {
        "default": {
            "ENGINE": env("DB_ENGINE"),
            "NAME": env("DB_NAME"),
            "USER": env("DB_USER"),
            "PASSWORD": env("DB_PASSWORD"),
            "HOST": env("DB_HOST"),
            "PORT": env("DB_PORT"),
        }
    }
else:
    DB_ENGINE = env("DB_ENGINE", default="django.db.backends.sqlite3")
    if DB_ENGINE == "django.db.backends.sqlite3":
        DATABASES = {
            "default": {
                "ENGINE": DB_ENGINE,
                "NAME": BASE_DIR / "db.sqlite3",
            }
        }
    else:
        DATABASES = {
            "default": {
                "ENGINE": DB_ENGINE,
                "NAME": env("DB_NAME", default="learning_api_local"),
                "USER": env("DB_USER", default="postgres"),
                "PASSWORD": env("DB_PASSWORD", default=""),
                "HOST": env("DB_HOST", default="localhost"),
                "PORT": env("DB_PORT", default="5432"),
            }
        }

# ─────────────────────────────
# AUTH / PASSWORD VALIDATORS
# ─────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ─────────────────────────────
# REST FRAMEWORK & JWT
# ─────────────────────────────
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=env.int("ACCESS_TOKEN_LIFETIME_MINUTES", 15)),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=env.int("REFRESH_TOKEN_LIFETIME_DAYS", 7)),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": False,
    "ALGORITHM": "HS256",
    "SIGNING_KEY": SECRET_KEY,
    "AUTH_HEADER_TYPES": ("Bearer",),
}

# ─────────────────────────────
# CORS
# ─────────────────────────────
# Read comma-separated CORS_ALLOWED_ORIGINS from env (full origins required, e.g. https://example.com)
_raw_cors = env("CORS_ALLOWED_ORIGINS", default="")
if isinstance(_raw_cors, (list, tuple)):
    CORS_ALLOWED_ORIGINS = list(_raw_cors)
else:
    CORS_ALLOWED_ORIGINS = [o.strip() for o in str(_raw_cors).split(",") if o.strip()]

# Helpful: allow all vercel.app subdomains (useful for previews)
CORS_ALLOWED_ORIGIN_REGEXES = [
    r"^https://.*\.vercel\.app$",
]

# Optional toggle (for quick debugging only; do NOT use long-term in production)
if env.bool("CORS_ALLOW_ALL_ORIGINS", False):
    CORS_ALLOW_ALL_ORIGINS = True

# Provide sensible defaults if none configured
if not CORS_ALLOWED_ORIGINS and not env.bool("CORS_ALLOW_ALL_ORIGINS", False):
    CORS_ALLOWED_ORIGINS = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]

# ─────────────────────────────
# I18N / TIMEZONE
# ─────────────────────────────
LANGUAGE_CODE = "en-us"
TIME_ZONE = env("TIME_ZONE", default="UTC")
USE_I18N = True
USE_TZ = True

# ─────────────────────────────
# STATIC / MEDIA
# ─────────────────────────────
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ─────────────────────────────
# DRF-YASG / SWAGGER
# ─────────────────────────────
SWAGGER_SETTINGS = {
    "USE_SESSION_AUTH": False,
    "SECURITY_DEFINITIONS": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": 'JWT Authorization header using the Bearer scheme. Example: "Authorization: Bearer <token>"',
        }
    },
}
