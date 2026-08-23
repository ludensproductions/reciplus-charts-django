from django.utils.translation import gettext_lazy as _

APP_NAME = "albums"
MODEL_NAME = "album"

INDEX_URL = f"{APP_NAME}:index"
CREATE_URL = f"{APP_NAME}:create"
EDIT_URL = f"{APP_NAME}:edit"
DELETE_URL = f"{APP_NAME}:delete"
DETAIL_URL = f"{APP_NAME}:detail"
DASHBOARD_URL = "catalogos:index"

FILTER_FIELDS = {
    "title": {"label": _("Título"), "placeholder": _("Título")},
    "year": {"label": _("Año")},
    "artist": {"label": _("Artista")},
    "songs__title": {"label": _("Título de la canción")},
}

INDEX_FIELDS = {
    "title": _("Título"),
    "year": _("Año"),
    "artist": _("Artista"),
}

DETAIL_FIELDS = {
    "title": _("Título"),
    "year": _("Año"),
    "artist": _("Artista"),
    "cover": _("Portada"),
}

# Model verbose names
ALBUM_VERBOSE_NAME = _("Álbum")
ALBUM_VERBOSE_NAME_PLURAL = _("Álbumes")
SONG_VERBOSE_NAME = _("Canción")
SONG_VERBOSE_NAME_PLURAL = _("Canciones")
ALBUM_MERCH_VERBOSE_NAME = _("Mercancía del álbum")
ALBUM_MERCH_VERBOSE_NAME_PLURAL = _("Mercancías del álbum")
ALBUM_GENRE_RELATION_VERBOSE_NAME = _("Relación de género del álbum")
ALBUM_GENRE_RELATION_VERBOSE_NAME_PLURAL = _("Relaciones de género del álbum")
MERCH_PRODUCT_TYPE_RELATION_VERBOSE_NAME = _("Relación de tipo de producto")
MERCH_PRODUCT_TYPE_RELATION_VERBOSE_NAME_PLURAL = _("Relaciones de tipo de producto")

ERROR_DUPLICATED_REGISTER = _("Ya existe un registro con estos datos.")
ERROR_DUPLICATED_PRIMARY_TAG = _("Ya existe un álbum con esta etiqueta principal.")
ERROR_DUPLICATED_SONG_TITLE = _("No pueden haber canciones con el mismo título")
ERROR_AT_LEAST_ONE_SONG = _("Debe agregar al menos una canción")
ERROR_SONG_TITLE_EXISTS = _("Ya existe una canción con este título.")
ERROR_DUPLICATED_MERCH_NAME = _("No pueden haber mercancías con el mismo nombre")
ERROR_PRODUCT_TYPE_REQUIRED = _("Debe seleccionar al menos un tipo de producto")
ERROR_PRODUCT_TYPE_TOO_SHORT = _("El tipo de producto '{name}' es muy corto. Debe tener al menos 3 caracteres.")
ERROR_PRODUCT_TYPE_INVALID_START = _("El tipo de producto '{name}' no puede empezar con caracteres especiales.")
ERROR_PRODUCT_TYPE_ONLY_NUMBERS = _("El tipo de producto '{name}' no puede ser solo números.")
ERROR_PRODUCT_TYPE_FORBIDDEN = _("El tipo de producto '{name}' no está permitido.")
ERROR_PRODUCT_TYPE_TOO_MANY_WORDS = _("El tipo de producto '{name}' tiene demasiadas palabras. Máximo 5 palabras.")
ERROR_PRODUCT_TYPE_TOO_GENERIC = _("El tipo de producto '{name}' es demasiado genérico. Use un nombre más específico.")
ERROR_GENRE_INVALID_CHARACTERS = _("El género '{genre_name}' contiene caracteres especiales no permitidos.")
ERROR_GENRE_TOO_GENERIC = _("El género '{genre_name}' es demasiado genérico.")


# Field labels
ALBUM_TITLE_LABEL = _("Título")
ALBUM_YEAR_LABEL = _("Año")
ALBUM_ARTIST_LABEL = _("Artista")
ALBUM_COVER_LABEL = _("Portada")
ALBUM_PRIMARY_TAG_LABEL = _("Etiqueta principal")
ALBUM_GENRES_LABEL = _("Géneros")
SONG_TITLE_LABEL = _("Título")
SONG_DURATION_LABEL = _("Duración")
SONG_ALBUM_LABEL = _("Álbum")
SONG_THEME_LABEL = _("Tema")
MERCH_NAME_LABEL = _("Nombre de la mercancía")
MERCH_PRICE_LABEL = _("Precio")
MERCH_ALBUM_LABEL = _("Álbum")
MERCH_PRODUCT_TYPES_LABEL = _("Tipos de producto")
ALBUM_GENRE_LABEL = _("Género")

# Placeholders
ALBUM_TITLE_PLACEHOLDER = _("Título del álbum")
ALBUM_YEAR_PLACEHOLDER = ALBUM_YEAR_LABEL
ALBUM_ARTIST_PLACEHOLDER = ALBUM_ARTIST_LABEL
SONG_TITLE_PLACEHOLDER = _("Título de la canción")
SONG_DURATION_PLACEHOLDER = SONG_DURATION_LABEL
MERCH_NAME_PLACEHOLDER = MERCH_NAME_LABEL
MERCH_PRICE_PLACEHOLDER = MERCH_PRICE_LABEL

# Display formats
ALBUM_DISPLAY = _("{album}")
SONG_DISPLAY = _("{album} - {title}")
MERCH_DISPLAY = _("{album} - {merch}")
ALBUM_GENRE_DISPLAY = _("{album} ↔ {genre}")
MERCH_PRODUCT_TYPE_DISPLAY = _("{merch} ↔ {product_type}")

CHILDREN_ENTITIES = {
    "songs": {"title": _("Nombre de la canción"), "theme": _("Tema"), "duration": _("Duración")},
    "merch": {
        "merch_name": _("Nombre del artículo"),
        "price": _("Precio"),
        "product_types": _("Tipos de producto"),
    },
    "genres": {"genre": _("Género")},
}

TABLE_TITLES = {"songs": _("Canciones"), "merch": _("Mercancías"), "genres": _("Géneros")}

SONGS_FORMSET_PREFIX = "songs"
MERCH_FORMSET_PREFIX = "merch"

# View titles
INDEX_TITLE = _("Álbumes")
CREATE_TITLE = _("Crear álbum")
EDIT_TITLE = _("Editar álbum")
DETAIL_TITLE = _("Detalles del álbum")

# Ordering
ORDERING = ["-id"]

# Context
CONTEXT_OBJECT_NAME = "album"

# Permissions
PERMISSION_VIEW = f"{APP_NAME}.view_{MODEL_NAME}"
PERMISSION_ADD = f"{APP_NAME}.add_{MODEL_NAME}"
PERMISSION_CHANGE = f"{APP_NAME}.change_{MODEL_NAME}"
PERMISSION_DELETE = f"{APP_NAME}.delete_{MODEL_NAME}"
