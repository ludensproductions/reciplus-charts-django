"""Constants for the facturas app."""

from django.utils.translation import gettext_lazy as _

# Base identifiers
APP_NAME = "facturas"
MODEL_NAME = "factura"
MODULE_VERBOSE_NAME = _("Facturas")
MODEL_DISPLAY_NAME = _("factura")

# Permissions (built from APP_NAME and MODEL_NAME)
PERMISSION_VIEW = f"{APP_NAME}.view_{MODEL_NAME}"
PERMISSION_ADD = f"{APP_NAME}.add_{MODEL_NAME}"
PERMISSION_CHANGE = f"{APP_NAME}.change_{MODEL_NAME}"
PERMISSION_DELETE = f"{APP_NAME}.delete_{MODEL_NAME}"

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
COMMON_FIELDS = ["codigo_factura", "fecha", "cliente", "total"]
INDEX_FIELDS = COMMON_FIELDS
DETAIL_FIELDS = COMMON_FIELDS

# View titles (used in CRUD)
INDEX_TITLE = MODULE_VERBOSE_NAME
CREATE_TITLE = _("Crear factura")
EDIT_TITLE = _("Editar factura")
DETAIL_TITLE = _("Detalles de factura")

# Default ordering
DEFAULT_ORDERING = ["-id"]

# Error messages
ERROR_DUPLICATE_PRODUCT = _("No puedes agregar dos veces el mismo producto.")

# Formset configuration
FACTURA_DETAIL_FORMSET_PREFIX = "detalle"
FACTURA_DETAIL_TITLE = DETAIL_TITLE
FACTURA_DETAIL_FORMSET_TITLE = FACTURA_DETAIL_TITLE
FACTURA_DETAIL_RELATED_NAME = "factura"

# Model verbose names
FACTURA_VERBOSE_NAME = _("Factura")
FACTURA_VERBOSE_NAME_PLURAL = MODULE_VERBOSE_NAME
DETALLE_FACTURA_VERBOSE_NAME = _("Detalle de factura")
DETALLE_FACTURA_VERBOSE_NAME_PLURAL = _("Detalles de factura")

# Field labels
CODIGO_FACTURA_LABEL = _("Código de factura")
FECHA_LABEL = _("Fecha")
CLIENTE_LABEL = _("Cliente")
TOTAL_LABEL = _("Total")
FACTURA_LABEL = FACTURA_VERBOSE_NAME
PRODUCTO_LABEL = _("Producto")
CANTIDAD_LABEL = _("Cantidad")
PRECIO_UNITARIO_LABEL = _("Precio unitario")
SUBTOTAL_LABEL = _("Subtotal")
CODIGO_DETALLE_LABEL = _("Código de detalle")

# Filter labels
FILTER_CODIGO_FACTURA_LABEL = _("Código factura")
FILTER_FECHA_LABEL = FECHA_LABEL
FILTER_CLIENTE_LABEL = CLIENTE_LABEL
FILTER_TOTAL_LABEL = TOTAL_LABEL

# Display formats
FACTURA_DISPLAY = _("Factura {code}")
DETALLE_FACTURA_DISPLAY = _("Detalle {code}")

# Detail fields for DetallesFactura
PRECIO_UNITARIO_TABLE_LABEL = _("Precio unitario")

TABLE_DETAIL_FIELDS = {
    "detalles": {
        "producto": PRODUCTO_LABEL,
        "cantidad": CANTIDAD_LABEL,
        "precio_unitario": PRECIO_UNITARIO_TABLE_LABEL,
        "subtotal": SUBTOTAL_LABEL,
    }
}
TABLE_TITLES = {
    "detalles": FACTURA_DETAIL_TITLE,
}

# Placeholders
CLIENTE_PLACEHOLDER = CLIENTE_LABEL
PRODUCTO_PLACEHOLDER = PRODUCTO_LABEL
CANTIDAD_PLACEHOLDER = CANTIDAD_LABEL
PRECIO_UNITARIO_PLACEHOLDER = PRECIO_UNITARIO_LABEL
