from enum import Enum

from tests.pages.catalogos.page_producto import FieldProductosEnum, PageProducto
from tests.pages.core.constants import AllowedDatesFormates, DeleteModeEnum, DependencyAction, InputType
from tests.pages.core.fields_page import FieldsPage
from tests.pages.core.generic_page import GenericPage


class FieldAbarrotesEnum(Enum):
    """Enum de campos del módulo Abarrotes."""

    ABARROTES = "abarrotes"
    PRODUCTO = "producto"
    CANTIDAD = "cantidad"
    FECHA = "fecha"


class PageAbarrotes(GenericPage):
    """Page Object para el módulo de Abarrotes."""

    def __init__(self, page):
        super().__init__(
            page,
            module_name="Abarrotes",
            navigation=["Catálogos", "Abarrotes"],
        )

        self.delete_mode = DeleteModeEnum.TOGGLE

        self.sidebar_button_selector = 'a:has-text("Catálogos")'
        self.index_page_button_selector = 'a[title="Abarrotes"]'
        self.index_page_title_selector = 'h1:has-text("Abarrotes")'
        self.create_form_button_selector = 'a:has-text("Agregar abarrote")'
        self.create_form_title_selector = 'h1:has-text("Crear inventario abarrotes")'
        self.edit_form_title_selector = 'h1:has-text("Editar inventario abarrotes")'
        self.detail_page_title_selector = 'h1:has-text("Detalles del inventario del abarrotes")'
        self.detail_button_selector = 'a[title="Show"]'
        self.edit_button_selector = 'a[title="Update"]'
        self.detail_page_title_selector = 'h1:has-text("Detalles del inventario de abarrotes")'
        self.edit_form_title_selector = 'h1:has-text("Editar inventario de abarrotes")'
        self.enable_button_selector = 'input[title=" Habilitar "]'

        self.input_field_dependencies = {
            PageProducto: {
                DependencyAction.CREATE: {
                    FieldAbarrotesEnum.PRODUCTO.value: [FieldProductosEnum.PRODUCTO.value],
                }
            }
        }

        self.input_field_instances = {
            FieldAbarrotesEnum.ABARROTES.value: FieldsPage(
                self.page,
                name=FieldAbarrotesEnum.ABARROTES.value,
                max_length=100,
                is_indexable=False,
                is_data_validate=False,
            ),
            FieldAbarrotesEnum.PRODUCTO.value: FieldsPage(
                self.page,
                name=FieldAbarrotesEnum.PRODUCTO.value,
                input_type=InputType.SELECT,
                num_dependencies=1,
            ),
            FieldAbarrotesEnum.CANTIDAD.value: FieldsPage(
                self.page,
                name=FieldAbarrotesEnum.CANTIDAD.value,
                input_type=InputType.NUMBER,
                min_value=0,
                max_value=2147483647,
            ),
            FieldAbarrotesEnum.FECHA.value: FieldsPage(
                self.page,
                name=FieldAbarrotesEnum.FECHA.value,
                input_type=InputType.DATE,
                detail_format_date=AllowedDatesFormates.DATE_IN_SPANISH,
                index_format_date=AllowedDatesFormates.DD_MM_AAAA,
                is_indexable=False,
            ),
        }
