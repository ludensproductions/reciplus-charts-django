from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.utils.text import format_lazy
from django.utils.translation import gettext_lazy as _

from apps.catalogos.models import CatalogosModule
from apps.groups.consts import UserGroups
from apps.groups.models import CustomGroup as Group

catalogos_content_type = ContentType.objects.get_for_model(CatalogosModule)


class Command(BaseCommand):
    """Django management command to seed user groups and assign permissions."""

    help = "Seed permissions"

    def handle(self, *args, **kwargs):
        """Seed user groups and assign admin permissions."""
        seed_groups(self)
        set_admin_permissions()

        self.stdout.write(str(_("Finalizo la carga de datos.")))


def seed_groups(self):
    """Create missing user groups defined in UserGroups."""
    group_names = [
        value for attr, value in vars(UserGroups).items() if not attr.startswith("__") and isinstance(value, str)
    ]

    for name in group_names:
        group, created = Group.objects.get_or_create(name=name, defaults={"display_name": name})
        status = _("creado") if created else _("ya existe")
        self.stdout.write(str(format_lazy(_("Grupo {name} {status}"), name=name, status=status)))


def set_admin_permissions():
    """Assign all permissions to the admin group."""
    admin_group = Group.objects.filter(name=UserGroups.ADMINISTRADOR).first()
    permission = Permission.objects.all()
    admin_group.permissions.clear()
    admin_group.permissions.set(permission)
    admin_group.save()
