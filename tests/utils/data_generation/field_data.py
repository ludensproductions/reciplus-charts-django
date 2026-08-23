"""Módulo que define la estructura estandarizada para datos generados por estrategias."""

from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class FieldData:
    """Estructura estandarizada para datos generados por estrategias.

    Esta clase reemplaza el uso de tuplas con posiciones implícitas,
    proporcionando un contrato explícito entre estrategias y consumidores.

    Attributes:
        value: Valor principal para llenar el campo (obligatorio).
        filter_value: Valor para usar en filtros. Por defecto igual a value.
        selector: Selector CSS si la estrategia lo modifica (opcional).
        validate_value: Valor específico para validación. Por defecto igual a filter_value.
        index_value: Valor para mostrar en la tabla índice. Por defecto igual a value.

    Example:
        >>> data = FieldData(value="test@email.com")
        >>> data.filter_value  # Será "test@email.com" por defecto
        >>> data.validate_value  # Será "test@email.com" por defecto

        >>> data = FieldData(
        ...     value={"selector": "value"},
        ...     filter_value="value",
        ...     validate_value="value",
        ... )
    """

    value: Any
    filter_value: Optional[Any] = None
    selector: Optional[str] = None
    validate_value: Optional[Any] = None
    index_value: Optional[Any] = None

    def __post_init__(self):
        """Aplica valores por defecto después de la inicialización."""
        if self.filter_value is None:
            self.filter_value = self.value
        if self.validate_value is None:
            self.validate_value = self.filter_value
        if self.index_value is None:
            self.index_value = self.value
