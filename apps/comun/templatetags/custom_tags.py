import datetime
import os
import re

from django import template
from django.apps import apps
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import ForeignKey
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _

from apps.comun.consts import RELATED_APPS

register = template.Library()


@register.filter
def addstr(arg1, arg2):
    """Concatenate two values as strings.

    Args:
        arg1 (Any): First value.
        arg2 (Any): Second value.

    Returns:
        str: Concatenated string.
    """
    return str(arg1) + str(arg2)


@register.filter
def is_active_section(request, value):
    """Check whether the current request matches a menu section.

    Args:
        request (HttpRequest): Current request.
        value (str): Expected app or app:url value.

    Returns:
        bool: True when the section is active.
    """
    match = request.resolver_match
    if not match:
        return False

    app_name = match.app_name or ""
    namespace = match.namespace or ""
    url_name = match.url_name or ""

    # 🔹 Caso 1: viene app:url
    if ":" in value:
        expected_app, expected_url = value.split(":", 1)
        return (expected_app == app_name or expected_app == namespace) and expected_url == url_name

    # 🔹 Caso 2: apps relacionadas
    if value in RELATED_APPS:
        print(f"Comparando {app_name} y {namespace} con relacionados de {value}: {RELATED_APPS[value]}")
        return app_name in RELATED_APPS[value] or namespace in RELATED_APPS[value]

    # 🔹 Caso 3: solo app
    return value == app_name or value == namespace


@register.filter(name="get_name_model")
def get_name_model(value):
    """Return the class name for a model instance.

    Args:
        value (Any): Model instance.

    Returns:
        str: Class name.
    """
    name = value.__class__.__name__
    return name


@register.filter(name="get_app_name")
def get_app_name(value):
    """Return the app label for a model instance.

    Args:
        value (Any): Model instance.

    Returns:
        str: App label.
    """
    app_name = value._meta.app_label
    return app_name


@register.filter(name="replace_model_name")
def replace_model_name(value):
    """Convert model class names to spaced labels.

    Args:
        value (str): Class name.

    Returns:
        str: Humanized label.
    """
    remove_historical = value.replace("Historical", "")

    # pascalcase to whitespace except if there two uppercase letters together
    return re.sub(r"(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])", " ", remove_historical)


ignore_fields = [
    "custom_id",
    "history_change_reason",
    "deleted_by_cascade",
    "id",
    "history_id",
    "password",
    "history_date",
]

_LABEL_FIELDS = ("title", "name", "nombre", "display_name", "nombre_departamento")

LABELS_DICT = {
    "created_by": _("Creado por"),
    "created_at": _("Fecha de creación"),
    "updated_by": _("Actualizado por"),
    "updated_at": _("Fecha de actualización"),
    "deleted": _("Fecha de eliminación"),
    "history_date": _("Fecha cambio"),
    "history_type": _("Tipo de cambio"),
    "history_user": _("Usuario"),
    "display_name": _("Nombre de visualización"),
}


@register.filter(name="get_all_fields")
def get_all_fields(value):
    """Return a sorted list of fields and values for a model instance.

    Args:
        value (Model): Model instance.

    Returns:
        list[dict]: Field label and value pairs.
    """
    response = []
    for field in value._meta.concrete_fields:
        if field.name in ignore_fields:
            continue
        temp = {}

        # Check if the field is a ForeignKey
        if isinstance(field, ForeignKey):
            try:
                related_object = getattr(value, field.name)
                field_value = str(related_object) if related_object else None
            except ObjectDoesNotExist:
                related_id = getattr(value, field.attname, None)
                field_value = _("Registro relacionado eliminado (id=%(related_id)s)") % {"related_id": related_id}
        else:
            field_value = field.value_from_object(value)

        field_name = LABELS_DICT[field.name] if field.name in LABELS_DICT else field.name

        temp["key"] = field_name.replace("_", " ")
        temp["value"] = field_value
        response.append(temp)

    response.sort(key=lambda x: x["key"])

    return response


@register.filter(name="get_percentage_dashboard")
def get_percentage_dashboard(data):
    """Calculate percentage of records created this year.

    Args:
        data (dict): Aggregation data with app, table, and count.

    Returns:
        float: Percentage value rounded to 2 decimals.
    """
    app = data["app__sistema"]
    tabla = data["tabla"]
    current_count = data["count"]

    model = apps.get_model(app, tabla)
    today = datetime.date.today()
    year = today.year

    total_records = model.objects.filter(created_at__year=year).count()

    if total_records == 0:
        return 0

    percentage = current_count * 100 / total_records

    return round(percentage, 2)


@register.filter(name="get_item")
def get_item(obj, key):
    """Get a nested dict key or attribute using double-underscore notation.

    Args:
        obj (Any): Dict or object to read from.
        key (str): Key or attribute path.

    Returns:
        Any: Resolved value or None.
    """
    if obj is None:
        return None

    try:
        if isinstance(obj, dict):
            return obj.get(key, None)
        elif hasattr(obj, key):
            return getattr(obj, key, None)
        elif "__" in key:
            # Acceso recursivo tipo objeto__subobjeto__campo
            for part in key.split("__"):
                if isinstance(obj, dict):
                    obj = obj.get(part, None)
                else:
                    obj = getattr(obj, part, None)
                if obj is None:
                    return None
            return obj
    except Exception:
        return None


@register.filter(name="get_field")
def get_field(instance, field):
    """Get a field value with optional double-underscore path.

    Args:
        instance (Any): Object instance.
        field (str): Field or attribute path.

    Returns:
        Any: Resolved value or None.
    """
    if "__" in field:
        fields = field.split("__")
        for f in fields:
            instance = getattr(instance, f, None)
            if instance is None:
                return None
        return instance

    return getattr(instance, field, None)


@register.filter(name="return_values")
def return_values(value):
    """Return an empty JSON string when value is None.

    Args:
        value (Any): Input value.

    Returns:
        Any: Input value or empty JSON string.
    """
    if value == None:
        return '""'

    return value


@register.filter(name="get_data_by_field")
def get_data_by_field(instance, field):
    """Return a field value or a default string when missing.

    Args:
        instance (Any): Object instance.
        field (str): Field name.

    Returns:
        Any: Field value or fallback string.
    """
    try:
        data = getattr(instance, field, "Sin información")
        if data == None:
            return "Sin información"
        return data
    except:
        return "Sin información"


@register.filter(name="get_class")
def get_class(value):
    """Return the class name for a value.

    Args:
        value (Any): Input value.

    Returns:
        str: Class name.
    """
    return value.__class__.__name__


@register.filter(name="get_updated_by")
def get_updated_by(instance):
    """Return the last user who updated or created the record.

    Args:
        instance (Any): Model instance.

    Returns:
        Any: User object or fallback string.
    """
    if hasattr(instance, "updated_at") and instance.updated_by:
        return instance.updated_by
    elif hasattr(instance, "created_by") and instance.created_by:
        return instance.created_by
    return "Sin información"


@register.filter(name="safe_history_instance")
def safe_history_instance(log):
    """Return a safe display label for a historical record.

    If the related record or any ForeignKey target has been deleted,
    rendering log.instance raises DoesNotExist and crashes the full page.
    This filter catches that exception and returns a fallback label in
    Spanish so the history list keeps working for all other rows.

    Args:
        log: A django-simple-history historical model instance.

    Returns:
        str: Display label or a localised fallback when the relation is broken.
    """
    try:
        return str(log.instance)
    except Exception:
        for field_name in _LABEL_FIELDS:
            value = getattr(log, field_name, None)
            if value:
                return _("(relación eliminada) - %(value)s") % {"value": value}

        pk = getattr(log, "id", None) or getattr(log, "pk", None)
        model_name = log._meta.verbose_name
        if pk:
            return _("%(model)s #%(pk)s (registro relacionado eliminado)") % {
                "model": model_name,
                "pk": pk,
            }
        return _("Registro relacionado eliminado")


@register.filter
def env(key):
    """Read an environment variable.

    Args:
        key (str): Environment variable name.

    Returns:
        str | None: Variable value.
    """
    return os.environ.get(key, None)


@register.filter(name="set_visibility")
def set_visibility(field_name, required_fields):
    """Return a style attribute for hiding fields.

    Args:
        field_name (str): Field name to check.
        required_fields (Iterable[str]): Fields to hide.

    Returns:
        SafeString: Style attribute or empty string.
    """
    if field_name in required_fields:
        return mark_safe("style='display: none;'")
    return ""


@register.filter(name="split")
def split(value, key):
    """Split a string by a delimiter.

    Args:
        value (str): Input string.
        key (str): Delimiter.

    Returns:
        list[str]: Split values.
    """
    value.split("key")
    return value.split(key)


def get_client_ip(request):
    """Get the client IP address from request headers.

    Args:
        request (HttpRequest): Incoming request.

    Returns:
        str: Client IP address.
    """
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


@register.filter
def get_type(value):
    """Return the type name for a value.

    Args:
        value (Any): Input value.

    Returns:
        str: Type name.
    """
    return type(value).__name__


@register.filter
def empty_to_dash(value):
    """Convert empty values to a dash placeholder.

    Args:
        value (Any): Input value.

    Returns:
        Any: Placeholder string or original value.
    """
    if value in (None, "", [], {}):
        return "---"

    if isinstance(value, str) and value.strip() == "":
        return "---"
    return value
