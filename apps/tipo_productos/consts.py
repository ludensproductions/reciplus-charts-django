from django.utils.translation import gettext_lazy as _

APP_NAME = "tipo_productos"
MODEL_NAME = "tipoproducto"
MODULE_VERBOSE_NAME = _("Tipo productos")

# URLs
INDEX_URL = f"{APP_NAME}:index"
CREATE_URL = f"{APP_NAME}:create"
DELETE_URL = f"{APP_NAME}:delete"
DETAIL_URL = f"{APP_NAME}:detail"
EDIT_URL = f"{APP_NAME}:edit"
RETURN_URL = "catalogos:index"

# Permissions
VIEW_PERMISSION = f"{APP_NAME}.view_{MODEL_NAME}"
ADD_PERMISSION = f"{APP_NAME}.add_{MODEL_NAME}"
CHANGE_PERMISSION = f"{APP_NAME}.change_{MODEL_NAME}"
DELETE_PERMISSION = f"{APP_NAME}.delete_{MODEL_NAME}"

# Titles
INDEX_TITLE = MODULE_VERBOSE_NAME
CREATE_TITLE = _("Crear tipo producto")
EDIT_TITLE = _("Editar tipo producto")
DETAIL_TITLE = _("Detalles del tipo producto")

# Default ordering
DEFAULT_ORDERING = ["-id"]

# Fields
INDEX_FIELDS = {
    "nombre": _("Tipo producto"),
}

DETAIL_FIELDS = {
    "nombre": _("Nombre"),
}
