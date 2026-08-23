from django.utils.translation import gettext_lazy as _

# Identificadores base
APP_NAME = "discord"

# URLs de navegación
LOGIN_URL_NAME = "login"

# Mensajes de error (usuario)
ERROR_NO_ROLES = _("No cuentas con los roles necesarios para acceder a este sistema")
ERROR_NO_PERMISSIONS = _("No tienes permisos para acceder a este sistema")

# Backend de autenticación
DISCORD_AUTH_BACKEND = "apps.discord.auth.DiscordAuthenticationBackend"

# Endpoints de la API de Discord
OAUTH2_TOKEN_ENDPOINT = "/oauth2/token"
GUILD_MEMBER_ENDPOINT = "/v6/users/@me/guilds/{guild_id}/member"
USER_ME_ENDPOINT = "/users/@me"

# Headers
CONTENT_TYPE_FORM_URLENCODED = "application/x-www-form-urlencoded"

# Discord CDN
DISCORD_AVATAR_URL = "https://cdn.discordapp.com/avatars/{user_id}/{avatar}.png"
DISCORD_DEFAULT_AVATAR_URL = "https://cdn.discordapp.com/embed/avatars/{index}.png"
