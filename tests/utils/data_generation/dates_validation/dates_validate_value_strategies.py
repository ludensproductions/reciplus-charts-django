from abc import ABC, abstractmethod

from tests.pages.core.constants import DateValidateLocation, InputType
from tests.utils.data_generation.base_input_attributes import BaseInputAttributes
from utils.format_dates_functions import (
    format_date_aa_dd_mm,
    format_date_aa_dd_mm_hh_mm,
    format_date_aa_dd_mm_hh_mm_ss,
    format_date_aa_mm_dd,
    format_date_aa_mm_dd_hh_mm,
    format_date_aa_mm_dd_hh_mm_ss,
    format_date_aaaa_dd_mm,
    format_date_aaaa_dd_mm_hh_mm,
    format_date_aaaa_dd_mm_hh_mm_ss,
    format_date_aaaa_mm_dd,
    format_date_aaaa_mm_dd_hh_mm,
    format_date_aaaa_mm_dd_hh_mm_ss,
    format_date_date_in_spanish,
    format_date_datetime_in_spanish,
    format_date_dd_abbreviate_month_yyyy,
    format_date_dd_complete_month_yyyy,
    format_date_dd_mm_aa,
    format_date_dd_mm_aa_hh_mm,
    format_date_dd_mm_aa_hh_mm_ss,
    format_date_dd_mm_aaaa,
    format_date_dd_mm_aaaa_hh_mm,
    format_date_dd_mm_aaaa_hh_mm_ss,
    format_date_mm_dd_aa,
    format_date_mm_dd_aa_hh_mm,
    format_date_mm_dd_aa_hh_mm_ss,
    format_date_mm_dd_aaaa,
    format_date_mm_dd_aaaa_hh_mm,
    format_date_mm_dd_aaaa_hh_mm_ss,
    format_time_hh_mm,
    format_time_hh_mm_am_pm,
    format_time_hh_mm_ss,
    format_time_hh_mm_ss_am_pm,
)


class DatesValidateValueStrategy(ABC, BaseInputAttributes):
    """Clase base para las estrategias de validación de fechas."""

    def __init__(self, field_instance, location=DateValidateLocation.DETAIL):
        """Initializes the DatesValidateValueStrategy."""
        BaseInputAttributes.__init__(self, field_instance=field_instance)
        self.location = location

    @abstractmethod
    def generate_validate_data(self):
        """Generates validated data for the specific strategy."""
        raise NotImplementedError("Es necesario implementar generate_validate_data")

    def generate_date_value(self, method, **kwargs):
        """Genera un valor de fecha formateado aplicando el método de formato especificado.

        Args:
            method: Función de formato a aplicar
            **kwargs: Parámetros adicionales para la función de formato

        Returns:
            str: Fecha o rango de fechas formateado
        """

        def apply_format(value):
            return method(value, **kwargs) if kwargs else method(value)

        if self.input_type == InputType.RANGE_OF_DATES:
            start_value, end_value = self.field_value
            separator = (
                self.detail_range_of_dates_separator
                if self.location == DateValidateLocation.DETAIL
                else self.index_range_of_dates_separator
            )
            return f"{apply_format(start_value)}{separator}{apply_format(end_value)}"

        return apply_format(self.field_value)


class DD_MM_AA_STRATEGY(DatesValidateValueStrategy):
    """Strategy for DD/MM/AA date format."""

    def generate_validate_data(self):
        """Generates validated data for DD/MM/AA format."""
        return self.generate_date_value(format_date_dd_mm_aa, **{"date_separator": self.date_separator})


class MM_DD_AA_STRATEGY(DatesValidateValueStrategy):
    """Strategy for MM/DD/AA date format."""

    def generate_validate_data(self):
        """Generates validated data for MM/DD/AA format."""
        return self.generate_date_value(format_date_mm_dd_aa, **{"date_separator": self.date_separator})


class AA_DD_MM_STRATEGY(DatesValidateValueStrategy):
    """Strategy for AA/DD/MM date format."""

    def generate_validate_data(self):
        """Generates validated data for AA/DD/MM format."""
        return self.generate_date_value(format_date_aa_dd_mm, **{"date_separator": self.date_separator})


class AA_MM_DD_STRATEGY(DatesValidateValueStrategy):
    """Strategy for AA/MM/DD date format."""

    def generate_validate_data(self):
        """Generates validated data for AA/MM/DD format."""
        return self.generate_date_value(format_date_aa_mm_dd, **{"date_separator": self.date_separator})


class DD_MM_AAAA_STRATEGY(DatesValidateValueStrategy):
    """Strategy for DD/MM/AAAA date format."""

    def generate_validate_data(self):
        """Generates validated data for DD/MM/AAAA format."""
        return self.generate_date_value(format_date_dd_mm_aaaa, **{"date_separator": self.date_separator})


class MM_DD_AAAA_STRATEGY(DatesValidateValueStrategy):
    """Strategy for MM/DD/AAAA date format."""

    def generate_validate_data(self):
        """Generates validated data for MM/DD/AAAA format."""
        return self.generate_date_value(format_date_mm_dd_aaaa, **{"date_separator": self.date_separator})


class AAAA_DD_MM_STRATEGY(DatesValidateValueStrategy):
    """Strategy for AAAA/DD/MM date format."""

    def generate_validate_data(self):
        """Generates validated data for AAAA/DD/MM format."""
        return self.generate_date_value(format_date_aaaa_dd_mm, **{"date_separator": self.date_separator})


class AAAA_MM_DD_STRATEGY(DatesValidateValueStrategy):
    """Strategy for AAAA/MM/DD date format."""

    def generate_validate_data(self):
        """Generates validated data for AAAA/MM/DD format."""
        return self.generate_date_value(format_date_aaaa_mm_dd, **{"date_separator": self.date_separator})


class HH_MM_SS_STRATEGY(DatesValidateValueStrategy):
    """Strategy for HH:MM:SS time format."""

    def generate_validate_data(self):
        """Generates validated data for HH:MM:SS format."""
        return self.generate_date_value(format_time_hh_mm_ss, **{"time_separator": self.time_separator})


class HH_MM_STRATEGY(DatesValidateValueStrategy):
    """Strategy for HH:MM time format."""

    def generate_validate_data(self):
        """Generates validated data for HH:MM format."""
        return self.generate_date_value(format_time_hh_mm, **{"time_separator": self.time_separator})


class HH_MM_AM_PM_STRATEGY(DatesValidateValueStrategy):
    """Strategy for HH:MM AM/PM time format."""

    def generate_validate_data(self):
        """Generates validated data for HH:MM AM/PM format."""
        return self.generate_date_value(format_time_hh_mm_am_pm, **{"time_separator": self.time_separator})


class HH_MM_SS_AM_PM_STRATEGY(DatesValidateValueStrategy):
    """Strategy for HH:MM:SS AM/PM time format."""

    def generate_validate_data(self):
        """Generates validated data for HH:MM:SS AM/PM format."""
        return self.generate_date_value(format_time_hh_mm_ss_am_pm, **{"time_separator": self.time_separator})


class DD_MM_AA_HH_MM_SS_STRATEGY(DatesValidateValueStrategy):
    """Strategy for DD/MM/AA HH:MM:SS date-time format."""

    def generate_validate_data(self):
        """Generates validated data for DD/MM/AA HH:MM:SS format."""
        return self.generate_date_value(
            format_date_dd_mm_aa_hh_mm_ss,
            **{
                "date_separator": self.date_separator,
                "datetime_separator": self.datetime_separator,
                "time_separator": self.time_separator,
            },
        )


class MM_DD_AA_HH_MM_SS_STRATEGY(DatesValidateValueStrategy):
    """Strategy for MM/DD/AA HH:MM:SS date-time format."""

    def generate_validate_data(self):
        """Generates validated data for MM/DD/AA HH:MM:SS format."""
        return self.generate_date_value(
            format_date_mm_dd_aa_hh_mm_ss,
            **{
                "date_separator": self.date_separator,
                "datetime_separator": self.datetime_separator,
                "time_separator": self.time_separator,
            },
        )


class AA_MM_DD_HH_MM_SS_STRATEGY(DatesValidateValueStrategy):
    """Strategy for AA/MM/DD HH:MM:SS date-time format."""

    def generate_validate_data(self):
        """Generates validated data for AA/MM/DD HH:MM:SS format."""
        return self.generate_date_value(
            format_date_aa_mm_dd_hh_mm_ss,
            **{
                "date_separator": self.date_separator,
                "datetime_separator": self.datetime_separator,
                "time_separator": self.time_separator,
            },
        )


class AA_DD_MM_HH_MM_SS_STRATEGY(DatesValidateValueStrategy):
    """Strategy for AA/DD/MM HH:MM:SS date-time format."""

    def generate_validate_data(self):
        """Generates validated data for AA/DD/MM HH:MM:SS format."""
        return self.generate_date_value(
            format_date_aa_dd_mm_hh_mm_ss,
            **{
                "date_separator": self.date_separator,
                "datetime_separator": self.datetime_separator,
                "time_separator": self.time_separator,
            },
        )


class DD_MM_AAAA_HH_MM_SS_STRATEGY(DatesValidateValueStrategy):
    """Strategy for DD/MM/AAAA HH:MM:SS date-time format."""

    def generate_validate_data(self):
        """Generates validated data for DD/MM/AAAA HH:MM:SS format."""
        return self.generate_date_value(
            format_date_dd_mm_aaaa_hh_mm_ss,
            **{
                "date_separator": self.date_separator,
                "datetime_separator": self.datetime_separator,
                "time_separator": self.time_separator,
            },
        )


class MM_DD_AAAA_HH_MM_SS_STRATEGY(DatesValidateValueStrategy):
    """Strategy for MM/DD/AAAA HH:MM:SS date-time format."""

    def generate_validate_data(self):
        """Generates validated data for MM/DD/AAAA HH:MM:SS format."""
        return self.generate_date_value(
            format_date_mm_dd_aaaa_hh_mm_ss,
            **{
                "date_separator": self.date_separator,
                "datetime_separator": self.datetime_separator,
                "time_separator": self.time_separator,
            },
        )


class AAAA_DD_MM_HH_MM_SS_STRATEGY(DatesValidateValueStrategy):
    """Strategy for AAAA/DD/MM HH:MM:SS date-time format."""

    def generate_validate_data(self):
        """Generates validated data for AAAA/DD/MM HH:MM:SS format."""
        return self.generate_date_value(
            format_date_aaaa_dd_mm_hh_mm_ss,
            **{
                "date_separator": self.date_separator,
                "datetime_separator": self.datetime_separator,
                "time_separator": self.time_separator,
            },
        )


class AAAA_MM_DD_HH_MM_SS_STRATEGY(DatesValidateValueStrategy):
    """Strategy for AAAA/MM/DD HH:MM:SS date-time format."""

    def generate_validate_data(self):
        """Generates validated data for AAAA/MM/DD HH:MM:SS format."""
        return self.generate_date_value(
            format_date_aaaa_mm_dd_hh_mm_ss,
            **{
                "date_separator": self.date_separator,
                "datetime_separator": self.datetime_separator,
                "time_separator": self.time_separator,
            },
        )


class DD_MM_AA_HH_MM_STRATEGY(DatesValidateValueStrategy):
    """Strategy for DD/MM/AA HH:MM date-time format."""

    def generate_validate_data(self):
        """Generates validated data for DD/MM/AA HH:MM format."""
        return self.generate_date_value(
            format_date_dd_mm_aa_hh_mm,
            **{
                "date_separator": self.date_separator,
                "datetime_separator": self.datetime_separator,
                "time_separator": self.time_separator,
            },
        )


class MM_DD_AA_HH_MM_STRATEGY(DatesValidateValueStrategy):
    """Strategy for MM/DD/AA HH:MM date-time format."""

    def generate_validate_data(self):
        """Generates validated data for MM/DD/AA HH:MM format."""
        return self.generate_date_value(
            format_date_mm_dd_aa_hh_mm,
            **{
                "date_separator": self.date_separator,
                "datetime_separator": self.datetime_separator,
                "time_separator": self.time_separator,
            },
        )


class AA_MM_DD_HH_MM_STRATEGY(DatesValidateValueStrategy):
    """Strategy for AA/MM/DD HH:MM date-time format."""

    def generate_validate_data(self):
        """Generates validated data for AA/MM/DD HH:MM format."""
        return self.generate_date_value(
            format_date_aa_mm_dd_hh_mm,
            **{
                "date_separator": self.date_separator,
                "datetime_separator": self.datetime_separator,
                "time_separator": self.time_separator,
            },
        )


class AA_DD_MM_HH_MM_STRATEGY(DatesValidateValueStrategy):
    """Strategy for AA/DD/MM HH:MM date-time format."""

    def generate_validate_data(self):
        """Generates validated data for AA/DD/MM HH:MM format."""
        return self.generate_date_value(
            format_date_aa_dd_mm_hh_mm,
            **{
                "date_separator": self.date_separator,
                "datetime_separator": self.datetime_separator,
                "time_separator": self.time_separator,
            },
        )


class DD_MM_AAAA_HH_MM_STRATEGY(DatesValidateValueStrategy):
    """Strategy for DD/MM/AAAA HH:MM date-time format."""

    def generate_validate_data(self):
        """Generates validated data for DD/MM/AAAA HH:MM format."""
        return self.generate_date_value(
            format_date_dd_mm_aaaa_hh_mm,
            **{
                "date_separator": self.date_separator,
                "datetime_separator": self.datetime_separator,
                "time_separator": self.time_separator,
            },
        )


class MM_DD_AAAA_HH_MM_STRATEGY(DatesValidateValueStrategy):
    """Strategy for MM/DD/AAAA HH:MM date-time format."""

    def generate_validate_data(self):
        """Generates validated data for MM/DD/AAAA HH:MM format."""
        return self.generate_date_value(
            format_date_mm_dd_aaaa_hh_mm,
            **{
                "date_separator": self.date_separator,
                "datetime_separator": self.datetime_separator,
                "time_separator": self.time_separator,
            },
        )


class AAAA_DD_MM_HH_MM_STRATEGY(DatesValidateValueStrategy):
    """Strategy for AAAA/DD/MM HH:MM date-time format."""

    def generate_validate_data(self):
        """Generates validated data for AAAA/DD/MM HH:MM format."""
        return self.generate_date_value(
            format_date_aaaa_dd_mm_hh_mm,
            **{
                "date_separator": self.date_separator,
                "datetime_separator": self.datetime_separator,
                "time_separator": self.time_separator,
            },
        )


class AAAA_MM_DD_HH_MM_STRATEGY(DatesValidateValueStrategy):
    """Strategy for AAAA/MM/DD HH:MM date-time format."""

    def generate_validate_data(self):
        """Generates validated data for AAAA/MM/DD HH:MM format."""
        return self.generate_date_value(
            format_date_aaaa_mm_dd_hh_mm,
            **{
                "date_separator": self.date_separator,
                "datetime_separator": self.datetime_separator,
                "time_separator": self.time_separator,
            },
        )


class DATE_IN_SPANISH_STRATEGY(DatesValidateValueStrategy):
    """Strategy for date in Spanish format."""

    def generate_validate_data(self):
        """Generates validated data in Spanish date format."""
        return self.generate_date_value(format_date_date_in_spanish)


class DATETIME_IN_SPANISH_STRATEGY(DatesValidateValueStrategy):
    """Strategy for date and time in Spanish format."""

    def generate_validate_data(self):
        """Generates validated data in Spanish date and time format."""
        return self.generate_date_value(format_date_datetime_in_spanish)


class DD_COMPLETE_MONTH_YYYY_STRATEGY(DatesValidateValueStrategy):
    """Strategy for DD Complete Month YYYY date format."""

    def generate_validate_data(self):
        """Generates validated data for DD Complete Month YYYY format."""
        return self.generate_date_value(format_date_dd_complete_month_yyyy)


class DD_ABBREVIATE_MONTH_YYYY_STRATEGY(DatesValidateValueStrategy):
    """Strategy for DD Abbreviated Month YYYY date format."""

    def generate_validate_data(self):
        """Generates validated data for DD Abbreviated Month YYYY format."""
        return self.generate_date_value(format_date_dd_abbreviate_month_yyyy)
