from enum import Enum

from tests.pages.core.constants import DeleteModeEnum, InputType
from tests.pages.core.fields_page import FieldsPage
from tests.pages.core.generic_page import GenericPage

INVALID_REMOTE_LOCATION_ERROR = "Los trabajos remotos deben tener ubicación 'Remoto'."


class FieldTrabajoEnum(Enum):
    """Enum de campos para el módulo de Trabajos."""

    TITLE = "title"
    COMPANY = "company"
    LOCATION = "location"
    JOB_TYPE = "job_type"
    MIN_SALARY = "min_salary"
    MAX_SALARY = "max_salary"
    IS_REMOTE = "is_remote"
    IS_ACTIVE = "is_active"


class PageTrabajos(GenericPage):
    """Page Object para el módulo de Trabajos."""

    def __init__(self, page):
        super().__init__(page, module_name="Trabajos", navigation=["Catálogos", "Trabajos"])
        self.delete_mode = DeleteModeEnum.TOGGLE

        self.input_field_instances = {
            FieldTrabajoEnum.TITLE.value: FieldsPage(
                page=page,
                max_length=200,
                min_length=5,
                name=FieldTrabajoEnum.TITLE.value,
                regex_pattern=r"^[a-zA-Z]{2,} [a-zA-Z]{2,}$",
                input_type=InputType.REGEX,
            ),
            FieldTrabajoEnum.COMPANY.value: FieldsPage(
                page=page,
                max_length=100,
                name=FieldTrabajoEnum.COMPANY.value,
            ),
            FieldTrabajoEnum.LOCATION.value: FieldsPage(
                page=page,
                max_length=100,
                name=FieldTrabajoEnum.LOCATION.value,
            ),
            FieldTrabajoEnum.JOB_TYPE.value: FieldsPage(
                page=page,
                name=FieldTrabajoEnum.JOB_TYPE.value,
                input_type=InputType.SELECT,
                allowed_values=["Tiempo completo", "Medio tiempo", "Contrato"],
            ),
            FieldTrabajoEnum.MIN_SALARY.value: FieldsPage(
                page=page,
                name=FieldTrabajoEnum.MIN_SALARY.value,
                input_type=InputType.DECIMAL,
                decimal_places=2,
                min_value=0.01,
                max_value=5000000,
            ),
            FieldTrabajoEnum.MAX_SALARY.value: FieldsPage(
                page=page,
                name=FieldTrabajoEnum.MAX_SALARY.value,
                input_type=InputType.DECIMAL,
                decimal_places=2,
                min_value=5000001,
                max_value=99999999,
            ),
            FieldTrabajoEnum.IS_REMOTE.value: FieldsPage(
                page=page,
                name=FieldTrabajoEnum.IS_REMOTE.value,
                input_type=InputType.CHECKBOX,
                is_filter=False,
                is_indexable=False,
                is_data_validate=False,
                is_required=False,
            ),
            FieldTrabajoEnum.IS_ACTIVE.value: FieldsPage(
                page=page,
                name=FieldTrabajoEnum.IS_ACTIVE.value,
                input_type=InputType.CHECKBOX,
                is_filter=False,
                is_indexable=False,
                is_data_validate=False,
                is_required=False,
            ),
        }

    async def generate_random_data(self, is_edit: bool = False, create_on_dependency_page=True, **kwargs):
        """Override to enforce business rule: is_remote=True requires location='Remoto'.

        Args:
            is_edit (bool): Whether generating data for an edit operation.
            create_on_dependency_page (bool): Whether to create dependencies on their own page.
            **kwargs: Additional values forwarded to the parent.
        """
        await super().generate_random_data(
            is_edit=is_edit, create_on_dependency_page=create_on_dependency_page, **kwargs
        )
        is_remote = self.input_field_instances[FieldTrabajoEnum.IS_REMOTE.value]
        if is_remote.field_value:
            self.set_input_instance_value(**{FieldTrabajoEnum.LOCATION.value: "Remoto"})
