import logging

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend

from apps.users.consts import ERROR_USER_BANNED
from apps.users.utils import normalize_email

logger = logging.getLogger(__name__)

User = get_user_model()


class OAuth2Backend(BaseBackend):
    """Authentication backend for OAuth2 provider (acceso unico).

    Authenticates users based on user data received from the OAuth2
    provider's userinfo endpoint. If the user does not exist locally,
    it is created automatically.
    """

    def authenticate(self, request, user_data=None, token_data=None, **kwargs):
        """Authenticates or creates a user from OAuth2 provider data.

        Args:
            request: The current HTTP request.
            user_data: Dict with user info from the OAuth2 provider.
            token_data: Dict with token info from the OAuth2 provider.

        Returns:
            User instance if authentication succeeds, None otherwise.
        """
        if user_data is None:
            return None

        username = user_data.get("username")
        email = normalize_email(user_data.get("email") or username)
        if not username and not email:
            return None

        try:
            existing_user = None

            if username:
                existing_user = User.objects.filter(username=username).first()

            if not existing_user and email:
                existing_user = User.objects.filter(email__iexact=email).first()

            if existing_user and existing_user.is_banned:
                request.oauth2_login_error = ERROR_USER_BANNED
                return None

            if existing_user:
                fields_to_update = []
                if email and existing_user.email != email:
                    existing_user.email = email
                    fields_to_update.append("email")
                if user_data.get("first_name") and existing_user.first_name != user_data.get("first_name"):
                    existing_user.first_name = user_data.get("first_name")
                    fields_to_update.append("first_name")
                if user_data.get("last_name") and existing_user.last_name != user_data.get("last_name"):
                    existing_user.last_name = user_data.get("last_name")
                    fields_to_update.append("last_name")
                if fields_to_update:
                    existing_user.save(update_fields=fields_to_update)
                return existing_user

            user = User.objects.create(
                username=email or username,
                email=email or "",
                first_name=user_data.get("first_name", ""),
                last_name=user_data.get("last_name", ""),
            )

            return user
        except Exception:
            logger.exception("Error authenticating user via OAuth2")
            return None

    def get_user(self, user_id):
        """Retrieves a user by primary key.

        Args:
            user_id: The user's primary key.

        Returns:
            User instance or None.
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
