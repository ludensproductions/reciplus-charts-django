from django.utils.translation import gettext_lazy as _

APP_NAME = "song_reviews"
MODEL_NAME = "songreview"

# Model labels
MODEL_SONG_REVIEW_VERBOSE_NAME = _("Reseña de canción")
MODEL_SONG_REVIEW_VERBOSE_NAME_PLURAL = _("Reseñas de canciones")
FIELD_ALBUM_LABEL = _("Álbum")
FIELD_SONG_LABEL = _("Canción")
FIELD_SCORE_LABEL = _("Calificación")
FIELD_REVIEW_LABEL = _("Reseña")
PARENT_RELATION_ALBUMS_LABEL = _("álbumes")
PARENT_RELATION_SONGS_LABEL = _("canciones")

# Shared index labels
INDEX_SONG_LABEL = FIELD_SONG_LABEL
INDEX_ALBUM_LABEL = FIELD_ALBUM_LABEL
INDEX_SCORE_LABEL = FIELD_SCORE_LABEL

# Shared titles
TITLE_SONG_REVIEW_LIST = MODEL_SONG_REVIEW_VERBOSE_NAME_PLURAL

INDEX_URL = f"{APP_NAME}:index"
CREATE_URL = f"{APP_NAME}:create"
EDIT_URL = f"{APP_NAME}:edit"
DELETE_URL = f"{APP_NAME}:delete"
DETAIL_URL = f"{APP_NAME}:detail"
DASHBOARD_URL = "catalogos:index"

INDEX_FIELDS = {
    "song": INDEX_SONG_LABEL,
    "album": INDEX_ALBUM_LABEL,
    "score": INDEX_SCORE_LABEL,
}

DETAIL_FIELDS = [
    "song",
    "album",
    "score",
    "review",
]

# Export URL
EXPORT_CSV_URL = f"{APP_NAME}:export_csv"
MODAL_INDEX_URL = f"{APP_NAME}:modal_index"

# View Titles
INDEX_TITLE = TITLE_SONG_REVIEW_LIST
CREATE_TITLE = _("Crear reseña de canción")
EDIT_TITLE = _("Editar reseña")
DETAIL_TITLE = _("Detalles de reseña de canción")
MODAL_INDEX_TITLE = TITLE_SONG_REVIEW_LIST

# Ordering
ORDERING = ["-id"]

# Verbose names
VERBOSE_NAME = _("Reseña")

# General extra actions
EXPORT_BUTTON_TITLE = _("Descargar calificaciones")
EXPORT_BUTTON_ICON = "fas fa-download"
EXPORT_BUTTON_CLASS = "btn-primary btn_movil_view_size margin_bottom_btn"


# Notification messages
SUCCESS_REVIEW_CREATED_MESSAGE = _("Canción %(song)s reseñada exitosamente.")
SUCCESS_REVIEW_CREATED_TITLE = _("Nueva reseña creada.")
SUCCESS_REVIEW_UPDATED_MESSAGE = _("Reseña de %(song)s editada exitosamente.")
SUCCESS_REVIEW_UPDATED_TITLE = _("Reseña editada.")

# Export CSV
CSV_FILENAME = "songs_scores.csv"

# Permissions
PERMISSION_VIEW = f"{APP_NAME}.view_{MODEL_NAME}"
PERMISSION_ADD = f"{APP_NAME}.add_{MODEL_NAME}"
PERMISSION_CHANGE = f"{APP_NAME}.change_{MODEL_NAME}"
PERMISSION_DELETE = f"{APP_NAME}.delete_{MODEL_NAME}"
PERMISSION_VIEW_SONG = "albums.view_song"

# Form labels and placeholders
FORM_ALBUM_LABEL = FIELD_ALBUM_LABEL
FORM_SONG_LABEL = FIELD_SONG_LABEL
FORM_SCORE_LABEL = FIELD_SCORE_LABEL
FORM_REVIEW_LABEL = FIELD_REVIEW_LABEL
FORM_SCORE_PLACEHOLDER = FORM_SCORE_LABEL
FORM_REVIEW_PLACEHOLDER = _("Escribe tu reseña aquí")

# Filter labels
FILTER_SCORE_LABEL = FIELD_SCORE_LABEL
FILTER_ALBUM_LABEL = FIELD_ALBUM_LABEL
FILTER_SONG_LABEL = FIELD_SONG_LABEL
