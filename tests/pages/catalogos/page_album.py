from enum import Enum

from pages.catalogos.page_etiqueta_musicales import FieldEtiquetasMusicalesEnum, PageEtiquetasMusicales
from pages.catalogos.page_generos_musicales import FieldGenerosMusicalesEnum, PageGenerosMusicales
from pages.catalogos.page_temas_musicales import FieldTemasMusicalesEnum, PageTemasMusicales
from pages.catalogos.page_tipo_producto import FieldTipoProductoEnum, PageTipoProducto
from tests.pages.core.constants import DeleteModeEnum, DependencyAction, InputType
from tests.pages.core.fields_page import FieldsPage
from tests.pages.core.generic_page import GenericPage


class FieldAlbumEnum(Enum):
    """Enumeration of fields for the Album page."""

    # Campos del formulario principal de Álbum
    TITULO = "title"
    AÑO = "year"
    ARTISTA = "artist"
    ETIQUETA_PRINCIPAL = "primary_tag"
    GENEROS = "genres"

    # Campos del formset de Canciones (Song)
    CANCION = "songs"
    CANCION_TITULO = "title"
    CANCION_DURACION = "duration"
    CANCION_TEMA = "theme"

    # Campos del formset de Mercancía (Merch)
    MERCANCIA_NOMBRE = "merch_name"
    MERCANCIA_PRECIO = "price"
    MERCANCIA_TIPO_PRODUCTO = "product_types"


class PageAlbum(GenericPage):
    """Clase PageAlbum que representa la página de administración de Álbumes en el sistema.

    Hereda de GenericPage, una clase genérica que centraliza selectores y lógica reutilizable
    como navegación, validaciones, llenado de formularios, etc.

    El constructor define los campos del formulario y los formsets necesarios
    para crear y editar álbumes, canciones y mercancía asociada.
    """

    def __init__(self, page):
        # Se inicializa el padre con los valores clave del módulo:
        # sidebar: nombre de la sección principal (ej. "Catálogos")
        # module_name: nombre que se muestra en título y enlaces (ej. "Álbumes")
        super().__init__(page, module_name="Álbumes", navigation=["Catálogos", "Álbumes"])
        self.enable_button_selector = 'input[title=" Habilitar "]'
        self.delete_mode = DeleteModeEnum.TOGGLE

        self.input_field_dependencies = {
            PageEtiquetasMusicales: {
                DependencyAction.CREATE: {
                    FieldAlbumEnum.ETIQUETA_PRINCIPAL.value: [FieldEtiquetasMusicalesEnum.TAG.value],
                },
            },
            PageGenerosMusicales: {
                DependencyAction.CREATE: {
                    FieldAlbumEnum.GENEROS.value: [FieldGenerosMusicalesEnum.GENERO.value],
                },
                # Sin separador configurado en VALIDATE
                # Esto permite que cada género se valide individualmente como tabla
            },
            PageTemasMusicales: {
                DependencyAction.CREATE: {
                    FieldAlbumEnum.CANCION_TEMA.value: [FieldTemasMusicalesEnum.TEMA.value],
                },
                DependencyAction.VALIDATE: {
                    FieldAlbumEnum.CANCION_TEMA.value: [FieldTemasMusicalesEnum.TEMA.value],
                },
            },
            PageTipoProducto: {
                DependencyAction.CREATE: {
                    FieldAlbumEnum.MERCANCIA_TIPO_PRODUCTO.value: [FieldTipoProductoEnum.NOMBRE.value],
                },
                DependencyAction.VALIDATE: {
                    FieldAlbumEnum.MERCANCIA_TIPO_PRODUCTO.value: [FieldTipoProductoEnum.NOMBRE.value, " | "],
                },
            },
        }

        # Se definen los campos individuales del formulario principal de álbumes
        self.input_field_instances = {
            FieldAlbumEnum.TITULO.value: FieldsPage(
                self.page,
                name="title",
                max_length=100,
                min_length=2,
            ),
            FieldAlbumEnum.AÑO.value: FieldsPage(
                self.page,
                name="year",
                min_value=1895,  # Primer año posible para un álbum
                max_value=2147483647,  # Límite arbitrario
                input_type=InputType.NUMBER,
            ),
            FieldAlbumEnum.ARTISTA.value: FieldsPage(
                self.page,
                name="artist",
                max_length=100,
            ),
            FieldAlbumEnum.ETIQUETA_PRINCIPAL.value: FieldsPage(
                self.page,
                input_type=InputType.SELECT2,
                name="primary_tag",
                is_filter=False,
                is_indexable=False,
                max_length=100,
                is_data_validate=False,
                num_dependencies=1,
            ),
            FieldAlbumEnum.GENEROS.value: FieldsPage(
                self.page,
                input_type=InputType.SELECT2_MULTIPLE,
                name=FieldAlbumEnum.GENEROS.value,
                is_filter=False,
                is_indexable=False,
                num_dependencies=2,
                table_suffix="genre",
                is_data_validate=False,
            ),
        }

        # Se definen los formsets (campos repetibles anidados dentro del álbum)
        self.formset_fields = {
            FieldAlbumEnum.CANCION.value: {
                "add_button_selector": 'button[id="songs"]',
                "is_required": True,  # Se espera al menos una canción por álbum
                "fields": {
                    FieldAlbumEnum.CANCION_TITULO.value: FieldsPage(
                        self.page,
                        field_selector='input[name="songs-0-title"]',
                        filter_selector='input[name="songs__title"]',
                        name="title",
                        max_length=100,
                        min_length=2,
                        is_filter=False,
                        is_indexable=False,
                    ),
                    FieldAlbumEnum.CANCION_DURACION.value: FieldsPage(
                        self.page,
                        field_selector='input[name="songs-0-duration"]',
                        name="duration",
                        input_type=InputType.TIME,
                        is_filter=False,
                        is_indexable=False,
                        min_value=0,  # No puede ser negativo
                    ),
                    FieldAlbumEnum.CANCION_TEMA.value: FieldsPage(
                        self.page,
                        input_type=InputType.SELECT2,
                        field_selector="#div_id_songs-0-theme",
                        name=FieldAlbumEnum.CANCION_TEMA.value,
                        is_filter=False,
                        is_indexable=False,
                        is_required=False,
                        is_data_validate=False,
                    ),
                },
            },
            "merch": {
                "add_button_selector": 'button[id="merch"]',
                "fields": {
                    FieldAlbumEnum.MERCANCIA_NOMBRE.value: FieldsPage(
                        self.page,
                        field_selector='input[name="merch-0-merch_name"]',
                        name="merch_name",
                        max_length=100,
                        min_length=2,
                        is_filter=False,
                        is_indexable=False,
                    ),
                    FieldAlbumEnum.MERCANCIA_PRECIO.value: FieldsPage(
                        self.page,
                        field_selector='input[name="merch-0-price"]',
                        name=FieldAlbumEnum.MERCANCIA_PRECIO.value,
                        input_type=InputType.NUMBER,
                        is_filter=False,
                        is_indexable=False,
                        min_value=0,
                        max_value=999999,
                    ),
                    FieldAlbumEnum.MERCANCIA_TIPO_PRODUCTO.value: FieldsPage(
                        self.page,
                        field_selector="#div_id_merch-0-product_types",
                        name=FieldAlbumEnum.MERCANCIA_TIPO_PRODUCTO.value,
                        max_length=100,
                        input_type=InputType.SELECT2_MULTIPLE,
                        is_filter=False,
                        is_indexable=False,
                        num_dependencies=2,
                        is_data_validate=False,
                    ),
                },
            },
        }
