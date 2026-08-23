import time

from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Seed database with initial data"

    def handle(self, *args, **kwargs):
        start = time.time()

        call_command("seed_permissions")
        self.stdout.write(f"seed_permissions: {time.time() - start}s")
        
        call_command("seed_admin")
        self.stdout.write(f"seed_admin: {time.time() - start}s")

        call_command("seed_paises")
        self.stdout.write(f"seed_paises: {time.time() - start}s")

        call_command("seed_codigos_postales")
        self.stdout.write(f"seed_codigos_postales: {time.time() - start}s")

        self.stdout.write(self.style.SUCCESS("Seeded all tables successfully"))

        # 30777
