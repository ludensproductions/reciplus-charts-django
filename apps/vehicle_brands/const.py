from django.utils.translation import gettext_lazy as _

# App configuration
APP_NAME = "vehicle_brands"
MODEL_NAME = "vehiclebrand"
MODULE_VERBOSE_NAME = _("Marcas de vehículos")

# URLs
VEHICLE_BRAND_INDEX_URL = f"{APP_NAME}:index"
VEHICLE_BRAND_CREATE_URL = f"{APP_NAME}:create"
VEHICLE_BRAND_DELETE_URL = f"{APP_NAME}:delete"
VEHICLE_BRAND_DETAIL_URL = f"{APP_NAME}:detail"
VEHICLE_BRAND_EDIT_URL = f"{APP_NAME}:edit"
RETURN_URL = "catalogos:index"

# Permissions
PERMISSION_VIEW = f"{APP_NAME}.view_{MODEL_NAME}"
PERMISSION_ADD = f"{APP_NAME}.add_{MODEL_NAME}"
PERMISSION_CHANGE = f"{APP_NAME}.change_{MODEL_NAME}"
PERMISSION_DELETE = f"{APP_NAME}.delete_{MODEL_NAME}"

# Titles
INDEX_TITLE = MODULE_VERBOSE_NAME
CREATE_TITLE = _("Crear Marca de vehículo")
EDIT_TITLE = _("Editar Marca de vehículo")
DETAIL_TITLE = _("Detalle de Marca de vehículo")

# Default ordering
DEFAULT_ORDERING = ["name"]

# Fields
VEHICLE_BRAND_SHOWN_FIELDS = {
    "name": _("Marca"),
}

# Context
CONTEXT_OBJECT_NAME = "vehicle_brand"
