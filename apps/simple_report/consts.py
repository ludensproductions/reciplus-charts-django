from django.utils.text import format_lazy
from django.utils.translation import gettext_lazy as _

# Identificadores base
APP_NAME = "simple_report"
MODEL_NAME = "simple report"
MODULE_VERBOSE_NAME = _("Simple Report")

# Permisos (construidos a partir de APP_NAME y MODEL_NAME)
PERMISSION_VIEW = f"{APP_NAME}.view_{MODEL_NAME}"
PERMISSION_ADD = f"{APP_NAME}.add_{MODEL_NAME}"
PERMISSION_CHANGE = f"{APP_NAME}.change_{MODEL_NAME}"
PERMISSION_DELETE = f"{APP_NAME}.delete_{MODEL_NAME}"

# URLs de navegación (construidas a partir de APP_NAME)
INDEX_URL = f"{APP_NAME}:index"
CREATE_URL = f"{APP_NAME}:create"
EDIT_URL = f"{APP_NAME}:edit"
DELETE_URL = f"{APP_NAME}:delete"
DETAIL_URL = f"{APP_NAME}:detail"
DASHBOARD_URL = "catalogos:index"
DISABLED_INDEX_URL = f"{APP_NAME}:disabled_index"
ENABLE_URL = f"{APP_NAME}:enable"

# Campos mostrados en vistas
INDEX_FIELDS = ["title", "notes"]

DETAIL_FIELDS = ["title", "notes"]

CHILDREN_ENTITIES = {"files": {"get_file_url": _("Archivos")}}

TABLE_TITLES = {
    "files": _("Archivos"),
}

# Títulos de vistas (usados en CRUD)
INDEX_TITLE = MODULE_VERBOSE_NAME
CREATE_TITLE = format_lazy(_("Crear {module_verbose}"), module_verbose=MODULE_VERBOSE_NAME)
EDIT_TITLE = format_lazy(_("Editar {module_verbose}"), module_verbose=MODULE_VERBOSE_NAME)
DETAIL_TITLE = format_lazy(_("Detalles de {module_verbose}"), module_verbose=MODULE_VERBOSE_NAME)

# Ordenamiento por defecto
DEFAULT_ORDERING = ["-id"]

MODEL_SIMPLE_REPORT_NAME = _("Reporte simple")
MODEL_SIMPLE_REPORT_NAME_PLURAL = _("Reportes simples")
MODEL_SIMPLE_REPORT_FILE_NAME = _("Archivo de reporte")
MODEL_SIMPLE_REPORT_FILE_NAME_PLURAL = _("Archivos de reporte")
FIELD_TITLE_LABEL = _("Titulo")
FIELD_NOTES_LABEL = _("Notas")
FIELD_REPORT_LABEL = _("Reporte")
FIELD_FILE_LABEL = _("Archivo")
FIELD_FILES_LABEL = _("Archivos")
FIELD_FILES_PLACEHOLDER = _("Seleccionar archivos")
FIELD_TITLE_PLACEHOLDER = _("Titulo")
FIELD_NOTES_PLACEHOLDER = _("Notas")
SIMPLE_REPORT_FILTER_FIELDS = {
    "title": {"label": FIELD_TITLE_LABEL},
    "notes": {"label": FIELD_NOTES_LABEL},
}
