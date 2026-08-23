from django.utils.translation import gettext_lazy as _

APP_NAME = "bodega"
MODEL_NAME = "bodega"

INDEX_URL = f"{APP_NAME}:index"
CREATE_URL = f"{APP_NAME}:create"
EDIT_URL = f"{APP_NAME}:edit"
DELETE_URL = f"{APP_NAME}:delete"
DETAIL_URL = f"{APP_NAME}:detail"
DASHBOARD_URL = "catalogos:index"

INDEX_FIELDS = {
    "bodega": _("Bodega"),
    "producto": _("Producto"),
    "abarrotes": _("Abarrotes"),
    "lote": _("Lote"),
}

DETAIL_FIELDS = list(INDEX_FIELDS.keys())

# View Titles
INDEX_TITLE = _("Bodega")
CREATE_TITLE = _("Crear bodega")
EDIT_TITLE = _("Editar bodega")
DETAIL_TITLE = _("Detalles de la bodega")

# Ordering
ORDERING = ["-id"]

# Permissions
PERMISSION_VIEW = f"{APP_NAME}.view_{MODEL_NAME}"
PERMISSION_ADD = f"{APP_NAME}.add_{MODEL_NAME}"
PERMISSION_CHANGE = f"{APP_NAME}.change_{MODEL_NAME}"
PERMISSION_DELETE = f"{APP_NAME}.delete_{MODEL_NAME}"
