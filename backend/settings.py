"""
Django settings (dev + prod friendly)

Usage:
- Create a local `.env` based on `.env.example`.
- For local dev you can keep USE_RENDER_DB=False (default) and use SQLite or local Postgres.
- To use Render Postgres set USE_RENDER_DB=True (or configure Render env vars) and deploy.

Security reminder: never commit your real `.env` to git.
"""

import os
from pathlib import Path
import environ
from datetime import timedelta

# ──────────────────────────────────────────────────────────────────────────────
# ENV
# ──────────────────────────────────────────────────────────────────────────────
env = environ.Env(
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(list, []),
    TIME_ZONE=(str, "UTC"),
    CORS_ALLOWED_ORIGINS=(list, []),
    USE_RENDER_DB=(bool, False),  # Toggle that decides whether to use Render's DB
)

BASE_DIR = Path(__file__).resolve().parent.parent

# Load .env in project root if present
env_file = BASE_DIR / ".env"
if env_file.exists():
    environ.Env.read_env(env_file)

# ──────────────────────────────────────────────────────────────────────────────
# SECURITY / GENERAL
# ──────────────────────────────────────────────────────────────────────────────
SECRET_KEY = env("SECRET_KEY")
DEBUG = env("DEBUG")
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["localhost", "127.0.0.1"])

# ──────────────────────────────────────────────────────────────────────────────
# APPS / MIDDLEWARE
# ──────────────────────────────────────────────────────────────────────────────
INSTALLED_APPS = [
    "corsheaders",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third-party
    "rest_framework",
    "rest_framework_simplejwt.token_blacklist",
    "drf_yasg",

    # Local
    "quotes",
    
    'whitenoise.runserver_nostatic',  # Must come before django.contrib.staticfiles
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # keep first for CORS
    'whitenoise.middleware.WhiteNoiseMiddleware',  # add this right after CorsMiddleware    "django.middleware.security.SecurityMiddleware",
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

# ──────────────────────────────────────────────────────────────────────────────
# DATABASES
# - Behavior:
#   * If USE_RENDER_DB=True (env boolean) -> use the Render Postgres credentials (DB_HOST, DB_NAME, etc).
#   * Else -> use DB_ENGINE value. Default is sqlite3 for zero-config local dev.
# ──────────────────────────────────────────────────────────────────────────────
USE_RENDER_DB = env.bool("USE_RENDER_DB", False)

if USE_RENDER_DB:
    # Render Postgres (or any remote Postgres). Ensure these env vars are set on the host.
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": env("DB_NAME"),
            "USER": env("DB_USER"),
            "PASSWORD": env("DB_PASSWORD"),
            "HOST": env("DB_HOST"),
            "PORT": env("DB_PORT", default="5432"),
        }
    }
else:
    # Local/dev DB selection
    DB_ENGINE = env("DB_ENGINE", default="django.db.backends.sqlite3")
    if DB_ENGINE == "django.db.backends.sqlite3":
        DATABASES = {
            "default": {
                "ENGINE": DB_ENGINE,
                "NAME": BASE_DIR / "db.sqlite3",
            }
        }
    else:
        # Local Postgres (if you prefer to run Postgres locally)
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

# Example (commented) — if you want to hardcode switching, you can uncomment below:
# -----------------------------------------
# # Production (Render) direct config example:
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": "learning_api_huru",
#         "USER": "henry",
#         "PASSWORD": "RENDER_PASSWORD",
#         "HOST": "dpg-d2bk64re5dus738aqj2g-a.oregon-postgres.render.com",
#         "PORT": "5432",
#     }
# }
# -----------------------------------------

# ──────────────────────────────────────────────────────────────────────────────
# AUTH / PASSWORD VALIDATION
# ──────────────────────────────────────────────────────────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ──────────────────────────────────────────────────────────────────────────────
# REST FRAMEWORK + SIMPLE JWT
# ──────────────────────────────────────────────────────────────────────────────
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

# ──────────────────────────────────────────────────────────────────────────────
# CORS / INTERNATIONALIZATION / STATIC / MEDIA
# ──────────────────────────────────────────────────────────────────────────────
CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS", default=[])
LANGUAGE_CODE = "en-us"
TIME_ZONE = env("TIME_ZONE", default="UTC")
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ──────────────────────────────────────────────────────────────────────────────
# DRF-YASG / SWAGGER
# ──────────────────────────────────────────────────────────────────────────────
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

# ──────────────────────────────────────────────────────────────────────────────
# Helpful debug-print (optional) — uncomment for debugging env loading
# ──────────────────────────────────────────────────────────────────────────────
# print("DEBUG =", DEBUG)
# print("ALLOWED_HOSTS =", ALLOWED_HOSTS)
# print("USE_RENDER_DB =", USE_RENDER_DB)
# print("DB_HOST (ENV) =", os.getenv("DB_HOST"))
