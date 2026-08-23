from django.core.management.base import BaseCommand
from apps.users.models import User
from django.contrib.auth.hashers import make_password

from apps.groups.consts import UserGroups
from apps.groups.models import CustomGroup as Group

PASSWORD = make_password("12345")

class Command(BaseCommand):
    help = "Seed database with initial data"

    def handle(self, *args, **kwargs):
        seed_admin()
        self.stdout.write(self.style.SUCCESS("Seeded users successfully"))


def seed_admin():
    user, created = User.objects.get_or_create(
        username="admin",
        defaults={
            "email": "admin@admin.com",
            "is_active": True,
            "is_staff": False,
            "is_superuser": False,
            "first_name": "admin",
            "last_name": "admin",
            "celular": "6441234567",
        },
    )

    # if created:

    admin_group = Group.objects.filter(name=UserGroups.ADMINISTRADOR).first()
    user.groups.add(admin_group)
    user.password = PASSWORD
    user.save()
