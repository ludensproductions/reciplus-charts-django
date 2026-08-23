from django.utils.translation import gettext_lazy as _

# Base identifiers
APP_NAME = "music_tags"
MODEL_NAME = "musictags"
MODULE_VERBOSE_NAME = _("Etiquetas musicales")

# Navigation URLs (built from APP_NAME)
INDEX_URL = f"{APP_NAME}:index"
CREATE_URL = f"{APP_NAME}:create"
EDIT_URL = f"{APP_NAME}:edit"
DELETE_URL = f"{APP_NAME}:delete"
DETAIL_URL = f"{APP_NAME}:detail"
DASHBOARD_URL = "catalogos:index"

# Fields shown in views
INDEX_FIELDS = {
    "tag": _("Etiqueta"),
}

# Filter fields
FILTER_FIELDS = {
    "tag": {"label": _("Etiqueta"), "placeholder": _("Etiqueta")},
}

# View titles (used in CRUD)
INDEX_TITLE = MODULE_VERBOSE_NAME
CREATE_TITLE = _("Crear etiqueta musical")
EDIT_TITLE = _("Editar etiqueta musical")

# Default ordering
DEFAULT_ORDERING = ["-id"]

# Permissions (built from APP_NAME and MODEL_NAME)
PERMISSION_VIEW = f"{APP_NAME}.view_{MODEL_NAME}"
PERMISSION_ADD = f"{APP_NAME}.add_{MODEL_NAME}"
PERMISSION_CHANGE = f"{APP_NAME}.change_{MODEL_NAME}"
PERMISSION_DELETE = f"{APP_NAME}.delete_{MODEL_NAME}"

# Model verbose names
MODEL_MUSIC_TAG_VERBOSE_NAME = _("Etiqueta musical")
MODEL_MUSIC_TAG_VERBOSE_NAME_PLURAL = _("Etiquetas musicales")

# Field labels
FIELD_TAG_LABEL = _("Etiqueta")

# Form labels and placeholders
FORM_TAG_LABEL = _("Etiqueta")
FORM_TAG_PLACEHOLDER = _("Etiqueta")

# Filter labels
MUSIC_TAGS_FILTER_FIELDS = {
    "tag": {"label": _("Etiqueta")},
}
