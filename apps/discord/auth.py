import os

from django.contrib.auth.backends import BaseBackend

from apps.discord.consts import ERROR_NO_ROLES
from apps.users.consts import ERROR_USER_BANNED
from apps.users.models import User

ALLOWED_ROLES = os.getenv("ALLOWED_ROLES", "").split(",")


class DiscordAuthenticationBackend(BaseBackend):
    """Docstring for class DiscordAuthenticationBackend."""

    def authenticate(self, request, user) -> User:
        """Docstring for authenticate."""
        user_id = user.get("id", {})
        if not user_id:
            return None

        existing_user = User.objects.filter(discord_id=user_id, deleted__isnull=True, is_active=True).first()
        if existing_user and existing_user.is_banned:
            request.discord_login_error = ERROR_USER_BANNED
            return None

        roles = user.get("roles", [])
        if not set(roles).intersection(ALLOWED_ROLES):
            request.discord_login_error = ERROR_NO_ROLES
            return None
        return User.objects.create_update_discord_user(user, request)

    def get_user(self, user_id):
        """Docstring for get_user."""
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
