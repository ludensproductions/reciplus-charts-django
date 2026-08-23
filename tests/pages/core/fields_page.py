import copy
import inspect
import logging
from datetime import datetime
from enum import Enum
from typing import List, Optional, Union

from playwright.async_api import Page

from tests.pages.core.constants import AllowedDatesFormates, Constants, DateValidateLocation, InputType
from tests.pages.core.standard_django_page import StandardDjangoPage
from tests.utils.data_generation.field_data import FieldData
from tests.utils.selectors.selector_builder import FieldSelectorBuilder
from utils.data_generation.dates_validation.dates_validate_value_strategy_factory import (
    DatesValidateValueStrategyFactory,
)
from utils.strategies.field_page_strategy_factory.field_page_strategy_factory import (
    FieldDataStrategyFactory,
)
from utils.utils_functions import get_format_file_list, regex_flags_from_str
from utils.validation.invalid_validation_strategy_factory.invalid_data_factory import (
    InvalidDataFactory,
)
from utils.validation.valid_validation_strategy_factory.valid_data_factory import ValidDataFactory

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FieldsPage(StandardDjangoPage, Constants):
    """Clase para representar un campo con validaciones específicas."""

    def __init__(
        self,
        page: Page,
        name: str,
        field_selector: Optional[str] = None,
        filter_selector: Optional[str] = None,
        max_length: Optional[int] = 20,
        min_length: int = 4,
        min_value: Optional[int] = 1,
        max_value: Optional[int] = 9999,
        is_required: bool = True,
        allowed_values: List[str] = [],
        prioritized_values: List[str] = [],
        priority_percentage: float = 0.7,
        input_type: Enum = InputType.TEXT,
        filter_type: Optional[Enum] = None,
        is_filter: bool = True,
        is_data_validate: bool = True,
        is_indexable: bool = True,
        is_editable: bool = True,
        num_dependencies: Optional[int] = 1,
        decimal_places: Optional[int] = 2,
        field_format_date: Optional[AllowedDatesFormates] = None,
        detail_format_date: Optional[AllowedDatesFormates] = None,
        index_format_date: Optional[AllowedDatesFormates] = None,
        validate_value_for_nullable: Optional[str] = None,
        title_for_validate: Optional[str] = None,
        is_dependent: bool = False,
        field_truncate_length: Optional[int] = None,
        filter_truncate_length: Optional[int] = None,
        index_truncate_length: Optional[int] = None,
        validate_truncate_length: Optional[int] = None,
        field_truncate_suffix: str = "...",
        filter_truncate_suffix: str = "...",
        index_truncate_suffix: str = "...",
        validate_truncate_suffix: str = "...",
        activating_values: Optional[list[str]] = None,
        activating_field: Optional[str] = None,
        is_generated_field: bool = False,
        date_separator: str = "/",
        detail_range_of_dates_separator: str = " - ",
        index_range_of_dates_separator: str = " - ",
        datetime_separator: str = " ",
        time_separator: str = ":",
        regex_pattern: str = None,
        regex_flags: Union[str, int] = 0,
        table_suffix: Optional[str] = None,
    ):
        """Inicializa la clase FieldsPage.

        :param page: Instancia de Playwright Page.
        :param name: Nombre del campo (para reportes o logs).
        :param field_selector: Selector del campo.
        :param filter_selector: Selector del campo en los filtros.
        :param max_length: Longitud máxima permitida.
        :param min_length: Longitud mínima permitida.
        :param min_value: Valor mínimo permitido.
        :param max_value: Valor máximo permitido.
        :param is_required: Si el campo es obligatorio.
        :param allowed_values: Valores permitidos para el campo.
        :param prioritized_values: Valores que tienen prioridad para ser seleccionados.
        :param priority_percentage: Porcentaje de probabilidad (0.0-1.0) de seleccionar un valor priorizado.
        :param input_type: Tipo de entrada (text, number, email, etc.).
        :param filter_type: Tipo de filtro a usar (opcional, sobrescribe input_type si se especifica).
        :param is_filter: Si el campo es un filtro.
        :param is_data_validate: Si se debe validar el dato.
        :param is_indexable: Si el campo aparece en la tabla del index.
        :param is_editable: Si el campo es editable.
        :param num_dependencies: La cantidad de dependencias que creará para asignar al campo.
        :param decimal_places: El número de decimales que tendrá el valor float después del punto.
        :param field_format_date: El tipo de formato en el que se creará la fecha para la vista de creación/edición.
        :param detail_format_date: El tipo de formato en el que se creará la fecha para la vista de detalle.
        :param index_format_date: El tipo de formato en el que se creará la fecha para la vista de índice.
        :param validate_value_for_nullable: Si el valor es nulo y aparece en los detalles.
        :param title_for_validate: El título para mostrar al validar el campo.
        :param is_dependent: Si el campo depende de otro campo.
        :param field_truncate_length: Longitud máxima para truncar el valor del campo.
        :param filter_truncate_length: Longitud máxima para truncar el valor en el filtro.
        :param index_truncate_length: Longitud máxima para truncar el valor en el índice.
        :param validate_truncate_length: Longitud máxima para truncar el valor en validación.
        :param field_truncate_suffix: Sufijo a agregar al truncar el valor del campo (por ejemplo, "...").
        :param filter_truncate_suffix: Sufijo a agregar al truncar el valor en el filtro (por ejemplo, "...").
        :param index_truncate_suffix: Sufijo a agregar al truncar el valor en el índice (por ejemplo, "...").
        :param validate_truncate_suffix: Sufijo a agregar al truncar el valor en validación (por ejemplo, "...").
        :param activating_values: Valores que activan este campo dependiente.
        :param activating_field: Nombre del campo que activa este campo.
        :param is_generated_field: Si el campo es auto-generado.
        :param date_separator: Separador para fechas (por defecto "/").
        :param detail_range_of_dates_separator: Separador para rangos de fechas en detalle (por defecto " - ").
        :param index_range_of_dates_separator: Separador para rangos de fechas en índice (por defecto " - ").
        :param datetime_separator: Separador entre fecha y hora (por defecto " ").
        :param time_separator: Separador para horas (por defecto ":").
        :param regex_pattern: Patrón regex para validación de campos de tipo REGEX. Es necesario mandar el regex como string con r ejemplo: r''.
        :param regex_flags: Flags de regex como string ("I", "IM") o int (re.IGNORECASE). String usa RegexFlag enum.
        :param table_suffix: Para SELECT2_MULTIPLE tipo tabla formset, especifica el sufijo del selector (ej: "genre" genera "genres-{index}-genre"). Si se configura, el campo se trata automáticamente como tabla.
        """
        super().__init__(page)
        self.page = page
        self.field_selector = field_selector
        self.original_field_selector = field_selector
        self.filter_selector = filter_selector
        self.filter_value = ""
        self.original_filter_value = ""
        self.validate_value = ""
        self.index_value = ""
        self.name = name
        self.title_for_validate = title_for_validate or name
        self.is_indexable = is_indexable
        self.max_length = max_length
        self.min_length = min_length
        self.min_value = min_value
        self.field_truncate_length = field_truncate_length
        self.filter_truncate_length = filter_truncate_length
        self.index_truncate_length = index_truncate_length
        self.validate_truncate_length = validate_truncate_length
        self.field_truncate_suffix = field_truncate_suffix
        self.filter_truncate_suffix = filter_truncate_suffix
        self.index_truncate_suffix = index_truncate_suffix
        self.validate_truncate_suffix = validate_truncate_suffix
        self.max_value = max_value
        self.is_required = is_required
        self.input_type = input_type
        self.filter_type = filter_type
        self.is_filter = is_filter
        self.is_data_validate = is_data_validate
        self.is_editable = is_editable
        self.allowed_values = allowed_values
        self.prioritized_values = prioritized_values
        self.priority_percentage = priority_percentage
        self.decimal_places = decimal_places
        self.format_list = get_format_file_list()
        self.field_value = None
        self.original_value = None
        self.select2_search_selector = ""
        self.custom_value = None
        self.num_dependencies = num_dependencies
        self.date_now = datetime.now()
        self.field_format_date = field_format_date
        self.detail_format_date = detail_format_date
        self.index_format_date = index_format_date
        self.validate_value_for_nullable = validate_value_for_nullable
        self.date_separator = date_separator
        self.detail_range_of_dates_separator = detail_range_of_dates_separator
        self.index_range_of_dates_separator = index_range_of_dates_separator
        self.datetime_separator = datetime_separator
        self.time_separator = time_separator
        self.regex_pattern = regex_pattern
        # Convertir regex_flags de string a int si es necesario
        self.regex_flags = regex_flags_from_str(regex_flags) if isinstance(regex_flags, str) else regex_flags

        # Para campos dependientes
        self.is_dependent = is_dependent
        self.activating_values = activating_values
        self.activating_field = activating_field

        # Para campos generados
        self.is_generated_field = is_generated_field

        # Para SELECT2_MULTIPLE tipo tabla
        self.table_suffix = table_suffix
        self.select2_multiple_selector_template = None  # Se genera automáticamente en _initialize_values()

        # Inicializar factories y builders
        self.selector_builder = FieldSelectorBuilder()
        self._initialize_values()
        self.field_data_factory = FieldDataStrategyFactory(self)
        self.date_validate_value_factory = DatesValidateValueStrategyFactory(self)
        self.valid_data_factory = ValidDataFactory(self)
        self.invalid_data_factory = InvalidDataFactory(self)
        self.generate_valid_data()

    def __deepcopy__(self, memo):
        """Implementación de copia profunda para la clase FieldsPage."""
        # Crear una nueva instancia de la clase
        new_instance = self.__class__.__new__(self.__class__)

        # Copiar todos los atributos dinámicamente
        for key, value in self.__dict__.items():
            if key == "page":  # Evitar copiar el objeto 'page' (no es serializable)
                setattr(new_instance, key, value)
            else:
                setattr(new_instance, key, copy.deepcopy(value, memo))

        return new_instance

    @classmethod
    def from_existing(cls, instance_to_copy: "FieldsPage") -> "FieldsPage":
        """Genera la copia de una instancia de Field Page.

        :param instance_to_copy: La instancia con los valores a duplicar.

        """
        init_params = inspect.signature(cls.__init__).parameters
        init_keys = set(init_params.keys()) - {"self"}

        # Extrae solo los atributos esperados por __init__
        init_args = {key: getattr(instance_to_copy, key) for key in init_keys if hasattr(instance_to_copy, key)}

        return cls(**init_args)

    def __str__(self):
        """Representación en string del campo."""
        return f"<{self.__class__.__name__}> Campo: {self.name} - Selector: {self.field_selector} - Tipo: {self.input_type} - Name: {self.name}"

    def __repr__(self):
        """Representación para debugging del campo."""
        return f"<{self.__class__.__name__}> Campo: {self.name} Field Value {self.field_value}"

    def truncate_select_value(self, value: str, truncate_type: str = "field") -> str:
        """Trunca un valor si excede la longitud máxima definida para su tipo.

        Si el valor contiene separadores comunes (como " - ", ", ", "; ", " / "), aplica el truncado
        a cada parte individualmente y las reconstruye con el separador original.

        Args:
            value (str): El valor a truncar
            truncate_type (str): Tipo de truncado: "field", "filter", "index" o "validate"
                               Determina qué longitud y sufijo se usarán al truncar

        Returns:
            str: El valor truncado con el sufijo correspondiente si excede la longitud definida para su tipo,
                 o el valor original si no hay longitud definida o el valor es más corto.
                 Si contiene separadores, cada parte se trunca individualmente.

        Example:
            >>> field.truncate_select_value("1997 - rHzvcDbPiDgZtJWcIVPVmZtvfmhfsjrbPLN", "field")
            "1997 - rHzvcDbPiD..."
        """
        # Mapear tipos a sus configuraciones correspondientes
        config_map = {
            "field": (self.field_truncate_length, self.field_truncate_suffix),
            "filter": (self.filter_truncate_length, self.filter_truncate_suffix),
            "index": (self.index_truncate_length, self.index_truncate_suffix),
            "validate": (self.validate_truncate_length, self.validate_truncate_suffix),
        }

        # Obtener la configuración para el tipo especificado
        truncate_length, suffix = config_map.get(
            truncate_type, (self.field_truncate_length, self.field_truncate_suffix)
        )

        # Si no hay longitud definida, retornar el valor original
        if not truncate_length:
            return value

        # Lista de separadores comunes a detectar (ordenados por prioridad de detección)
        separators = [" - ", ", ", "; ", " / ", " | ", " "]

        # Detectar si hay algún separador en el valor
        detected_separator = None
        for sep in separators:
            if sep in value:
                detected_separator = sep
                break

        # Si se detectó un separador, truncar cada parte individualmente
        if detected_separator:
            parts = value.split(detected_separator)
            truncated_parts = []

            for part in parts:
                if len(part) > truncate_length:
                    truncated_parts.append(part[:truncate_length] + suffix)
                else:
                    truncated_parts.append(part)

            return detected_separator.join(truncated_parts)

        # Si no hay separador, aplicar truncado normal
        if len(value) <= truncate_length:
            return value

        return value[:truncate_length] + suffix

    def _initialize_values(self):
        """Inicializa los selectores basados en las restricciones del campo."""
        self.field_selector = self.field_selector or self.selector_builder.build(self.input_type, self.name)
        self.original_field_selector = self.field_selector

        if not self.filter_selector:
            self.filter_type = self.filter_type or self.input_type

            self.filter_selector = self.selector_builder.build(self.filter_type, self.name)

        self.filter_selector = self.filter_selector or self.field_selector

        self._apply_select2_logic(is_filter=False)
        self._apply_select2_logic(is_filter=True)

    def _apply_select2_logic(self, is_filter: bool):
        input_type = self.filter_type if is_filter else self.input_type
        selector_attr = "filter_selector" if is_filter else "field_selector"

        selector = getattr(self, selector_attr)

        if input_type == InputType.SELECT2_MULTIPLE:
            if not is_filter:
                self.select2_search_selector = f"{selector} {self.MULTI_SELECT2_TEXTAREA_SELECTOR}"
            setattr(self, selector_attr, f"{selector} {self.MULTI_SELECT2_SELECTOR}")

            if not is_filter and self.table_suffix:
                self.select2_multiple_selector_template = self._generate_table_selector_template()

        elif input_type == InputType.SELECT2:
            if not is_filter:
                self.select2_search_selector = self.SELECT2_INPUT_SELECTOR
            setattr(self, selector_attr, f"{selector} {self.SELECT2_SELECTOR}")

    def _generate_table_selector_template(self) -> str:
        """Genera el template de selector para tablas formset.

        Usa self.name como base, o title_for_validate si name no sirve.
        Si hay suffix configurado: "name-{index}-suffix"
        Si no hay suffix: "name-{index}"

        Returns:
            str: Template de selector con placeholder {index}
        """
        # Determinar el nombre base (preferir title_for_validate, fallback a name)
        base_name = self.title_for_validate.lower().replace(" ", "_")

        # Si name no es apropiado (muy corto o genérico), usar title_for_validate
        if len(base_name) < 2 or base_name in ["id", "pk"]:
            base_name = self.name.lower().replace(" ", "_")

        # Construir template con o sin sufijo
        if self.table_suffix:
            return f"{base_name}-{{index}}-{self.table_suffix}"
        else:
            return f"{base_name}-{{index}}"

    def get_table_selector_for_index(self, index: int) -> str:
        """Genera el selector específico para un índice en una tabla formset.

        Args:
            index (int): Índice del elemento (0-based)

        Returns:
            str: Selector con el índice reemplazado (ej: "members-0-user")
        """
        if not self.table_suffix or not self.select2_multiple_selector_template:
            return ""

        return self.select2_multiple_selector_template.format(index=index)

    def truncate_if_needed(self, value: str, truncate_type: str = "field") -> str:
        """Aplica el truncado al valor si se ha definido una longitud máxima para el tipo especificado.

        Args:
            value (str): El valor a truncar
            truncate_type (str): Tipo de truncado a aplicar: "field", "filter", "index" o "validate"

        Returns:
            str: El valor truncado si hay una longitud de truncado definida para el tipo,
                 o el valor original si no hay longitud definida.

        Nota:
            Con definir la longitud (*_truncate_length) es suficiente para activar el truncado.
            Para desactivarlo, simplemente no definas la longitud.
        """
        if not value:
            return value

        # Obtener la longitud de truncado para el tipo específico
        truncate_length_map = {
            "field": self.field_truncate_length,
            "filter": self.filter_truncate_length,
            "index": self.index_truncate_length,
            "validate": self.validate_truncate_length,
        }
        truncate_length = truncate_length_map.get(truncate_type)

        # Si hay longitud definida, aplicar truncado
        if truncate_length is not None:
            # Manejar listas (como en campos SELECT2_MULTIPLE)
            if isinstance(value, list):
                return [self.truncate_select_value(str(v), truncate_type) for v in value]
            # No convertir dicts a string (formato de campo SELECT2: {selector: valor})
            if isinstance(value, dict):
                return value
            return self.truncate_select_value(str(value), truncate_type)

        return value

    def generate_valid_data(self, is_for_validate=False, ignore_dependent_fields=True, ignore_generated_fields=True):
        """Genera y almacena datos válidos para el campo basándose en sus restricciones y tipo de input.

        Este método utiliza el patrón Factory para crear estrategias específicas de generación
        de datos según el tipo de campo (InputType), aplicando las restricciones definidas
        como longitud máxima/mínima, valores permitidos, etc.

        Args:
            is_for_validate (bool, optional): Si es True, solo genera datos para validación
                sin establecer filter_value ni llamar generate_data_validate().
                Por defecto False.
            ignore_dependent_fields (bool, optional): Si es True, omite la generación
                para campos dependientes (is_dependent=True). Por defecto True.
            ignore_generated_fields (bool, optional): Si es True, omite la generación
                para campos generados automáticamente (is_generated_field=True).
                Por defecto True.

        Efectos:
            - Establece self.field_value con el valor principal del campo
            - Establece self.validate_value (inicialmente igual a field_value)
            - Si not is_for_validate:
                * Establece self.filter_value para usar en filtros
                * Llama a generate_data_validate() para formatear validate_value
            - Guarda una copia del valor original en self.original_value
            - Puede actualizar self.field_selector si la estrategia devuelve un selector específico

        Retorna:
            None: El método modifica los atributos del objeto directamente.

        Notas:
            - Utiliza FieldDataStrategyFactory para obtener la estrategia apropiada
            - La estrategia puede devolver una tupla (value, filter_value, selector)
              o un valor simple
            - Los campos dependientes y generados se omiten por defecto para evitar
              conflictos en la generación masiva de datos

        Ejemplo:
            >>> field = FieldsPage(page, field_selector='input[name="title"]',
            ...                    input_type=InputType.TEXT, max_length=100)
            >>> field.generate_valid_data()
            >>> print(field.field_value)  # 'TextoAleatorio123'
            >>> print(field.filter_value)  # 'TextoAleatorio123'
        """
        # No se generan los datos para evitar ser llenado al llamar el fill_data

        if ignore_generated_fields and self.is_generated_field:
            return

        if ignore_dependent_fields and self.is_dependent:
            return

        field_data_strategy = self.field_data_factory.get_field_data_strategy(
            input_type=self.input_type,
        )
        data: FieldData = field_data_strategy.generate_data()

        # Actualizar selector si la estrategia lo proporciona
        if data.selector:
            self.field_selector = data.selector

        # Aplicar truncado si es necesario
        value = self.truncate_if_needed(data.value, "field")
        filter_value = self.truncate_if_needed(data.filter_value, "filter")

        self.field_value = value
        self.validate_value = data.validate_value or filter_value
        self.index_value = data.index_value or value

        if not is_for_validate:
            self.filter_value = filter_value
            self.generate_data_validate()

        if not self.original_value:
            self.original_value = copy.deepcopy(self.field_value)

    # TODO contemplar formato en los tiempos al ver los detalles
    def generate_data_validate(self):
        """Genera los valores de validación formateados para detail e index.

        Para SELECT2_MULTIPLE tipo tabla (cuando table_suffix está definido), genera una lista
        de valores individuales que pueden tener selectores específicos con índice.
        """
        if self.input_type in [
            InputType.DATE,
            InputType.DATE_START,
            InputType.DATE_MIDDLE,
            InputType.DATE_END,
            InputType.RANGE_OF_DATES,
            InputType.DATE_TIME,
            InputType.TIME,
        ]:
            # Usar field_format_date como fallback si detail_format_date o index_format_date no están definidos
            detail_format = self.detail_format_date or self.field_format_date
            index_format = self.index_format_date or self.field_format_date

            if detail_format:
                detail_date_strategy = self.date_validate_value_factory.get_dates_validate_value_strategy(
                    format_date=detail_format
                )
                self.validate_value = detail_date_strategy.generate_validate_data()

            if index_format:
                index_date_strategy = self.date_validate_value_factory.get_dates_validate_value_strategy(
                    format_date=index_format, location=DateValidateLocation.INDEX
                )
                self.index_value = index_date_strategy.generate_validate_data()

        elif self.input_type == InputType.RANGE_OF_DATES:
            start_value, end_value = self.field_value
            final_value = f"{start_value}{self.range_of_dates_separator}{end_value}"
            self.validate_value = final_value
            self.index_value = final_value
        elif self.input_type == InputType.FILE:
            self.validate_value = self.field_value["name"]
            self.index_value = self.field_value["name"]
        elif self.input_type == InputType.SELECT2:
            validate_value = self.truncate_if_needed(str(self.get_values_from_select2()[0]), "validate")
            index_value = self.truncate_if_needed(str(self.get_values_from_select2()[0]), "index")

            self.validate_value = validate_value
            self.index_value = index_value
        elif self.input_type == InputType.SELECT2_MULTIPLE:
            # Para SELECT2_MULTIPLE tipo tabla, mantener como lista para validación individual
            # La concatenación de valores se maneja en generic_page.py cuando hay dependencias
            values = self.get_values_from_select2()
            self.validate_value = [self.truncate_if_needed(str(v), "validate") for v in values]
            self.index_value = [self.truncate_if_needed(str(v), "index") for v in values]
        else:
            # Aplicar truncado independiente de si es dependencia
            # TODO - Acá estaba el field value pero cuando es select2 multiple se almacena como dict cuando
            # no tiene sentido simplemente hay que almacenar la lista de valores o el valor simple
            validate_value = self.truncate_if_needed(str(self.filter_value), "validate")
            index_value = self.truncate_if_needed(str(self.field_value), "index")

            self.validate_value = validate_value
            self.index_value = index_value

    def convert_to_select2_format_value(self, value):
        """Devuelve el valor con el formato para el uso correcto en un campo de tipo select2."""
        return {self.select2_search_selector: value}

    def generate_select2_value(self, input_type, value):
        """Genera el valor con el formato para el uso correcto en un campo de tipo select2."""
        if input_type == InputType.SELECT2:
            return {self.SELECT2_INPUT_SELECTOR: value}
        elif input_type == InputType.SELECT2_MULTIPLE:
            return {self.select2_search_selector: value}
        return value

    def add_value_to_select2_multiple(self, value):
        """Agrega un valor adicional a un campo de tipo select2 multiple."""
        if not isinstance(self.field_value, dict) or self.select2_search_selector not in self.field_value:
            self.field_value = {self.select2_search_selector: []}

        if not isinstance(self.field_value[self.select2_search_selector], list):
            raise ValueError("El valor actual del campo SELECT2_MULTIPLE no es una lista")

        self.field_value[self.select2_search_selector].append(value)

    def clear_values_to_select2_multiple(self):
        """Limpia todos los valores seleccionados en un campo de tipo select2 multiple."""
        self.field_value = {self.select2_search_selector: []}

    def get_values_from_select2(self) -> List[str]:
        """Obtiene los valores seleccionados en un campo de tipo select2 multiple."""
        if not isinstance(self.field_value, dict) or self.select2_search_selector not in self.field_value:
            return []
        values = self.field_value[self.select2_search_selector]

        if isinstance(values, list):
            return values
        elif isinstance(values, str):
            return [values]

        return []

    async def clear_multi_selector_options(self, original_value=None):
        """Removes all selected options from a multi-select input.

        Iterates through each selected option and clicks its remove button until
        the field is cleared. Supports both dict (grouped values by field) and list inputs.

        Args:
            original_value (dict | list | None): Options to clear. If not provided,
                defaults to the current `self.field_value`.

        Raises:
            PlaywrightError: If an option's remove button cannot be found or clicked.
        """
        options = original_value if original_value else self.field_value
        # Remover opción de una en una
        if isinstance(options, dict):
            for field, value in options.items():
                for option in value:
                    remove_button = self.page.locator(f'li[title="{option}"] {self.REMOVE_OPTION_BUTTON_SELECTOR}')
                    await remove_button.wait_for(state="visible")
                    await remove_button.click()
        elif isinstance(options, list):
            for option in options:
                remove_button = self.page.locator(f'li[title="{option}"] {self.REMOVE_OPTION_BUTTON_SELECTOR}')
                await remove_button.wait_for(state="visible")
                await remove_button.click()
        await self.page.wait_for_timeout(500)

    async def clear_select2_options(self):
        """Clears the current selection from a Select2 input.

        Resets the underlying `<select>` element value to empty
        and dispatches a `change` event to notify listeners.

        Raises:
            PlaywrightError: If the select element cannot be found or updated.
        """
        name_selector = self.name.lower().replace(" ", "_")
        select_locator = self.page.locator(f"{self.original_field_selector} select[name={name_selector}]")
        await select_locator.evaluate(
            """el => {
                    el.value = '';
                    const event = new Event('change', { bubbles: true });
                    el.dispatchEvent(event);
                }"""
        )

    async def clear_select_option(self):
        """Clears the selected value from a standard HTML <select> element.

        Sets the `value` attribute to an empty string and dispatches a `change` event
        to ensure dependent scripts detect the update.

        Raises:
            PlaywrightError: If the select element cannot be found or updated.
        """
        select_locator = self.page.locator(self.field_selector)
        await select_locator.evaluate(
            """el => {
                        el.value = '';
                        const event = new Event('change', { bubbles: true });
                        el.dispatchEvent(event);
            }"""
        )

    async def _remove_radio_option(self):
        """Unchecks and removes the `required` attribute from all radio button options of a field.

        Iterates over all radio options associated with the field name and ensures none
        of them are selected, effectively clearing the field.

        Raises:
            PlaywrightError: If the radio options cannot be found or updated.
        """
        radio_options = await self.get_radio_options(self.name.lower())
        for option in radio_options:
            await option.evaluate(
                """el => {
                el.checked = false;
                el.removeAttribute("required");
            }"""
            )
