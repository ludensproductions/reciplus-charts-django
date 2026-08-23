import operator
from functools import reduce

from django import forms
from django.conf import settings
from django.contrib.admin.utils import lookup_spawns_duplicates
from django.db.models import Q
from django_select2 import forms as s2forms
from django_select2.forms import ModelSelect2Widget

from apps.comun import consts as comun_consts


class GenericSelect2Widget(ModelSelect2Widget):
    """Generic Select2 widget with customizable model, search fields, and dependencies."""

    def __init__(
        self,
        model=None,
        search_fields=None,
        attrs=None,
        dependent_fields=None,
        **kwargs,
    ):
        self.model = model
        self.search_fields = search_fields or []
        self.dependent_fields = dependent_fields or {}

        if self.dependent_fields:
            self.require_dependencies = True

        super().__init__(
            attrs={
                "data-placeholder": comun_consts.SELECT2_EMPTY_PLACEHOLDER,
                "data-width": "100%",
                "data-theme": "bootstrap-5",
                "data-minimum-input-length": 0,
                **(attrs or {}),
            },
            **kwargs,
        )

    def get_queryset(self):
        """Return all objects from the configured model."""
        return self.model.objects.all()

    def filter_queryset(self, request, term, queryset=None, **dependent_fields):
        """Return QuerySet filtered by search_fields matching the passed term.

        Args:
            request (django.http.request.HttpRequest): The request is being passed from
                the JSON view and can be used to dynamically alter the response queryset.
            term (str): Search term
            queryset (django.db.models.query.QuerySet): QuerySet to select choices from.
            **dependent_fields: Dependent fields and their values. If you want to inherit
                from ModelSelect2Mixin and later call to this method, be sure to pop
                everything from keyword arguments that is not a dependent field.

        Returns:
            QuerySet: Filtered QuerySet

        """
        if queryset is None:
            queryset = self.get_queryset()
        search_fields = self.get_search_fields()
        select = Q()

        use_distinct = False
        if search_fields and term:
            for bit in term.split():
                or_queries = [Q(**{orm_lookup: bit}) for orm_lookup in search_fields]
                select &= reduce(operator.or_, or_queries)
            or_queries = [Q(**{orm_lookup: term}) for orm_lookup in search_fields]
            select |= reduce(operator.or_, or_queries)
            use_distinct |= any(
                lookup_spawns_duplicates(queryset.model._meta, search_spec) for search_spec in search_fields
            )

        if dependent_fields:
            select &= Q(**dependent_fields)

        use_distinct |= any(
            lookup_spawns_duplicates(queryset.model._meta, search_spec) for search_spec in dependent_fields.keys()
        )

        try:
            queryset = queryset.filter(select)

            if use_distinct:
                return queryset.distinct()
        except Exception:
            # If the queryset is not valid, return an empty queryset
            return queryset.none()
        return queryset


class TruncateLabelMixin:
    """Truncate option labels to a fixed length for Select2 widgets.

    Works for:
    - Classic <select> widgets (via optgroups override)
    - ModelSelect2 (AJAX-backed) widgets (via label_from_instance)

    Usage: include this mixin first in the base classes of your widget.
    You can customize the maximum length passing truncate_length in __init__.
    """

    truncate_length = 50  # default maximum characters

    def __init__(self, *args, truncate_length: int | None = None, **kwargs):
        if truncate_length is not None:
            self.truncate_length = int(truncate_length)
        super().__init__(*args, **kwargs)

    def _truncate(self, text: object) -> str:
        if text is None:
            return ""
        s = str(text)
        max_len = getattr(self, "truncate_length", 50)
        if len(s) <= max_len:
            return s
        # Use ellipsis and keep total length <= max_len
        return f"{s[: max(0, max_len - 1)]}…"

    def label_from_instance(self, obj):  # type: ignore[override]
        """Get truncated label from instance for AJAX-backed Select2 widgets."""
        try:
            label = super().label_from_instance(obj)  # type: ignore[attr-defined]
        except AttributeError:
            label = str(obj)
        return self._truncate(label)

    # For classic <select> widgets (static choices)
    def optgroups(self, name, value, attrs=None):  # type: ignore[override]
        """Truncate option labels for classic select widgets with static choices."""
        groups = super().optgroups(name, value, attrs)
        for _, group_options, _ in groups:
            for option in group_options:
                # Option dict contains label and attrs
                original = str(option.get("label", ""))
                truncated = self._truncate(original)
                option["label"] = truncated
                option.setdefault("attrs", {})
                if original:
                    option["attrs"]["title"] = original
                try:
                    option["attrs"]["data-max-length"] = str(len(original))
                except Exception:
                    option["attrs"]["data-max-length"] = "0"
        return groups


class ModelSelect2WidgetMixin:
    """Mixin providing common attributes configuration for ModelSelect2 widgets."""

    def build_attrs(self, base_attrs, extra_attrs):
        """Build widget attributes with default Select2 configuration."""
        extra_attrs.update(
            {
                "data-minimum-input-length": 0,
                "data-placeholder": comun_consts.SELECT2_EMPTY_PLACEHOLDER_ALT,
                "data-token-separators": "[]",  # Empty list of separators.
            }
        )
        return super().build_attrs(base_attrs, extra_attrs)

    def _get_cache_key(self):
        """Generate cache key for Select2 widget using UUID."""
        return f"{settings.SELECT2_CACHE_PREFIX}{self.uuid}"  # type: ignore


class Select2SingleTagWidget(s2forms.Select2TagMixin, s2forms.Select2Mixin, forms.Select):
    """Select2 widget with tag creation support and Bootstrap 5 theme."""

    theme = "bootstrap-5"


class HeavySelect2SingleTagWidget(ModelSelect2WidgetMixin, s2forms.HeavySelect2Mixin, Select2SingleTagWidget):
    """Heavy (AJAX-loaded) Select2 widget with tag creation support."""

    pass


class BaseModelSelect2MultipleWidget(ModelSelect2WidgetMixin, s2forms.ModelSelect2MultipleWidget):
    """Base ModelSelect2 widget for multiple selections."""

    theme = "bootstrap-5"
    require_dependencies = False


class BaseModelSelect2Widget(ModelSelect2WidgetMixin, s2forms.ModelSelect2Widget):
    """Base ModelSelect2 widget for single selection."""

    theme = "bootstrap-5"
    require_dependencies = False


# For get_or_create tag select2 fields
class ModelSelect2SingleTagWidget(s2forms.ModelSelect2Mixin, HeavySelect2SingleTagWidget):
    """Model-backed Select2 widget with tag creation support."""

    theme = "bootstrap-5"
    require_dependencies = False

    def value_from_datadict(self, data, files, name):  # noqa
        value = super().value_from_datadict(data, files, name)

        # If it's a prefixed tag creation, return raw value
        if isinstance(value, str) and value.startswith(comun_consts.NEW_PREFIX):
            return value

        return value

    def optgroups(self, name, value, attrs=None):  # noqa
        if value:
            if isinstance(value, str):
                if value.startswith(comun_consts.NEW_PREFIX):
                    # Do not attempt queryset resolution
                    return super().optgroups(name, [], attrs)

            elif isinstance(value, (list, tuple)):
                value = [v for v in value if not (isinstance(v, str) and v.startswith(comun_consts.NEW_PREFIX))]

        return super().optgroups(name, value, attrs)


class BaseModelSelect2TagWidget(ModelSelect2WidgetMixin, s2forms.ModelSelect2TagWidget):
    """Base ModelSelect2 widget with tag creation support."""

    theme = "bootstrap-5"
    require_dependencies = False

    def optgroups(self, name, value, attrs=None):  # noqa
        if value:
            if isinstance(value, str):
                if value.startswith(comun_consts.NEW_PREFIX):
                    # Do not attempt queryset resolution
                    return super().optgroups(name, [], attrs)

            elif isinstance(value, (list, tuple)):
                value = [v for v in value if not (isinstance(v, str) and v.startswith(comun_consts.NEW_PREFIX))]

        return super().optgroups(name, value, attrs)


class TruncateAttrsMixin:
    """Adds data attribute to expose truncate length only for truncated widgets."""

    def build_attrs(self, base_attrs, extra_attrs):  # type: ignore[override]
        """Build attributes including truncate length for widget."""
        extra_attrs = dict(extra_attrs or {})
        extra_attrs["data-truncate-length"] = getattr(self, "truncate_length", 50)
        return super().build_attrs(base_attrs, extra_attrs)


# New truncated widgets that DO NOT affect existing ones
class TruncatedSelect2SingleTagWidget(
    TruncateAttrsMixin, TruncateLabelMixin, s2forms.Select2TagMixin, s2forms.Select2Mixin, forms.Select
):
    """Plain Select2 with tags support, truncates static choices to 50 chars by default."""


class TruncatedBaseModelSelect2Widget(
    TruncateAttrsMixin, TruncateLabelMixin, ModelSelect2WidgetMixin, s2forms.ModelSelect2Widget
):
    """Model-backed Select2 single, truncates labels to 50 chars by default."""

    theme = "bootstrap-5"
    require_dependencies = False


class TruncatedBaseModelSelect2MultipleWidget(
    TruncateAttrsMixin, TruncateLabelMixin, ModelSelect2WidgetMixin, s2forms.ModelSelect2MultipleWidget
):
    """Model-backed Select2 multiple, truncates labels to 50 chars by default."""

    theme = "bootstrap-5"
    require_dependencies = False


class TruncatedModelSelect2SingleTagWidget(
    TruncateAttrsMixin, TruncateLabelMixin, s2forms.ModelSelect2Mixin, HeavySelect2SingleTagWidget
):
    """Model-backed Select2 with tags, truncates server-provided labels to 50 chars by default."""

    theme = "bootstrap-5"
    require_dependencies = False
