from enum import Enum

from tests.pages.core.constants import DeleteModeEnum
from tests.pages.core.fields_page import FieldsPage
from tests.pages.core.generic_page import GenericPage


class FieldTipoProductoEnum(Enum):
    """Enum de campos para el módulo de Tipos de Producto."""

    NOMBRE = "nombre"


class PageTipoProducto(GenericPage):
    """Page Object para el módulo de Tipos de Producto."""

    def __init__(self, page):
        super().__init__(page, navigation=["Catálogos", "Tipo productos"])

        self.delete_mode = DeleteModeEnum.TOGGLE

        self.input_field_instances = {
            FieldTipoProductoEnum.NOMBRE.value: FieldsPage(
                self.page,
                name=FieldTipoProductoEnum.NOMBRE.value,
                max_length=255,
            ),
        }
