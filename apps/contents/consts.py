from django.db import models
from django.utils.translation import gettext_lazy as _

# Base identifiers
APP_NAME = "contents"
MODEL_NAME = "content"
MODULE_VERBOSE_NAME = _("Contenidos")
MODEL_VERBOSE_NAME = _("Contenido")
MODEL_VERBOSE_NAME_PLURAL = _("Contenidos")

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
CONTENT_TYPE_LABEL = _("Tipo de contenido")
VIDEO_URL_LABEL = _("URL del video")
ARTICLE_BODY_LABEL = _("Cuerpo")
ARTICLE_CATEGORY_LABEL = _("Categoría")

# Model field labels
CONTENT_TITLE_LABEL = TITLE_LABEL
CONTENT_TYPE_FIELD_LABEL = CONTENT_TYPE_LABEL

# Form labels
CONTENT_FORM_TITLE_LABEL = TITLE_LABEL
CONTENT_FORM_TYPE_LABEL = CONTENT_TYPE_LABEL

# Placeholders
CONTENT_TITLE_PLACEHOLDER = TITLE_LABEL

# Content type labels
CONTENT_TYPE_ARTICLE_LABEL = _("Artículo")
CONTENT_TYPE_VIDEO_LABEL = _("Video")

# Fields shown in views
INDEX_FIELDS = {
    "title": TITLE_LABEL,
    "content_type": CONTENT_TYPE_LABEL,
}

DETAIL_FIELDS = {
    "title": TITLE_LABEL,
    "content_type": CONTENT_TYPE_LABEL,
    "video__video_url": VIDEO_URL_LABEL,
    "article__body": ARTICLE_BODY_LABEL,
    "article__category": ARTICLE_CATEGORY_LABEL,
}

# Filter fields
FILTER_FIELDS = {
    "title": {"label": TITLE_LABEL, "placeholder": TITLE_LABEL},
    "content_type": {"label": CONTENT_TYPE_LABEL, "placeholder": CONTENT_TYPE_LABEL},
}

# View titles (used in CRUD)
INDEX_TITLE = MODULE_VERBOSE_NAME
CREATE_TITLE = _("Crear contenido")
EDIT_TITLE = _("Editar contenido")
DETAIL_TITLE = _("Detalles del contenido")

# Default ordering
DEFAULT_ORDERING = ["-id"]

# Permissions (built from APP_NAME and MODEL_NAME)
PERMISSION_VIEW = f"{APP_NAME}.view_{MODEL_NAME}"
PERMISSION_ADD = f"{APP_NAME}.add_{MODEL_NAME}"
PERMISSION_CHANGE = f"{APP_NAME}.change_{MODEL_NAME}"
PERMISSION_DELETE = f"{APP_NAME}.delete_{MODEL_NAME}"

# Messages
SUCCESS_CREATE_MESSAGE = _("¡Elemento creado exitosamente!")
SUCCESS_UPDATE_MESSAGE = _("¡Elemento actualizado exitosamente!")
SUCCESS_DELETE_MESSAGE = _("¡Elemento {action} exitosamente!")

# Custom templates
FORM_TEMPLATE = "contents/generic/form.html"

# Custom JS files
CUSTOM_JS_FILES = ["assets/js/events/examples/contents_events.js"]


class ContentTypes(models.TextChoices):
    """Define content type choices for content records."""

    ARTICLE = ("article", CONTENT_TYPE_ARTICLE_LABEL)
    VIDEO = ("video", CONTENT_TYPE_VIDEO_LABEL)
