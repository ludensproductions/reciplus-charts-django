from enum import Enum

from tests.pages.core.constants import DeleteModeEnum, DependencyAction, FieldRef, InputType
from tests.pages.core.fields_page import FieldsPage
from tests.pages.core.generic_page import GenericPage

from .page_album import FieldAlbumEnum, PageAlbum


class FieldResenaEnum(Enum):
    """Enumeration of fields for the Resena page."""

    # Campos del formulario principal de Reseña
    ALBUM = "album"
    CANCION = "song"
    PUNTUACION = "score"
    RESENA = "review"


class PageResena(GenericPage):
    """Clase PageResena que representa la página de administración de Reseñas de Canciones en el sistema.

    Hereda de GenericPage, una clase genérica que centraliza selectores y lógica reutilizable
    como navegación, validaciones, llenado de formularios, etc.

    El constructor define los campos del formulario necesarios para crear y editar reseñas
    de canciones asociadas a álbumes.
    """

    def __init__(self, page):
        # Se inicializa el padre con los valores clave del módulo:
        # module_name: nombre que se muestra en título y enlaces (ej. "Reseñas de canciones")
        # navigation: ruta de navegación en el sidebar
        super().__init__(page, module_name="Reseñas de canciones", navigation=["Catálogos", "Reseñas de canciones"])
        self.enable_button_selector = 'input[title=" Habilitar "]'
        self.delete_mode = DeleteModeEnum.TOGGLE
        self.detail_page_title_selector = "h1:has-text('Detalles de reseña de canción')"

        _cancion_tokens = [
            FieldRef(FieldAlbumEnum.TITULO.value, lookup_formset=False),
            " - ",
            FieldRef(FieldAlbumEnum.CANCION_TITULO.value, lookup_formset=True),
        ]

        # Configuración de dependencias con otras páginas
        self.input_field_dependencies = {
            PageAlbum: {
                DependencyAction.CREATE: {
                    FieldResenaEnum.ALBUM.value: [FieldRef(FieldAlbumEnum.TITULO.value, lookup_formset=False)],
                    FieldResenaEnum.CANCION.value: [
                        FieldRef(FieldAlbumEnum.CANCION_TITULO.value, lookup_formset=True)
                    ],
                },
                DependencyAction.FILTER: {
                    FieldResenaEnum.CANCION.value: _cancion_tokens,
                    FieldResenaEnum.ALBUM.value: [FieldRef(FieldAlbumEnum.TITULO.value, lookup_formset=False)],
                },
                DependencyAction.INDEX: {
                    FieldResenaEnum.CANCION.value: _cancion_tokens,
                },
                DependencyAction.VALIDATE: {
                    FieldResenaEnum.CANCION.value: _cancion_tokens,
                },
            },
        }

        # Se definen los campos individuales del formulario principal de reseñas
        self.input_field_instances = {
            FieldResenaEnum.ALBUM.value: FieldsPage(
                self.page,
                field_selector=f"#div_id_{FieldResenaEnum.ALBUM.value}",
                name=FieldResenaEnum.ALBUM.value,
                input_type=InputType.SELECT2,
                filter_type=InputType.SELECT,
                is_filter=True,
                is_indexable=False,
                num_dependencies=1,
            ),
            FieldResenaEnum.CANCION.value: FieldsPage(
                self.page,
                field_selector=f"#div_id_{FieldResenaEnum.CANCION.value}",
                name=FieldResenaEnum.CANCION.value,
                input_type=InputType.SELECT2,
                filter_type=InputType.SELECT,
            ),
            FieldResenaEnum.PUNTUACION.value: FieldsPage(
                self.page,
                name=FieldResenaEnum.PUNTUACION.value,
                min_value=0,
                max_value=10,
                input_type=InputType.NUMBER,
                is_filter=True,
                is_indexable=True,
            ),
            FieldResenaEnum.RESENA.value: FieldsPage(
                self.page,
                name=FieldResenaEnum.RESENA.value,
                input_type=InputType.TEXTAREA,
                is_filter=False,
                is_indexable=False,
                max_length=500,
                min_length=10,
            ),
        }
