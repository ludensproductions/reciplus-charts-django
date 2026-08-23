from enum import Enum

from tests.pages.core.constants import AllowedDatesFormates, InputType
from tests.pages.core.fields_page import FieldsPage
from tests.pages.core.generic_page import GenericPage


class FieldReservacionesEnum(Enum):
    """Enum de campos para el módulo de Reservaciones."""

    RESERVADOR = "guest"
    FECHA_RESERVACION = "booking_range"
    FECHA_INICIO_CANCELACION = "cancel_start"
    FECHA_FIN_CANCELACION = "cancel_end"
    FECHA_HORA_LLEGADA = "scheduled_arrive"
    TIPO_RESERVACION = "reservation_type"
    PUNTOS_PROMOCION = "promotion_points"
    CARGO_EXTRA = "extra_fee"
    TIEMPO_CANCELACION = "cancel_time"


class TipoReservacionAllowedValues(Enum):
    """Enum de valores permitidos para tipo de reservación."""

    SIN_ANTICIPACION = "Sin anticipación"
    ESTANDAR = "Estándar"


class PageReservacion(GenericPage):
    """Page Object para el módulo de Reservaciones."""

    def __init__(self, page):
        super().__init__(page, module_name="Reservaciones", navigation=["Catálogos", "Reservaciones"])

        self.detail_page_title_selector = "h1:has-text('Detalles de la reservación')"
        self.input_field_instances = {
            FieldReservacionesEnum.RESERVADOR.value: FieldsPage(
                self.page,
                name=FieldReservacionesEnum.RESERVADOR.value,
                max_length=100,
                # allowed_values=[],
                # prioritized_values=["Juan Pérez", "María Gómez"],
                # priority_percentage=0.8,
            ),
            FieldReservacionesEnum.FECHA_RESERVACION.value: FieldsPage(
                self.page,
                name=FieldReservacionesEnum.FECHA_RESERVACION.value,
                input_type=InputType.RANGE_OF_DATES,
                detail_format_date=AllowedDatesFormates.DD_ABBREVIATE_MONTH_YYYY,
                index_format_date=AllowedDatesFormates.DD_ABBREVIATE_MONTH_YYYY,
                detail_range_of_dates_separator=" - ",
                index_range_of_dates_separator=" | ",
                is_filter=False,
                is_indexable=False,
                is_data_validate=False,
            ),
            FieldReservacionesEnum.FECHA_INICIO_CANCELACION.value: FieldsPage(
                self.page,
                name=FieldReservacionesEnum.FECHA_INICIO_CANCELACION.value,
                input_type=InputType.DATE_START,
                detail_format_date=AllowedDatesFormates.DATE_IN_SPANISH,
                index_format_date=AllowedDatesFormates.DD_MM_AAAA,
                date_separator="-",
                is_filter=False,
                is_data_validate=False,
            ),
            FieldReservacionesEnum.TIEMPO_CANCELACION.value: FieldsPage(
                page=self.page,
                name=FieldReservacionesEnum.TIEMPO_CANCELACION.value,
                input_type=InputType.TIME,
                field_format_date=AllowedDatesFormates.HH_MM,
                index_format_date=AllowedDatesFormates.HH_MM_SS,
                is_filter=False,
            ),
            FieldReservacionesEnum.FECHA_FIN_CANCELACION.value: FieldsPage(
                self.page,
                name=FieldReservacionesEnum.FECHA_FIN_CANCELACION.value,
                input_type=InputType.DATE_END,
                detail_format_date=AllowedDatesFormates.DATE_IN_SPANISH,
                index_format_date=AllowedDatesFormates.DD_COMPLETE_MONTH_YYYY,
                is_filter=False,
                is_data_validate=False,
            ),
            FieldReservacionesEnum.FECHA_HORA_LLEGADA.value: FieldsPage(
                self.page,
                name=FieldReservacionesEnum.FECHA_HORA_LLEGADA.value,
                input_type=InputType.DATE_TIME,
                field_format_date=AllowedDatesFormates.DD_MM_AAAA_HH_MM,
                detail_format_date=AllowedDatesFormates.DATETIME_IN_SPANISH,
                is_filter=False,
                is_data_validate=False,
            ),
            FieldReservacionesEnum.TIPO_RESERVACION.value: FieldsPage(
                self.page,
                name=FieldReservacionesEnum.TIPO_RESERVACION.value,
                input_type=InputType.SELECT,
                allowed_values=[
                    TipoReservacionAllowedValues.ESTANDAR.value,
                    TipoReservacionAllowedValues.SIN_ANTICIPACION.value,
                ],
                prioritized_values=[TipoReservacionAllowedValues.ESTANDAR.value],
                priority_percentage=0.7,
                is_filter=False,
                is_indexable=False,
                is_data_validate=False,
            ),
            FieldReservacionesEnum.PUNTOS_PROMOCION.value: FieldsPage(
                page=self.page,
                name=FieldReservacionesEnum.PUNTOS_PROMOCION.value,
                input_type=InputType.NUMBER,
                is_dependent=True,
                activating_field=FieldReservacionesEnum.TIPO_RESERVACION.value,
                activating_values=[
                    TipoReservacionAllowedValues.ESTANDAR.value,
                ],
                is_filter=False,
                is_indexable=False,
                validate_value_for_nullable="--",
            ),
            FieldReservacionesEnum.CARGO_EXTRA.value: FieldsPage(
                page=self.page,
                name=FieldReservacionesEnum.CARGO_EXTRA.value,
                input_type=InputType.DECIMAL,
                is_dependent=True,
                activating_field=FieldReservacionesEnum.TIPO_RESERVACION.value,
                activating_values=[TipoReservacionAllowedValues.SIN_ANTICIPACION.value],
                is_filter=False,
                is_indexable=False,
                validate_value_for_nullable="--",
            ),
        }
