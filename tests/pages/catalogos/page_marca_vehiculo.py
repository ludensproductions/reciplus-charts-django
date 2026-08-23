from enum import Enum

from tests.pages.core.constants import DeleteModeEnum
from tests.pages.core.fields_page import FieldsPage
from tests.pages.core.generic_page import GenericPage


class FieldMarcaVehiculoEnum(Enum):
    """Enumeración de campos del formulario de marca de vehículo."""

    NOMBRE = "name"


class PageMarcaVehiculo(GenericPage):
    """Page Object para el módulo de marcas de vehículos."""

    def __init__(self, page):
        super().__init__(
            page,
            module_name="Marcas de vehículos",
            navigation=["Catálogos", "Marcas de vehículos"],
        )

        self.delete_mode = DeleteModeEnum.DEFAULT

        self.index_page_title_selector = 'h1:has-text("Marcas de vehículos")'
        self.create_form_title_selector = 'h1:has-text("Crear Marca de vehículo")'
        self.edit_form_title_selector = 'h1:has-text("Editar Marca de vehículo")'
        self.detail_page_title_selector = 'h1:has-text("Detalle de Marca de vehículo")'

        self.input_field_instances = {
            FieldMarcaVehiculoEnum.NOMBRE.value: FieldsPage(
                self.page,
                name=FieldMarcaVehiculoEnum.NOMBRE.value,
                max_length=150,
                min_length=2,
            ),
        }
