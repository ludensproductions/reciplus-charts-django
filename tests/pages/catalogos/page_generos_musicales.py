from enum import Enum

from tests.pages.core.constants import DeleteModeEnum
from tests.pages.core.fields_page import FieldsPage
from tests.pages.core.generic_page import GenericPage


class FieldGenerosMusicalesEnum(Enum):
    """Enum de campos para el módulo de Géneros Musicales."""

    GENERO = "genre"


class PageGenerosMusicales(GenericPage):
    """Page Object para el módulo de Géneros Musicales."""

    def __init__(self, page):
        super().__init__(page, module_name="Géneros musicales", navigation=["Catálogos", "Géneros musicales"])
        self.delete_mode = DeleteModeEnum.TOGGLE
        self.edit_form_title_selector = 'h1:has-text("Editar género musical")'
        self.input_field_instances = {
            FieldGenerosMusicalesEnum.GENERO.value: FieldsPage(
                page=page,
                name=FieldGenerosMusicalesEnum.GENERO.value,
                is_indexable=False,
                max_length=100,
                min_length=1,
            )
        }
