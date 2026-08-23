# your_app/management/commands/makemigrations.py
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from django.apps import apps
from django.core.management.commands.makemigrations import Command as MakeMigrationsCommand

from apps.comun.consts import CRUDOperatorsEnum

from .generators.api_generator import APIGenerator
from .generators.crud_generator import CRUDGenerator

MIN_LINES_TO_PRESERVE = 10  # Número mínimo de líneas para considerar que un archivo tiene contenido significativo

_ALL_OPERATIONS = [
    CRUDOperatorsEnum.INDEX,
    CRUDOperatorsEnum.CREATE,
    CRUDOperatorsEnum.READ,
    CRUDOperatorsEnum.UPDATE,
    CRUDOperatorsEnum.DELETE,
]


@dataclass
class FileToGenerate:
    """Representa un archivo a generar con su contenido y path opcional."""

    filename: str
    content: str
    relative_path: Optional[str] = None  # Path relativo desde base_path, ej: "../" o "subdir/"

    @property
    def path_parts(self) -> tuple[str, str]:
        """Retorna (relative_path, filename) para facilitar el procesamiento."""
        return (self.relative_path or "", self.filename)


class Command(MakeMigrationsCommand):
    """Extended makemigrations command with CRUD and API scaffolding generation.

    Adds --generate-crud and --skip-existing flags to automatically generate
    views, forms, URLs, and API endpoints after creating migrations.
    """

    help = "makemigrations con parámetros extra"

    def add_arguments(self, parser):
        """Adds custom command-line arguments.

        Args:
            parser: ArgumentParser instance to add arguments to.
        """
        super().add_arguments(parser)
        parser.add_argument(
            "--generate-crud",
            action="store_true",
            help="Genera scaffolding CRUD y APIs dependiendo de la configuracion del modelo después de escribir migraciones.",
        )

        parser.add_argument(
            "--for-app",
            type=str,
            default=None,
            help="Especifica una app en particular para generar CRUD/API. Si no se proporciona, genera para todas las apps con migraciones.",
        )

        parser.add_argument(
            "--skip-existing",
            action="store_true",
            help="No sobrescribir archivos existentes al generar CRUD/API (omite archivos ya creados).",
        )

        parser.add_argument(
            "--overwrite",
            action="store_true",
            help="Sobrescribe TODOS los archivos existentes sin restricciones. Solo válido junto con --for-app. Solicita confirmación antes de proceder.",
        )

    def handle(self, *app_labels, **options):
        """Handles the command execution.

        Args:
            *app_labels: Variable length app label arguments.
            **options: Command options including generate_crud and skip_existing.

        Returns:
            Result from parent command's handle method.
        """
        self._generate_crud = bool(options.get("generate_crud"))
        self._skip_existing = bool(options.get("skip_existing"))
        self._for_app = options.get("for_app")
        self._overwrite = bool(options.get("overwrite"))

        if self._overwrite and not self._for_app:
            raise SystemExit(self.style.ERROR("Error: --overwrite solo puede usarse junto con --for-app."))

        return super().handle(*app_labels, **options)

    def write_migration_files(self, changes):
        """Writes migration files and optionally generates CRUD/API scaffolding.

        After writing migrations, checks model Config for crud_operations/api_operations
        (or infers them for models whose db_table starts with "cat_") and generates the
        corresponding files based on those operations.

        Args:
            changes: Dict mapping app_label to list of Migration objects.

        Returns:
            Result from parent command's write_migration_files method.
        """
        result = super().write_migration_files(changes)

        migrated_apps = [label for label, migs in changes.items() if migs]
        if migrated_apps:
            self.stdout.write(self.style.SUCCESS(f"Apps con migraciones nuevas: {', '.join(migrated_apps)}"))
        else:
            self.stdout.write(self.style.WARNING("No hubo migraciones nuevas."))

        if getattr(self, "_generate_crud", False) and migrated_apps:
            # Filtrar por app específica si se proporcionó --for-app
            target_app = getattr(self, "_for_app", None)
            if target_app:
                if target_app in migrated_apps:
                    apps_to_process = [target_app]
                    self.stdout.write(self.style.SUCCESS(f"Generando solo para la app especificada: {target_app}"))
                    if getattr(self, "_overwrite", False):
                        self.stdout.write(
                            self.style.WARNING(
                                f"\n¡ADVERTENCIA! Se sobrescribirán TODOS los archivos existentes de la app '{target_app}'."
                                f"\nEsta acción no se puede deshacer."
                            )
                        )
                        confirm = input("¿Deseas continuar? [s/N]: ").strip().lower()
                        if confirm not in ("s", "si", "sí", "y", "yes"):
                            self.stdout.write(self.style.WARNING("Operación cancelada por el usuario."))
                            return result
                else:
                    self.stdout.write(
                        self.style.WARNING(
                            f"Advertencia: La app '{target_app}' no tiene migraciones nuevas o no existe."
                        )
                    )
                    apps_to_process = []
            else:
                apps_to_process = migrated_apps

            for app_label in apps_to_process:
                for model in apps.all_models[app_label].values():
                    if "historical" in model.__name__.lower():
                        continue

                    db_table = getattr(model._meta, "db_table", "")
                    is_catalog = db_table.startswith("cat_")
                    config = getattr(model, "Config", None)

                    if config:
                        # An explicit Config always wins, even on a `cat_`-prefixed model,
                        # so catalogs can still limit what gets generated. crud_operations
                        # and api_operations must each be declared explicitly; there is no
                        # shared "operations" fallback.
                        crud_operations = getattr(config, "crud_operations", None)
                        api_operations = getattr(config, "api_operations", None)
                    elif is_catalog:
                        # No Config declared: `cat_` prefix defaults to every operation.
                        crud_operations = list(_ALL_OPERATIONS)
                        api_operations = list(_ALL_OPERATIONS)
                    else:
                        crud_operations = None
                        api_operations = None

                    crud = bool(crud_operations)
                    api = bool(api_operations)

                    if not crud and not api:
                        continue

                    base_path = Path(apps.get_app_config(app_label).path)
                    model_name_lower = model.__name__.lower()

                    if crud:
                        crud_generator = CRUDGenerator(app_label, model)
                        files_to_generate = [
                            FileToGenerate("views.py", crud_generator.views(crud_operations)),
                            FileToGenerate("urls.py", crud_generator.urls()),
                            FileToGenerate("forms.py", crud_generator.forms()),
                            FileToGenerate("filters.py", crud_generator.filters(crud_operations)),
                            FileToGenerate("consts.py", crud_generator.consts(include_crud=True, include_api=api)),
                        ]
                        self._generate_files(app_label, base_path, files_to_generate, "CRUD", model_name_lower)

                    if api:
                        api_generator = APIGenerator(app_label, model)
                        files_to_generate = [
                            FileToGenerate("controller.py", api_generator.controller(api_operations)),
                            FileToGenerate("schema.py", api_generator.schemas()),
                            FileToGenerate("service.py", api_generator.service()),
                            FileToGenerate("filters.py", api_generator.filters(api_operations), "../"),
                        ]
                        # Solo generar consts.py si no se generó con CRUD
                        if not crud:
                            files_to_generate.append(
                                FileToGenerate(
                                    "consts.py", api_generator.consts(include_crud=False, include_api=True), "../"
                                )
                            )
                        self._generate_files(app_label, base_path / "api", files_to_generate, "API", model_name_lower)

        return result

    def _generate_files(self, app_label, base_path, files_to_generate, gen_type, model_name):
        """Generates files and displays progress messages.

        Args:
            app_label: Name of the Django app.
            base_path: Base directory path for file generation.
            files_to_generate: List of FileToGenerate instances.
            gen_type: Type of generation ("CRUD" or "API").
            model_name: Name of the model being processed.
        """
        self.stdout.write(self.style.SUCCESS(f"Generando {gen_type} para {app_label}... Ubicación: {base_path}"))
        overwrite = getattr(self, "_overwrite", False)
        skip_existing = self._skip_existing if not overwrite else False
        self.make_and_write_files(base_path, files_to_generate, skip_existing=skip_existing, force_overwrite=overwrite)
        self.stdout.write(self.style.SUCCESS(f"{gen_type} generado para {model_name}."))

    def make_and_write_files(self, base_path, files_to_generate, *, skip_existing=False, force_overwrite=False):
        """Creates and writes files to disk with smart overwrite handling.

        Creates new files or overwrites existing ones based on skip_existing flag
        and file size heuristics (files under MIN_LINES_TO_PRESERVE are always overwritten).
        If force_overwrite is True, all existing files are unconditionally overwritten.

        Args:
            base_path: Base Path object for file generation.
            files_to_generate: List of FileToGenerate instances.
            skip_existing: If True, preserves existing files over MIN_LINES_TO_PRESERVE lines.
            force_overwrite: If True, overwrites all existing files without any checks.
        """
        base_path = Path(base_path)
        for file_instance in files_to_generate:
            # Si relative_path está definido, usarlo para modificar la ubicación
            if file_instance.relative_path is not None:
                target_path = base_path / file_instance.relative_path / file_instance.filename
            else:
                target_path = base_path / file_instance.filename

            # Si el archivo no existe, lo crea directamente
            if not target_path.exists():
                target_path.parent.mkdir(parents=True, exist_ok=True)
                target_path.write_text(file_instance.content, encoding="utf-8", newline="\n")
                self.stdout.write(self.style.SUCCESS(f"Archivo creado: {target_path}"))
                continue

            # Si force_overwrite está activo, sobrescribe sin restricciones
            if force_overwrite:
                target_path.write_text(file_instance.content, encoding="utf-8", newline="\n")
                self.stdout.write(self.style.SUCCESS(f"Archivo sobreescrito (forzado): {target_path}"))
                continue

            # Si el archivo existe y la opción skip_existing está activa
            if skip_existing:
                # Contar líneas del archivo existente
                try:
                    line_count = len(target_path.read_text(encoding="utf-8").splitlines())
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f"Error leyendo {target_path}: {e}"))
                    self.stdout.write(
                        self.style.ERROR("Se omite este archivo para evitar sobrescribir datos por error.")
                    )
                    continue

                # Si tiene menos de 10 líneas, se sobrescribe
                if line_count < MIN_LINES_TO_PRESERVE:
                    target_path.write_text(file_instance.content, encoding="utf-8", newline="\n")
                    self.stdout.write(
                        self.style.WARNING(f"Archivo sobrescrito (solo {line_count} líneas): {target_path}")
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f"Omitido (archivo existente con {line_count} líneas): {target_path}")
                    )
                continue

            # Si skip_existing no está activo, siempre sobrescribe
            target_path.write_text(file_instance.content, encoding="utf-8", newline="\n")
            self.stdout.write(self.style.SUCCESS(f"Archivo sobrescrito: {target_path}"))
