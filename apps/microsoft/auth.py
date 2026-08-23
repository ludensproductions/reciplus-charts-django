from django.contrib.auth.backends import BaseBackend

from apps.groups.consts import UserGroups
from apps.groups.models import CustomGroup as Group
from apps.microsoft.consts import ERROR_NO_EMAIL, ERROR_USERNAME_TAKEN
from apps.users.consts import ERROR_USER_BANNED
from apps.users.models import User
from apps.users.utils import normalize_email
from django.db.models import Q


class MicrosoftAuthenticationBackend(BaseBackend):
    """Backend de autenticación mediante Microsoft OAuth2."""

    def authenticate(self, request, user=None) -> User:
        """Autentica o crea un usuario a partir de los datos de Microsoft Graph."""
        if hasattr(request, "microsoft_login_error"):
            del request.microsoft_login_error
        if not user:
            return None
        microsoft_id = user.get("id")
        email = normalize_email(user.get("mail") or user.get("userPrincipalName"))
        if not email:
            request.microsoft_login_error = ERROR_NO_EMAIL
            return None

        # Split surname into last_name and second_last_name
        surname = user.get("surname", "")
        surname_parts = surname.split(maxsplit=1)
        last_name = surname_parts[0] if surname_parts else ""
        second_last_name = surname_parts[1] if len(surname_parts) > 1 else ""

        existing_user = User.objects.filter(microsoft_id=microsoft_id, deleted__isnull=True, is_active=True).first()

        if not existing_user:
            existing_user = User.objects.filter(email__iexact=email, deleted__isnull=True, is_active=True).first()

        if existing_user and existing_user.is_banned:
            request.microsoft_login_error = ERROR_USER_BANNED
            return None

        created = False

        if existing_user:
            update_fields = []

            if existing_user.microsoft_id != microsoft_id:
                existing_user.microsoft_id = microsoft_id
                update_fields.append("microsoft_id")

            if not existing_user.email and email:
                existing_user.email = email
                update_fields.append("email")

            given_name = user.get("givenName", "")
            if not existing_user.first_name and given_name:
                existing_user.first_name = given_name
                update_fields.append("first_name")

            if not existing_user.last_name and last_name:
                existing_user.last_name = last_name
                update_fields.append("last_name")

            if not existing_user.second_last_name and second_last_name:
                existing_user.second_last_name = second_last_name
                update_fields.append("second_last_name")

            if update_fields:
                existing_user.save(update_fields=update_fields)

            user_database = existing_user
        else:
            if User.all_objects.filter(Q(email__iexact=email) | Q(username=email)).exists():
                request.microsoft_login_error = ERROR_USERNAME_TAKEN
                return None

            user_database = User.objects.create(
                microsoft_id=microsoft_id,
                email=email,
                first_name=user.get("givenName", ""),
                last_name=last_name,
                second_last_name=second_last_name,
                username=email,
            )
            created = True

        if created:
            default_group = Group.objects.filter(name=UserGroups.ADMINISTRADOR).first()
            if default_group:
                user_database.groups.add(default_group)
        return user_database

    def get_user(self, user_id):
        """Retorna el usuario por su PK."""
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
