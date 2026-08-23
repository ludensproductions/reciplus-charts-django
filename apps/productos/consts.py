from django.utils.translation import gettext_lazy as _

APP_NAME = "productos"

INDEX_URL = f"{APP_NAME}:index"
CREATE_URL = f"{APP_NAME}:create"
EDIT_URL = f"{APP_NAME}:edit"
DELETE_URL = f"{APP_NAME}:delete"
DETAIL_URL = f"{APP_NAME}:detail"
DASHBOARD_URL = "catalogos:index"

INDEX_FIELDS = {
    "producto": _("Producto"),
    "tipo_producto": _("Tipo de producto"),
}

# Model verbose names
PRODUCTO_VERBOSE_NAME = _("Producto")
PRODUCTO_VERBOSE_NAME_PLURAL = _("Productos")

# Model field labels
PRODUCTO_LABEL = _("Producto")
TIPO_PRODUCTO_LABEL = _("Tipo de producto")
FECHA_CREACION_LABEL = _("Fecha de creación")

# Form labels
FORM_PRODUCTO_LABEL = _("Producto")
FORM_TIPO_PRODUCTO_LABEL = _("Tipo de producto")
FORM_FECHA_CREACION_LABEL = _("Fecha de creación")

# Placeholders
FORM_PRODUCTO_PLACEHOLDER = FORM_PRODUCTO_LABEL
FORM_TIPO_PRODUCTO_PLACEHOLDER = _("--------")

# Filter labels
FILTER_PRODUCTO_LABEL = _("Producto")
FILTER_FECHA_CREACION_LABEL = _("Fecha de creación")

DETAIL_FIELDS = [
    "producto",
    "tipo_producto",
    "fecha_creacion",
]

# View titles
INDEX_TITLE = _("Productos")
CREATE_TITLE = _("Crear producto")
EDIT_TITLE = _("Editar producto")
DETAIL_TITLE = _("Detalles del producto")

# Ordering
ORDERING = ["-id"]

# Permissions
PERMISSION_VIEW = f"{APP_NAME}.view_producto"
PERMISSION_ADD = f"{APP_NAME}.add_producto"
PERMISSION_CHANGE = f"{APP_NAME}.change_producto"
PERMISSION_DELETE = f"{APP_NAME}.delete_producto"
