from enum import Enum

from tests.pages.core.constants import DeleteModeEnum
from tests.pages.core.fields_page import FieldsPage
from tests.pages.core.generic_page import GenericPage


class FieldTemasMusicalesEnum(Enum):
    """Enum de campos para el módulo de Temas Musicales."""

    TEMA = "theme"


class PageTemasMusicales(GenericPage):
    """Page Object para el módulo de Temas Musicales."""

    def __init__(self, page):
        super().__init__(page, module_name="Temas musicales", navigation=["Catálogos", "Temas musicales"])
        self.delete_mode = DeleteModeEnum.TOGGLE
        self.edit_form_title_selector = 'h1:has-text("Editar tema musical")'
        self.input_field_instances = {
            FieldTemasMusicalesEnum.TEMA.value: FieldsPage(
                page=page,
                name=FieldTemasMusicalesEnum.TEMA.value,
                is_indexable=False,
                max_length=100,
                min_length=1,
            )
        }
