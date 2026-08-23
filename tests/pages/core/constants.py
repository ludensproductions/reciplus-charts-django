from dataclasses import dataclass
from enum import Enum, auto


class Constants:
    """Clase contenedora de constantes de error y selectores comunes.

    Se utiliza para centralizar mensajes de validación y selectores de inputs
    con el fin de mantener consistencia en todas las pruebas.
    """

    WRONG_RANGE_OF_DATES_ERROR_MESSAGE = "La fecha final debe ser mayor a la fecha inicial"
    READONLY_ERROR_MESSAGE = "El campo no es editable"
    INVALID_CURP_MESSAGE = "CURP inválida"
    MAX_LENGTH_ERROR_MESSAGE = "Asegúrese de que este valor tenga como máximo {max_length} caracteres"
    MIN_LENGTH_ERROR_MESSAGE = "Asegúrese de que este valor tenga como mínimo {min_length} caracteres"
    REQUIRED_FIELD_MESSAGE = "Este campo es requerido."
    NUMBER_DATA_TYPE_MESSAGE = "Introduzca un número"
    INVALID_WEIGHT_ERROR_MESSAGE = "El tamaño máximo del archivo es de {max_value}MB"
    INVALID_DATE_ERROR_MESSAGE = "El formato de la fecha es inválido"
    LETTERS_ERROR_MESSAGE = "Solo puede introducir letras"
    NEGATIVE_NUMBER_ERROR_MESSAGE = "El número no puede ser negativo."
    MAX_VALUE_ERROR_MESSAGE = "El valor no puede ser mayor que {max_value}."
    MIN_VALUE_ERROR_MESSAGE = "El valor no puede ser menor que {min_value}."
    NO_SPECIAL_CHARS_ERROR_MESSAGE = "El campo no puede contener caracteres especiales."
    ALPHANUMERIC_ERROR_MESSAGE = "Solo se pueden ingresar numeros y letras"
    INVALID_EMAIL_MESSAGE = "Introduzca una dirección de correo electrónico válida"
    DUPLICATED_EMAIL_MESSAGE = "Ya existe un registro con este correo electrónico"
    DUPLICATED_REGISTER_MESSAGE = "Ya existe un registro con estos datos."
    WEAK_PASSWORD_MESSAGE = "La contraseña debe contener al menos un caracter especial, un número, una letra mayúscula, una letra minúscula y tener al menos 8 caracteres de longitud"
    INVALID_FORMAT_MESSAGE = "Por favor seleccione solo un archivo. ({allowed_formats})"
    INVALID_PHONE_MESSAGE = "El número de teléfono debe tener al menos 10 dígitos y solo contener números"

    # Selectores para los select2
    SELECT2_SELECTOR = "span.select2-selection.select2-selection--single"
    SELECT2_INPUT_SELECTOR = 'input[class="select2-search__field"]'
    MULTI_SELECT2_SELECTOR = "span.select2-selection.select2-selection--multiple"
    MULTI_SELECT2_TEXTAREA_SELECTOR = 'textarea[class="select2-search__field"]'
    CLEAR_ALL_BUTTON_SELECTOR = "button.select2-selection__clear"
    REMOVE_OPTION_BUTTON_SELECTOR = "button.select2-selection__choice__remove"


class ValidDataType(Enum):
    """Enumeración que define los tipos de datos válidos para pruebas de formularios.

    Se utiliza en los tests automatizados para validar
    escenarios donde la entrada debe ser aceptada.
    """

    LETTERS = auto()
    """Entrada compuesta únicamente por letras."""
    SPECIAL_CHARS = auto()
    """Entrada con caracteres especiales permitidos."""
    NUMBERS = auto()
    """Entrada numérica válida (solo números enteros)."""
    NEGATIVE_NUMBER = auto()
    """Número negativo válido (cuando la lógica lo permite)."""
    ALPHANUMERIC = auto()
    """Entrada alfanumérica, combinando letras y números."""
    DATE_DD_MM_YYYY = auto()
    """Fecha válida en formato dd/mm/yyyy."""
    DECIMAL = auto()
    """Número decimal válido."""
    DISABLED = auto()
    """Campo deshabilitado que se acepta como válido."""
    VALID_FORMAT = auto()
    """Archivo en un formato permitido."""
    EMPTY = auto()
    """Campo vacío aceptado explícitamente como válido."""
    ALLOW_DUPLICATES = auto()
    """Registro duplicado permitido según la lógica de negocio."""


class InvalidDataType(Enum):
    """Enumeración que define los tipos de datos inválidos para pruebas de formularios.

    Se utiliza en los tests automatizados para validar
    escenarios donde la entrada debe ser rechazada.
    """

    ALPHANUMERIC = auto()
    """Entrada con letras y números mezclados cuando no está permitido."""
    DATE_DD_MM_YYYY = auto()
    """Fecha en formato inválido (dd/mm/yyyy en lugar del esperado)."""
    DUPLICATED = auto()
    """Registro duplicado que no debería aceptarse."""
    EMAIL = auto()
    """Correo electrónico con formato incorrecto."""
    INVALID_FORMAT = auto()
    """Archivo con formato no permitido."""
    FILE_WEIGHT = auto()
    """Archivo que excede el tamaño máximo permitido."""
    INVALID_OPTION = auto()
    """Opción no válida en un campo de selección (select o radio button)."""
    NUMBERS = auto()
    """Entrada numérica cuando solo se permiten letras."""
    MAX_LENGTH = auto()
    """Entrada que excede la longitud máxima."""
    MAX_VALUE = auto()
    """Número que excede el valor máximo permitido."""
    MIN_LENGTH = auto()
    """Entrada que no alcanza la longitud mínima requerida."""
    MIN_VALUE = auto()
    """Número que no alcanza el valor mínimo permitido."""
    NEGATIVE_NUMBER = auto()
    """Número negativo cuando no está permitido."""
    NO_SPECIAL_CHARS = auto()
    """Entrada con caracteres especiales no permitidos."""
    LETTERS = auto()
    """Entrada alfabética cuando solo se permiten números."""
    REQUIRED = auto()
    """Campo obligatorio que fue dejado vacío."""
    WEAK_PASSWORD = auto()
    """Contraseña considerada débil según las reglas de seguridad."""
    CURP = auto()
    """CURP con formato inválido."""
    RANGE_OF_DATES = auto()
    """Rango de fechas incorrecto o incoherente."""
    READONLY = auto()
    """Intento de modificar un campo de solo lectura."""
    BLANKS = auto()
    """Entrada con espacios en blanco no permitidos."""
    CUSTOM = auto()
    """Validación personalizada que se aplica en casos específicos."""


class AllowedDatesFormates(Enum):
    """Enumeración que define los formatos de fecha y hora permitidos en el sistema.

    Se utiliza en validaciones y pruebas automatizadas
    para garantizar que las fechas ingresadas respeten
    los formatos configurados.
    """

    # ============================
    # FECHA (AÑO 2 DÍGITOS)
    # ============================

    DD_MM_AA = auto()
    """Formato Día / Mes / Año con dos dígitos para el año (ej. 25/12/24)."""

    MM_DD_AA = auto()
    """Formato Mes / Día / Año con dos dígitos para el año (ej. 12/25/24)."""

    AA_MM_DD = auto()
    """Formato Año / Mes / Día con dos dígitos para el año (ej. 24/12/25)."""

    AA_DD_MM = auto()
    """Formato Año / Día / Mes con dos dígitos para el año (ej. 24/25/12)."""

    # ============================
    # FECHA (AÑO 4 DÍGITOS)
    # ============================

    DD_MM_AAAA = auto()
    """Formato Día / Mes / Año con cuatro dígitos para el año (ej. 25/12/2024)."""

    MM_DD_AAAA = auto()
    """Formato Mes / Día / Año con cuatro dígitos para el año (ej. 12/25/2024)."""

    AAAA_MM_DD = auto()
    """Formato Año / Mes / Día con cuatro dígitos para el año (ej. 2024/12/25)."""

    AAAA_DD_MM = auto()
    """Formato Año / Día / Mes con cuatro dígitos para el año (ej. 2024/25/12)."""

    # ============================
    # HORA
    # ============================

    HH_MM = auto()
    """Formato de hora con horas y minutos (ej. 10:05)."""

    HH_MM_SS = auto()
    """Formato de hora con horas, minutos y segundos (ej. 10:05:26)."""

    HH_MM_AM_PM = auto()
    """Formato de hora con horas y minutos en formato 12h con AM/PM (ej. 02:30 PM)."""

    HH_MM_SS_AM_PM = auto()
    """Formato de hora con horas, minutos y segundos en formato 12h con AM/PM (ej. 02:30:45 PM)."""

    # ============================
    # FECHA + HORA (CON SEGUNDOS, AÑO 2 DÍGITOS)
    # ============================

    DD_MM_AA_HH_MM_SS = auto()
    """Formato Día / Mes / Año (2 dígitos) + Hora:Minuto:Segundo (ej. 25/12/24 10:05:26)."""

    MM_DD_AA_HH_MM_SS = auto()
    """Formato Mes / Día / Año (2 dígitos) + Hora:Minuto:Segundo (ej. 12/25/24 10:05:26)."""

    AA_MM_DD_HH_MM_SS = auto()
    """Formato Año / Mes / Día (2 dígitos) + Hora:Minuto:Segundo (ej. 24/12/25 10:05:26)."""

    AA_DD_MM_HH_MM_SS = auto()
    """Formato Año / Día / Mes (2 dígitos) + Hora:Minuto:Segundo (ej. 24/25/12 10:05:26)."""

    # ============================
    # FECHA + HORA (CON SEGUNDOS, AÑO 4 DÍGITOS)
    # ============================

    DD_MM_AAAA_HH_MM_SS = auto()
    """Formato Día / Mes / Año (4 dígitos) + Hora:Minuto:Segundo (ej. 25/12/2024 10:05:26)."""

    MM_DD_AAAA_HH_MM_SS = auto()
    """Formato Mes / Día / Año (4 dígitos) + Hora:Minuto:Segundo (ej. 12/25/2024 10:05:26)."""

    AAAA_DD_MM_HH_MM_SS = auto()
    """Formato Año / Día / Mes (4 dígitos) + Hora:Minuto:Segundo (ej. 2024/25/12 10:05:26)."""

    AAAA_MM_DD_HH_MM_SS = auto()
    """Formato Año / Mes / Día (4 dígitos) + Hora:Minuto:Segundo (ej. 2024/12/25 10:05:26)."""

    # ============================
    # FECHA + HORA (SIN SEGUNDOS, AÑO 2 DÍGITOS)
    # ============================

    DD_MM_AA_HH_MM = auto()
    """Formato Día / Mes / Año (2 dígitos) + Hora:Minuto (ej. 25/12/24 10:05)."""

    MM_DD_AA_HH_MM = auto()
    """Formato Mes / Día / Año (2 dígitos) + Hora:Minuto (ej. 12/25/24 10:05)."""

    AA_MM_DD_HH_MM = auto()
    """Formato Año / Mes / Día (2 dígitos) + Hora:Minuto (ej. 24/12/25 10:05)."""

    AA_DD_MM_HH_MM = auto()
    """Formato Año / Día / Mes (2 dígitos) + Hora:Minuto (ej. 24/25/12 10:05)."""

    # ============================
    # FECHA + HORA (SIN SEGUNDOS, AÑO 4 DÍGITOS)
    # ============================

    DD_MM_AAAA_HH_MM = auto()
    """Formato Día / Mes / Año (4 dígitos) + Hora:Minuto (ej. 25/12/2024 10:05)."""

    MM_DD_AAAA_HH_MM = auto()
    """Formato Mes / Día / Año (4 dígitos) + Hora:Minuto (ej. 12/25/2024 10:05)."""

    AAAA_DD_MM_HH_MM = auto()
    """Formato Año / Día / Mes (4 dígitos) + Hora:Minuto (ej. 2024/25/12 10:05)."""

    AAAA_MM_DD_HH_MM = auto()
    """Formato Año / Mes / Día (4 dígitos) + Hora:Minuto (ej. 2024/12/25 10:05)."""

    # ============================
    # FECHA EN TEXTO (ESPAÑOL)
    # ============================

    DATE_IN_SPANISH = auto()
    """Formato de fecha larga en español (ej. "25 de diciembre de 2024")."""

    DATETIME_IN_SPANISH = auto()
    """Formato de fecha y hora en español (ej. "25 de diciembre de 2024 a las 10:05")."""

    DD_ABBREVIATE_MONTH_YYYY = auto()
    """Formato Día / Mes abreviado / Año (ej. 25 Dic 2024)."""

    DD_COMPLETE_MONTH_YYYY = auto()
    """Formato Día / Mes completo / Año (ej. 25 Diciembre 2024)."""


class InputType(Enum):
    """Enumeración que define los tipos de inputs soportados en formularios.

    Se utiliza para mapear validaciones, selectores y flujos de prueba
    en formularios automatizados.
    """

    CHECKBOX = auto()
    """Campo de tipo checkbox (casilla de verificación única)."""
    CHECKBOX_LIST = auto()
    """Lista de checkboxes, donde se pueden seleccionar múltiples opciones."""
    DATE = auto()
    """Campo de selección de fecha (día, mes y año)."""
    DECIMAL = auto()
    """Campo para números decimales."""
    EMAIL = auto()
    """Campo para capturar direcciones de correo electrónico."""
    FILE = auto()
    """Campo para carga de archivos."""
    TEXT = auto()
    """Campo de texto simple."""
    NUMBER = auto()
    """Campo numérico (enteros)."""
    PASSWORD = auto()
    """Campo para contraseñas, con entrada oculta."""
    PHONE = auto()
    """Campo para números telefónicos."""
    RADIO = auto()
    """Grupo de botones de opción (radio buttons)."""
    SELECT = auto()
    """Campo de selección desplegable estándar (HTML <select>)."""
    SELECT2 = auto()
    """Campo desplegable con búsqueda (Select2)."""
    SELECT2_MULTIPLE = auto()
    """Campo desplegable con búsqueda y selección múltiple (Select2)."""
    CURP = auto()
    """Campo específico para CURP (México)."""
    TIME = auto()
    """Campo de hora, minutos y segundos."""
    DATE_START = auto()
    """Campo de fecha inicial en un rango."""
    DATE_MIDDLE = auto()
    """Campo de fecha intermedia en un rango."""
    DATE_END = auto()
    """Campo de fecha final en un rango."""
    TEXTAREA = auto()
    """Área de texto multilínea."""
    IP = auto()
    """Campo para dirección IP."""
    MAC = auto()
    """Campo para dirección MAC."""
    RFC = auto()
    """Campo específico para RFC (México)."""
    ZIPCODE = auto()
    """Campo para código postal."""
    DATE_TIME = auto()
    """Campo combinado de fecha y hora."""
    RANGE_OF_DATES = auto()
    """Campo para seleccionar un rango de fechas."""
    REGEX = auto()
    """Campo que genera valores basados en patrones de expresiones regulares."""
    URL = auto()
    """Campo para URLs."""
    WYSIWYG = auto()
    """Campo de texto enriquecido (What You See Is What You Get)."""
    MULTIPLE_FILES = auto()
    """Campo para carga de múltiples archivos."""


class DeleteModeEnum(Enum):
    """Enumeración que define los diferentes modos de eliminación de registros.

    Esta enumeración se utiliza para especificar la estrategia de
    "eliminación" de un registro según el contexto de la prueba.
    """

    TOGGLE = auto()
    """Modo en el que el registro se elimina o restaura mediante
    un interruptor (toggle), simulando activación o desactivación."""

    DISABLE_INDEX = auto()
    """Modo en el que el registro se deshabilita únicamente en el índice principal y para ser activado es necesario
    acceder al índice de registros deshabilitados."""

    DEFAULT = auto()
    """Modo por defecto: eliminación estándar del registro,
    generalmente borrado lógico."""


class RegexFlag(str, Enum):
    """Enumeración de flags de regex con representación de una letra.

    Usa las letras estándar de Python regex flags para simplificar su uso en tests.
    Puedes combinar múltiples flags usando un string: "IM" = IGNORECASE + MULTILINE.
    """

    I = "I"  # re.IGNORECASE - Case insensitive matching
    """Case insensitive: coincide mayúsculas y minúsculas."""

    M = "M"  # re.MULTILINE - ^ y $ coinciden inicio/fin de línea
    """Multiline: ^ y $ coinciden con inicio/fin de cada línea."""

    S = "S"  # re.DOTALL - . coincide con saltos de línea
    """Dot matches all: el punto coincide con cualquier carácter incluyendo \\n."""

    U = "U"  # re.UNICODE - Coincidencias Unicode
    """Unicode matching: habilita coincidencias Unicode."""

    A = "A"  # re.ASCII - Solo coincidencias ASCII
    """ASCII-only: limita coincidencias solo a caracteres ASCII."""

    X = "X"  # re.VERBOSE - Permite comentarios y espacios
    """Verbose: permite comentarios y espacios en el patrón regex."""


@dataclass
class FieldRef:
    """Referencia explícita a un campo de dependencia con alcance de búsqueda definido.

    Úsalo en lugar de un string plano en la lista de tokens de ``input_field_dependencies``
    cuando el nombre del campo es ambiguo, por ejemplo cuando el mismo nombre existe tanto
    en el formulario principal como en un formset de la misma página de dependencia.

    Args:
        name: Nombre del campo a buscar.
        lookup_formset: Si es True, busca únicamente en las instancias del formset.
                        Si es False (defecto), busca únicamente en input_field_instances.
    """

    name: str
    lookup_formset: bool = False


class DependencyAction(str, Enum):
    """Enumeración que define las acciones soportadas para la resolución de dependencias.

    Cada miembro representa un contexto específico en el que se pueden
    evaluar las dependencias de los campos de entrada. La enumeración
    hereda de `str` para permitir el uso directo de los valores de texto
    en diccionarios y en serialización JSON.
    """

    CREATE = "create"
    """Acción utilizada al crear un nuevo registro."""

    VALIDATE = "validate"
    """Acción utilizada al validar un registro existente."""

    FILTER = "filter"
    """Acción utilizada al filtrar registros en un conjunto de datos."""

    INDEX = "index"
    """Acción utilizada al indexar múltiples registros, donde puede aplicarse un separador."""


class DateValidateLocation(str, Enum):
    """Enumeración que define las ubicaciones donde se validan las fechas.

    Cada miembro representa un contexto específico en el que se pueden
    evaluar las fechas de los campos de entrada. La enumeración
    hereda de `str` para permitir el uso directo de los valores de texto
    en diccionarios y en serialización JSON.
    """

    DETAIL = "detail"
    """Ubicación utilizada al validar la fecha en la vista de detalle del registro."""

    INDEX = "index"
    """Ubicación utilizada al validar la fecha en la vista de índice o lista de registros."""


class FileTypeEnum(Enum):
    """Enumeration of file types."""

    TXT = ".txt"
    CSV = ".csv"
    LOG = ".log"
    PDF = ".pdf"
    DOC = ".doc"
    DOCX = ".docx"
    ODT = ".odt"
    XLS = ".xls"
    XLSX = ".xlsx"
    ODS = ".ods"
    PPT = ".ppt"
    PPTX = ".pptx"
    ODP = ".odp"
    JPG = ".jpg"
    JPEG = ".jpeg"
    PNG = ".png"
    GIF = ".gif"
    BMP = ".bmp"
    WEBP = ".webp"
    ZIP = ".zip"
    RAR = ".rar"


class HtmlTagEnum(Enum):
    """Enumeration of HTML tag names as returned by el.tagName."""

    A = "A"
    BUTTON = "BUTTON"
    CANVAS = "CANVAS"
    DIV = "DIV"
    H2 = "H2"
    INPUT = "INPUT"
    LABEL = "LABEL"
    SELECT = "SELECT"
    SPAN = "SPAN"
    TEXTAREA = "TEXTAREA"
