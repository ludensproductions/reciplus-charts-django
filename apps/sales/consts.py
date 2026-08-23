from django.utils.translation import gettext_lazy as _

APP_NAME = "sales"

INDEX_URL = f"{APP_NAME}:index"
CREATE_URL = f"{APP_NAME}:create"
EDIT_URL = f"{APP_NAME}:edit"
DELETE_URL = f"{APP_NAME}:delete"
DETAIL_URL = f"{APP_NAME}:detail"
DASHBOARD_URL = "dashboard:index"

INDEX_FIELDS = ["folio", "date", "name", "total"]

DETAIL_FIELDS = {
    "name": _("Nombre"),
    "date": _("Fecha"),
    "encargado": _("Encargado"),
    "total": _("Total"),
    "folio": _("Folio"),
}

CHILDREN_ENTITIES = {"movie": {"movie": _("Título"), "quantity": _("Cantidad")}}

TABLE_TITLES = {
    "movie": _("Películas"),
}

MOVIE_SALES_FORMSET_CONFIG = {
    "title": _("Películas"),
    "prefix": "movies",
    "related_name": "sale",
}

# View Titles
INDEX_TITLE = _("Ventas")
CREATE_TITLE = _("Crear venta")
DETAIL_TITLE = _("Detalle de la venta")

# Custom button title
CUSTOM_BUTTON_TITLE = _("Eliminar fila")

# Query field
QUERY_FIELD = "encargado"

# Context
CONTEXT_OBJECT_NAME = "sale"

# Permissions
PERMISSION_VIEW = f"{APP_NAME}.view_sale"
PERMISSION_ADD = f"{APP_NAME}.add_sale"
PERMISSION_DELETE = f"{APP_NAME}.delete_sale"

# Form labels and placeholders
FORM_SALE_NAME_LABEL = _("Asunto")
FORM_SALE_NAME_PLACEHOLDER = _("Asunto")
FORM_MOVIE_LABEL = _("Película")
FORM_QUANTITY_LABEL = _("Cantidad")
FORM_MOVIE_PLACEHOLDER = _("Película")
FORM_QUANTITY_PLACEHOLDER = _("Cantidad")

# Filter labels
SALE_FILTER_FIELDS = {
    "folio": {"label": _("Folio")},
    "name": {"label": _("Asunto")},
    "date": {"label": _("Fecha")},
    "total": {"label": _("Total")},
}

# Error messages
ERROR_DUPLICATE_MOVIE = _("No puedes agregar dos veces la misma película")
ERROR_AT_LEAST_ONE_MOVIE = _("Debe agregar al menos una película")
