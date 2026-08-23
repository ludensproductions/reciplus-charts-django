from enum import Enum

from tests.pages.core.constants import DeleteModeEnum
from tests.pages.core.fields_page import FieldsPage
from tests.pages.core.generic_page import GenericPage


class FieldGenerosEnum(Enum):
    """Enum de campos para el módulo de Géneros."""

    DISPLAY_NAME = "display_name"
    GENRE = "genre"


class PageGeneros(GenericPage):
    """Page Object para el módulo de Géneros."""

    def __init__(self, page):
        super().__init__(page, module_name="Géneros", navigation=["Catálogos", "Géneros"])
        self.delete_mode = DeleteModeEnum.TOGGLE

        self.input_field_instances = {
            FieldGenerosEnum.DISPLAY_NAME.value: FieldsPage(
                page=page,
                name=FieldGenerosEnum.DISPLAY_NAME.value,
                max_length=255,
            ),
        }
