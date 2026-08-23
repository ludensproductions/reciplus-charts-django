import email

from django.contrib.auth import models
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from safedelete.managers import SafeDeleteManager

from apps.groups.consts import UserGroups
from apps.groups.models import CustomGroup as Group
from apps.users.const import ERROR_USERNAME_TAKEN
from apps.users.utils import normalize_email


class UserOAuth2Manager(models.UserManager):
    """Docstring for class UserOAuth2Manager."""

    def create_update_discord_user(self, user, request):
        """Docstring for create_update_discord_user."""
        discord_tag = "%s#%s" % (user["username"], user["discriminator"])
        normalized_email = normalize_email(user.get("email"))
        updated_user = self.filter(discord_id=user["id"]).first()
        created = False

        if not updated_user and normalized_email:
            updated_user = self.filter(email__iexact=normalized_email, deleted__isnull=True, is_active=True).first()

        if updated_user:
            update_fields = []

            if updated_user.discord_id != user["id"]:
                updated_user.discord_id = user["id"]
                update_fields.append("discord_id")

            if not updated_user.discord_tag and discord_tag:
                updated_user.discord_tag = discord_tag
                update_fields.append("discord_tag")

            if not updated_user.first_name and user["nick"]:
                updated_user.first_name = user["nick"]
                update_fields.append("first_name")

            if not updated_user.email and normalized_email:
                updated_user.email = normalized_email
                update_fields.append("email")

            if update_fields:
                updated_user.save(update_fields=update_fields)
        else:
            if self.model.all_objects.filter(Q(email__iexact=normalized_email) | Q(username=normalized_email), deleted__isnull=True, is_active=True).exists():
                request.discord_login_error = ERROR_USERNAME_TAKEN
                return None
            

            updated_user = self.create(
                discord_id=user["id"],
                username=normalized_email,
                first_name=user["nick"],
                email=normalized_email,
                discord_tag=discord_tag,
            )
            created = True

        if created:
            director_group = Group.objects.get(name=UserGroups.ADMINISTRADOR)
            updated_user.groups.add(director_group)
            updated_user.save()
        return updated_user


class SafeUserOAuth2Manager(SafeDeleteManager, UserOAuth2Manager):
    """Combina SafeDelete + UserOAuth2Manager.

    SafeDelete es primero en MRO para asegurar el filtrado de objetos eliminados.

    """

    pass
