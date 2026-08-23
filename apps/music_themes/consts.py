from django.utils.translation import gettext_lazy as _

# Base identifiers
APP_NAME = "music_themes"
MODEL_NAME = "musicthemes"
MODULE_VERBOSE_NAME = _("Temas musicales")

# Navigation URLs (built from APP_NAME)
INDEX_URL = f"{APP_NAME}:index"
CREATE_URL = f"{APP_NAME}:create"
EDIT_URL = f"{APP_NAME}:edit"
DELETE_URL = f"{APP_NAME}:delete"
DETAIL_URL = f"{APP_NAME}:detail"
DASHBOARD_URL = "catalogos:index"

# Fields shown in views
INDEX_FIELDS = {
    "theme": _("Tema"),
}

# Filter fields
FILTER_FIELDS = {
    "theme": {"label": _("Tema"), "placeholder": _("Tema")},
}

# View titles (used in CRUD)
INDEX_TITLE = MODULE_VERBOSE_NAME
CREATE_TITLE = _("Crear tema musical")
EDIT_TITLE = _("Editar tema musical")

# Default ordering
DEFAULT_ORDERING = ["-id"]

# Permissions (built from APP_NAME and MODEL_NAME)
PERMISSION_VIEW = f"{APP_NAME}.view_{MODEL_NAME}"
PERMISSION_ADD = f"{APP_NAME}.add_{MODEL_NAME}"
PERMISSION_CHANGE = f"{APP_NAME}.change_{MODEL_NAME}"
PERMISSION_DELETE = f"{APP_NAME}.delete_{MODEL_NAME}"

# Model verbose names
MODEL_MUSIC_THEME_VERBOSE_NAME = _("Tema musical")
MODEL_MUSIC_THEME_VERBOSE_NAME_PLURAL = _("Temas musicales")

# Field labels
FIELD_THEME_LABEL = _("Tema")

# Form labels and placeholders
FORM_THEME_LABEL = _("Tema")
FORM_THEME_PLACEHOLDER = _("Tema")

# Filter labels
MUSIC_THEMES_FILTER_FIELDS = {
    "theme": {"label": _("Tema")},
}
