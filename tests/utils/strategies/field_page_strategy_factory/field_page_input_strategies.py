import random
from abc import ABC, abstractmethod
from datetime import timedelta
from enum import Enum
from typing import Any, Optional

from tests.pages.core.constants import AllowedDatesFormates, FileTypeEnum, InputType
from tests.utils.data_generation.base_input_attributes import BaseInputAttributes
from tests.utils.data_generation.field_data import FieldData
from tests.utils.format_dates_functions import (
    format_time_hh_mm,
    format_time_hh_mm_ss,
)
from tests.utils.utils_functions import (
    format_date_in_dd_mm_aaaa,
    generate_base64_file,
    generate_custom_date,
    generate_custom_random_float,
    generate_datetime,
    generate_random_curp,
    generate_random_email,
    generate_random_int,
    generate_random_ip,
    generate_random_mac,
    generate_random_municipio,
    generate_random_phone_number,
    generate_random_rfc,
    generate_random_state,
    generate_random_string,
    generate_random_url,
    generate_time_with_format,
    generate_valid_password,
    generate_value_from_pattern,
    get_prioritized_value_from_list,
    get_random_boolean,
    get_random_postal_code,
    get_random_value_from_list,
)

SELECT2_INPUT_SELECTOR = 'input[class="select2-search__field"]'


class FieldPageAtrributeEnum(Enum):
    """Enum con los nombres de atributos usados en FieldPage."""

    MIN_VALUE = "min_value"
    MAX_VALUE = "max_value"
    MIN_LENGTH = "min_length"
    MAX_LENGTH = "max_length"
    DECIMAL_PLACES = "decimal_places"
    NAME = "name"
    INPUT_TYPE = "input_type"
    FIELD_SELECTOR = "field_selector"
    REQUIRED = "is_required"
    ALLOWED_VALUES = "allowed_values"
    REGEX_PATTERN = "regex_pattern"


class InputStrategy(ABC, BaseInputAttributes):
    """Clase base abstracta para todas las estrategias de generación de datos de input."""

    required_attributes = []

    def __init__(self, field_instance):
        BaseInputAttributes.__init__(self, field_instance=field_instance)
        self.validate_required_attributes()

    def validate_required_attributes(self):
        """Valida que todos los atributos requeridos estén presentes y no sean None."""
        default_required_attributes = [
            FieldPageAtrributeEnum.NAME.value,
            FieldPageAtrributeEnum.INPUT_TYPE.value,
            FieldPageAtrributeEnum.FIELD_SELECTOR.value,
        ]
        errors = []
        for attr in self.required_attributes + default_required_attributes:
            if not hasattr(self, attr) or getattr(self, attr) is None:
                errors.append(f"{attr}")
        if errors:
            raise ValueError(
                f"Los siguientes atributos son obligatorios para el campo '{self.name}' de tipo {self.input_type}: {', '.join(errors)}"
            )

    def get_value_from_allowed_list(self):
        """Selecciona un valor de allowed_values considerando la priorización si está configurada.

        Returns:
            str: Valor seleccionado, o None si no hay allowed_values (indica dependencia)
        """
        if not self.allowed_values:
            # Si no hay allowed_values, puede ser una dependencia de otro módulo
            # Retornar None para que las estrategias lo manejen apropiadamente
            return None

        # Usar priorización si está configurada
        if hasattr(self, "prioritized_values") and self.prioritized_values:
            return get_prioritized_value_from_list(
                self.allowed_values, self.prioritized_values, getattr(self, "priority_percentage", 0.7)
            )
        else:
            return get_random_value_from_list(self.allowed_values)

    def create_field_data(
        self,
        value: Any,
        filter_value: Optional[Any] = None,
        selector: Optional[str] = None,
        validate_value: Optional[Any] = None,
        index_value: Optional[Any] = None,
    ) -> FieldData:
        """Crea un objeto FieldData con valores por defecto inteligentes.

        Args:
            value: Valor principal para llenar el campo.
            filter_value: Valor para filtros. Por defecto igual a value.
            selector: Selector CSS modificado (opcional).
            validate_value: Valor para validación. Por defecto igual a filter_value.
            index_value: Valor para índice. Por defecto igual a value.

        Returns:
            FieldData: Objeto con todos los valores necesarios para el campo.
        """
        return FieldData(
            value=value,
            filter_value=filter_value,
            selector=selector,
            validate_value=validate_value,
            index_value=index_value,
        )

    @abstractmethod
    def generate_data(self) -> FieldData:
        """Genera datos válidos para el tipo de input específico.

        Returns:
            FieldData: Objeto con value, filter_value, selector, validate_value, index_value.
        """
        raise NotImplementedError("Es necesario implementar generate_data")


class TextInputStrategy(InputStrategy):
    """Estrategia para generar datos de campos de texto."""

    required_attributes = InputStrategy.required_attributes + [
        FieldPageAtrributeEnum.MIN_LENGTH.value,
        FieldPageAtrributeEnum.MAX_LENGTH.value,
    ]

    def generate_data(self) -> FieldData:
        """Genera un string aleatorio o selecciona de allowed_values."""
        if self.allowed_values:
            value = self.get_value_from_allowed_list()
            return self.create_field_data(value=value)

        max_length = self.max_length if self.max_length and self.max_length <= 10 else 10
        length = max(self.min_length, max_length)
        value = generate_random_string(length)
        return self.create_field_data(value=value)


class NumberInputStrategy(InputStrategy):
    """Estrategia para generar datos de campos numéricos."""

    required_attributes = InputStrategy.required_attributes + [
        FieldPageAtrributeEnum.MIN_VALUE.value,
        FieldPageAtrributeEnum.MAX_VALUE.value,
    ]

    def generate_data(self) -> FieldData:
        """Genera un número entero aleatorio o selecciona de allowed_values."""
        if self.allowed_values:
            value = self.get_value_from_allowed_list()
            return self.create_field_data(value=value)

        value = str(generate_random_int(self.min_value, self.max_value))
        return self.create_field_data(value=value)


class DecimalInputStrategy(InputStrategy):
    """Estrategia para generar datos de campos decimales."""

    required_attributes = InputStrategy.required_attributes + [
        FieldPageAtrributeEnum.MIN_VALUE.value,
        FieldPageAtrributeEnum.MAX_VALUE.value,
        FieldPageAtrributeEnum.DECIMAL_PLACES.value,
    ]

    def generate_data(self) -> FieldData:
        """Genera un número decimal aleatorio."""
        value = (
            str(generate_custom_random_float(self.min_value, self.max_value, self.allowed_values))
            if self.allowed_values
            else str(round(random.uniform(self.min_value, self.max_value), self.decimal_places))
        )
        return self.create_field_data(value=value)


class EmailInputStrategy(InputStrategy):
    """Estrategia para generar datos de campos de email."""

    def generate_data(self) -> FieldData:
        """Genera un email aleatorio o selecciona de allowed_values."""
        if self.allowed_values:
            value = self.get_value_from_allowed_list()
            return self.create_field_data(value=value)

        value = generate_random_email()
        return self.create_field_data(value=value)


class CheckboxInputStrategy(InputStrategy):
    """Estrategia para generar datos de campos checkbox."""

    required_attributes = InputStrategy.required_attributes + [
        FieldPageAtrributeEnum.REQUIRED.value,
    ]

    def generate_data(self) -> FieldData:
        """Genera un valor booleano para checkbox."""
        value = True if self.is_required else get_random_boolean()
        return self.create_field_data(value=value)


class CheckboxListInputStrategy(InputStrategy):
    """Estrategia para generar datos de listas de checkboxes."""

    required_attributes = InputStrategy.required_attributes + [
        FieldPageAtrributeEnum.ALLOWED_VALUES.value,
    ]

    def generate_data(self) -> FieldData:
        """Genera una lista de valores seleccionados aleatoriamente."""
        # Selecciona la cantidad de opciones entre 1 y el numero total de elementos de la lista
        num_options = random.randint(1, len(self.allowed_values))
        # Devuelve un numero de opciones de la lista aleatoriamente
        random_options_list = random.sample(self.allowed_values, num_options)

        field_selector = f'{self.field_selector} input[type="checkbox"]'
        return self.create_field_data(
            value=random_options_list,
            selector=field_selector,
        )


class PasswordInputStrategy(InputStrategy):
    """Estrategia para generar datos de campos de contraseña."""

    required_attributes = InputStrategy.required_attributes + [
        FieldPageAtrributeEnum.MIN_LENGTH.value,
        FieldPageAtrributeEnum.MAX_LENGTH.value,
    ]

    def generate_data(self) -> FieldData:
        """Genera una contraseña válida o selecciona de allowed_values."""
        if self.allowed_values:
            value = self.get_value_from_allowed_list()
            return self.create_field_data(value=value)

        value = generate_valid_password(self.min_length, self.max_length)
        return self.create_field_data(value=value)


class PhoneInputStrategy(InputStrategy):
    """Estrategia para generar datos de campos de teléfono."""

    required_attributes = InputStrategy.required_attributes + [
        FieldPageAtrributeEnum.MIN_LENGTH.value,
        FieldPageAtrributeEnum.MAX_LENGTH.value,
    ]

    def generate_data(self) -> FieldData:
        """Genera un número de teléfono aleatorio o selecciona de allowed_values."""
        if self.allowed_values:
            value = self.get_value_from_allowed_list()
            return self.create_field_data(value=value)

        value = generate_random_phone_number(self.min_length, self.max_length)
        return self.create_field_data(value=value)


class DateInputStrategy(InputStrategy):
    """Estrategia para generar datos de campos de fecha."""

    def generate_data(self) -> FieldData:
        """Genera una fecha en formato DD/MM/AAAA."""
        value = (
            format_date_in_dd_mm_aaaa(self.date_now)
            if not self.allowed_values
            else format_date_in_dd_mm_aaaa(generate_custom_date(get_random_value_from_list(self.allowed_values)))
        )
        return self.create_field_data(value=value)


class RadioInputStrategy(InputStrategy):
    """Estrategia para generar datos de campos radio button."""

    required_attributes = InputStrategy.required_attributes + [FieldPageAtrributeEnum.ALLOWED_VALUES.value]

    def generate_data(self) -> FieldData:
        """Selecciona un valor de allowed_values para radio button."""
        value = self.get_value_from_allowed_list()
        field_selector = f"input[value={value}]"
        return self.create_field_data(
            value=value,
            selector=field_selector,
        )


class FileInputStrategy(InputStrategy):
    """Estrategia para generar datos de campos de archivo."""

    def generate_data(self) -> FieldData:
        """Genera un archivo en base64 con la extensión especificada."""
        extension = self.get_value_from_allowed_list() if self.allowed_values else "pdf"
        value = generate_base64_file(extension=extension)
        file_name = extension[0] if isinstance(extension, list) else extension
        return self.create_field_data(
            value=value,
            filter_value=file_name,
            validate_value=file_name,
            index_value=file_name,
        )


class Select2InputStrategy(InputStrategy):
    """Estrategia para generar datos de campos Select2."""

    def generate_data(self) -> FieldData:
        """Genera un valor en formato Select2.

        Returns:
            FieldData: Objeto con value como dict y valores para filtro/validación.
        """
        # Obtener valor seleccionado (de allowed_values o aleatorio)
        original_value = self.get_value_from_allowed_list() if self.allowed_values else generate_random_string(10)

        # Value siempre es dict para SELECT2 (para llenar el campo)
        value = {SELECT2_INPUT_SELECTOR: original_value}

        # Filter_value depende del tipo de filtro configurado
        if self.filter_type == InputType.SELECT2:
            filter_value = {SELECT2_INPUT_SELECTOR: original_value}
        else:
            filter_value = original_value

        return self.create_field_data(
            value=value,
            filter_value=filter_value,
            validate_value=original_value,
            index_value=original_value,
        )


class SelectInputStrategy(InputStrategy):
    """Estrategia para generar datos de campos select."""

    # [FieldPageAtrributeEnum.ALLOWED_VALUES.value]
    required_attributes = InputStrategy.required_attributes

    def generate_data(self) -> FieldData:
        """Selecciona un valor de allowed_values o genera placeholder para dependencias."""
        value = self.get_value_from_allowed_list()

        # Si no hay allowed_values (dependencia de otro módulo), verificar num_dependencies
        if value is None:
            # Verificar que tenga num_dependencies configurado
            if not hasattr(self, "num_dependencies") or not self.num_dependencies:
                raise ValueError(
                    f"El campo SELECT '{self.name}' no tiene 'allowed_values' ni 'num_dependencies' configurado. "
                    f"Los campos SELECT deben tener 'allowed_values' (lista de opciones) o 'num_dependencies' (para dependencias de otros módulos)."
                )
            # Para campos SELECT con dependencias, retornar string vacío
            # El valor real será asignado por GenericPage al crear las dependencias
            return self.create_field_data(value="")

        return self.create_field_data(value=value)


class Select2MultipleInputStrategy(InputStrategy):
    """Estrategia para generar datos de campos Select2 múltiple."""

    def generate_data(self) -> FieldData:
        """Genera múltiples valores en formato Select2."""
        if self.allowed_values:
            num_options = random.randint(1, len(self.allowed_values))
            random_options_list = random.sample(self.allowed_values, num_options)
            value = {self.select2_search_selector: random_options_list}
            filter_value = random_options_list
        elif self.num_dependencies:
            option_list = [generate_random_string(10) for _ in range(self.num_dependencies)]
            value = {self.select2_search_selector: option_list}
            filter_value = option_list
        else:
            value = {self.select2_search_selector: []}
            filter_value = []

        return self.create_field_data(
            value=value,
            filter_value=filter_value,
        )


class CURPInputStrategy(InputStrategy):
    """Estrategia para generar datos de campos CURP."""

    def generate_data(self) -> FieldData:
        """Genera un CURP aleatorio o selecciona de allowed_values."""
        if self.allowed_values:
            value = self.get_value_from_allowed_list()
            return self.create_field_data(value=value)

        value = generate_random_curp()
        return self.create_field_data(value=value)


class RFCInputStrategy(InputStrategy):
    """Estrategia para generar datos de campos RFC."""

    def generate_data(self) -> FieldData:
        """Genera un RFC aleatorio o selecciona de allowed_values."""
        if self.allowed_values:
            value = self.get_value_from_allowed_list()
            return self.create_field_data(value=value)

        value = generate_random_rfc()
        return self.create_field_data(value=value)


class TimeInputStrategy(InputStrategy):
    """Estrategia para generar datos de campos de tiempo."""

    # Mapeo de formatos de hora permitidos
    TIME_FORMAT_MAPPING = {
        AllowedDatesFormates.HH_MM: format_time_hh_mm,
        AllowedDatesFormates.HH_MM_SS: format_time_hh_mm_ss,
    }

    def generate_data(self) -> FieldData:
        """Genera una hora en el formato especificado por field_format_date."""
        # Generar valor base en formato completo
        internal_value = generate_time_with_format()

        # Aplicar formato personalizado si está configurado
        if self.field_format_date and self.field_format_date in self.TIME_FORMAT_MAPPING:
            format_function = self.TIME_FORMAT_MAPPING[self.field_format_date]
            formatted_value = format_function(internal_value, time_separator=self.time_separator)
            return self.create_field_data(value=formatted_value, validate_value=formatted_value)

        # Si no hay formato personalizado, usar el valor interno por defecto
        return self.create_field_data(value=internal_value, validate_value=internal_value)


class InitialDateInputStrategy(InputStrategy):
    """Estrategia para generar fecha inicial."""

    def generate_data(self) -> FieldData:
        """Genera la fecha actual."""
        value = format_date_in_dd_mm_aaaa(self.date_now)
        return self.create_field_data(value=value)


class MiddleDateInputStrategy(InputStrategy):
    """Estrategia para generar fecha intermedia."""

    def generate_data(self) -> FieldData:
        """Genera la fecha actual más un día."""
        value = format_date_in_dd_mm_aaaa(self.date_now + timedelta(days=1))
        return self.create_field_data(value=value)


class FinalDateInputStrategy(InputStrategy):
    """Estrategia para generar fecha final."""

    def generate_data(self) -> FieldData:
        """Genera la fecha actual más dos días."""
        value = format_date_in_dd_mm_aaaa(self.date_now + timedelta(days=2))
        return self.create_field_data(value=value)


class DateTimeInputStrategy(InputStrategy):
    """Estrategia para generar datos de fecha y hora."""

    def generate_data(self) -> FieldData:
        """Genera una fecha y hora en formato interno (YYYY-MM-DD HH:MM)."""
        value = generate_datetime()
        return self.create_field_data(value=value)


class TextareaInputStrategy(InputStrategy):
    """Estrategia para generar datos de campos textarea."""

    required_attributes = InputStrategy.required_attributes + [
        FieldPageAtrributeEnum.MAX_LENGTH.value,
        FieldPageAtrributeEnum.MIN_LENGTH.value,
    ]

    def generate_data(self) -> FieldData:
        """Genera un texto largo aleatorio o selecciona de allowed_values."""
        if self.allowed_values:
            value = self.get_value_from_allowed_list()
            return self.create_field_data(value=value)

        max_length = self.max_length if self.max_length and self.max_length <= 100 else 100
        length = max(self.min_length, max_length)
        value = generate_random_string(length)
        return self.create_field_data(value=value)


class RangeOfDatesInputStrategy(InputStrategy):
    """Estrategia para generar rango de fechas."""

    def generate_data(self) -> FieldData:
        """Genera un rango de fechas de dos días."""
        start_date = format_date_in_dd_mm_aaaa(self.date_now)
        end_date = format_date_in_dd_mm_aaaa(self.date_now + timedelta(days=2))
        value = [start_date, end_date]
        return self.create_field_data(value=value)


class IPInputStrategy(InputStrategy):
    """Estrategia para generar direcciones IP."""

    def generate_data(self) -> FieldData:
        """Genera una dirección IP aleatoria o selecciona de allowed_values."""
        if self.allowed_values:
            value = self.get_value_from_allowed_list()
            return self.create_field_data(value=value)

        value = generate_random_ip()
        return self.create_field_data(value=value)


class MACInputStrategy(InputStrategy):
    """Estrategia para generar direcciones MAC."""

    def generate_data(self) -> FieldData:
        """Genera una dirección MAC aleatoria o selecciona de allowed_values."""
        if self.allowed_values:
            value = self.get_value_from_allowed_list()
            return self.create_field_data(value=value)

        value = generate_random_mac()
        return self.create_field_data(value=value)


class ZipCodeInputStrategy(InputStrategy):
    """Estrategia para generar códigos postales."""

    def generate_data(self) -> FieldData:
        """Genera un código postal aleatorio basado en estado y municipio."""
        estado = generate_random_state()
        municipio = generate_random_municipio(estado)
        value = get_random_postal_code(municipio)
        return self.create_field_data(value=value)


class RegexInputStrategy(InputStrategy):
    """Estrategia específica para generar valores basados en patrones regex.

    Requiere que el campo tenga un regex_pattern definido.
    """

    required_attributes = InputStrategy.required_attributes + [
        FieldPageAtrributeEnum.REGEX_PATTERN.value,
    ]

    def generate_data(self) -> FieldData:
        """Genera un valor basado en el patrón regex o selecciona de allowed_values."""
        if self.allowed_values:
            value = self.get_value_from_allowed_list()
            return self.create_field_data(value=value)

        if not self.regex_pattern:
            raise ValueError("RegexInputStrategy requiere un regex_pattern definido")

        value = generate_value_from_pattern(self.regex_pattern, self.regex_flags)
        return self.create_field_data(value=value)


class URLInputStrategy(InputStrategy):
    """Estrategia para generar URLs."""

    def generate_data(self) -> FieldData:
        """Genera una URL aleatoria o selecciona de allowed_values."""
        if self.allowed_values:
            value = self.get_value_from_allowed_list()
            return self.create_field_data(value=value)

        value = generate_random_url()
        return self.create_field_data(value=value)


class WYSIWYGInputStrategy(InputStrategy):
    """Estrategia para generar datos de campos textarea con editor WYSIWYG (TipTap, TinyMCE, etc.)."""

    def generate_data(self) -> FieldData:
        """Genera un texto con formato HTML aleatorio o selecciona de allowed_values."""
        if self.allowed_values:
            value = self.get_value_from_allowed_list()
            return self.create_field_data(value=value)

        max_length = self.max_length if self.max_length and self.max_length <= 100 else 100
        length = max(self.min_length, max_length)
        value = generate_random_string(length)
        return self.create_field_data(value=value)


class MultipleFilesInputStrategy(InputStrategy):
    """Estrategia para generar datos de campos de archivo múltiple."""

    def generate_data(self) -> FieldData:
        """Genera múltiples archivos en base64 con las extensiones especificadas."""
        if self.allowed_values:
            extensions = self.get_value_from_allowed_list()
            if not isinstance(extensions, list):
                extensions = [extensions]
        else:
            extensions = [e.value for e in FileTypeEnum]

        value = [generate_base64_file(extension=ext) for ext in extensions]
        file_names = [ext if isinstance(ext, str) else str(ext) for ext in extensions]

        return self.create_field_data(
            value=value,
            filter_value=file_names,
            validate_value=file_names,
            index_value=file_names,
        )
