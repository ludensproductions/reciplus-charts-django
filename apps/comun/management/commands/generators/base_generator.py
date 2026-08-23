from django.db.models import BigAutoField, FileField, ImageField, JSONField

from apps.comun.consts import CRUDOperatorsEnum
from apps.comun.models import AbstractModel, AbstractNullableModel

from .consts import DISPLAY_NAME, STR_METHOD


class BaseGenerator:
    """Base class for code generators with common utilities.

    Provides shared functionality for CRUD and API generators including
    field sanitization, display name detection, and code formatting.
    """

    # Lo dejé así separado por si en caso de que ocupe extenderse no estar haciendo uniones y demas cosas.
    FIELDS_EXCLUDED_IN_FORMS_AND_LABELS = (JSONField, BigAutoField)
    ABSTRACT_BASES_MODELS = (AbstractModel, AbstractNullableModel)
    FIELDS_EXCLUDED_IN_INDEX_TABLE = (FileField, ImageField, JSONField, BigAutoField)
    FIELDS_EXCLUDED_IN_FILTERS = (FileField, ImageField, JSONField, BigAutoField)

    def __init__(self, app_label, model):
        self.app_label = app_label
        self.module_name = app_label.title()
        self.model = model
        self.model_name = model.__name__
        self.model_lower = self.model_name.lower()
        # CRUD
        self.module_form = f"{self.model_name}Form"
        self.module_filter = f"{self.model_name}Filter"
        # API
        self.module_controller = f"{self.model_name}Controller"
        self.module_schema_in = f"{self.model_name}SchemaIn"
        self.module_schema_out = f"{self.model_name}SchemaOut"
        self.sanitize_fields()

    def sanitize_fields(self):
        """Excludes fields inherited from AbstractModel and AbstractNullableModel.

        Filters the model's fields to exclude those defined in abstract base
        classes, keeping only concrete fields that are not many-to-many.
        """
        # Nombres de campos de los abstractos
        base_field_names = {
            f.name for base in self.ABSTRACT_BASES_MODELS for f in base._meta.get_fields() if hasattr(f, "name")
        }

        # Filtra los campos del modelo actual
        self.model_fields = [
            f
            for f in self.model._meta.get_fields()
            if getattr(f, "concrete", False)
            and not getattr(f, "many_to_many", False)
            and f.name not in base_field_names
        ]

    @staticmethod
    def _format_code(code: str) -> str:
        """Formats generated code to comply with linting standards.

        Removes trailing whitespace from each line and ensures the file
        ends with exactly one newline character.

        Args:
            code: Raw generated code string.

        Returns:
            Formatted code string compliant with pre-commit hooks.
        """
        # Normalize line endings to LF (\n) only
        code = code.replace("\r\n", "\n").replace("\r", "\n")
        # Remove leading empty lines
        lines = code.lstrip("\n").splitlines()
        # Remove trailing whitespace from each line
        lines = [line.rstrip() for line in lines]
        # Join with newlines and ensure file ends with exactly one newline
        return "\n".join(lines) + "\n"

    @staticmethod
    def _format_fields_list(fields) -> str:
        """Formats a list of field names as a comma-separated string with double quotes.

        Args:
            fields: List of field names (strings) or field objects with .name attribute.

        Returns:
            Formatted string like: '["field1", "field2", "field3"]'
        """
        field_names = [f.name if hasattr(f, "name") else f for f in fields]
        formatted = ", ".join([f'"{field}"' for field in field_names])
        return f"[{formatted}]"

    def _label_const_name(self, field_name: str) -> str:
        """Builds the consts.py constant name for a field's label.

        Args:
            field_name: Name of the model field.

        Returns:
            str: Constant name, e.g. "STUDENT_NAME_LABEL".
        """
        return f"{self.model_name.upper()}_{field_name.upper()}_LABEL"

    def _filter_label_const_name(self, field_name: str) -> str:
        """Builds the consts.py constant name for a field's filter label.

        Args:
            field_name: Name of the model field.

        Returns:
            str: Constant name, e.g. "STUDENT_NAME_FILTER_LABEL".
        """
        return f"{self.model_name.upper()}_{field_name.upper()}_FILTER_LABEL"

    def _filter_fields_const_name(self) -> str:
        """Builds the consts.py constant name for the model's filter fields dict.

        Returns:
            str: Constant name, e.g. "STUDENT_FILTER_FIELDS".
        """
        return f"{self.model_name.upper()}_FILTER_FIELDS"

    def _labelable_fields(self):
        """Returns model fields eligible for a LABEL constant (used by forms)."""
        return [f for f in self.model_fields if not isinstance(f, self.FIELDS_EXCLUDED_IN_FORMS_AND_LABELS)]

    def _own_m2m_fields(self):
        """Returns many-to-many fields declared directly on this model (not on an abstract base).

        These are excluded from `self.model_fields` (see sanitize_fields) because they
        aren't used by forms/filters, but they still need a LABEL constant since the
        model itself typically sets their `verbose_name` from one.
        """
        base_field_names = {
            f.name for base in self.ABSTRACT_BASES_MODELS for f in base._meta.get_fields() if hasattr(f, "name")
        }
        return [
            f
            for f in self.model._meta.get_fields()
            if getattr(f, "concrete", False) and getattr(f, "many_to_many", False) and f.name not in base_field_names
        ]

    def _model_label_fields(self):
        """All fields (concrete + own m2m) on this model eligible for a LABEL constant."""
        return self._labelable_fields() + self._own_m2m_fields()

    def _filterable_fields(self):
        """Returns model fields eligible for a FILTER_LABEL constant (used by filters)."""
        return [
            f
            for f in self.model_fields
            if not isinstance(f, self.FIELDS_EXCLUDED_IN_FILTERS) and f.name != DISPLAY_NAME
        ]

    @staticmethod
    def _label_text_from_field(field) -> str:
        """Best-effort human readable label derived from the field's verbose_name.

        Uses the field's own `verbose_name` (explicitly set by the developer, or
        Django's auto-generated default) as the base text so the translator only
        needs to adjust the generated `_("...")` string when it isn't already in
        Spanish.

        Args:
            field: Model field instance.

        Returns:
            str: Capitalized label text, safe to embed inside a Python string literal.
        """
        text = str(field.verbose_name).replace("_", " ").strip()
        text = text[:1].upper() + text[1:] if text else text
        return text.replace('"', r"\"")

    def get_display_name_field_alias(self):
        """Detecta el campo principal del modelo para usar como alias en display_name.

        Busca un campo con atributo 'display_name' (DisplayNameField) y retorna
        el nombre del campo al que apunta. Si no lo encuentra, retorna '__str__'.

        Returns:
            str: El nombre del campo principal o '__str__' como fallback
        """
        for field in self.model._meta.get_fields():
            if hasattr(field, DISPLAY_NAME) and field.display_name:
                return field.display_name
        return STR_METHOD

    def filters(self, operations):
        """Generates the filters.py file content.

        Args:
            operations: List of CRUD operations to include.

        Returns:
            String with the complete filters.py code or empty string if not needed.
        """
        if CRUDOperatorsEnum.INDEX not in operations and CRUDOperatorsEnum.READ not in operations:
            return ""

        filter_fields_const = self._filter_fields_const_name()

        code = f'''
from apps.comun.filters import AbstractFilter

from .consts import {filter_fields_const}
from .models import {self.model_name}


class {self.module_filter}(AbstractFilter):
    """Filter class for {self.model_name} model with filtering capabilities for index view."""

    class Meta:
        model = {self.model_name}
        fields = list({filter_fields_const}.keys())
        fields_dict = {filter_fields_const}
'''
        return self._format_code(code)

    def consts(self, include_crud=True, include_api=True):
        """Generates the consts.py file with centralized constants.

        Creates constants for URLs, field lists, titles, and permissions following
        the project's standard pattern. All user-facing strings are marked as
        translatable using gettext_lazy.

        Args:
            include_crud: If True, includes CRUD constants (URLs, fields, titles).
            include_api: If True, includes API constants (tags, paths, descriptions).

        Returns:
            String with the complete consts.py file content.
        """
        # Campos para INDEX (sin BigAutoField, ImageField)
        index_fields = [f.name for f in self.model_fields if not isinstance(f, (BigAutoField, ImageField))]

        # Campos para DETAIL (sin BigAutoField)
        detail_fields = [f.name for f in self.model_fields if not isinstance(f, BigAutoField)]

        # Formatear listas en una sola línea
        index_fields_str = self._format_fields_list(index_fields)
        detail_fields_str = self._format_fields_list(detail_fields)

        # Obtener verbose_name del modelo si existe, sino usar nombres por defecto
        verbose_name_plural = getattr(self.model._meta, "verbose_name_plural", self.module_name)
        verbose_name = getattr(self.model._meta, "verbose_name", self.model_lower)
        model_prefix = self.model_name.upper()

        # Sección base (siempre se incluye)
        base_section = f"""from django.utils.text import format_lazy
from django.utils.translation import gettext_lazy as _

# Base identifiers
APP_NAME = "{self.app_label}"
MODEL_NAME = "{self.model_lower}"
MODULE_VERBOSE_NAME = _("{verbose_name_plural}")
MODULE_VERBOSE_NAME_SINGULAR = _("{verbose_name}")

# Model verbose names
{model_prefix}_MODEL_VERBOSE_NAME = MODULE_VERBOSE_NAME_SINGULAR
{model_prefix}_MODEL_VERBOSE_NAME_PLURAL = MODULE_VERBOSE_NAME

# Permissions (built from APP_NAME and MODEL_NAME)
PERMISSIONS = "permissions"
PERMISSION_VIEW = f"{{APP_NAME}}.view_{{MODEL_NAME}}"
PERMISSION_ADD = f"{{APP_NAME}}.add_{{MODEL_NAME}}"
PERMISSION_CHANGE = f"{{APP_NAME}}.change_{{MODEL_NAME}}"
PERMISSION_DELETE = f"{{APP_NAME}}.delete_{{MODEL_NAME}}"
"""

        # Sección CRUD
        crud_section = f"""
# Navigation URLs
INDEX_URL = f"{{APP_NAME}}:index"
CREATE_URL = f"{{APP_NAME}}:create"
EDIT_URL = f"{{APP_NAME}}:edit"
DELETE_URL = f"{{APP_NAME}}:delete"
DETAIL_URL = f"{{APP_NAME}}:detail"
DISABLED_INDEX_URL = f"{{APP_NAME}}:disabled_index"
ENABLE_URL = f"{{APP_NAME}}:enable"
DASHBOARD_URL = "catalogos:index"

# Fields displayed in views
INDEX_FIELDS = {index_fields_str}

DETAIL_FIELDS = {detail_fields_str}

# View titles
INDEX_TITLE = MODULE_VERBOSE_NAME
CREATE_TITLE = format_lazy(_("Crear {{}}"), MODULE_VERBOSE_NAME_SINGULAR)
EDIT_TITLE = format_lazy(_("Editar {{}}"), MODULE_VERBOSE_NAME_SINGULAR)
DETAIL_TITLE = format_lazy(_("Detalles del {{}}"), MODULE_VERBOSE_NAME_SINGULAR)

# Default ordering
DEFAULT_ORDERING = ["name"]
"""

        # Sección API
        api_section = """
# API - Tags and paths
API_TAG = MODULE_VERBOSE_NAME
API_PATH = f"/{APP_NAME}"

# API - Descriptions
API_CREATE_SUMMARY = format_lazy(_("Crear un nuevo {}"), MODULE_VERBOSE_NAME_SINGULAR)
API_CREATE_DESCRIPTION = format_lazy(_("Crear un nuevo {}"), MODULE_VERBOSE_NAME_SINGULAR)
"""

        # Sección de labels por campo (usada por forms.py, filters.py y por el propio modelo
        # para el verbose_name de sus campos, incluyendo relaciones many-to-many propias).
        label_lines = [
            f'{self._label_const_name(field.name)} = _("{self._label_text_from_field(field)}")'
            for field in self._model_label_fields()
        ]
        filterable_fields = self._filterable_fields()
        filter_label_lines = [
            f"{self._filter_label_const_name(field.name)} = {self._label_const_name(field.name)}"
            for field in filterable_fields
        ]
        filter_fields_lines = [
            f'    "{field.name}": {{"label": {self._filter_label_const_name(field.name)}}},'
            for field in filterable_fields
        ]

        labels_section = ""
        if label_lines:
            labels_section += "\n# Model labels\n" + "\n".join(label_lines) + "\n"
        if filter_label_lines:
            labels_section += "\n# Filter labels\n" + "\n".join(filter_label_lines) + "\n"
        # filters.py always imports this constant whenever CRUDOperatorsEnum.INDEX/READ is
        # generated, so it must exist even if no field ended up eligible for filtering.
        filter_fields_body = "\n".join(filter_fields_lines)
        labels_section += f"\n# Filter fields\n{self._filter_fields_const_name()} = {{\n{filter_fields_body}\n}}\n"

        # Construir contenido según los flags
        content = base_section
        if include_crud:
            content += crud_section
        if include_api:
            content += api_section
        content += labels_section

        return self._format_code(content)
