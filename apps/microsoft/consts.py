from django.utils.translation import gettext_lazy as _

# Identificadores base
APP_NAME = "microsoft"

# Template
TEMPLATE_NAME_INVALID_LOGIN = "microsoft/invalid_login.html"

# URLs de navegación
LOGIN_URL_NAME = "login"

# Backend de autenticación
MICROSOFT_AUTH_BACKEND = "apps.microsoft.auth.MicrosoftAuthenticationBackend"

# Mensajes de error (usuario)
ERROR_NO_EMAIL = _("La cuenta de Microsoft no proporcionó un email válido.")
ERROR_SESSION_EXPIRED = _("La sesión de autenticación expiró o es inválida. Intenta de nuevo.")
ERROR_TOKEN_FAILED = _("No se pudo obtener el token.")
ERROR_PROFILE_FAILED = _("No se pudo leer el perfil de Microsoft.")
ERROR_AUTH_FAILED = _("Autenticación fallida: Credenciales inválidas o acceso denegado.")
ERROR_USERNAME_TAKEN = _("El email de Microsoft ya está asociado a una cuenta existente o desactivada.")

# Mensajes de éxito (usuario)
MSG_SESSION_CLOSED = _("Tu sesión se ha cerrado correctamente")

# Microsoft Graph API
USER_ME_ENDPOINT = "/me"
SESSION_KEY_TOKEN_CACHE = "token_cache"
SESSION_KEY_AUTH_FLOW = "auth_flow"
SESSION_KEY_USER = "user"
