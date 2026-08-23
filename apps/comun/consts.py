"""Shared constants, enums, and regex helpers used across common app modules."""

import re
from enum import Enum

from django.utils.translation import gettext_lazy as _


class HistoriasUsuario(str, Enum):
    """Enumerates user stories identified with the `HU###` convention."""

    # --- Autenticación y Usuarios ---
    HU001 = "HU001"
    HU002 = "HU002"

    # --- Inventario y Productos ---
    HU003 = "HU003"
    HU004 = "HU004"
    HU005 = "HU005"

    def describe(self) -> str:
        """Return the business description associated with each user story.

        Returns:
            str: Human-readable description for the selected user story.
        """
        descriptions = {
            HistoriasUsuario.HU001: "Inicio de sesión de usuarios",
            HistoriasUsuario.HU002: "Registro de nuevos usuarios",
            HistoriasUsuario.HU003: "CRUD de productos en bodega",
            HistoriasUsuario.HU004: "Gestión de inventario de películas",
            HistoriasUsuario.HU005: "Gestión de géneros de películas",
        }
        return descriptions.get(self, "No hay descripción disponible")


DEFAULT_GRID_CLASSES = "col-xd-6 col-sm-6 col-md-3 col-l-3 col-xl-3 pb-4"
DEFAULT_RENDERABLE_CLASSES = "col-12 pb-4"
NEW_PREFIX = "new_"
SUPPORTED_TEXT_SUFFIXES = {".html", ".htm", ".css", ".js", ".mjs"}
EXTERNAL_ASSET_ROOT = "external_cdns"

HTML_ASSET_URL_REGEX = re.compile(
    r"(?:href|src)\s*=\s*[\"']((?:https?:)?//[^\s\"'<>]+)[\"']",
    re.IGNORECASE,
)
# Also capture URLs passed to the {% external_static_url '...' %} template tag.
DJANGO_EXTERNAL_STATIC_TAG_REGEX = re.compile(
    r"""{%-?\s*external_static_url\s+[\"']((?:https?:)?//[^\s\"']+)[\"']\s*-?%}""",
    re.IGNORECASE,
)
CSS_ASSET_URL_REGEX = re.compile(
    r"@import\s+(?:url\()?\s*[\"']?((?:https?:)?//[^\s\"')]+)",
    re.IGNORECASE,
)
CSS_NESTED_ASSET_URL_REGEX = re.compile(
    r"url\(\s*[\"']?((?:https?:)?//[^\s\"')]+)",
    re.IGNORECASE,
)
# Relative url(...) references — excludes data: URIs and absolute URLs.
CSS_RELATIVE_URL_REGEX = re.compile(
    r"""url\(\s*[\"']?(?!(?:https?:)?//|data:)([^\"')\s#?][^\"')\s]*)[\"']?\s*\)""",
    re.IGNORECASE,
)
JS_IMPORT_URL_REGEX = re.compile(
    r"import\s+(?:[^;]*?\sfrom\s*)?[\"']((?:https?:)?//[^\s\"']+)[\"']",
    re.IGNORECASE,
)

# Select2 placeholders
SELECT2_EMPTY_PLACEHOLDER = _("---------")
SELECT2_EMPTY_PLACEHOLDER_ALT = _("----------")

ERROR_AUTH_CREDENTIALS_MISSING = _("No se proporcionaron credenciales de autenticación.")
ERROR_PERMISSION_DENIED = _("Permiso denegado.")
ERROR_OBJECT_DOES_NOT_EXIST = _("El objeto no existe.")
ERROR_VALIDATION_FAILED = _("La validación falló.")
ERROR_BAD_REQUEST = _("Solicitud incorrecta.")
ERROR_INTERNAL_SERVER = _("Error interno del servidor.")
ERROR_DISABLE_ALREADY_DISABLED = _("No se puede deshabilitar {object}, ya que está deshabilitado.")


class RegexValidator:
    """Provides reusable regex patterns and validation helpers.

    Attributes:
        ALPHABETIC (str): Pattern that allows letters only.
        ALPHANUMERIC (str): Pattern that allows letters and digits.
        ALPHANUMERIC_WITH_SPACE (str): Pattern that allows letters, digits,
            and spaces.
        NUMERIC_ONLY (str): Pattern that allows digits only.
        MEX_PLATE_EXTENDED (Pattern[str]): Pattern for multiple Mexican plate
            formats.
    """

    # Patterns
    ALPHABETIC = r"^[a-zA-Z]+$"  # Only letters
    ALPHANUMERIC = r"^[a-zA-Z0-9]+$"  # Only letters and numbers
    ALPHANUMERIC_WITH_SPACE = r"^[a-zA-Z0-9\s]+$"  # Letters, numbers and spaces
    NUMERIC_ONLY = r"^\d+$"  # Only numbers

    # Mexican license plate patterns
    MEX_PLATE_EXTENDED = re.compile(
        r"^(?:"
        r"[A-Z]{3}-\d{4}"  # New format (e.g., ABC-1234)
        r"|"
        r"\d{1}[A-Z]{2}\d{2}"  # Old format (e.g., 1AB23)
        r"|"
        r"[A-Z]{3}\d{3}"  # Compact format (e.g., ABC123)
        r")$"
    )

    @classmethod
    def validate(cls, value: str, pattern: str) -> bool:
        """Validate a value against a regex pattern.

        Args:
            value (str): Input value to validate.
            pattern (str): Regex pattern used for validation.

        Returns:
            bool: `True` when the value matches the pattern; otherwise `False`.
        """
        return bool(re.match(pattern, value))


RFC_FORMAT_REGEX = re.compile(r"^[A-Z&Ñ]{3,4}[0-9]{2}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])[A-Z0-9]{2}[0-9A]$")
CURP_FORMAT_REGEX = re.compile(r"^[A-ZÑ]{4}\d{6}[HM][A-Z]{2}[A-Z]{3}[0-9A-Z]{2}$")


RFC_STRICT_REGEX = re.compile(
    r"""
    ^(
        # ───────────────────────────────
        # PERSONAS MORALES (companies) – 12 chars
        # 3 letters + valid date + homoclave + check digit
        # ───────────────────────────────
        (
            [A-ZÑ&]{3}                       # initials or abbreviation
            (
                (                            # valid date (YYMMDD)
                    (([02468][048])|([13579][26]))0229  # leap day
                    |
                    (\d{2})(
                        (02(0[1-9]|1\d|2[0-8])) |       # Feb (non-leap)
                        (((0[13456789])|1[012])(0[1-9]|[12]\d|30)) |  # 30-day months
                        (((0[13578])|(1[02]))31)        # 31-day months
                    )
                )
            )
            [A-Z\d]{3}                     # homoclave + check digit
        )
        |
        # ───────────────────────────────
        # PERSONAS FÍSICAS (individuals) – 13 chars
        # 4 letters + valid date + homoclave + check digit
        # Avoids offensive words
        # ───────────────────────────────
        (
            (?!(
                # offensive prefixes (blacklist)
                (
                    ([CcKk][Aa][CcKkGg][AaOo]) |
                    ([Bb][Uu][Ee][YyIi]) |
                    ([Kk][Oo](([Gg][Ee])|([Jj][Oo]))) |
                    ([Cc][Oo](([Gg][Ee])|([Jj][AaEeIiOo]))) |
                    ([QqCcKk][Uu][Ll][Oo]) |
                    ((([Ff][Ee])|([Jj][Oo])|([Pp][Uu]))[Tt][Oo]) |
                    ([Rr][Uu][Ii][Nn]) |
                    ([Gg][Uu][Ee][Yy]) |
                    ((([Pp][Uu])|([Rr][Aa]))[Tt][Aa]) |
                    ([Pp][Ee](([Dd][Oo])|([Dd][Aa])|([Nn][Ee]))) |
                    ([Mm](
                        ([Aa][Mm][OoEe]) |
                        ([Ee][Aa][SsRr]) |
                        ([Ii][Oo][Nn]) |
                        ([Uu][Ll][Aa]) |
                        ([Ee][Oo][Nn]) |
                        ([Oo][Cc][Oo])
                    ))
                )
            ))
            [A-ZÑ&]{1}                    # first letter of paternal surname
            [AEIOU]{1}                    # first internal vowel
            [A-ZÑ&]{2}                    # initials (maternal + given)
            (
                (                         # valid date (YYMMDD)
                    (([02468][048])|([13579][26]))0229 |
                    (\d{2})(
                        (02(0[1-9]|1\d|2[0-8])) |
                        (((0[13456789])|1[012])(0[1-9]|[12]\d|30)) |
                        (((0[13578])|(1[02]))31)
                    )
                )
            )
            [A-Z\d]{3}                    # homoclave + check digit
        )
        |
        # ───────────────────────────────
        # RFC genérico (e.g., extranjero)
        # ───────────────────────────────
        ([Xx][AaEe][Xx]{2}010101000)
    )$
    """,
    re.VERBOSE,
)


CURP_STRICT_REGEX = re.compile(
    r"""
    ^                                   # start
    [A-ZÑ]{1}[AEIOUX]{1}[A-ZÑ]{2}       # first 4 letters (paternal initial + vowel + maternal initial + name initial)
    (\d{2})                             # year (YY)
    (0[1-9]|1[0-2])                     # month (01-12)
    (0[1-9]|[12][0-9]|3[01])            # day (01-31)
    [HM]                                # gender: H or M
    (?:AS|BC|BS|CC|CL|CM|CS|CH|DF|DG|GT|GR|HG|JC|MC|MN|MS|NT|NL|OC|PL|QT|QR|SP|SL|SR|TC|TS|TL|VZ|YN|ZS|NE)
                                        # state code (RENAPO catalog / "NE" = extranjero)
    [B-DF-HJ-NP-TV-Z]{3}                # internal consonants (no vowels)
    [0-9A-Z]{1}                         # homoclave char (alnum)
    \d                                  # last digit
    $                                   # end
""",
    re.VERBOSE,
)


# Apps that share context or navigation.
RELATED_APPS = {
    "users_module": ["users_module", "users", "departments", "groups", "positions"],
}


class PermissionCode:
    """Defines translated permission action labels for UI composition."""

    CAN = _("Puede")

    ADD = _("agregar")
    CHANGE = _("modificar")
    DELETE = _("eliminar")
    ENABLE = _("habilitar")
    VIEW = _("ver")
    DISABLE = _("deshabilitar")


class CRUDOperatorsEnum(Enum):
    """Enumerates supported CRUD operation identifiers."""

    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
    INDEX = "index"


# Shared error and success messages
ERROR_REQUIRED_FIELD = _("Este campo es requerido.")
ERROR_NEGATIVE_NUMBER = _("El número no puede ser negativo.")
ERROR_MIN_LENGTH = _("Asegúrese de que este valor tenga como mínimo {min_length} caracteres")
ERROR_MIN_VALUE = _("El valor no puede ser menor que {min_value}")
ERROR_MAX_VALUE = _("El valor no puede ser mayor que {max_value}")
ERROR_MAX_LENGTH = _("Este campo no puede tener más de {max_length} caracteres.")
ERROR_ACTION_BLOCKED = _(
    "No se puede {action} el elemento <strong>{object}</strong> porque tiene elementos relacionados: {related}. "
    "Por favor, revise los registros antes de {action} este elemento."
)
ERROR_RESTORE_BLOCKED_WITH_REASON = _("No se puede restaurar el elemento <strong>{object}</strong>. {reason}")
ERROR_FILE_TOO_LARGE = _("El archivo es demasiado grande. El tamaño no debe exceder %(max_mb)s MiB.")
ERROR_LETTERS_ONLY = _("Este campo solo puede contener letras.")
ERROR_RFC_INVALID = _("El RFC no es válido.")
ERROR_CURP_INVALID = _("La CURP no es válida.")
ERROR_CONTENT_TYPE_MISMATCH = _("El contenido al que está ligado no corresponde con el tipo de contenido actual.")
ERROR_NO_PERMISSION_ACCESS = _("No tienes permiso para acceder a este elemento.")
ERROR_REPORT_NO_VALID_DATA = _("El reporte no contiene datos válidos.")
ERROR_CREATE = _("Error al crear.")
ERROR_UPDATE = _("Error al editar.")
ERROR_DELETE = _("Error al eliminar.")
SUCCESS_ITEM_DELETED = _("Elemento eliminado.")
SUCCESS_REPORT_SENT = _("Reporte enviado con éxito.")
SUCCESS_GROUPS_ASSIGNED = _("Grupos asignados exitosamente.")
SUCCESS_CREATED = _("Creado exitosamente.")
SUCCESS_UPDATED = _("Actualizado exitosamente.")
SUCCESS_DELETED = _("Eliminado exitosamente.")
ERROR_INTERNAL_SERVER_DETAIL = _("Hubo un error inesperado al procesar su solicitud.")
ERROR_AUTH_CREDENTIALS_MISSING = "Authentication credentials were not provided."
ERROR_PERMISSION_DENIED = "Permission denied."


# Shared action labels and UI strings
ACTION_CREATED_LABEL = _("creado")
ACTION_UPDATED_LABEL = _("actualizado")
ACTION_DELETED_LABEL = _("eliminado")
ACTION_RESTORED_LABEL = _("restaurado")
SUCCESS_ITEM_ACTION = _("¡Elemento {action} exitosamente!")
FIELD_DISABLE_LABEL = _("Deshabilitar")
LIST_CONJUNCTION_AND = _("y")
ACTION_DELETE_VERB = _("eliminar")
ACTION_RESTORE_VERB = _("restaurar")

# Shared auth and report messages
ERROR_USER_DELETED = _("El usuario está eliminado")
ERROR_USER_INACTIVE = _("El usuario está inactivo")
ERROR_REPORT_GENERATION = _("Hubo un error al generar el reporte. Intente más tarde.")
ERROR_REPORT_DEBUG_NO_RESPONSE = _("<br><br>DEBUG: Servidor no respondió.")
REPORT_EMAIL_SUBJECT = _("Reporte reporte.pdf")
REPORT_FILE_NAME = _("reporte.pdf")


# For BaseApiController
class _NoPermissions(list):
    """Sentinel value to explicitly declare that an endpoint requires no permissions.

    Using `None` or `[]` for permissions is falsy and causes Django Ninja Extra to
    fall back to the controller-level permissions. This sentinel is a truthy empty
    list, so the `or` short-circuit is bypassed while still resulting in no
    permission checks being applied.

    Usage:
        @http_get("/public-endpoint", permissions=NO_PERMISSIONS)
        def public_endpoint(self, request):
            ...
    """

    def __bool__(self):
        return True

    def __repr__(self):
        return "NO_PERMISSIONS"


NO_PERMISSIONS = _NoPermissions()

DJANGO_LOOKUP_EXPRESSIONS = (
    "exact",
    "iexact",
    "contains",
    "icontains",
    "in",
    "gt",
    "gte",
    "lt",
    "lte",
    "startswith",
    "istartswith",
    "endswith",
    "iendswith",
    "range",
    "isnull",
    "regex",
    "iregex",
    "year",
    "month",
    "day",
    "hour",
    "minute",
    "second",
    "week",
    "week_day",
    "quarter",
    "time",
    "date",
    "datetime",
    "overlap",
    "unaccent",
    "trigram_similar",
)
