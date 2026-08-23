import django_filters
from django.contrib.postgres.fields import DateRangeField
from django.db.backends.postgresql.psycopg_any import DateRange
from django_filters.widgets import RangeWidget

from apps.comun.filters import AbstractFilter

from .consts import RESERVATION_FILTER_FIELDS
from .models import Reservation


class DateRangeOverlapFilter(django_filters.Filter):
    """Filter that matches overlapping date ranges from a widget input."""

    def filter(self, qs, value):
        """Apply overlap filtering using start/stop values.

        Args:
            qs (QuerySet): Base queryset to filter.
            value (list | None): List with [start, stop] dates.

        Returns:
            QuerySet: Filtered queryset.
        """
        if value:
            # value is a list [start, stop] from RangeWidget
            start = value[0] if len(value) > 0 else None
            stop = value[1] if len(value) > 1 else None

            if start and stop:
                date_range = DateRange(start, stop)
                return qs.filter(**{f"{self.field_name}__overlap": date_range})
            elif start:
                return qs.filter(**{f"{self.field_name}__startswith__gte": start})
            elif stop:
                return qs.filter(**{f"{self.field_name}__endswith__lte": stop})
        return qs


class ReservationFilter(AbstractFilter):
    """Filter set for reservations and booking date ranges."""

    class Meta:
        model = Reservation
        fields = list(RESERVATION_FILTER_FIELDS.keys())
        fields_dict = RESERVATION_FILTER_FIELDS
        filter_overrides = {
            DateRangeField: {
                "filter_class": DateRangeOverlapFilter,
                "extra": lambda f: {
                    "lookup_expr": "overlap",
                    "widget": RangeWidget(attrs={"type": "date"}),
                },
            },
        }
