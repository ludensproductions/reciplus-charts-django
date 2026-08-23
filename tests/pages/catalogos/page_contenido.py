from enum import Enum

from tests.pages.core.constants import DeleteModeEnum, DependencyAction, InputType
from tests.pages.core.fields_page import FieldsPage
from tests.pages.core.generic_page import GenericPage

from .page_categoria import FieldCategoriaEnum, PageCategorias


class FieldContenidoEnum(Enum):
    """Enum de campos para el módulo de Contenidos."""

    TITULO = "title"
    TIPO_CONTENIDO = "content_type"
    CUERPO = "article-body"
    CATEGORIA = "article-category"
    URL = "video-video_url"


class PageContenido(GenericPage):
    """Page Object para el módulo de Contenidos."""

    def __init__(self, page):
        super().__init__(
            page,
            module_name="Contenidos",
            navigation=["Catálogos", "Contenidos"],
        )

        self.sidebar_button_selector = 'a:has-text("Catálogos")'
        self.index_page_button_selector = 'a[title="Contenidos"]'
        self.index_page_title_selector = 'h1:has-text("Contenidos")'
        self.create_form_button_selector = 'a:has-text("Agregar contenido")'
        self.detail_button_selector = 'a[title="Show"]'
        self.edit_button_selector = 'a[title="Update"]'
        self.detail_page_title_selector = 'h1:has-text("Detalles del contenido")'
        self.edit_form_title_selector = 'h1:has-text("Editar contenido")'
        self.enable_button_selector = 'input[title=" Habilitar "]'

        self.delete_mode = DeleteModeEnum.TOGGLE

        self.input_field_dependencies = {
            PageCategorias: {
                DependencyAction.CREATE: {
                    FieldContenidoEnum.CATEGORIA.value: [FieldCategoriaEnum.CATEGORIA.value],
                }
            }
        }

        self.input_field_instances = {
            FieldContenidoEnum.TITULO.value: FieldsPage(
                self.page,
                is_indexable=False,
                max_length=200,
                name=FieldContenidoEnum.TITULO.value,
                min_length=1,
            ),
            FieldContenidoEnum.TIPO_CONTENIDO.value: FieldsPage(
                self.page,
                name=FieldContenidoEnum.TIPO_CONTENIDO.value,
                input_type=InputType.SELECT,
                allowed_values=["Artículo", "Video"],
            ),
            FieldContenidoEnum.CUERPO.value: FieldsPage(
                self.page,
                name=FieldContenidoEnum.CUERPO.value,
                input_type=InputType.TEXTAREA,
                field_selector='input[name="article-body"]',
                is_dependent=True,
                activating_field=FieldContenidoEnum.TIPO_CONTENIDO.value,
                activating_values=["Artículo"],
                is_filter=False,
                is_data_validate=False,
                is_indexable=False,
            ),
            FieldContenidoEnum.CATEGORIA.value: FieldsPage(
                self.page,
                name=FieldContenidoEnum.CATEGORIA.value,
                input_type=InputType.SELECT,
                field_selector='select[name="article-category"]',
                is_dependent=True,
                activating_field=FieldContenidoEnum.TIPO_CONTENIDO.value,
                activating_values=["Artículo"],
                is_filter=False,
                is_data_validate=False,
                is_indexable=False,
            ),
            FieldContenidoEnum.URL.value: FieldsPage(
                self.page,
                name=FieldContenidoEnum.URL.value,
                input_type=InputType.URL,
                field_selector=f'input[name="{FieldContenidoEnum.URL.value}"]',
                is_dependent=True,
                activating_field=FieldContenidoEnum.TIPO_CONTENIDO.value,
                activating_values=["Video"],
                is_filter=False,
                is_data_validate=False,
                is_indexable=False,
            ),
        }
