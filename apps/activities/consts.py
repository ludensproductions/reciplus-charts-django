from django.utils.text import format_lazy
from django.utils.translation import gettext_lazy as _

# Base identifiers
APP_NAME = "activities"
MODEL_NAME = "activity"
MODULE_VERBOSE_NAME = _("Actividad")
MODULE_VERBOSE_NAME_PLURAL = _("Actividades")

# Navigation URLs (built from APP_NAME)
INDEX_URL = f"{APP_NAME}:index"
CREATE_URL = f"{APP_NAME}:create"
EDIT_URL = f"{APP_NAME}:edit"
DELETE_URL = f"{APP_NAME}:delete"
DETAIL_URL = f"{APP_NAME}:detail"
DASHBOARD_URL = "catalogos:index"
DISABLED_INDEX_URL = f"{APP_NAME}:disabled_index"
ENABLE_URL = f"{APP_NAME}:enable"

# Filter labels
FILTER_NAME_LABEL = _("Nombre")
FILTER_LOCATION_LABEL = _("Ubicación")
FILTER_ACTIVITY_TYPE_LABEL = _("Tipo de actividad")
FILTER_ACTIVITY_TYPES_PLACEHOLDER = _("Seleccione tipos de actividad")
ACTIVITY_TYPE_WORKSHOP = _("Taller")
ACTIVITY_TYPE_CONFERENCE = _("Conferencia")
ACTIVITY_TYPE_WEBINAR = _("Seminario web")

# Fields shown in views
INDEX_FIELDS = ["name", "location", "activity_type"]

DETAIL_FIELDS = ["name", "location", "activity_type"]

# View titles (used in CRUD)
INDEX_TITLE = MODULE_VERBOSE_NAME_PLURAL
CREATE_TITLE = format_lazy(_("Crear {module_verbose}"), module_verbose=MODULE_VERBOSE_NAME)
EDIT_TITLE = format_lazy(_("Editar {module_verbose}"), module_verbose=MODULE_VERBOSE_NAME)
DETAIL_TITLE = format_lazy(_("Detalles de la {module_verbose}"), module_verbose=MODULE_VERBOSE_NAME)

# Default ordering
DEFAULT_ORDERING = ["name"]

# Context
CONTEXT_OBJECT_NAME = "activity"

# Permissions (built from APP_NAME and MODEL_NAME)
PERMISSION_VIEW = f"{APP_NAME}.view_{MODEL_NAME}"
PERMISSION_ADD = f"{APP_NAME}.add_{MODEL_NAME}"
PERMISSION_CHANGE = f"{APP_NAME}.change_{MODEL_NAME}"
PERMISSION_DELETE = f"{APP_NAME}.delete_{MODEL_NAME}"
