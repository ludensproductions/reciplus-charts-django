import mimetypes
import os
from datetime import timedelta
from pathlib import Path
from urllib.parse import urlparse

from django.utils.log import DEFAULT_LOGGING
from django.utils.translation import gettext_lazy as _
from dotenv import load_dotenv

from utils.sequences import SEQUENCES_DICT, create_sequences

load_dotenv(override=True)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.getenv("SECRET_KEY")

# Variable to allow some debug features to be enabled even in productions
DEBUG = os.getenv("DEBUG") == "True"
# Variable to allow some development features to be enabled even in production
DEVELOPMENT = os.getenv("DEVELOPMENT") == "True"
WEB_URLS = [url for url in os.getenv("WEB_URL", "").split(",") if url]
ALLOWED_HOSTS = [urlparse(url).hostname for url in WEB_URLS]
CSRF_TRUSTED_ORIGINS = WEB_URLS
ENABLE_REDIS = os.getenv("ENABLE_REDIS").lower() == "true"
ENABLE_CLUSTER = os.getenv("ENABLE_CLUSTER")
mimetypes.add_type("application/javascript", ".js", True)
SITE_THEME = os.getenv("SITE_THEME", "axxon")

# Sesión compartida con reciplus-djangoninja (SSO real en web: la sesión ya existe
# cuando se abre /graphs, sin exchange) y validación de los JWT que emite ninja_jwt
# para el exchange-code nativo — ambos usan SECRET_KEY porque debe ser EXACTAMENTE
# el mismo valor que en reciplus-djangoninja/.env. El algoritmo (HS256) no es un
# setting — es constante en apps.graphs.auth_bridge, igual que en NINJA_JWT['ALGORITHM']
# de reciplus-djangoninja/djangoproject/settings.py (tampoco viene de variable de entorno ahí).

# Application definition
INSTALLED_APPS = [
    "daphne",
    # Django
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Project apps — este proyecto solo sirve las gráficas; casi nada del template
    # se usa. apps.comun se queda por sus utilidades genéricas (forms, filters, PDF, etc).
    "apps.comun.apps.ComunConfig",
    "apps.graphs",
    # Reciplus shared schema (hsl-7-common, mismo repo que reciplus-djangoninja usa) —
    # mismos nombres de app que ahí, para que AUTH_USER_MODEL/FKs resuelvan igual.
    "common.django.user",
    "common.django.hsl_7",
    # Third Pary Apps
    "rest_framework",
    "crispy_forms",
    "crispy_bootstrap5",
    "simple_history",
    "django_filters",
    "corsheaders",
    "ninja_extra",
    "django_q",
    "safedelete",
    "django_select2",
    "django_eventstream",
]

if DEVELOPMENT:
    INSTALLED_APPS.append("debug_toolbar")


MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "djangoproject.middleware.ForceLogoutMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "simple_history.middleware.HistoryRequestMiddleware",
    "utils.error_handler.ExceptionErrorHandler",
]

if DEVELOPMENT:
    MIDDLEWARE.append("debug_toolbar.middleware.DebugToolbarMiddleware")

AUTHENTICATION_BACKENDS = [
    "apps.comun.backends.CustomModelBackend",
    # Mismo backend que reciplus-djangoninja usa al crear la sesión compartida
    # (django.contrib.auth.login) — sin esto, AuthenticationMiddleware.get_user()
    # descarta la sesión aunque decodifique bien, porque el backend guardado no
    # está en esta lista.
    "django.contrib.auth.backends.ModelBackend",
]

# Django Debug Toolbar Configuration
if DEVELOPMENT:
    DEBUG_TOOLBAR_CONFIG = {
        "SHOW_COLLAPSED": True,
        # DISABLE_PANELS for default has disabled the profiling and redirect panels
        "DISABLE_PANELS": {
            "debug_toolbar.panels.redirects.RedirectsPanel",
            "debug_toolbar.panels.cache.CachePanel",
        },  # Disable panels, see https://django-debug-toolbar.readthedocs.io/en/latest/configuration.html#debug-toolbar-config
    }
# End of Django Debug Toolbar Configuration

INTERNAL_IPS = [
    "127.0.0.1",
]


ROOT_URLCONF = "djangoproject.urls"


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates", "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "apps.comun.context_processors.site_theme",
            ],
        },
    },
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("SQL_DBNAME"),
        "USER": os.getenv("SQL_USER"),
        "PASSWORD": os.getenv("SQL_PASSWORD"),
        "HOST": os.getenv("SQL_HOST"),
        "PORT": os.getenv("SQL_PORT"),
        "DISABLE_SERVER_SIDE_CURSORS": True,
        "OPTIONS": {
            "application_name": os.getenv("PROJECT_CODENAME"),
            "connect_timeout": 5,
        },
    }
}

# SQL_* debe apuntar a la MISMA base que reciplus-djangoninja (mismos valores de .env) —
# no es una base nueva, es la real de la plataforma.
DATABASE_ROUTERS = ["djangoproject.router_database.DatabaseRouter"]

# CORS: el frontend (reciplus-kotlin) llama al endpoint de intercambio SSO desde otro
# origen (otro puerto en dev). CORS_ALLOW_CREDENTIALS es obligatorio para que el
# Set-Cookie de la sesión de intercambio se guarde en el navegador.
CORS_ALLOWED_ORIGINS = [o.strip() for o in os.getenv("CORS_ALLOWED_ORIGINS", "").split(",") if o.strip()]
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOW_CREDENTIALS = True

SESSION_COOKIE_SAMESITE = "Lax"
SESSION_COOKIE_SECURE = not DEBUG


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


REDIS_PORT = os.getenv("REDIS_PORT", "6379")
REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_DB_NUMBER = os.getenv("REDIS_DB_NUMBER")
REDIS_PASS = os.getenv("REDIS_PASS")

if ENABLE_CLUSTER:
    Q_CLUSTER = {
        "name": os.getenv("PROJECT_CODENAME"),
        "workers": 2,
        "recycle": 1,
        "timeout": 75000,
        "retry": 75010,
        "compress": True,
        "save_limit": 250,
        "queue_limit": 500,
        "cpu_affinity": 1,
        "label": "Django Q",
    }

if ENABLE_CLUSTER and ENABLE_REDIS:
    Q_CLUSTER["redis"] = {
        "host": REDIS_HOST,
        "port": REDIS_PORT,
        "db": int(REDIS_DB_NUMBER),
        "password": REDIS_PASS,
    }

LANGUAGE_CODE = "es-mx"  # Mexico: es-mx
TIME_ZONE = "America/Mexico_City"  # Mexico city: America/Mexico_City || Hermosillo: America/Hermosillo
USE_I18N = True
USE_TZ = True

# Internationalization: enable multiple languages and locale paths

LANGUAGES = [
    ("es-mx", _("Español (México)")),
    ("en", _("Inglés")),
]

LOCALE_PATHS = [
    BASE_DIR / "locale",
]


STATIC_URL = "static/"
STATICFILES_DIRS = [
    BASE_DIR / "static",
]

# Caso de uso para k8s
if os.getenv("STATIC_ROOT_PATH"):
    STATICFILES_DIRS.append(os.getenv("STATIC_ROOT_PATH"))

STATICFILES_STORAGE = "whitenoise.storage.CompressedStaticFilesStorage"

if os.getenv("STATIC_ROOT_PATH"):
    STATIC_ROOT = os.path.join(os.getenv("STATIC_ROOT_PATH"), "staticfiles")
else:
    STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"


DATE_INPUT_FORMATS = ("%d-%m-%Y",)


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024

# Third Party Apps' Dependencies
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

ENABLE_OAUTH2_LOGIN = os.getenv("ENABLE_OAUTH2_LOGIN", "false").lower() == "true"
LOGIN_URL = "/oauth2/authorize/" if ENABLE_OAUTH2_LOGIN else "/"

LOGIN_REDIRECT_URL = "dashboard:index"
# Usuario compartido con reciplus-djangoninja (mismo hsl-7-common) — no es un usuario
# local del template, es el mismo user.User que ya usa el resto de la plataforma.
AUTH_USER_MODEL = "user.User"

# Logging for Production purposes
if os.getenv("LOG_FILE") == "True":
    if not os.path.exists(os.path.join(BASE_DIR, "logs")):
        os.mkdir(os.path.join(BASE_DIR, "logs"))
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "json": {"()": "pythonjsonlogger.jsonlogger.JsonFormatter"},
            "django.server": DEFAULT_LOGGING["formatters"]["django.server"],
        },
        "handlers": {
            "file_logger": {
                "class": "logging.handlers.TimedRotatingFileHandler",
                "filename": os.path.join(BASE_DIR, "logs", "debug.log"),
                "when": "midnight",
                "encoding": "utf-8",
                "backupCount": 30,
            },
            "console": {
                "class": "logging.StreamHandler",
            },
            "django.server": DEFAULT_LOGGING["handlers"]["django.server"],
        },
        "loggers": {
            "file_logger": {
                "handlers": ["file_logger", "console"],
            },
            "django.server": DEFAULT_LOGGING["loggers"]["django.server"],
        },
    }

# Mail related settings
EMAIL_BACKEND = os.getenv("EMAIL_BACKEND", "django.core.mail.backends.smtp.EmailBackend")
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587"))
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "True") == "True"
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", "")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", EMAIL_HOST_USER)
PASSWORD_RESET_BASE_URL = os.getenv("PASSWORD_RESET_BASE_URL")
PASSWORD_RESET_TIMEOUT = 3600  # 1 hour

# Creating sequences
create_sequences(SEQUENCES_DICT.keys())

SESSION_COOKIE_AGE = 8 * 60 * 60  # 8 horas

# Ninja JWT Settings
NINJA_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=60),
    "SLIDING_TOKEN_LIFETIME": timedelta(days=60),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=60),
}


# Ninja default settings
NINJA_EXTRA = {
    "PAGINATION_CLASS": "ninja_extra.pagination.PageNumberPaginationExtra",
    "ORDERING_CLASS": "someapp.somemodule.CustomOrdering",
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB_NUMBER}",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    },
    "select2": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB_NUMBER}",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
        "TIMEOUT": 60 * 60 * 24 * 5,  # 5 days
    },
}


SELECT2_CACHE_BACKEND = "select2"

# Tell select2 which cache configuration to use:
SELECT2_JS = []
SELECT2_CSS = []


# Configurar el backend para Channels
ASGI_APPLICATION = "djangoproject.asgi.application"


CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(REDIS_HOST, REDIS_PORT)],
            # Configura un límite máximo de conexiones si tu servidor lo permite.
            # "MAX_CONNECTIONS": 1000,  # Ejemplo para permitir más conexiones.
        },
    }
}


# Render docx and doc
ENABLE_DOC_RENDERING = os.getenv("ENABLE_DOC_RENDERING", "false").lower() == "true"
RENDERABLE_FILE_EXT = [".pdf"]
if ENABLE_DOC_RENDERING:
    RENDERABLE_FILE_EXT.append(".doc")
    RENDERABLE_FILE_EXT.append(".docx")

# X Frame Option
X_FRAME_OPTIONS = os.getenv("X_FRAME_OPTIONS", "DENY").upper()


# Django eventstream settings
if ENABLE_REDIS:
    EVENTSTREAM_REDIS = {
        "host": os.getenv("REDIS_HOST"),
        "port": os.getenv("REDIS_PORT"),
        "db": int(os.getenv("REDIS_DB_NUMBER")),
    }

EVENTSTREAM_CHANNELMANAGER_CLASS = "djangoproject.channelmanager.AuthenticationChannelManager"
DJANGO_EVENTSTREAM_KEEP_ALIVE_INTERVAL = 10


REPORTES_API_INTERNAL = os.getenv("REPORTES_API_INTERNAL")

# OAuth2 client settings
CODE_CHALLENGER_METHOD = os.getenv("CODE_CHALLENGER_METHOD", "S256")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI_EXTERNAL = os.getenv("REDIRECT_URI_EXTERNAL")
PROVIDER_URL_INTERNAL = os.getenv("PROVIDER_URL_INTERNAL")
PROVIDER_URL_EXTERNAL = os.getenv("PROVIDER_URL_EXTERNAL")
REDIRECT_URI_LOGOUT = os.getenv("REDIRECT_URI_LOGOUT")
API_KEY_OAUTH2_PROVIDER = os.getenv("API_KEY_OAUTH2_PROVIDER")

# Gotenberg settings
GOTENBERG_API_INTERNAL = os.getenv("GOTENBERG_API_INTERNAL")
GOTENBERG_API_ENABLE_BASIC_AUTH = os.getenv("GOTENBERG_API_ENABLE_BASIC_AUTH", "false").lower() == "true"
GOTENBERG_API_BASIC_AUTH_USERNAME = os.getenv("GOTENBERG_API_BASIC_AUTH_USERNAME")
GOTENBERG_API_BASIC_AUTH_PASSWORD = os.getenv("GOTENBERG_API_BASIC_AUTH_PASSWORD")

# Microsoft OAuth2 Settings
MICROSOFT_APP_ID = os.getenv("MICROSOFT_APP_ID")
MICROSOFT_TENANT_ID = os.getenv("MICROSOFT_TENANT_ID")
MICROSOFT_APP_SECRET = os.getenv("MICROSOFT_APP_SECRET")
MICROSOFT_REDIRECT_URI = os.getenv("MICROSOFT_REDIRECT_URI")
MICROSOFT_AUTHORITY_URL = os.getenv("MICROSOFT_AUTHORITY_URL", "https://login.microsoftonline.com")
MICROSOFT_GRAPH_API_URL = os.getenv("MICROSOFT_GRAPH_API_URL", "https://graph.microsoft.com/v1.0")
MICROSOFT_SCOPES = ["User.Read", "User.ReadBasic.All"]

# Discord OAuth2 Settings
DISCORD_CLIENT_ID = os.getenv("DISCORD_CLIENT_ID")
DISCORD_CLIENT_SECRET = os.getenv("DISCORD_CLIENT_SECRET")
DISCORD_REDIRECT_URI = os.getenv("DISCORD_REDIRECT_URI")
DISCORD_AUTH_URL = os.getenv("DISCORD_AUTH_URL", "https://discord.com/oauth2/authorize")
DISCORD_API_URL = os.getenv("DISCORD_API_URL", "https://discord.com/api")
DISCORD_GUILD_ID = os.getenv("DISCORD_GUILD_ID")
DISCORD_RESPONSE_TYPE = "code"
DISCORD_GRANT_TYPE = "authorization_code"
DISCORD_SCOPES = ["identify", "email", "guilds.members.read"]
