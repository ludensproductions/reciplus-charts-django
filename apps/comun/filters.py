import django_filters
from django.forms import HiddenInput

from apps.comun.filter_fields import CommaSeparatedFilter

from .consts import DJANGO_LOOKUP_EXPRESSIONS


# The `AbstractFilter` class in Python is a Django filter set that customizes filter fields and
class AbstractFilter(django_filters.FilterSet):
    """Base filter set with shared widget and soft-delete behavior."""

    id = CommaSeparatedFilter(field_name="id")

    # The class `Meta` in Python contains abstract attributes and a dictionary for fields.
    class Meta:
        abstract = True
        fields_dict = {}

    def filter_queryset(self, queryset):
        """Apply form-derived filters while excluding soft-deleted related records."""
        if not self.is_bound or not self.form.is_valid():
            return queryset.distinct()

        filtered_queryset = queryset.all()

        for field_name, value in self.form.cleaned_data.items():
            if value in (None, "", [], (), {}):
                continue

            filter_instance = self.filters.get(field_name)
            if filter_instance is None:
                continue

            field_path = getattr(filter_instance, "field_name", field_name)
            path_parts = field_path.split("__")

            has_explicit_lookup = path_parts[-1] in DJANGO_LOOKUP_EXPRESSIONS
            base_parts = path_parts[:-1] if has_explicit_lookup else path_parts

            # No related path, apply the filter normally
            if len(base_parts) < 2:
                filtered_queryset = filter_instance.filter(filtered_queryset, value)
                continue

            relation_path = "__".join(base_parts[:-1])

            if has_explicit_lookup:
                lookup_key = field_path
            else:
                lookup_expr = getattr(filter_instance, "lookup_expr", "exact")
                lookup_key = field_path if lookup_expr == "exact" else f"{field_path}__{lookup_expr}"

            lookup_kwargs = {lookup_key: value}
            relation_filter = {f"{relation_path}__deleted__isnull": True}
            filtered_queryset = filtered_queryset.filter(**lookup_kwargs, **relation_filter)

        return filtered_queryset.distinct()

    def __init__(self, *args, **kwargs):
        """The function initializes filters for fields in a Django model form, setting labels, attributes, and input types based on field types."""
        super().__init__(*args, **kwargs)

        fields_dict = self.Meta.fields_dict

        for field_name in self.get_fields():
            label = fields_dict[field_name]["label"]
            self.filters[field_name].label = label
            self.filters[field_name].field.widget.attrs.update(
                {
                    "class": "form-control",
                    "placeholder": fields_dict[field_name].get("placeholder", label),
                },
            )

            # If it's an input field, change it so that it uses contains
            if self.filters[field_name].__class__.__name__ == "CharFilter":
                self.filters[field_name].lookup_expr = "icontains"

            elif self.filters[field_name].__class__.__name__ == "DateFilter":
                self.filters[field_name].field.widget.input_type = "date"

            elif self.filters[field_name].__class__.__name__ == "DateTimeFilter":
                self.filters[field_name].field.widget.input_type = "datetime-local"

            elif self.filters[field_name].__class__.__name__ == "TimeFilter":
                self.filters[field_name].field.widget.input_type = "time"

            elif "ChoiceFilter" in self.filters[field_name].__class__.__name__:
                self.filters[field_name].field.widget.attrs.update(
                    {"class": "select form-select"},
                )

        if not "id" in fields_dict:
            print("No id field")
            self.filters["id"].field.widget = HiddenInput()

        elif fields_dict["id"].get("hidden", True):
            print("Hidden id field")
            self.filters["id"].field.widget = HiddenInput()


def create_generic_filter(modelo, fields_dicts):
    """Create a dynamic filter class for a model and field configuration."""

    class DynamicFilter(AbstractFilter):
        class Meta:
            model = modelo
            fields_dict = fields_dicts
            fields = list(fields_dicts.keys())

    return DynamicFilter
