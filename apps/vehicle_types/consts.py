from django.utils.translation import gettext_lazy as _

# App configuration
APP_NAME = "vehicle_types"
MODEL_NAME = "vehicletype"
MODULE_VERBOSE_NAME = _("Tipos de vehículos")

# URLs
VEHICLE_TYPE_INDEX_URL = f"{APP_NAME}:index"
VEHICLE_TYPE_CREATE_URL = f"{APP_NAME}:create"
VEHICLE_TYPE_DELETE_URL = f"{APP_NAME}:delete"
VEHICLE_TYPE_DETAIL_URL = f"{APP_NAME}:detail"
VEHICLE_TYPE_EDIT_URL = f"{APP_NAME}:edit"
RETURN_URL = "catalogos:index"

# Permissions
PERMISSION_VIEW = f"{APP_NAME}.view_{MODEL_NAME}"
PERMISSION_ADD = f"{APP_NAME}.add_{MODEL_NAME}"
PERMISSION_CHANGE = f"{APP_NAME}.change_{MODEL_NAME}"
PERMISSION_DELETE = f"{APP_NAME}.delete_{MODEL_NAME}"

# Titles
INDEX_TITLE = MODULE_VERBOSE_NAME
CREATE_TITLE = _("Crear tipo de vehículo")
EDIT_TITLE = _("Editar tipo de vehículo")
DETAIL_TITLE = _("Detalle de tipo de vehículo")

# Default ordering
DEFAULT_ORDERING = ["name"]

# Fields
VEHICLE_TYPE_SHOWN_FIELDS = {
    "name": _("Tipo de vehículo"),
}

VEHICLE_TYPE_LABELS = {"name": _("Tipo de vehículo")}
VEHICLE_TYPE_PLACEHOLDERS = {"name": _("Tipo de vehículo")}
VEHICLE_TYPE_FILTER_FIELDS = {"name": {"label": _("Tipo de vehículo")}}

# Context
CONTEXT_OBJECT_NAME = "vehicle_type"

# View deleted objects
VIEW_DELETED_OBJECTS = False
