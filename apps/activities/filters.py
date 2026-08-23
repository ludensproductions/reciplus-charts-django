import django_filters
from django_select2 import forms as s2forms

from apps.comun.filters import AbstractFilter

from . import consts as activities_consts
from .models import Activity

activity_fields = {
    "name": {"label": activities_consts.FILTER_NAME_LABEL},
    "location": {"label": activities_consts.FILTER_LOCATION_LABEL},
    "activity_type": {"label": activities_consts.FILTER_ACTIVITY_TYPE_LABEL},
}


class ActivityFilter(AbstractFilter):
    """Filter for Activity model with Select2 multiple choice for activity type."""

    activity_type = django_filters.MultipleChoiceFilter(
        field_name="activity_type",
        label=activities_consts.FILTER_ACTIVITY_TYPE_LABEL,
        choices=[
            ("WORKSHOP", activities_consts.ACTIVITY_TYPE_WORKSHOP),
            ("CONFERENCE", activities_consts.ACTIVITY_TYPE_CONFERENCE),
            ("WEBINAR", activities_consts.ACTIVITY_TYPE_WEBINAR),
        ],
        widget=s2forms.Select2MultipleWidget(
            attrs={
                "data-theme": "bootstrap-5",
                "data-placeholder": activities_consts.FILTER_ACTIVITY_TYPES_PLACEHOLDER,
                "style": "width: 100%;",
            }
        ),
    )

    class Meta:
        """Meta configuration for ActivityFilter."""

        model = Activity
        fields = list(activity_fields.keys())
        fields_dict = activity_fields
