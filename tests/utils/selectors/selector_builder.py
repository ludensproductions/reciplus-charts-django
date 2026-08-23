from typing import Dict

from tests.pages.core.constants import InputType


class SelectorTemplate:
    """Templates de selectores CSS para cada tipo de input.

    Esta clase interna actúa como un registro de patrones de selectores,
    facilitando el mantenimiento y la extensión de nuevos tipos de input.
    """

    INPUT = 'input[name="{name}"]'
    SELECT2 = "#div_id_{name}"
    SELECT = 'select[name="{name}"]'
    TEXTAREA = 'textarea[name="{name}"]'
    CHECKBOX_LIST = "#div_id_{name}"
    WYSIWYG = "#div_id_{name}"
    MULTIPLE_FILES = "#div_id_{name}"

    _TEMPLATES: Dict[InputType, str] = {
        InputType.TEXT: INPUT,
        InputType.NUMBER: INPUT,
        InputType.EMAIL: INPUT,
        InputType.PASSWORD: INPUT,
        InputType.PHONE: INPUT,
        InputType.DECIMAL: INPUT,
        InputType.CURP: INPUT,
        InputType.RFC: INPUT,
        InputType.ZIPCODE: INPUT,
        InputType.IP: INPUT,
        InputType.MAC: INPUT,
        InputType.URL: INPUT,
        InputType.REGEX: INPUT,
        InputType.DATE: INPUT,
        InputType.TIME: INPUT,
        InputType.DATE_TIME: INPUT,
        InputType.DATE_START: INPUT,
        InputType.DATE_MIDDLE: INPUT,
        InputType.DATE_END: INPUT,
        InputType.RANGE_OF_DATES: INPUT,
        InputType.TEXTAREA: TEXTAREA,
        InputType.SELECT: SELECT,
        InputType.SELECT2: SELECT2,
        InputType.SELECT2_MULTIPLE: SELECT2,
        InputType.CHECKBOX: INPUT,
        InputType.CHECKBOX_LIST: CHECKBOX_LIST,
        InputType.RADIO: INPUT,
        InputType.FILE: INPUT,
        InputType.WYSIWYG: WYSIWYG,
        InputType.MULTIPLE_FILES: MULTIPLE_FILES,
    }

    @classmethod
    def get_template(cls, input_type: InputType) -> str:
        """Obtiene el template de selector para un tipo de input específico.

        Args:
            input_type: Tipo de input del campo.

        Returns:
            Template de selector CSS con placeholder {name}.

        Raises:
            ValueError: Si el tipo de input no está soportado.
        """
        template = cls._TEMPLATES.get(input_type)
        if template is None:
            raise ValueError(
                f"InputType '{input_type.name}' no tiene un template de selector definido. "
                f"Tipos soportados: {', '.join(t.name for t in cls._TEMPLATES.keys())}"
            )
        return template

    @classmethod
    def is_supported(cls, input_type: InputType) -> bool:
        """Verifica si un tipo de input está soportado.

        Args:
            input_type: Tipo de input a verificar.

        Returns:
            True si el tipo está soportado, False en caso contrario.
        """
        return input_type in cls._TEMPLATES

    @classmethod
    def get_supported_types(cls) -> list[str]:
        """Obtiene la lista de tipos de input soportados.

        Returns:
            Lista con los nombres de los tipos soportados.
        """
        return [input_type.name for input_type in cls._TEMPLATES.keys()]


class FieldSelectorBuilder:
    """Generador dinámico de selectores CSS para campos de formulario.

    Implementa el patrón Factory para construir selectores basados en
    el tipo de input y el nombre del campo.


    """

    def build(self, input_type: InputType, field_name: str) -> str:
        """Construye un selector CSS para un campo de formulario.

        Args:
            input_type: Tipo de input del campo.
            field_name: Nombre del campo (atributo 'name' en HTML).

        Returns:
            Selector CSS completo para el campo.

        Raises:
            ValueError: Si el tipo de input no está soportado.
            TypeError: Si los argumentos no son del tipo esperado.

        """
        self._validate_arguments(input_type, field_name)
        template = SelectorTemplate.get_template(input_type)
        return template.format(name=field_name)

    @staticmethod
    def quick_build(input_type: InputType, field_name: str) -> str:
        """Método estático para construcción rápida de selectores.

        Crea una instancia temporal del builder y construye el selector.
        Recomendado para uso en casos simples donde no se necesita
        reutilizar la instancia.

        Args:
            input_type: Tipo de input del campo.
            field_name: Nombre del campo.

        Returns:
            Selector CSS completo.
        """
        return FieldSelectorBuilder().build(input_type, field_name)

    @staticmethod
    def is_input_type_supported(input_type: InputType) -> bool:
        """Verifica si un tipo de input está soportado.

        Args:
            input_type: Tipo de input a verificar.

        Returns:
            True si está soportado, False en caso contrario.

        """
        return SelectorTemplate.is_supported(input_type)

    def _validate_arguments(self, input_type: InputType, field_name: str) -> None:
        """Valida los argumentos de entrada.

        Args:
            input_type: Tipo de input a validar.
            field_name: Nombre del campo a validar.

        Raises:
            TypeError: Si los tipos de argumentos son incorrectos.
            ValueError: Si el tipo de input no está soportado o el nombre está vacío.
        """
        if not isinstance(input_type, InputType):
            raise TypeError(f"input_type debe ser InputType, se recibió {type(input_type).__name__}")

        if not isinstance(field_name, str):
            raise TypeError(f"field_name debe ser str, se recibió {type(field_name).__name__}")

        if not field_name.strip():
            raise ValueError("field_name no puede estar vacío")

        if not SelectorTemplate.is_supported(input_type):
            supported = ", ".join(SelectorTemplate.get_supported_types())
            raise ValueError(f"InputType '{input_type.name}' no está soportado. " f"Tipos soportados: {supported}")
