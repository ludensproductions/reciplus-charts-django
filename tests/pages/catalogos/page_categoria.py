from enum import Enum

from tests.pages.core.constants import DeleteModeEnum
from tests.pages.core.fields_page import FieldsPage
from tests.pages.core.generic_page import GenericPage


class FieldCategoriaEnum(Enum):
    """Enum de campos para el módulo de Categorías."""

    CATEGORIA = "name"


class PageCategorias(GenericPage):
    """Page Object para el módulo de Categorías."""

    def __init__(self, page):
        super().__init__(page, module_name="Categorías", navigation=["Catálogos", "Categorías"])
        self.disabled_index_page_title_selector = 'h1:has-text("Categorías deshabilitadas")'
        self.delete_mode = DeleteModeEnum.DISABLE_INDEX
        self.input_field_instances = {
            FieldCategoriaEnum.CATEGORIA.value: FieldsPage(
                page=page,
                max_length=100,
                name=FieldCategoriaEnum.CATEGORIA.value,
                min_length=1,
            )
        }
