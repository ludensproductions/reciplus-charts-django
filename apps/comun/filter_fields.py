import django_filters

from apps.comun.fields import PipeSeparatedMultipleChoiceField
from apps.comun.forms import TruncatedModelChoiceField


class CommaSeparatedFilter(django_filters.Filter):
    def filter(self, qs, value):
        if not value:
            return qs
        values = value.split(",")
        return qs.filter(id__in=values)


class PipeSeparatedMultipleChoiceFilter(django_filters.ModelMultipleChoiceFilter):
    field_class = PipeSeparatedMultipleChoiceField

    def filter(self, qs, value):
        if value and isinstance(value, str):
            try:
                value = [int(v.strip()) for v in value.split("|") if v.strip()]
            except ValueError:
                value = [v.strip() for v in value.split("|") if v.strip()]
        return super().filter(qs, value)


class TruncatedModelChoiceFilter(django_filters.ModelChoiceFilter):
    field_class = TruncatedModelChoiceField

    def __init__(self, truncate_length=50, *args, **kwargs):
        self.truncate_length = truncate_length
        super().__init__(*args, **kwargs)

    @property
    def field(self):
        value = super().field
        try:
            value.truncate_length = self.truncate_length
            # Expose the truncate length for frontend usage/debugging
            value.widget.attrs["data-truncate-length"] = str(value.truncate_length)
        except Exception:
            # In case a custom widget without attrs mapping is provided
            pass
        return value
