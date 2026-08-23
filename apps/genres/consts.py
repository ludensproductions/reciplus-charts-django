from django.utils.text import format_lazy
from django.utils.translation import gettext_lazy as _

# Base identifiers
APP_NAME = "genres"
MODEL_NAME = "genre"
MODULE_VERBOSE_NAME = _("Género")
MODULE_VERBOSE_NAME_PLURAL = _("Géneros")

# Field labels
FIELD_GENRE_LABEL = MODULE_VERBOSE_NAME
FIELD_DISPLAY_NAME_LABEL = _("Nombre de visualización")

# Permissions (built from APP_NAME and MODEL_NAME)
PERMISSION_VIEW = f"{APP_NAME}.view_{MODEL_NAME}"
PERMISSION_ADD = f"{APP_NAME}.add_{MODEL_NAME}"
PERMISSION_CHANGE = f"{APP_NAME}.change_{MODEL_NAME}"
PERMISSION_DELETE = f"{APP_NAME}.delete_{MODEL_NAME}"
PERMISSION_ENABLE = f"{APP_NAME}.enable_{MODEL_NAME}"


# Navigation URLs (built from APP_NAME)
INDEX_URL = f"{APP_NAME}:index"
CREATE_URL = f"{APP_NAME}:create"
EDIT_URL = f"{APP_NAME}:edit"
DELETE_URL = f"{APP_NAME}:delete"
DETAIL_URL = f"{APP_NAME}:detail"
DASHBOARD_URL = "catalogos:index"
DISABLED_INDEX_URL = f"{APP_NAME}:disabled_index"
ENABLE_URL = f"{APP_NAME}:enable"

# Fields shown in views
INDEX_FIELDS = {
    "display_name": FIELD_DISPLAY_NAME_LABEL,
}

DETAIL_FIELDS = [
    "display_name",
]

# View titles (used in CRUD)
INDEX_TITLE = MODULE_VERBOSE_NAME_PLURAL
CREATE_TITLE = format_lazy(_("Crear {module_verbose}"), module_verbose=MODULE_VERBOSE_NAME)
EDIT_TITLE = format_lazy(_("Editar {module_verbose}"), module_verbose=MODULE_VERBOSE_NAME)
DETAIL_TITLE = format_lazy(_("Detalles del {module_verbose}"), module_verbose=MODULE_VERBOSE_NAME)
DISABLED_INDEX_TITLE = format_lazy(
    _("{module_verbose} deshabilitados"),
    module_verbose=MODULE_VERBOSE_NAME_PLURAL,
)

# Default ordering
DEFAULT_ORDERING = ["-id"]

# API - Tags and paths (built from base constants)
API_TAG = MODULE_VERBOSE_NAME
API_PATH = f"/{APP_NAME}"

# API - Descriptions (built from APP_NAME)
API_CREATE_SUMMARY = format_lazy(
    _("Crear un nuevo {module_verbose}"),
    module_verbose=MODULE_VERBOSE_NAME,
)
API_CREATE_DESCRIPTION = format_lazy(
    _("Crear un nuevo {module_verbose}"),
    module_verbose=MODULE_VERBOSE_NAME,
)

# Error messages
ERROR_LETTERS_BLANKS_ONLY = _("Este campo solo puede contener letras y espacios.")

# Model verbose names
MODEL_GENRE_VERBOSE_NAME = MODULE_VERBOSE_NAME
MODEL_GENRE_VERBOSE_NAME_PLURAL = MODULE_VERBOSE_NAME_PLURAL

# Filter labels
GENRE_FILTER_FIELDS = {
    "display_name": {"label": FIELD_DISPLAY_NAME_LABEL},
}
