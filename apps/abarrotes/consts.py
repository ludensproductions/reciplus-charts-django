from django.utils.translation import gettext_lazy as _

APP_NAME = "abarrotes"
MODEL_NAME = "abarrotes"

INDEX_URL = f"{APP_NAME}:index"
CREATE_URL = f"{APP_NAME}:create"
EDIT_URL = f"{APP_NAME}:edit"
DELETE_URL = f"{APP_NAME}:delete"
DETAIL_URL = f"{APP_NAME}:detail"
DASHBOARD_URL = "catalogos:index"

PRODUCTO_LABEL = _("Producto")
CANTIDAD_LABEL = _("Cantidad")
FECHA_LABEL = _("Fecha")
ABARROTES_LABEL = _("Abarrotes")
SELECT_EMPTY_PLACEHOLDER = _("--------")

INDEX_FIELDS = {
    "producto": PRODUCTO_LABEL,
    "cantidad": CANTIDAD_LABEL,
    "Fecha": FECHA_LABEL,
}

DETAIL_FIELDS = [
    "producto",
    "cantidad",
    "fecha",
]

# View titles
INDEX_TITLE = ABARROTES_LABEL
CREATE_TITLE = _("Crear inventario de abarrotes")
EDIT_TITLE = _("Editar inventario de abarrotes")
DETAIL_TITLE = _("Detalles del inventario de abarrotes")

# Ordering
ORDERING = ["-id"]

# Permissions
PERMISSION_VIEW = f"{APP_NAME}.view_{MODEL_NAME}"
PERMISSION_ADD = f"{APP_NAME}.add_{MODEL_NAME}"
PERMISSION_CHANGE = f"{APP_NAME}.change_{MODEL_NAME}"
PERMISSION_DELETE = f"{APP_NAME}.delete_{MODEL_NAME}"
