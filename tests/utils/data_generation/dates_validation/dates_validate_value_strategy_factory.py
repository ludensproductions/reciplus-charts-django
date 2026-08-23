from tests.pages.core.constants import AllowedDatesFormates

from . import dates_validate_value_strategies as d


class DatesValidateValueStrategyFactory:
    """Clase para crear estrategias de validación de fechas."""

    def __init__(self, field_instance):
        """Initializes the DatesValidateValueStrategyFactory."""
        self.strategies = {
            AllowedDatesFormates.DD_MM_AA: d.DD_MM_AA_STRATEGY,
            AllowedDatesFormates.MM_DD_AA: d.MM_DD_AA_STRATEGY,
            AllowedDatesFormates.AA_DD_MM: d.AA_DD_MM_STRATEGY,
            AllowedDatesFormates.AA_MM_DD: d.AA_MM_DD_STRATEGY,
            AllowedDatesFormates.DD_MM_AAAA: d.DD_MM_AAAA_STRATEGY,
            AllowedDatesFormates.MM_DD_AAAA: d.MM_DD_AAAA_STRATEGY,
            AllowedDatesFormates.AAAA_DD_MM: d.AAAA_DD_MM_STRATEGY,
            AllowedDatesFormates.AAAA_MM_DD: d.AAAA_MM_DD_STRATEGY,
            AllowedDatesFormates.HH_MM_SS: d.HH_MM_SS_STRATEGY,
            AllowedDatesFormates.HH_MM: d.HH_MM_STRATEGY,
            AllowedDatesFormates.HH_MM_AM_PM: d.HH_MM_AM_PM_STRATEGY,
            AllowedDatesFormates.HH_MM_SS_AM_PM: d.HH_MM_SS_AM_PM_STRATEGY,
            AllowedDatesFormates.DD_MM_AA_HH_MM_SS: d.DD_MM_AA_HH_MM_SS_STRATEGY,
            AllowedDatesFormates.MM_DD_AA_HH_MM_SS: d.MM_DD_AA_HH_MM_SS_STRATEGY,
            AllowedDatesFormates.AA_MM_DD_HH_MM_SS: d.AA_MM_DD_HH_MM_SS_STRATEGY,
            AllowedDatesFormates.AA_DD_MM_HH_MM_SS: d.AA_DD_MM_HH_MM_SS_STRATEGY,
            AllowedDatesFormates.DD_MM_AAAA_HH_MM_SS: d.DD_MM_AAAA_HH_MM_SS_STRATEGY,
            AllowedDatesFormates.MM_DD_AAAA_HH_MM_SS: d.MM_DD_AAAA_HH_MM_SS_STRATEGY,
            AllowedDatesFormates.AAAA_DD_MM_HH_MM_SS: d.AAAA_DD_MM_HH_MM_SS_STRATEGY,
            AllowedDatesFormates.AAAA_MM_DD_HH_MM_SS: d.AAAA_MM_DD_HH_MM_SS_STRATEGY,
            AllowedDatesFormates.DD_MM_AA_HH_MM: d.DD_MM_AA_HH_MM_STRATEGY,
            AllowedDatesFormates.MM_DD_AA_HH_MM: d.MM_DD_AA_HH_MM_STRATEGY,
            AllowedDatesFormates.AA_MM_DD_HH_MM: d.AA_MM_DD_HH_MM_STRATEGY,
            AllowedDatesFormates.AA_DD_MM_HH_MM: d.AA_DD_MM_HH_MM_STRATEGY,
            AllowedDatesFormates.DD_MM_AAAA_HH_MM: d.DD_MM_AAAA_HH_MM_STRATEGY,
            AllowedDatesFormates.MM_DD_AAAA_HH_MM: d.MM_DD_AAAA_HH_MM_STRATEGY,
            AllowedDatesFormates.AAAA_DD_MM_HH_MM: d.AAAA_DD_MM_HH_MM_STRATEGY,
            AllowedDatesFormates.AAAA_MM_DD_HH_MM: d.AAAA_MM_DD_HH_MM_STRATEGY,
            AllowedDatesFormates.DATE_IN_SPANISH: d.DATE_IN_SPANISH_STRATEGY,
            AllowedDatesFormates.DATETIME_IN_SPANISH: d.DATETIME_IN_SPANISH_STRATEGY,
            AllowedDatesFormates.DD_COMPLETE_MONTH_YYYY: d.DD_COMPLETE_MONTH_YYYY_STRATEGY,
            AllowedDatesFormates.DD_ABBREVIATE_MONTH_YYYY: d.DD_ABBREVIATE_MONTH_YYYY_STRATEGY,
        }
        self.field_instance = field_instance

    def get_dates_validate_value_strategy(self, format_date, location="detail"):
        """Returns the appropriate validation strategy for the given date format."""
        strategy_cls = self.strategies.get(format_date)
        if not strategy_cls:
            raise ValueError(f"No strategy found for input type: {format_date}")
        return strategy_cls(self.field_instance, location)
