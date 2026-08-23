from enum import Enum

from tests.pages.core.constants import DeleteModeEnum
from tests.pages.core.fields_page import FieldsPage
from tests.pages.core.generic_page import GenericPage


class FieldEtiquetasMusicalesEnum(Enum):
    """Enum de campos para el módulo de Etiquetas Musicales."""

    TAG = "tag"


class PageEtiquetasMusicales(GenericPage):
    """Page Object para el módulo de Etiquetas Musicales."""

    def __init__(self, page):
        super().__init__(page, module_name="Etiquetas musicales", navigation=["Catálogos", "Etiquetas musicales"])
        self.delete_mode = DeleteModeEnum.TOGGLE
        self.edit_form_title_selector = 'h1:has-text("Editar etiqueta musical")'
        self.input_field_instances = {
            FieldEtiquetasMusicalesEnum.TAG.value: FieldsPage(
                page=page,
                name=FieldEtiquetasMusicalesEnum.TAG.value,
                max_length=100,
                min_length=1,
            )
        }
