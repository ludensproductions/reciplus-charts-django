from enum import Enum

from pages.catalogos.page_actividad import FieldActividadEnum, PageActividad
from pages.usuarios.page_usuarios import FieldUsuariosEnum, PageUsuarios

from tests.pages.core.constants import DependencyAction, InputType
from tests.pages.core.fields_page import FieldsPage
from tests.pages.core.generic_page import GenericPage
from utils.utils_functions import generate_random_int


class FieldEventoEnum(Enum):
    """Enumeration of fields for the Evento page."""

    TITULO = "title"
    FECHA_INICIO = "date_start"
    UBICACION = "location"
    RESPONSABLE = "responsible"

    # CAMPOS FORMSETS
    FORMSET_ACTIVIDADES = "activities"
    ACTIVIDAD = "activity"
    AFORO = "capacity"
    CODIGO = "code"

    # FORMSET ASISTENTES
    FORMSET_ASISTENTES = "attendees"
    NOMBRE_COMPLETO = "full_name"
    EMAIL = "email"
    TELEFONO = "phone"
    NOTAS = "notes"

    # Campo generado
    FOLIO = "folio"


class PageEventos(GenericPage):
    """Page object for the Eventos catalog page."""

    def __init__(self, page):
        super().__init__(
            page,
            module_name="Eventos",
            navigation=["Catálogos", "Eventos"],
        )
        self.detail_page_title_selector = 'h1:has-text("Detalle del Evento")'
        self.cancel_alert_button_selector = "button:has-text('Cancelar')"

        self.input_field_dependencies = {
            # Configuracion para la dependencia con la pagina de actividades
            PageActividad: {
                DependencyAction.CREATE: {
                    FieldEventoEnum.ACTIVIDAD.value: [
                        FieldActividadEnum.NOMBRE.value,
                        " - ",
                        FieldActividadEnum.UBICACION.value,
                    ],
                },
                DependencyAction.VALIDATE: {
                    FieldEventoEnum.ACTIVIDAD.value: [
                        FieldActividadEnum.NOMBRE.value,
                        " (",
                        FieldActividadEnum.UBICACION.value,
                        ")",
                    ],
                },
                DependencyAction.FILTER: {
                    FieldEventoEnum.ACTIVIDAD.value: [
                        FieldActividadEnum.NOMBRE.value,
                        " | ",
                        FieldActividadEnum.UBICACION.value,
                    ]
                },
                DependencyAction.INDEX: {
                    FieldEventoEnum.ACTIVIDAD.value: [
                        FieldActividadEnum.NOMBRE.value,
                        ", ",
                        FieldActividadEnum.UBICACION.value,
                    ]
                },
            },
            PageUsuarios: {
                DependencyAction.CREATE: {
                    FieldEventoEnum.RESPONSABLE.value: [
                        FieldUsuariosEnum.NOMBRES.value,
                        " ",
                        FieldUsuariosEnum.APELLIDO_PATERNO.value,
                    ],
                },
                DependencyAction.FILTER: {
                    FieldEventoEnum.RESPONSABLE.value: [
                        FieldUsuariosEnum.NOMBRES.value,
                        " - ",
                        FieldUsuariosEnum.APELLIDO_PATERNO.value,
                    ],
                },
                DependencyAction.INDEX: {
                    FieldEventoEnum.RESPONSABLE.value: [
                        FieldUsuariosEnum.NOMBRES.value,
                        ", ",
                        FieldUsuariosEnum.APELLIDO_PATERNO.value,
                    ],
                },
                DependencyAction.VALIDATE: {
                    FieldEventoEnum.RESPONSABLE.value: [
                        FieldUsuariosEnum.NOMBRES.value,
                        ", ",
                        FieldUsuariosEnum.APELLIDO_PATERNO.value,
                    ],
                },
            },
        }

        self.input_field_instances = {
            FieldEventoEnum.TITULO.value: FieldsPage(
                page=page,
                max_length=200,
                name=FieldEventoEnum.TITULO.value,
            ),
            FieldEventoEnum.FECHA_INICIO.value: FieldsPage(
                page=page,
                input_type=InputType.DATE,
                name=FieldEventoEnum.FECHA_INICIO.value,
                is_indexable=False,
                is_data_validate=False,
            ),
            FieldEventoEnum.UBICACION.value: FieldsPage(
                page=page,
                max_length=200,
                name=FieldEventoEnum.UBICACION.value,
            ),
            FieldEventoEnum.RESPONSABLE.value: FieldsPage(
                page=page,
                max_length=150,
                name=FieldEventoEnum.RESPONSABLE.value,
                field_selector=f"#div_id_{FieldEventoEnum.RESPONSABLE.value}",
                input_type=InputType.SELECT2,
                filter_type=InputType.SELECT,
                title_for_validate="get_responsible_name_index",
            ),
            # Campo generado
            FieldEventoEnum.FOLIO.value: FieldsPage(
                page=page,
                name=FieldEventoEnum.FOLIO.value,
                field_selector=f'th[name="{FieldEventoEnum.FOLIO.value}"]',
                filter_selector=f'input[name="{FieldEventoEnum.FOLIO.value}"]',
                is_generated_field=True,
            ),
        }

        self.formset_fields = {
            FieldEventoEnum.FORMSET_ACTIVIDADES.value: {
                "add_button_selector": 'button[id="activities"]',
                "prefix_validate": "event_activities",
                "is_required": True,
                "has_initial_row": False,  # El formset inicia con 0 filas (extra=0 en Django)
                "fields": {
                    FieldEventoEnum.ACTIVIDAD.value: FieldsPage(
                        self.page,
                        field_selector=f'select[name="{FieldEventoEnum.FORMSET_ACTIVIDADES.value}-0-{FieldEventoEnum.ACTIVIDAD.value}"]',
                        filter_selector='select[name="event_activity__activity"]',
                        name=FieldEventoEnum.ACTIVIDAD.value,
                        input_type=InputType.SELECT,
                        is_filter=False,
                    ),
                    FieldEventoEnum.AFORO.value: FieldsPage(
                        self.page,
                        field_selector=f'select[name="{FieldEventoEnum.FORMSET_ACTIVIDADES.value}-0-{FieldEventoEnum.AFORO.value}"]',
                        filter_selector='input[name="event_activity__capacity"]',
                        name=FieldEventoEnum.AFORO.value,
                        input_type=InputType.NUMBER,
                        min_value=0,
                        max_value=generate_random_int(1, 5000000),
                        is_indexable=False,
                        is_filter=False,
                    ),
                    FieldEventoEnum.CODIGO.value: FieldsPage(
                        self.page,
                        field_selector=f'input[name="{FieldEventoEnum.FORMSET_ACTIVIDADES.value}-0-{FieldEventoEnum.CODIGO.value}"]',
                        name=FieldEventoEnum.CODIGO.value,
                        is_filter=False,
                        max_length=50,
                        is_indexable=False,
                    ),
                },
            },
        }

    async def delete_formset_rows(self, formset_name, num_delete_rows, mode, **kwargs):
        """Elimina filas del formset y actualiza los datos de validación."""
        num_formsets = kwargs.get(f"num_{formset_name}", 0)
        await super().delete_formset_rows(formset_name, num_delete_rows, mode, **kwargs)
        rows = self.formset_instances.get(formset_name, {}).get(mode, [])
        remaining = max(num_formsets - num_delete_rows, 0)
        if len(rows) > remaining:
            self.formset_instances[formset_name][mode] = rows[:remaining]
            self.generate_filters_and_validate_data(is_edit=(mode == "edit"))
