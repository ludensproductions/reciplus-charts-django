from enum import Enum

from tests.pages.core.constants import DeleteModeEnum, InputType
from tests.pages.core.fields_page import FieldsPage
from tests.pages.core.generic_page import GenericPage


class FieldActividadEnum(Enum):
    """Enum de campos para el módulo de Actividades."""

    NOMBRE = "name"
    UBICACION = "location"
    TIPO_ACTIVIDAD = "activity_type"


class PageActividad(GenericPage):
    """Page Object para el módulo de Actividades."""

    def __init__(self, page):
        super().__init__(page, module_name="Actividades", navigation=["Catálogos", "Actividades"])
        self.detail_page_title_selector = 'h1:has-text("Detalles de la actividad")'
        self.delete_mode = DeleteModeEnum.TOGGLE
        self.input_field_instances = {
            FieldActividadEnum.NOMBRE.value: FieldsPage(
                page=page,
                max_length=150,
                name=FieldActividadEnum.NOMBRE.value,
            ),
            FieldActividadEnum.UBICACION.value: FieldsPage(
                page=page,
                max_length=150,
                name=FieldActividadEnum.UBICACION.value,
            ),
            FieldActividadEnum.TIPO_ACTIVIDAD.value: FieldsPage(
                page=page,
                input_type=InputType.SELECT2,
                filter_type=InputType.SELECT2_MULTIPLE,
                name=FieldActividadEnum.TIPO_ACTIVIDAD.value,
                allowed_values=["Taller", "Conferencia", "Seminario web"],
            ),
        }
