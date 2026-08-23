from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import FieldDoesNotExist, ValidationError
from django.core.validators import RegexValidator
from django.db.models import Model
from django.utils.translation import gettext_lazy as _

from apps.comun.consts import NEW_PREFIX
from apps.comun.fields import DisplayNameField
from apps.comun.models import AbstractModel, AbstractNullableModel
from apps.comun.regex_validators import regex_flags_to_str


class AbstractModelForm(forms.ModelForm):
    """AbstractModelForm base class for model forms."""

    class Meta:
        """Meta options for AbstractModelForm.

        Attributes:
            exclude (list): Fields to exclude from the form.
            abstract (bool): Whether the form is abstract.
        """

        exclude = ["created_by", "deleted", "updated_by"]
        abstract = True
        # required_user = True

    def __init__(self, *args, **kwargs):
        """Initializes the form and sets up field attributes and validators.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments. Can include 'user'.
        """
        self.user = kwargs.pop("user", None)
        # self.required_user = getattr(self._meta, "required_user", False)
        super().__init__(*args, **kwargs)
        model = self._meta.model._meta
        for field_name, field in self.fields.items():
            try:
                model_field = model.get_field(field_name)
            except FieldDoesNotExist:
                # Si el campo no existe en el modelo, simplemente saltar
                continue

            if isinstance(field, (SingleTagField, MultipleTagField)):
                field.user = self.user

            for validator in getattr(model_field, "validators", []):
                if isinstance(validator, RegexValidator):
                    field.widget.attrs.setdefault("regex-pattern", validator.regex.pattern)
                    field.widget.attrs.setdefault("regex-flags", regex_flags_to_str(validator.regex.flags))

            if field.widget.attrs.get("placeholder") is not None:
                continue

            if hasattr(model, field_name):
                field.widget.attrs["placeholder"] = model_field.verbose_name.capitalize()

    def save(self, commit=True):
        """Saves the form instance, setting user fields if applicable.

        Args:
            commit (bool): Whether to save the instance to the database.

        Returns:
            object: The saved model instance.
        """
        instance = super().save(commit=False)
        # self.required_user = getattr(self._meta, "required_user", False)
        # self.required_user and
        if issubclass(self._meta.model, AbstractModel) or issubclass(self._meta.model, AbstractNullableModel):
            if instance.id is None:
                instance.created_by = self.user
            else:
                instance.updated_by = self.user
        if commit:
            instance.save()
        return instance


class ModelChoiceFieldNoValidationAllowNull(forms.ModelChoiceField):
    """ModelChoiceField that allows null values without validation."""

    def clean(self, value):
        """Validates the given value and returns its cleaned value.

        Args:
            value: The value to clean.

        Returns:
            object or None: The cleaned value or None if empty.

        Raises:
            ValidationError: If the value is invalid.
        """
        if value == "":
            return None
        try:
            value = self.queryset.model.objects.get(pk=value)
        except self.queryset.model.DoesNotExist:
            raise ValidationError(self.error_messages["invalid_choice"], code="invalid_choice")

        return value


class ModelChoiceFieldNoValidation(forms.ModelChoiceField):
    """ModelChoiceField that skips validation for null values."""

    def clean(self, value):
        """Validates the given value and returns its cleaned value.

        Args:
            value: The value to clean.

        Returns:
            object: The cleaned value.

        Raises:
            ValidationError: If the value is invalid or required.
        """
        if value == "":
            raise ValidationError(self.error_messages["required"], code="required")

        try:
            value = self.queryset.model.objects.get(pk=value)
        except self.queryset.model.DoesNotExist:
            raise ValidationError(self.error_messages["invalid_choice"], code="invalid_choice")

        return value


class EmptyForm(forms.Form):
    """Empty form with optional user attribute."""

    def __init__(self, *args, **kwargs):
        """Initializes the form, optionally with a user.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments. Can include 'user'.
        """
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)


class GenericBaseFormSet(forms.BaseFormSet):
    """Base formset with generic validation logic."""

    def clean(self):
        """Performs generic validation for the formset.

        Raises:
            ValidationError: If any required field is missing in a form.
        """
        super().clean()
        if any(self.errors):
            # Don't bother validating the formset unless each form is valid on its own
            return

        for form in self.forms:
            for field_name, field in form.fields.items():
                if field.required and field_name not in form.cleaned_data:
                    form.add_error(field_name, _("Este campo es requerido."))


class GenericBaseInlineFormSet(forms.BaseInlineFormSet):
    """Base inline formset with generic validation logic."""

    def clean(self):
        """Performs generic validation for the inline formset.

        Raises:
            ValidationError: If any required field is missing in a form.
        """
        super().clean()
        if any(self.errors):
            # Don't bother validating the formset unless each form is valid on its own
            return

        for form in self.forms:
            for field_name, field in form.fields.items():
                if field.required and field_name not in form.cleaned_data:
                    form.add_error(field_name, _("Este campo es requerido."))


class AuthenticationForm(AuthenticationForm):
    """Authentication form with custom password field."""

    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password", "placeholder": _("Password")}),
    )


class TruncatedModelChoiceField(forms.ModelChoiceField):
    """ModelChoiceField that truncates long labels for display."""

    """A ModelChoiceField that truncates long labels for display.

    Args:
        truncate_length (int): Maximum length of the label before truncation.
        *args: Variable length argument list for ModelChoiceField.
        **kwargs: Arbitrary keyword arguments for ModelChoiceField.
    """

    def __init__(self, truncate_length=50, *args, **kwargs):
        """Initializes the field and sets the truncate length.

        Args:
            truncate_length (int, optional): Maximum label length. Defaults to 50.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        self.truncate_length = int(truncate_length)
        super().__init__(*args, **kwargs)
        # Expose the truncate length for frontend usage/debugging
        try:
            self.widget.attrs["data-truncate-length"] = str(self.truncate_length)
        except Exception:
            # In case a custom widget without attrs mapping is provided
            pass

    def label_from_instance(self, obj):
        """Returns a possibly truncated label for the given model instance.

        Args:
            obj: The model instance.

        Returns:
            str: The (possibly truncated) label.
        """
        label = super().label_from_instance(obj)
        if len(label) > self.truncate_length:
            return label[: self.truncate_length] + "..."

        return label


class BaseTagField:  # noqa
    default_error_messages = {
        "permission_denied": _("You don't have permission to create this item."),
        "invalid_new_value": _("Invalid value for new item."),
    }

    def _normalize(self, value) -> str:
        """Normalize a raw input string into a canonical form for lookup.

        The default implementation trims whitespace; override if different
        normalization (e.g., case folding or slugification) is needed.
        """
        if self._is_prefixed(value):
            value = value[len(NEW_PREFIX) :]
        return value.strip()

    def _is_prefixed(self, value) -> bool:
        return isinstance(value, str) and value.startswith(NEW_PREFIX)

    def _model_has_display_name(self):
        try:
            field = self.queryset.model._meta.get_field("display_name")
            return isinstance(field, DisplayNameField)
        except FieldDoesNotExist:
            return False

    def _build_defaults(self, value: str) -> dict:
        """Build defaults dict for `get_or_create` when creating instances.

        If the model defines `display_name` this will include
        `{'display_name': value}` so new instances get a friendly label.
        """
        defaults = {}

        if self._model_has_display_name():
            defaults["display_name"] = value

        if self.user:
            defaults["created_by"] = self.user

        return defaults

    def _can_create(self, value: str, model: type[Model]) -> bool:
        """Decide whether a new instance may be created.

        Semantics for `self.allow_create` (set on the concrete fields):
        - None (default): require Django model add permission when a user is provided
        - True: always allow creation
        - False: never allow creation
        - callable(user, model, value) -> bool: custom decision
        """
        allow = getattr(self, "allow_create", None)

        if callable(allow):
            try:
                return bool(allow(self.user, model, value))
            except Exception:
                return False

        if isinstance(allow, bool):
            return allow

        # Default: require user and the model add permission
        if not self.user:
            return False

        perm = f"{model._meta.app_label}.add_{model._meta.model_name}"
        try:
            return self.user.has_perm(perm)
        except Exception:
            return False


class SingleTagField(BaseTagField, forms.ModelChoiceField):
    """A ModelChoiceField that supports selecting or creating single tag-like models.

    Use this field when a form should accept either an existing model
    (selected by primary key) or create a new instance from a free-form
    value. New values are indicated by an input prefixed with
    `new_prefix` (by default "new_"). When creating a new instance the
    field will populate the provided `create_field` and, if available,
    optionally set a `display_name` field on the model.

    Attributes:
        new_prefix (str): Prefix that signals creation of a new instance.
        create_field (str): Model field name used to look up/create instances
            (e.g., 'name' or 'slug'). This is set during initialization.
    """

    def __init__(self, *args, create_field: str, user=None, allow_create=None, **kwargs):
        """Initialize the field.

        Args:
            *args: Positional args forwarded to `forms.ModelChoiceField`.
            create_field (str): Required. The model field name used when
                creating a new instance (e.g., 'name').
            user: Instance of the current user.
            allow_create: A bool or callable instance to determine if is allowed to create new objects.
                Default value is None. If value isn't set, then it uses user.has_perm by default to determine
                if user is allowed to create new objects. If it is a callable, it should receive this:
                `callable(user, model, value)`.
            **kwargs: Keyword args forwarded to `forms.ModelChoiceField`.
        """
        self.create_field = create_field
        self.user = user
        self.allow_create = allow_create
        super().__init__(*args, **kwargs)

    def prepare_value(self, value):
        """Ensure prefixed raw values don't crash widget rendering."""
        if isinstance(value, str) and value.startswith(NEW_PREFIX):
            return value  # Let Select2 re-display the raw input

        return super().prepare_value(value)

    def to_python(self, value):  # noqa
        if value in self.empty_values:
            return super().to_python(value)

        if not isinstance(value, str):
            return super().to_python(value)

        model = self.queryset.model

        if not self._is_prefixed(value):
            # Not prefixed — use standard PK resolution
            return super().to_python(value)

        value = self._normalize(value)

        if not self._can_create(value, model):
            raise forms.ValidationError(
                self.error_messages["permission_denied"],
                code="permission_denied",
            )

        if not value:
            raise forms.ValidationError(
                self.error_messages["invalid_new_value"],
                code="invalid_new_value",
            )

        instance, _ = model.objects.get_or_create(**{self.create_field: value}, defaults=self._build_defaults(value))
        return instance


class MultipleTagField(BaseTagField, forms.ModelMultipleChoiceField):
    """A ModelMultipleChoiceField that selects or creates multiple tag-like models.

    This field accepts a sequence of values where each value may be either
    an existing model primary key or a special prefixed string that signals
    creation of a new instance (prefix defined by `new_prefix`). The field
    resolves each input item to a model instance using `_resolve_single`, and
    returns a queryset filtered on the resolved primary keys (as expected by
    Django forms for multiple choice model fields).

    Attributes:
        new_prefix (str): Prefix that signals creation of a new instance.
        create_field (str): Model field name used to create/get instances
            when the input indicates a new value (set via `__init__`).
    """

    def __init__(self, *args, create_field: str, user=None, allow_create=None, **kwargs):
        """Initialize the MultipleTagField.

        Args:
            *args: Positional args forwarded to `forms.ModelMultipleChoiceField`.
            create_field (str): Required. Field name on the model to use when
                creating new instances (e.g., 'name').
            user: Instance of the current user.
            allow_create: A bool or callable instance to determine if is allowed to create new objects.
                Default value is None. If value isn't set, then it uses user.has_perm by default to determine
                if user is allowed to create new objects. If it is a callable, it should receive this:
                `callable(user, model, value)`.
            **kwargs: Keyword args forwarded to `forms.ModelMultipleChoiceField`.
        """
        self.create_field = create_field
        self.user = user
        self.allow_create = allow_create
        super().__init__(*args, **kwargs)

    def _resolve_single(self, raw_value):
        """Resolve a single raw input into a model instance.

        It removes the `new_prefix` when present, normalizes the value, and
        falls back to `get_or_create` using the configured `create_field`.

        Args:
            raw_value: A single item from the incoming value sequence.

        Returns:
            A model instance corresponding to `raw_value`.
        """
        model = self.queryset.model

        value = self._normalize(raw_value)

        # Fallback to create
        if not self._can_create(value, model):
            raise forms.ValidationError(
                self.error_messages["permission_denied"],
                code="permission_denied",
            )

        if not value:
            raise forms.ValidationError(
                self.default_error_messages["invalid_new_value"],
                code="invalid_new_value",
            )

        instance, _ = model.objects.get_or_create(**{self.create_field: value}, defaults=self._build_defaults(value))

        return instance

    def clean(self, value):  # noqa
        if not value:
            return super().clean(value)

        resolved_pks = []

        for item in value:
            if self._is_prefixed(item):
                instance = self._resolve_single(item)
                resolved_pks.append(instance.pk)
            else:
                resolved_pks.append(item)

        return super().clean(resolved_pks)
