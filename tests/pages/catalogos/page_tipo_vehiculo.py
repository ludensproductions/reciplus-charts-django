from enum import Enum

from tests.pages.core.constants import DeleteModeEnum
from tests.pages.core.fields_page import FieldsPage
from tests.pages.core.generic_page import GenericPage


class FieldTipoVehiculoEnum(Enum):
    """Enum de campos para el módulo de Tipos de Vehículos."""

    NOMBRE = "name"


class PageTipoVehiculo(GenericPage):
    """Page Object para el módulo de Tipos de Vehículos."""

    def __init__(self, page):
        super().__init__(
            page,
            module_name="Tipos de vehículos",
            navigation=["Catálogos", "Tipos de vehículos"],
        )

        self.delete_mode = DeleteModeEnum.DEFAULT

        self.detail_page_title_selector = 'h1:has-text("Detalle de tipo de vehículo")'
        self.edit_form_title_selector = 'h1:has-text("Editar tipo de vehículo")'

        # Messages
        self.success_create_message_text = "Elemento creado exitosamente!"
        self.success_delete_message_text = "Elemento eliminado exitosamente!"
        self.success_edit_message_text = "Elemento actualizado exitosamente!"

        # Fields
        self.input_field_instances = {
            FieldTipoVehiculoEnum.NOMBRE.value: FieldsPage(
                self.page,
                name=FieldTipoVehiculoEnum.NOMBRE.value,
                max_length=150,
            ),
        }
