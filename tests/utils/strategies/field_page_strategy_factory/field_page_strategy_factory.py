from tests.pages.core.constants import InputType

from . import field_page_input_strategies as f


class FieldDataStrategyFactory:
    """Clase para crear estrategias de manejo de inputs."""

    def __init__(self, field_instance):
        """Initializes the FieldDataStrategyFactory."""
        self.strategies = {
            InputType.CHECKBOX: f.CheckboxInputStrategy,
            InputType.CHECKBOX_LIST: f.CheckboxListInputStrategy,
            InputType.DATE: f.DateInputStrategy,
            InputType.DECIMAL: f.DecimalInputStrategy,
            InputType.EMAIL: f.EmailInputStrategy,
            InputType.FILE: f.FileInputStrategy,
            InputType.MULTIPLE_FILES: f.MultipleFilesInputStrategy,
            InputType.TEXT: f.TextInputStrategy,
            InputType.NUMBER: f.NumberInputStrategy,
            InputType.PASSWORD: f.PasswordInputStrategy,
            InputType.PHONE: f.PhoneInputStrategy,
            InputType.RADIO: f.RadioInputStrategy,
            InputType.SELECT: f.SelectInputStrategy,
            InputType.SELECT2: f.Select2InputStrategy,
            InputType.SELECT2_MULTIPLE: f.Select2MultipleInputStrategy,
            InputType.CURP: f.CURPInputStrategy,
            InputType.RFC: f.RFCInputStrategy,
            InputType.TIME: f.TimeInputStrategy,
            InputType.DATE_START: f.InitialDateInputStrategy,
            InputType.DATE_MIDDLE: f.MiddleDateInputStrategy,
            InputType.DATE_END: f.FinalDateInputStrategy,
            InputType.DATE_TIME: f.DateTimeInputStrategy,
            InputType.TEXTAREA: f.TextareaInputStrategy,
            InputType.RANGE_OF_DATES: f.RangeOfDatesInputStrategy,
            InputType.IP: f.IPInputStrategy,
            InputType.MAC: f.MACInputStrategy,
            InputType.ZIPCODE: f.ZipCodeInputStrategy,
            InputType.REGEX: f.RegexInputStrategy,
            InputType.URL: f.URLInputStrategy,
            InputType.WYSIWYG: f.WYSIWYGInputStrategy,
        }
        self.field_instance = field_instance

    def get_field_data_strategy(self, input_type):
        """Returns the appropriate field data strategy for the given input type."""
        strategy_cls = self.strategies.get(input_type)
        if not strategy_cls:
            raise ValueError(f"No strategy found for input type: {input_type}")
        return strategy_cls(self.field_instance)
