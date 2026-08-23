from django.utils.translation import gettext_lazy as _

APP_NAME = "movies"

# URL names
INDEX_URL = f"{APP_NAME}:index"
CREATE_URL = f"{APP_NAME}:create"
EDIT_URL = f"{APP_NAME}:edit"
DELETE_URL = f"{APP_NAME}:delete"
DETAIL_URL = f"{APP_NAME}:detail"
DASHBOARD_URL = "catalogos:index"

# Field definitions
INDEX_FIELDS = {
    "title": _("Título"),
    "year": _("Año"),
    "genre": _("Género"),
    "sales_count": _("Total de ventas"),
}

DETAIL_FIELDS = INDEX_FIELDS | {
    "plot": _("Sinopsis"),
    "price": _("Precio"),
}

SPECIAL_ATTRIBUTES = {
    "title": {
        "max-length": 35,
    }
}

DISABLE_EDIT_FIELDS = ["price"]

# View titles
INDEX_TITLE = _("Películas")
CREATE_TITLE = _("Crear película")
EDIT_TITLE = _("Editar película")
DETAIL_TITLE = _("Detalles de la película")

# Ordering
ORDERING = ["-id"]

# Context
CONTEXT_OBJECT_NAME = "movie"

# Permissions
PERMISSION_VIEW = f"{APP_NAME}.view_movie"
PERMISSION_ADD = f"{APP_NAME}.add_movie"
PERMISSION_CHANGE = f"{APP_NAME}.change_movie"
PERMISSION_DELETE = f"{APP_NAME}.delete_movie"

# Model verbose names
MODEL_MOVIE_VERBOSE_NAME = _("Película")
MODEL_MOVIE_VERBOSE_NAME_PLURAL = _("Películas")
MODEL_MOVIE_SALES_VERBOSE_NAME = _("Venta de película")
MODEL_MOVIE_SALES_VERBOSE_NAME_PLURAL = _("Ventas de películas")

# Field labels
FIELD_TITLE_LABEL = _("Título")
FIELD_YEAR_LABEL = _("Año")
FIELD_GENRE_LABEL = _("Género")
FIELD_PRICE_LABEL = _("Precio")
FIELD_PLOT_LABEL = _("Sinopsis")
FIELD_SALE_LABEL = _("Venta")
FIELD_MOVIE_LABEL = _("Película")
FIELD_QUANTITY_LABEL = _("Cantidad")

# Form labels and placeholders
FORM_TITLE_LABEL = _("Título")
FORM_YEAR_LABEL = _("Año")
FORM_GENRE_LABEL = _("Género")
FORM_PRICE_LABEL = _("Precio")
FORM_PLOT_LABEL = _("Sinopsis")
FORM_TITLE_PLACEHOLDER = _("Título de la película")
FORM_YEAR_PLACEHOLDER = _("Año")
FORM_PRICE_PLACEHOLDER = _("Precio")
FORM_PLOT_PLACEHOLDER = _("Sinopsis de la película")

# Filter labels
MOVIES_FILTER_FIELDS = {
    "title": {"label": _("Título")},
    "year": {"label": _("Año")},
    "genre": {"label": _("Género")},
}

ERROR_MOVIE_YEAR_MIN = _("No mames, la primera película salió en 1895, ponte verga")
ERROR_MOVIE_PRICE_NEGATIVE = _("No mames, el precio no puede ser negativo")
