from django.utils.text import format_lazy
from django.utils.translation import gettext_lazy as _

# Base identifiers
APP_NAME = "categories"
MODEL_NAME = "category"
MODULE_VERBOSE_NAME = _("Categoría")
MODULE_VERBOSE_NAME_PLURAL = _("Categorías")

# Navigation URLs (built from APP_NAME)
INDEX_URL = f"{APP_NAME}:index"
CREATE_URL = f"{APP_NAME}:create"
EDIT_URL = f"{APP_NAME}:edit"
DELETE_URL = f"{APP_NAME}:delete"
DETAIL_URL = f"{APP_NAME}:detail"
DASHBOARD_URL = "catalogos:index"
DISABLED_INDEX_URL = f"{APP_NAME}:disabled_index"
ENABLE_URL = f"{APP_NAME}:enable"

# Fields displayed in views
INDEX_FIELDS = {
    "name": _("Nombre"),
}

# Filter fields
FILTER_FIELDS = {
    "name": {"label": _("Nombre"), "placeholder": _("Nombre")},
}

# View titles (used in CRUD)
INDEX_TITLE = MODULE_VERBOSE_NAME_PLURAL
CREATE_TITLE = format_lazy(_("Crear {module_verbose}"), module_verbose=MODULE_VERBOSE_NAME)
EDIT_TITLE = format_lazy(_("Editar {module_verbose}"), module_verbose=MODULE_VERBOSE_NAME)
DETAIL_TITLE = format_lazy(_("Detalles de la {module_verbose}"), module_verbose=MODULE_VERBOSE_NAME)
DISABLED_INDEX_TITLE = format_lazy(_("{module_verbose} deshabilitadas"), module_verbose=MODULE_VERBOSE_NAME_PLURAL)

# Default ordering
DEFAULT_ORDERING = ["-id"]

# Permissions (built from APP_NAME and MODEL_NAME)
PERMISSION_VIEW = f"{APP_NAME}.view_{MODEL_NAME}"
PERMISSION_ADD = f"{APP_NAME}.add_{MODEL_NAME}"
PERMISSION_CHANGE = f"{APP_NAME}.change_{MODEL_NAME}"
PERMISSION_DELETE = f"{APP_NAME}.delete_{MODEL_NAME}"
