from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv(
    "DJANGO_SECRET_KEY",
    "dev-only-change-me",
)

DEBUG = (
    os.getenv(
        "DJANGO_DEBUG",
        "True",
    ).lower()
    == "true"
)

ALLOWED_HOSTS = [
    host.strip()
    for host in os.getenv(
        "DJANGO_ALLOWED_HOSTS",
        "127.0.0.1,localhost",
    ).split(",")
    if host.strip()
]


INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "accounts",
    "projects",
    "tasks",
    "dashboard",
]


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


ROOT_URLCONF = "config.urls"


TEMPLATES = [
    {
        "BACKEND":
            "django.template.backends.django.DjangoTemplates",

        "DIRS": [
            BASE_DIR / "templates",
        ],

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


WSGI_APPLICATION = "config.wsgi.application"


# =========================================================
# BANCO DE DADOS
# =========================================================

DB_ENGINE = os.getenv(
    "DB_ENGINE",
    "sqlite",
).lower()


if DB_ENGINE == "postgresql":

    DATABASES = {
        "default": {
            "ENGINE":
                "django.db.backends.postgresql",

            "NAME":
                os.getenv(
                    "DB_NAME",
                    "taskflow",
                ),

            "USER":
                os.getenv(
                    "DB_USER",
                    "postgres",
                ),

            "PASSWORD":
                os.getenv(
                    "DB_PASSWORD",
                    "postgres",
                ),

            "HOST":
                os.getenv(
                    "DB_HOST",
                    "localhost",
                ),

            "PORT":
                os.getenv(
                    "DB_PORT",
                    "5432",
                ),

            "CONN_MAX_AGE": 60,
        }
    }

else:

    DATABASES = {
        "default": {
            "ENGINE":
                "django.db.backends.sqlite3",

            "NAME":
                BASE_DIR / "db.sqlite3",
        }
    }


# =========================================================
# SENHAS
# =========================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME":
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator",
    },
    {
        "NAME":
            "django.contrib.auth.password_validation."
            "MinimumLengthValidator",
    },
    {
        "NAME":
            "django.contrib.auth.password_validation."
            "CommonPasswordValidator",
    },
    {
        "NAME":
            "django.contrib.auth.password_validation."
            "NumericPasswordValidator",
    },
]


# =========================================================
# LOCALIZAÇÃO
# =========================================================

LANGUAGE_CODE = "pt-br"

TIME_ZONE = "America/Bahia"

USE_I18N = True

USE_TZ = True


# =========================================================
# ARQUIVOS ESTÁTICOS
# =========================================================

STATIC_URL = "/static/"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]

STATIC_ROOT = (
    BASE_DIR
    / "staticfiles"
)


# Desenvolvimento e testes:
# utiliza os arquivos diretamente da pasta static.
#
# Produção:
# utiliza WhiteNoise com compressão e manifesto.

if DEBUG:

    STORAGES = {
        "default": {
            "BACKEND":
                "django.core.files.storage."
                "FileSystemStorage",
        },

        "staticfiles": {
            "BACKEND":
                "django.contrib.staticfiles.storage."
                "StaticFilesStorage",
        },
    }

else:

    STORAGES = {
        "default": {
            "BACKEND":
                "django.core.files.storage."
                "FileSystemStorage",
        },

        "staticfiles": {
            "BACKEND":
                "whitenoise.storage."
                "CompressedManifestStaticFilesStorage",
        },
    }


# =========================================================
# UPLOADS
# =========================================================

MEDIA_URL = "/media/"

MEDIA_ROOT = (
    BASE_DIR
    / "media"
)


# =========================================================
# MODELO DE USUÁRIO
# =========================================================

DEFAULT_AUTO_FIELD = (
    "django.db.models.BigAutoField"
)

AUTH_USER_MODEL = (
    "accounts.User"
)


# =========================================================
# LOGIN
# =========================================================

LOGIN_URL = (
    "accounts:login"
)

LOGIN_REDIRECT_URL = (
    "dashboard:home"
)

LOGOUT_REDIRECT_URL = (
    "accounts:login"
)


# =========================================================
# SEGURANÇA
# =========================================================

SESSION_COOKIE_HTTPONLY = True

CSRF_COOKIE_HTTPONLY = False

SECURE_CONTENT_TYPE_NOSNIFF = True

X_FRAME_OPTIONS = "DENY"