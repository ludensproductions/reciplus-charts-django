from tests.pages.core.constants import InvalidDataType

from . import invalid_value_generator_strategies as f


class InvalidDataFactory:
    """Factoría para crear estrategias de generación de datos inválidos.

    Esta factoría gestiona la creación de diferentes estrategias de generación de datos
    inválidos basándose en el enum InvalidDataType. Cada estrategia genera datos inválidos
    específicos para probar el comportamiento de validación de campos.

    Args:
        field_instance: La instancia del campo que contiene la configuración para la generación de datos.

    Attributes:
        strategies: Diccionario que mapea InvalidDataType a clases de estrategia.
        field_instance: La instancia del campo pasada durante la inicialización.
    """

    def __init__(self, field_instance):
        self.strategies = {
            InvalidDataType.EMAIL: f.InvalidEmailStrategy,
            InvalidDataType.MAX_LENGTH: f.MaxLengthStrategy,
            InvalidDataType.MIN_LENGTH: f.MinLengthStrategy,
            InvalidDataType.REQUIRED: f.RequiredFieldStrategy,
            InvalidDataType.READONLY: f.ReadOnlyStrategy,
            InvalidDataType.MIN_VALUE: f.MinValueStrategy,
            InvalidDataType.MAX_VALUE: f.MaxValueStrategy,
            InvalidDataType.NO_SPECIAL_CHARS: f.NoSpecialCharsStrategy,
            InvalidDataType.NUMBERS: f.InvalidNumberStrategy,
            InvalidDataType.LETTERS: f.InvalidLetterStrategy,
            InvalidDataType.NEGATIVE_NUMBER: f.NegativeNumberStrategy,
            InvalidDataType.DUPLICATED: f.DuplicatedStrategy,
            InvalidDataType.ALPHANUMERIC: f.AlphanumericStrategy,
            InvalidDataType.WEAK_PASSWORD: f.WeakPasswordStrategy,
            InvalidDataType.DATE_DD_MM_YYYY: f.DateDDMMYYYYStrategy,
            InvalidDataType.INVALID_FORMAT: f.InvalidFileFormatStrategy,
            InvalidDataType.FILE_WEIGHT: f.InvalidFileWeightStrategy,
            InvalidDataType.INVALID_OPTION: f.InvalidRadioOptionStrategy,
            InvalidDataType.CURP: f.InvalidCURPStrategy,
            InvalidDataType.RANGE_OF_DATES: f.InvalidRangeOfDates,
            InvalidDataType.BLANKS: f.BlankFieldStrategy,
            InvalidDataType.CUSTOM: f.CustomInvalidDataStrategy,
            # Agregar aquí otras estrategias según sea necesario
        }
        self.field_instance = field_instance

    def get_strategy(self, invalid_data_type):
        """Obtiene la estrategia apropiada de generación de datos inválidos.

        Args:
            invalid_data_type: El tipo de dato inválido a generar (enum InvalidDataType).

        Returns:
            Una instancia de la clase de estrategia para el tipo de dato inválido especificado.

        Raises:
            ValueError: Si no se encuentra ninguna estrategia para el tipo de dato inválido dado.
        """
        strategy_cls = self.strategies.get(invalid_data_type)
        if not strategy_cls:
            raise ValueError(f"No strategy found for invalid data type: {invalid_data_type}")
        return strategy_cls(self.field_instance)
