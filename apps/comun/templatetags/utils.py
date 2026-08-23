import datetime
import os

from django import template
from django.conf import settings
from django.core.handlers.asgi import ASGIRequest
from django.urls import reverse

from apps.comun.consts import DEFAULT_GRID_CLASSES, DEFAULT_RENDERABLE_CLASSES

register = template.Library()


def date_match_format(date):
    """Check if the given date string matches the expected format and return it in a human-readable format if it does.

    Args:
        date (str): The date string to be checked and formatted.

    Returns:
        str or bool: The formatted date string if it matches the expected format, otherwise False.
    """
    try:
        date = datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S%z")
        date = date.strftime("%d/%m/%Y %H:%M:%S")
        return date
    except TypeError:
        return False
    except ValueError:
        return False


@register.filter
def format_date(value):
    """Wrapper for date matching formatting in templates."""
    return date_match_format(value)


@register.filter
def get_type(value):
    """Get the type of a value as a string, with special handling for date strings."""
    if date_match_format(value):
        return "date"
    type = value.__class__.__name__
    return type


@register.filter()
def get_field_type(field):
    """Get the type of a field as a string.

    Args:
        field: The field whose type is to be determined.

    Returns:
        str: The name of the field's type.
    """
    return type(field).__name__


@register.filter()
def get_file_name(file_field):
    """Method to get the pure file name of a file.

    Args:
        file_field (Any): The file field from which to extract the file name. It can be a FileField, ImageField, or any object with a 'name' attribute.

    Returns:
        str: The pure file name of the given file field.
    """
    if not file_field:
        return ""
    return os.path.basename(file_field.name)


@register.filter
def get_format(field_attrs):
    """Get format and separator from field attributes.

    Args:
        field_attrs (dict): A dictionary of field attributes, expected to contain 'format' and 'separator' keys.

    Returns:
        tuple: A tuple containing the field format and separator, or (None, None) if field_attrs is not a dict.
    """
    if not isinstance(field_attrs, dict):
        return None

    field_format = field_attrs.get("format", None)
    separator = field_attrs.get("separator", "-")

    return field_format, separator


@register.simple_tag(takes_context=True)
def get_m2m_value(context, value):
    """Get a string representation of a ManyToMany field value."""
    if get_field_type(value) == "ManyRelatedManager" and hasattr(value, "all") and callable(getattr(value, "all")):
        items = value.all()
        separator: str = context["m2m_separator"]
        return separator.join([str(item) for item in items]).capitalize()

    return value


@register.filter(name="getattr")
def get_attr(model, field):
    """Get an attribute from a model or dict.

    If the field is a Django choices/TextChoices field, return its display label
    via get_<field>_display(). If the attribute itself is an Enum/TextChoices member,
    prefer its .label (then .value), else fallback to string/attribute value.

    For FileField/ImageField values, return an HTML anchor tag with the file URL
    (download link). For iterables of files, return a comma-separated list of anchors.
    """
    display_method_name = f"get_{field}_display"
    try:
        display_method = getattr(model, display_method_name, None)
        if callable(display_method):
            return display_method()
    except Exception:
        pass

    value = getattr(model, field, None)

    if value is None and isinstance(model, dict):
        value = model.get(field, "")

    return "" if value is None else value


@register.filter(name="dict_get")
def dict_get(mapping, key):
    """Safely get a key from a dict in templates.

    Usage: {{ mydict|dict_get:"some_key" }}
    Returns None when mapping is not a dict or key missing.
    """
    try:
        if isinstance(mapping, dict):
            return mapping.get(key)
    except Exception:
        pass
    return None


@register.simple_tag()
def get_classes(mapping: dict | None, key: str, can_render: bool) -> str:
    """Return CSS classes from a dict by key or a sensible default.

    - Accepts strings or list/tuple of class names.
    - When the key is missing/empty, returns DEFAULT_GRID_CLASSES.
    """
    try:
        value = None
        if isinstance(mapping, dict):
            value = mapping.get(key)

        if not value:
            if can_render:
                return DEFAULT_RENDERABLE_CLASSES

            return DEFAULT_GRID_CLASSES

        if isinstance(value, str):
            return value.strip() or DEFAULT_GRID_CLASSES

        if isinstance(value, (list, tuple)):
            joined = " ".join([str(v).strip() for v in value if v])
            return joined or DEFAULT_GRID_CLASSES

        # Unsupported type -> fallback
        return DEFAULT_GRID_CLASSES
    except Exception:
        return DEFAULT_GRID_CLASSES


@register.filter()
def truncate_value(value, max_len):
    """Truncate a string to a maximum length, adding an ellipsis if truncated.

    If value is None or empty, returns an empty string.
    If max_len is not a positive integer, returns the original value.
    """
    try:
        if value is None:
            return ""
        s = str(value)
        max_len = int(max_len)
        if max_len <= 0:
            return s
        if len(s) <= max_len:
            return s
        # Use ellipsis and keep total length <= max_len
        return f"{s[: max(0, max_len)]}…"
    except Exception:
        return value


@register.filter(name="dict_get_or")
def dict_get_or(mapping, keys: str):
    """Return the first present/non-empty value by trying multiple keys.

    keys: string separated by '|', e.g. "max_length|max-length".
    """
    if not isinstance(mapping, dict):
        return None
    for k in str(keys).split("|"):
        if k in mapping and mapping[k] not in [None, ""]:
            return mapping[k]
    return None


@register.filter(name="split")
def split(value, key):
    """Split a string by the given key."""
    return value.split(key)


@register.simple_tag(name="field_can_render")
def field_can_render(obj, field) -> tuple[bool, str | None]:
    """Determine if a field can be rendered inline in HTML.

    Returns a tuple: (can_render_inline: bool, ext: str|None)
    """
    field_type = get_field_type(field)

    # Images can always render
    if field_type == "ImageField":
        return True, None

    # Only FileFields can be rendered inline
    if field_type != "FileField":
        return False, None

    file_instance = get_attr(obj, field.name)
    if not file_instance or not file_instance.name:
        return False, None

    ext = os.path.splitext(str(file_instance.name))[1].lower()

    # Only handle extensions we know how to render
    if ext not in settings.RENDERABLE_FILE_EXT:
        return False, None

    # PDFs must respect X_FRAME_OPTIONS
    if ext == ".pdf":
        return (settings.X_FRAME_OPTIONS in ["SAMEORIGIN", "ALLOWALL"]), ext

    # DOCX can always render via external viewer
    if ext in [".docx", ".doc"]:
        return True, ext

    # Default fallback for other extensions
    return False, ext


@register.simple_tag(takes_context=True)
def absolute_url(context, relative_url):
    """Convert a relative URL to an absolute URL using the current request context."""
    request: ASGIRequest = context["request"]
    return request.build_absolute_uri(relative_url)


@register.filter
def call_if_true(obj, method_name):
    """Call a method on an object if the method name is a boolean True or if the method exists and returns True."""
    if type(method_name) is bool:
        return method_name

    if isinstance(method_name, dict):
        method = getattr(obj, method_name["method"], None)
        if callable(method):
            args = method_name.get("args", [])
            kwargs = method_name.get("kwargs", {})
            return method(*args, **kwargs)
        return False

    method = getattr(obj, method_name, None)
    if callable(method):
        return method()
    return False  # Return False when the method does not exist.


@register.simple_tag
def dynamic_url_params(viewname, params, item):
    """Generate a URL for a view with dynamic parameters based on an item."""
    if not params:
        return reverse(viewname)

    kwargs = {}

    for key, value in params.items():
        # Use direct values and fall back to item attributes when available.
        kwargs[key] = getattr(item, value, value)
    return reverse(viewname, kwargs=kwargs)
