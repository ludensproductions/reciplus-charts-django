from django.utils.translation import gettext_lazy as _

APP_NAME = "videos"
MODEL_NAME = "video"
MODULE_VERBOSE_NAME = _("Videos")

INDEX_URL = f"{APP_NAME}:index"
EDIT_URL = f"{APP_NAME}:edit"
DELETE_URL = f"{APP_NAME}:delete"
DETAIL_URL = f"{APP_NAME}:detail"
DASHBOARD_URL = "catalogos:index"

# Permissions
PERMISSION_VIEW = "contents.view_content"
PERMISSION_CHANGE = f"{APP_NAME}.change_{MODEL_NAME}"
PERMISSION_DELETE = "contents.delete_content"

# Titles
INDEX_TITLE = MODULE_VERBOSE_NAME
EDIT_TITLE = _("Editar video")
DETAIL_TITLE = _("Detalle de video")

# Verbose name
VERBOSE_NAME = _("Video")

# Default ordering
DEFAULT_ORDERING = ["-id"]

INDEX_FIELDS = {
    "content": _("Título"),
}

FILTER_FIELDS = {
    "content__title": {"label": _("Título"), "placeholder": _("Título")},
}

DETAIL_FIELDS = {
    "content": _("Título"),
    "video_url": _("URL"),
}

VIDEO_URL_LABEL = _("URL del video")
VIDEO_URL_PLACEHOLDER = _("URL del video")
