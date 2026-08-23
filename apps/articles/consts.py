from django.utils.translation import gettext_lazy as _

# Base identifiers
APP_NAME = "articles"
MODEL_NAME = "article"
MODULE_VERBOSE_NAME = _("Artículos")
MODEL_VERBOSE_NAME = _("Artículo")
MODEL_VERBOSE_NAME_PLURAL = _("Artículos")

# Navigation URLs (built from APP_NAME)
INDEX_URL = f"{APP_NAME}:index"
CREATE_URL = f"{APP_NAME}:create"
EDIT_URL = f"{APP_NAME}:edit"
DELETE_URL = f"{APP_NAME}:delete"
DETAIL_URL = f"{APP_NAME}:detail"
DASHBOARD_URL = "catalogos:index"
DISABLED_INDEX_URL = f"{APP_NAME}:disabled_index"
ENABLE_URL = f"{APP_NAME}:enable"

# Field labels
TITLE_LABEL = _("Título")
BODY_LABEL = _("Cuerpo")
CATEGORY_LABEL = _("Categoría")
CONTENT_LABEL = _("Contenido")

# Fields shown in views
INDEX_FIELDS = {
    "content": TITLE_LABEL,
}

DETAIL_FIELDS = {
    "content": TITLE_LABEL,
    "body": BODY_LABEL,
    "category": CATEGORY_LABEL,
}

# Filter fields
FILTER_FIELDS = {
    "content__title": {"label": TITLE_LABEL, "placeholder": TITLE_LABEL},
}

# View titles (used in CRUD)
INDEX_TITLE = MODULE_VERBOSE_NAME
CREATE_TITLE = _("Crear artículo")
EDIT_TITLE = _("Editar artículo")
DETAIL_TITLE = _("Detalles del artículo")

# Default ordering
DEFAULT_ORDERING = ["-id"]

# Permissions (built from APP_NAME and MODEL_NAME)
PERMISSION_VIEW = f"{APP_NAME}.view_{MODEL_NAME}"
PERMISSION_ADD = f"{APP_NAME}.add_{MODEL_NAME}"
PERMISSION_CHANGE = f"{APP_NAME}.change_{MODEL_NAME}"
PERMISSION_DELETE = f"{APP_NAME}.delete_{MODEL_NAME}"

# Mensajes
