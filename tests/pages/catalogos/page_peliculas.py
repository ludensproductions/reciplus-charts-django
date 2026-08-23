from enum import Enum

from pages.catalogos.page_generos import FieldGenerosEnum, PageGeneros
from tests.pages.core.constants import DeleteModeEnum, DependencyAction, InputType
from tests.pages.core.fields_page import FieldsPage
from tests.pages.core.generic_page import GenericPage


class FieldPeliculasEnum(Enum):
    """Enum de campos para el módulo de Películas."""

    TITLE = "title"
    YEAR = "year"
    GENRE = "genre"
    PRICE = "price"
    PLOT = "plot"


class PagePeliculas(GenericPage):
    """Page Object para el módulo de Películas."""

    def __init__(self, page):
        super().__init__(page, module_name="Películas", navigation=["Catálogos", "Películas"])
        self.delete_mode = DeleteModeEnum.TOGGLE
        self.detail_page_title_selector = "h1:has-text('Detalles de la película')"
        self.input_field_dependencies = {
            PageGeneros: {
                DependencyAction.CREATE: {
                    FieldPeliculasEnum.GENRE.value: [FieldGenerosEnum.DISPLAY_NAME.value],
                }
            }
        }

        self.input_field_instances = {
            FieldPeliculasEnum.TITLE.value: FieldsPage(
                page=page,
                name=FieldPeliculasEnum.TITLE.value,
                max_length=100,
                min_length=2,
                filter_truncate_length=35,
                index_truncate_length=35,
                validate_truncate_length=35,
                filter_truncate_suffix="",
                index_truncate_suffix="…",
                validate_truncate_suffix="…",
            ),
            FieldPeliculasEnum.YEAR.value: FieldsPage(
                page=page,
                name=FieldPeliculasEnum.YEAR.value,
                input_type=InputType.NUMBER,
                max_value=2147483647,
                min_value=1895,
                allowed_values=[],
            ),
            FieldPeliculasEnum.GENRE.value: FieldsPage(
                page=page,
                name=FieldPeliculasEnum.GENRE.value,
                input_type=InputType.SELECT,
                is_filter=False,
                max_length=255,
                min_length=2,
                field_truncate_length=50,
                filter_truncate_length=50,
                field_truncate_suffix="...",
                filter_truncate_suffix="...",
            ),
            FieldPeliculasEnum.PRICE.value: FieldsPage(
                page=page,
                is_filter=False,
                is_indexable=False,
                name=FieldPeliculasEnum.PRICE.value,
                input_type=InputType.NUMBER,
                max_value=255,
                min_value=2,
                is_data_validate=False,
                allowed_values=[255.50],
                is_editable=False,
            ),
            FieldPeliculasEnum.PLOT.value: FieldsPage(
                page=page,
                is_filter=False,
                is_editable=False,
                is_indexable=False,
                name=FieldPeliculasEnum.PLOT.value,
                input_type=InputType.TEXTAREA,
            ),
        }
