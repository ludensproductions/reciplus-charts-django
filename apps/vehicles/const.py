from django.utils.translation import gettext_lazy as _

# App configuration
APP_NAME = "vehicles"
MODEL_NAME = "vehicle"
MODULE_VERBOSE_NAME = _("Vehículos")

# URLs
VEHICLE_INDEX_URL = f"{APP_NAME}:index"
VEHICLE_CREATE_URL = f"{APP_NAME}:create"
VEHICLE_DELETE_URL = f"{APP_NAME}:delete"
VEHICLE_DETAIL_URL = f"{APP_NAME}:detail"
VEHICLE_EDIT_URL = f"{APP_NAME}:edit"
RETURN_URL = "catalogos:index"

# Permissions
PERMISSION_VIEW = f"{APP_NAME}.view_{MODEL_NAME}"
PERMISSION_ADD = f"{APP_NAME}.add_{MODEL_NAME}"
PERMISSION_CHANGE = f"{APP_NAME}.change_{MODEL_NAME}"
PERMISSION_DELETE = f"{APP_NAME}.delete_{MODEL_NAME}"

# Titles
INDEX_TITLE = MODULE_VERBOSE_NAME
CREATE_TITLE = _("Crear vehículo")
EDIT_TITLE = _("Editar vehículo")
DETAIL_TITLE = _("Detalle del vehículo")

# Default ordering
DEFAULT_ORDERING = ["name"]

# Fields
VEHICLE_SHOWN_FIELDS = {
    "name": _("Nombre del vehículo"),
    "brand": _("Marca"),
    "vehicle_type": _("Tipo de vehículo"),
    "license_plate": _("Placa"),
    "year": _("Año"),
    "model": _("Modelo"),
}

VEHICLE_FILTER_FIELDS = {
    "name": {"label": _("Nombre del vehículo")},
    "brand": {"label": _("Marca")},
    "vehicle_type": {"label": _("Tipo de vehículo")},
    "license_plate": {"label": _("Placa")},
}

# Context
CONTEXT_OBJECT_NAME = "vehicle"

# View deleted objects
VIEW_DELETED_OBJECTS = True

# Error messages
ERROR_INVALID_YEAR = _("Ingrese un año válido")
VEHICLE_LABELS = {
    "name": _("Nombre del vehículo"),
    "brand": _("Marca"),
    "vehicle_type": _("Tipo de vehículo"),
    "license_plate": _("Placa"),
    "year": _("Año"),
    "model": _("Modelo"),
}

VEHICLE_PLACEHOLDERS = {
    "name": _("Ingrese el nombre del vehículo"),
    "brand": _("Seleccione la marca"),
    "vehicle_type": _("Seleccione el tipo de vehículo"),
    "license_plate": _("Ingrese la placa"),
    "year": _("Ingrese el año"),
    "model": _("Ingrese el modelo"),
}
