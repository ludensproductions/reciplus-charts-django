from apps.comun.filters import AbstractFilter

from . import consts as event_planner_consts
from .models import Event

event_fields = {
    "title": {"label": event_planner_consts.FILTER_TITLE_LABEL},
    "date_start": {"label": event_planner_consts.FILTER_DATE_START_LABEL},
    "location": {"label": event_planner_consts.FILTER_LOCATION_LABEL},
    "event_activity__capacity": {"label": event_planner_consts.FILTER_ACTIVITY_CAPACITY_LABEL},
    "event_activity__activity__name": {"label": event_planner_consts.FILTER_ACTIVITY_NAME_LABEL},
    "event_activity__activity": {"label": event_planner_consts.FILTER_ACTIVITY_LABEL},
    "event_activity__activity__activity_type": {"label": event_planner_consts.FILTER_ACTIVITY_TYPE_LABEL},
    "responsible": {"label": event_planner_consts.FILTER_RESPONSIBLE_LABEL},
    "folio": {"label": event_planner_consts.FILTER_FOLIO_LABEL},
}


class EventFilter(AbstractFilter):
    """Filter for Event model with custom filtering methods for related fields."""

    class Meta:
        """Meta options for EventFilter."""

        model = Event
        fields = list(event_fields.keys())
        fields_dict = event_fields

    def filter_event_activity__activity__activity_type(self, queryset, name, value):
        """Filter by activity type in related event activity.

        Args:
            queryset: The queryset to filter.
            name (str): The field name.
            value: The value to filter by.

        Returns:
            QuerySet: The filtered queryset.
        """
        if value:
            return queryset.filter(
                event_activity__activity__activity_type=value,
                event_activity__deleted__isnull=True,
                event_activity__activity__deleted__isnull=True,
            )
        return queryset

    def filter_event_activity__activity__name(self, queryset, name, value):
        """Filter by activity name in related event activity.

        Args:
            queryset: The queryset to filter.
            name (str): The field name.
            value: The value to filter by.

        Returns:
            QuerySet: The filtered queryset.
        """
        if value:
            return queryset.filter(
                event_activity__activity__name__icontains=value,
                event_activity__deleted__isnull=True,
                event_activity__activity__deleted__isnull=True,
            )
        return queryset

    def filter_event_activity__capacity(self, queryset, name, value):
        """Filter by capacity in related event activity.

        Args:
            queryset: The queryset to filter.
            name (str): The field name.
            value: The value to filter by.

        Returns:
            QuerySet: The filtered queryset.
        """
        if value:
            return queryset.filter(
                event_activity__capacity=value,
                event_activity__deleted__isnull=True,
            )
        return queryset

    def event_activity__activity(self, queryset, name, value):
        """Filter by activity in related event activity.

        Args:
            queryset: The queryset to filter.
            name (str): The field name.
            value: The value to filter by.

        Returns:
            QuerySet: The filtered queryset.
        """
        if value:
            return queryset.filter(
                event_activity__activity=value,
                event_activity__deleted__isnull=True,
                event_activity__activity__deleted__isnull=True,
            )
        return queryset

    def __init__(self, *args, **kwargs):
        """Initialize the filter and assign custom filter methods and labels.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        super().__init__(*args, **kwargs)
        # Assign custom filtering methods.
        self.filters[
            "event_activity__activity__activity_type"
        ].method = self.filter_event_activity__activity__activity_type
        self.filters["event_activity__activity__name"].method = self.filter_event_activity__activity__name
        self.filters["event_activity__capacity"].method = self.filter_event_activity__capacity
        self.filters["event_activity__activity"].method = self.event_activity__activity

        self.filters["event_activity__activity"].field.label_from_instance = lambda obj: (
            event_planner_consts.ACTIVITY_LABEL_WITH_PIPE.format(name=obj.name, location=obj.location)
        )
        self.filters["responsible"].field.label_from_instance = lambda obj: (
            event_planner_consts.RESPONSIBLE_LABEL_WITH_DASH.format(
                first_name=obj.first_name,
                last_name=obj.last_name,
            )
        )
