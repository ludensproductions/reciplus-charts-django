import os
from pathlib import Path

from django.apps import apps as django_apps
from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Comando para eliminar archivos de migración de las apps del proyecto.

    Este comando elimina todos los archivos de migración (excepto __init__.py)
    de las aplicaciones locales del proyecto. Está diseñado únicamente para
    uso en desarrollo cuando es necesario reiniciar las migraciones.
    """

    help = "Borra migraciones de TUS apps (excepto __init__.py). Usa --dry-run para solo listar."

    def add_arguments(self, parser):
        """Agrega argumentos personalizados al comando.

        Args:
            parser: ArgumentParser de Django para agregar argumentos.
        """
        parser.add_argument("--dry-run", action="store_true", help="Solo mostrar; no borrar.")
        parser.add_argument("--apps", nargs="*", help="Limitar a estas apps (labels).")

    def handle(self, *args, **opts):
        """Ejecuta la lógica principal del comando.

        Args:
            *args: Argumentos posicionales (no utilizados).
            **opts: Opciones del comando (dry_run, apps).

        Returns:
            None
        """
        dry = opts["dry_run"]
        only = set(opts["apps"] or [])
        base_dir = Path(settings.BASE_DIR).resolve()
        venv_dir = Path(os.environ.get("VIRTUAL_ENV", "")).resolve() if os.environ.get("VIRTUAL_ENV") else None

        to_delete = []
        for cfg in django_apps.get_app_configs():
            label = cfg.label
            if only and label not in only:
                continue

            app_path = Path(cfg.path).resolve()
            if "site-packages" in str(app_path):
                continue
            if venv_dir and venv_dir in app_path.parents:
                continue
            if base_dir not in app_path.parents and app_path != base_dir:
                continue

            migs = app_path / "migrations"
            if not migs.exists():
                continue

            for f in migs.glob("*.py"):
                if f.name == "__init__.py":
                    continue
                to_delete.append(f)

        if not to_delete:
            self.stdout.write(self.style.WARNING("No hay archivos de migración para borrar."))
            return

        if dry:
            for f in to_delete:
                self.stdout.write(f"[dry-run] Borrar: {f}")
            self.stdout.write(f"Dry-run terminado. {len(to_delete)} archivos encontrados.")
            return

        self.stdout.write("")
        self.stdout.write(self.style.ERROR("=" * 70))
        self.stdout.write(self.style.ERROR("  ADVERTENCIA: Este comando es destructivo"))
        self.stdout.write(self.style.ERROR("=" * 70))
        self.stdout.write("")
        self.stdout.write(self.style.WARNING("Este comando NO debe ejecutarse en:"))
        self.stdout.write("  - Producción (PROD)")
        self.stdout.write("  - UAT / Staging")
        self.stdout.write("")
        self.stdout.write(self.style.WARNING("En Desarrollo (DEV) únicamente ejecutar si:"))
        self.stdout.write("  - Es extremadamente necesario")
        self.stdout.write("  - Hay autorización explícita")
        self.stdout.write("")
        self.stdout.write(self.style.WARNING("Riesgos potenciales:"))
        self.stdout.write("  - Comportamientos inesperados")
        self.stdout.write("  - Inconsistencias en la base de datos")
        self.stdout.write("  - Ruptura de funcionalidades existentes")
        self.stdout.write("  - Necesidad de validación y corrección manual posterior")
        self.stdout.write("")
        self.stdout.write(f"Se eliminarán {len(to_delete)} archivos de migración.")
        self.stdout.write("")

        confirm = input("¿Está seguro de continuar? [s/n]: ").strip().lower()
        if confirm not in ("s", "si", "sí", "y", "yes"):
            self.stdout.write(self.style.WARNING("Operación cancelada."))
            return

        deleted = []
        for f in to_delete:
            f.unlink(missing_ok=True)
            deleted.append(str(f))

        self.stdout.write(self.style.SUCCESS(f"\nBorrados {len(deleted)} archivos de migración."))
