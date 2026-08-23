ERROR_ACCESS_DENIED = "El usuario ha denegado el acceso a la aplicación"
ERROR_GENERIC = "Ha ocurrido un error."
ERROR_USER_NOT_FOUND = "User not found."
SUCCESS_LOGOUT = "User logged out successfully."

# URL names
URL_OAUTH2_AUTHORIZE = "oauth2:authorize"
URL_DASHBOARD_INDEX = "dashboard:index"

# Templates
TEMPLATE_LOGOUT = "registration/logout.html"

# Session keys
SESSION_KEY_ACCESS_TOKEN = "_oauth2_access_token"
SESSION_KEY_ID_TOKEN = "_oauth2_id_token"
SESSION_KEY_CODE_VERIFIER = "_oauth2_code_verifier"
SESSION_KEY_LOGIN_AT = "_session_login_at"

# OAuth2 provider paths
PROVIDER_PATH_AUTHORIZE = "/o/authorize/"
PROVIDER_PATH_TOKEN = "/o/token/"
PROVIDER_PATH_REVOKE = "/o/revoke_token/"
PROVIDER_PATH_USERINFO = "/o/userinfo/"
PROVIDER_PATH_LOGOUT = "/o/logout/"

# OAuth2 settings
OAUTH2_SCOPE = "openid profile email"
OAUTH2_BACKEND = "djangoproject.backends.OAuth2Backend"
PROVIDER_CHECK_INTERVAL = 60  # seconds between provider session checks

# Error callback keys
ERROR_KEY_ACCESS_DENIED = "access_denied"
