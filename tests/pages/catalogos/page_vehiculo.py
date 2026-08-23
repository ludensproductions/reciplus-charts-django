"""Page Object para el módulo de Vehículos.

Este módulo define el PageObject para las pruebas E2E del módulo de vehículos,
incluyendo la configuración de campos, dependencias y selectores.
"""

from enum import Enum

from pages.core.constants import RegexFlag
from tests.pages.core.constants import DeleteModeEnum, DependencyAction, InputType
from tests.pages.core.fields_page import FieldsPage
from tests.pages.core.generic_page import GenericPage

from .page_marca_vehiculo import PageMarcaVehiculo
from .page_tipo_vehiculo import PageTipoVehiculo


class FieldVehiculoEnum(Enum):
    """Enumeración de campos del formulario de vehículo."""

    NOMBRE = "name"
    MARCA = "brand"
    TIPO_VEHICULO = "vehicle_type"
    PLACA = "license_plate"
    ANIO = "year"
    MODELO = "model"


class PageVehiculo(GenericPage):
    """Page Object para el módulo de vehículos."""

    def __init__(self, page):
        super().__init__(
            page,
            module_name="Vehículos",
            navigation=["Catálogos", "Vehículos"],
        )

        self.delete_mode = DeleteModeEnum.DEFAULT

        self.index_page_title_selector = 'h1:has-text("Vehículos")'
        self.create_form_title_selector = 'h1:has-text("Crear vehículo")'
        self.edit_form_title_selector = 'h1:has-text("Editar vehículo")'
        self.detail_page_title_selector = 'h1:has-text("Detalle del vehículo")'

        # Dependencias FK
        self.input_field_dependencies = {
            PageMarcaVehiculo: {
                DependencyAction.CREATE: {
                    FieldVehiculoEnum.MARCA.value: ("name",),
                },
            },
            PageTipoVehiculo: {
                DependencyAction.CREATE: {
                    FieldVehiculoEnum.TIPO_VEHICULO.value: ("name",),
                },
            },
        }

        # Campos del formulario
        self.input_field_instances = {
            FieldVehiculoEnum.NOMBRE.value: FieldsPage(
                self.page,
                name=FieldVehiculoEnum.NOMBRE.value,
                max_length=150,
                min_length=2,
                is_required=False,
            ),
            FieldVehiculoEnum.MARCA.value: FieldsPage(
                self.page,
                name=FieldVehiculoEnum.MARCA.value,
                input_type=InputType.SELECT,
            ),
            FieldVehiculoEnum.TIPO_VEHICULO.value: FieldsPage(
                self.page,
                name=FieldVehiculoEnum.TIPO_VEHICULO.value,
                input_type=InputType.SELECT,
            ),
            FieldVehiculoEnum.PLACA.value: FieldsPage(
                self.page,
                name=FieldVehiculoEnum.PLACA.value,
                input_type=InputType.REGEX,
                max_length=20,
                min_length=4,
                regex_pattern=r"^(?:[A-Z]{3}-\d{4}|\d{1}[A-Z]{2}\d{2}|[A-Z]{3}\d{3})$",
                regex_flags=RegexFlag.U,  # Sin flags, o usa "I" para IGNORECASE, "IM" para IGNORECASE+MULTILINE, etc.
            ),
            FieldVehiculoEnum.ANIO.value: FieldsPage(
                self.page,
                name=FieldVehiculoEnum.ANIO.value,
                input_type=InputType.NUMBER,
                min_value=1900,
                max_value=2100,
                is_filter=False,
            ),
            FieldVehiculoEnum.MODELO.value: FieldsPage(
                self.page,
                name=FieldVehiculoEnum.MODELO.value,
                max_length=150,
                min_length=1,
                is_filter=False,
            ),
        }
