from tests.pages.core.constants import ValidDataType as v

from . import valid_value_generator_strategies as f


class ValidDataFactory:
    """Factory for creating valid data generation strategies."""

    def __init__(self, field_instance):
        """Initializes the ValidDataFactory."""
        self.strategies = {
            v.DISABLED: f.DisabledStrategy,
            v.NUMBERS: f.NumberStrategy,
            v.SPECIAL_CHARS: f.SpecialCharsStrategy,
            v.LETTERS: f.LettersStrategy,
            v.NEGATIVE_NUMBER: f.NegativeNumberStrategy,
            v.ALPHANUMERIC: f.AlphanumericStrategy,
            v.DATE_DD_MM_YYYY: f.DateMMDDYYStrategy,
            v.DECIMAL: f.DecimalNumberStrategy,
            v.VALID_FORMAT: f.FileStrategy,
            v.ALLOW_DUPLICATES: f.DuplicateAllowedStrategy,
            v.EMPTY: f.EmptyStrategy,
            # Agregar aquí otras estrategias según sea necesario
        }
        self.field_instance = field_instance

    def get_strategy(self, valid_data_type):
        """Returns the appropriate strategy for the given valid data type."""
        strategy_cls = self.strategies.get(valid_data_type)
        if not strategy_cls:
            raise ValueError(f"No strategy found for valid data type: {valid_data_type}")
        return strategy_cls(self.field_instance)
