from django.utils.translation import gettext_lazy as _

# Base identifiers
APP_NAME = "music_genres"
MODEL_NAME = "musicgenres"
MODULE_VERBOSE_NAME = _("Géneros musicales")

# Navigation URLs (built from APP_NAME)
INDEX_URL = f"{APP_NAME}:index"
CREATE_URL = f"{APP_NAME}:create"
EDIT_URL = f"{APP_NAME}:edit"
DELETE_URL = f"{APP_NAME}:delete"
DETAIL_URL = f"{APP_NAME}:detail"
DASHBOARD_URL = "catalogos:index"

# Fields shown in views
INDEX_FIELDS = {
    "genre": _("Género"),
}

# Filter fields
FILTER_FIELDS = {
    "genre": {"label": _("Género"), "placeholder": _("Género")},
}

# View titles (used in CRUD)
INDEX_TITLE = MODULE_VERBOSE_NAME
CREATE_TITLE = _("Crear género musical")
EDIT_TITLE = _("Editar género musical")

# Default ordering
DEFAULT_ORDERING = ["-id"]

# Permissions (built from APP_NAME and MODEL_NAME)
PERMISSION_VIEW = f"{APP_NAME}.view_{MODEL_NAME}"
PERMISSION_ADD = f"{APP_NAME}.add_{MODEL_NAME}"
PERMISSION_CHANGE = f"{APP_NAME}.change_{MODEL_NAME}"
PERMISSION_DELETE = f"{APP_NAME}.delete_{MODEL_NAME}"

# Model verbose names
MODEL_MUSIC_GENRE_VERBOSE_NAME = _("Género musical")
MODEL_MUSIC_GENRE_VERBOSE_NAME_PLURAL = _("Géneros musicales")

# Field labels
FIELD_GENRE_LABEL = _("Género")

# Form labels and placeholders
FORM_GENRE_LABEL = _("Género")
FORM_GENRE_PLACEHOLDER = _("Género")

# Filter labels
MUSIC_GENRES_FILTER_FIELDS = {
    "genre": {"label": _("Género")},
}
