from enum import Enum

from pages.catalogos.page_peliculas import FieldPeliculasEnum, PagePeliculas
from tests.pages.core.constants import DependencyAction, InputType
from tests.pages.core.fields_page import FieldsPage
from tests.pages.core.generic_page import GenericPage


class FieldsVentasEnum(Enum):
    """Enum de campos para el módulo de Ventas."""

    NAME = "name"
    MOVIE = "movie"
    QUANTITY = "quantity"

    FORMSET_MOVIES = "movies"


class PageSales(GenericPage):
    """Page Object para el módulo de Ventas."""

    def __init__(self, page):
        super().__init__(page, navigation=["Catálogos", "Ventas"])

        # self.sidebar_button_selector = 'a:has-text("Catálogos")'
        # self.index_page_button_selector = 'a[title="Ventas"]'
        # self.index_page_title_selector = 'h1:has-text("Sales")'
        # self.create_form_button_selector = 'a:has-text("Agregar sale")'
        # self.detail_anchor_selector = 'a[title="Show"]'
        # self.delete_span_selector = 'span[title="Delete"]'
        # self.detail_page_title_selector = 'h1:has-text("Detalles de venta")'
        self.detail_page_title_selector = 'h1:has-text("Detalle de la venta")'

        self.input_field_dependencies = {
            PagePeliculas: {
                DependencyAction.CREATE: {
                    # Movie.__str__ returns "year - title"; dependency must match the select label.
                    FieldsVentasEnum.MOVIE.value: [
                        FieldPeliculasEnum.YEAR.value,
                        " - ",
                        FieldPeliculasEnum.TITLE.value,
                    ],
                }
            }
        }

        self.input_field_instances = {
            FieldsVentasEnum.NAME.value: FieldsPage(
                self.page,
                name=FieldsVentasEnum.NAME.value,
                max_length=100,
            ),
        }

        self.formset_fields = {
            FieldsVentasEnum.FORMSET_MOVIES.value: {
                "add_button_selector": 'button[id="movies"]',
                "fields": {
                    FieldsVentasEnum.MOVIE.value: FieldsPage(
                        self.page,
                        field_selector='select[name="movies-0-movie"]',
                        name=FieldsVentasEnum.MOVIE.value,
                        is_filter=False,
                        is_indexable=False,
                        input_type=InputType.SELECT,
                        is_data_validate=False,
                        field_truncate_length=100,
                        field_truncate_suffix="",
                    ),
                    FieldsVentasEnum.QUANTITY.value: FieldsPage(
                        self.page,
                        field_selector='input[name="movies-0-quantity"]',
                        name=FieldsVentasEnum.QUANTITY.value,
                        is_indexable=False,
                        input_type=InputType.NUMBER,
                        min_value=1,
                        max_value=2147483647,
                        is_data_validate=False,
                        is_filter=False,
                    ),
                },
            },
        }
