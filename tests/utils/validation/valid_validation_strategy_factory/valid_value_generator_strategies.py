from abc import ABC, abstractmethod

from pages.core.standard_django_page import StandardDjangoPage

from tests.pages.core.constants import Constants, InputType
from tests.utils.data_generation.base_input_attributes import BaseInputAttributes
from utils.utils_functions import (
    format_date_in_dd_mm_aaaa,
    generate_base64_file,
    generate_negative_number,
    generate_random_float,
    generate_random_int,
    generate_random_phone_number,
    generate_random_string,
    generate_special_char_string,
    get_random_value_from_list,
)


class ValidDataStrategy(ABC, StandardDjangoPage, Constants, BaseInputAttributes):
    """Base class for valid data generation strategies."""

    def __init__(self, field_instance):
        """Initializes the ValidDataStrategy."""
        BaseInputAttributes.__init__(self, field_instance)

    @abstractmethod
    async def generate_data(self):
        """Generates valid data for the field."""
        raise NotImplementedError("You must implement generate_data")

    def _set_field_values(self, value, is_file=False):
        """Helper to set field_instance values consistently.

        Handles SELECT2/SELECT2_MULTIPLE automatically.
        """
        if self.input_type in [InputType.SELECT2, InputType.SELECT2_MULTIPLE]:
            value = self.field_instance.generate_select2_value(self.input_type, value)

        self.field_instance.field_value = value
        self.field_instance.index_value = value
        self.field_instance.filter_value = value if not is_file else self.field_instance.filter_value
        self.field_instance.validate_value = value if not is_file else self.field_instance.validate_value
        return self.field_instance


class DisabledStrategy(ValidDataStrategy):
    """Strategy for testing disabled fields."""

    async def generate_data(self):
        """Generates data for a disabled field."""
        await self.remove_disabled_attribute(self.field_selector)
        self.field_instance.is_editable = True
        value = generate_random_string(10)
        return self._set_field_values(value)


class NumberStrategy(ValidDataStrategy):
    """Strategy for generating random number data."""

    async def generate_data(self):
        """Generates a random number string."""
        value = str(generate_random_int(1, 99999))
        return self._set_field_values(value)


class SpecialCharsStrategy(ValidDataStrategy):
    """Strategy for generating special characters data."""

    async def generate_data(self):
        """Generates a string with special characters."""
        value = generate_special_char_string()
        return self._set_field_values(value)


class LettersStrategy(ValidDataStrategy):
    """Strategy for generating random letter data."""

    async def generate_data(self):
        """Generates a random string of letters."""
        value = generate_random_string(10)
        return self._set_field_values(value)


class NegativeNumberStrategy(ValidDataStrategy):
    """Strategy for generating negative number data."""

    async def generate_data(self):
        """Generates a negative number string."""
        value = str(generate_negative_number())
        return self._set_field_values(value)


class AlphanumericStrategy(ValidDataStrategy):
    """Strategy for generating alphanumeric data."""

    async def generate_data(self):
        """Generates an alphanumeric string."""
        value = str(generate_random_phone_number())
        return self._set_field_values(value)


class DateMMDDYYStrategy(ValidDataStrategy):
    """Strategy for generating MM/DD/YYYY date data."""

    async def generate_data(self):
        """Generates current date in MM/DD/AAAA format."""
        value = format_date_in_dd_mm_aaaa(self.date_now)
        self.field_instance.field_value = value
        self.field_instance.filter_value = value
        return self.field_instance


class DecimalNumberStrategy(ValidDataStrategy):
    """Strategy for generating decimal number data."""

    async def generate_data(self):
        """Generates a random decimal number string."""
        value = str(generate_random_float(1, 99999))
        return self._set_field_values(value)


class FileStrategy(ValidDataStrategy):
    """Strategy for generating file data."""

    async def generate_data(self):
        """Generates a file with valid format."""
        if self.custom_value:
            generated_file = generate_base64_file(extension=self.custom_value)
            self.field_instance.filter_value = self.custom_value
            self.field_instance.validate_value = generated_file["name"]
            return self._set_field_values(generated_file, is_file=True)

        accepted_format = [fmt for fmt in self.format_list if fmt in self.allowed_values]
        file_ext = get_random_value_from_list(accepted_format)
        generated_file = generate_base64_file(extension=file_ext)

        self.field_instance.filter_value = file_ext
        self.field_instance.validate_value = generated_file["name"]
        return self._set_field_values(generated_file, is_file=True)


class DuplicateAllowedStrategy(ValidDataStrategy):
    """Strategy for utilizing duplicate data."""

    async def generate_data(self):
        """Uses custom or original value for duplicate testing."""
        value = self.custom_value or self.original_value
        return self._set_field_values(value)


class EmptyStrategy(ValidDataStrategy):
    """Strategy for generating empty data."""

    async def generate_data(self):
        """Generates an empty value."""
        value = {} if self.input_type in [InputType.SELECT2, InputType.SELECT2_MULTIPLE] else ""
        return self._set_field_values(value)
