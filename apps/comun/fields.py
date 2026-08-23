from django import forms
from django.db import models


class DisplayNameField(models.CharField):
    """A CharField subclass that carries an optional `display_name` string.

    This field behaves like a standard `models.CharField` but stores an
    additional attribute `display_name` that can be used by views, forms,
    or admin helpers to provide an alternate human-friendly label for the
    field (for example, when choosing which field to show as the object's
    label in lists or select widgets).

    Attributes:
        display_name (str | None): Optional string to be used as the display
            label for the model field. When set to a non-empty string, it
            indicates this field should be used as the display name for an
            object in listings or selects. Defaults to ``None``.
    """

    def __init__(self, *args, display_name=None, **kwargs):
        """Initialize the DisplayNameField.

        Args:
            *args: Positional arguments forwarded to `models.CharField`.
            display_name (str, optional): Optional string to use as the
                display label for this field (e.g. shown in lists or select
                widgets). If not provided, the value is ``None`` and the
                field is not specially marked as a display name.
            **kwargs: Keyword arguments forwarded to `models.CharField`.
        """
        self.display_name = display_name
        super().__init__(*args, **kwargs)


class PropertyField:
    """A class that creates property-like fields for Django models.

    This class is used to create field-like objects for model properties,
    allowing them to be treated similarly to regular model fields in views.

    Attributes:
        name (str): The name of the property
        verbose_name (str): A human-readable name for the property, defaults to the titlecased name
        is_property (bool): Always True, indicates this is a property field
    """

    def __init__(view, name, verbose_name):
        """Initialize a new PropertyField instance.

        Args:
            name (str): The name of the property
            verbose_name (str, optional): A human-readable name for the property.
                If not provided, converts the name from snake_case to Title Case.
        """
        view.name = name
        view.verbose_name = verbose_name or name.replace("_", " ").title()
        view.is_property = True

    def value_from_object(view, obj):
        """Get the property value from a model instance.

        Args:
            obj: The model instance to get the property value from

        Returns:
            The value of the property for the given object
        """
        return getattr(obj, view.name)


class PipeSeparatedMultipleChoiceField(forms.ModelMultipleChoiceField):
    """A MultipleChoiceField that accepts pipe-separated strings.

    This field accepts input values in the following forms:
    - a list of values
    - a single string where items are separated by the pipe character (`|`)
    - a single-element list containing a pipe-separated string

    The class normalizes these inputs into a sequence of individual values
    before delegating to the parent `ModelMultipleChoiceField` behavior.
    """

    def to_python(self, value):
        """Normalize the incoming value into an iterable of values.

        Args:
            value: The raw input value which may be a string or list.

        Returns:
            A list/iterable of items suitable for the parent field's
            `to_python` processing.
        """
        if isinstance(value, list):
            if len(value) == 1 and isinstance(value[0], str) and "|" in value[0]:
                value = value[0].split("|")
        elif isinstance(value, str):
            value = value.split("|")
        return super().to_python(value)

    def prepare_value(self, value):
        """Prepare a value for rendering in a form widget.

        This method handles several input shapes:
        - pipe-separated strings are split into lists
        - lists with model instances are converted to a list of primary key
          strings (as expected by form widgets)

        Args:
            value: The value to prepare for widget rendering.

        Returns:
            A widget-friendly representation of the value.
        """
        if isinstance(value, str) and "|" in value:
            value = value.split("|")

        if isinstance(value, list) and len(value) == 1 and isinstance(value[0], str) and "|" in value[0]:
            value = value[0].split("|")

        if isinstance(value, list) and value and hasattr(value[0], "pk"):
            value = [str(item.pk) for item in value]

        return super().prepare_value(value)

    def clean(self, value):
        """Validate and convert the input to Python objects.

        This method first normalizes the input via `to_python`, then calls
        the parent's `clean` to perform validation and model lookups.

        Args:
            value: Raw input from the form.

        Returns:
            A queryset/list of model instances corresponding to the input.
        """
        value = self.to_python(value)
        return super().clean(value)


class MultiFileField(forms.FileField):
    """A FileField variant that accepts multiple files and returns a list.

    Use this field when a form allows uploading multiple files for a single
    field name. The `clean` method returns a list of cleaned file objects
    (empty list when no files are provided).
    """

    def __init__(self, *args, **kwargs):
        """Initialize the MultiFileField.

        Args:
            *args: Positional args forwarded to `forms.FileField`.
            **kwargs: Keyword args forwarded to `forms.FileField`.
        """
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        """Validate and clean multiple uploaded files.

        Args:
            data: The incoming file data. Can be None, a single file, or a
                sequence of files.
            initial: Optional initial file value (passed to parent `clean`).

        Returns:
            A list of cleaned file objects. Returns an empty list when
            `data` is None.
        """
        if data is None:
            return []
        if not isinstance(data, (list, tuple)):
            data = [data]
        result = []
        for item in data:
            result.append(super().clean(item, initial))
        return result
