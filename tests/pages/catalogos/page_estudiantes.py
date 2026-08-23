from enum import Enum

from tests.pages.core.constants import DeleteModeEnum, InputType
from tests.pages.core.fields_page import FieldsPage
from tests.pages.core.generic_page import GenericPage


class FieldEstudianteEnum(Enum):
    """Enum de campos para el módulo de Estudiantes."""

    NAME = "name"
    LAST_NAME = "last_name"
    EMAIL = "email"
    PHONE = "phone"
    ADDRESS = "address"
    IMAGE = "image"


class PageEstudiantes(GenericPage):
    """Page Object para el módulo de Estudiantes."""

    def __init__(self, page):
        super().__init__(page, module_name="Estudiantes", navigation=["Catálogos", "Estudiantes"])
        self.delete_mode = DeleteModeEnum.TOGGLE
        self.input_field_instances = {
            FieldEstudianteEnum.NAME.value: FieldsPage(
                page=page,
                name=FieldEstudianteEnum.NAME.value,
                max_length=255,
            ),
            FieldEstudianteEnum.LAST_NAME.value: FieldsPage(
                page=page,
                name=FieldEstudianteEnum.LAST_NAME.value,
                max_length=255,
            ),
            FieldEstudianteEnum.EMAIL.value: FieldsPage(
                page=page,
                name=FieldEstudianteEnum.EMAIL.value,
                input_type=InputType.EMAIL,
                max_length=255,
            ),
            FieldEstudianteEnum.PHONE.value: FieldsPage(
                page=page,
                name=FieldEstudianteEnum.PHONE.value,
                max_length=255,
            ),
            FieldEstudianteEnum.ADDRESS.value: FieldsPage(
                page=page,
                name=FieldEstudianteEnum.ADDRESS.value,
                max_length=255,
            ),
            FieldEstudianteEnum.IMAGE.value: FieldsPage(
                page=page,
                name=FieldEstudianteEnum.IMAGE.value,
                input_type=InputType.FILE,
                is_required=False,
                allowed_values=["jpg", "png", "jpeg"],
                is_filter=False,
                is_indexable=False,
                is_data_validate=False,
            ),
        }
