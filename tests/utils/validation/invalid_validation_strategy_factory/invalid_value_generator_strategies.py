import random
from abc import ABC, abstractmethod
from datetime import timedelta

from pages.core.standard_django_page import StandardDjangoPage

from tests.pages.core.constants import Constants, InputType
from tests.utils.data_generation.base_input_attributes import BaseInputAttributes
from utils.utils_functions import (
    format_date_in_dd_mm_aaaa,
    generate_base64_file,
    generate_negative_number,
    generate_random_email,
    generate_random_int,
    generate_random_number_with_length,
    generate_random_string,
    generate_special_char_string,
)


class InvalidDataStrategy(ABC, StandardDjangoPage, Constants, BaseInputAttributes):
    """Base class for invalid data generation strategies."""

    def __init__(self, field_instance):
        BaseInputAttributes.__init__(self, field_instance=field_instance)
        self._initialize_values()

    @abstractmethod
    async def generate_data(self):
        """Generates invalid data for the field."""
        raise NotImplementedError("Es necesario implementar generate_data")

    def _get_value_or_custom(self, default_value):
        """Retorna el custom_value si existe, de lo contrario retorna el valor por defecto.

        Args:
            default_value: Valor a usar si custom_value no está definido (puede ser un callable)

        Returns:
            El custom_value o el default_value
        """
        if self.custom_value:
            return self.custom_value
        return default_value() if callable(default_value) else default_value

    def _initialize_values(self):
        """Inicializa los mensajes de error basados en las restricciones del campo."""
        self.max_length_error_message = self.MAX_LENGTH_ERROR_MESSAGE.format(max_length=self.max_length)
        self.min_length_error_message = self.MIN_LENGTH_ERROR_MESSAGE.format(min_length=self.min_length)
        self.min_value_error_message = self.MIN_VALUE_ERROR_MESSAGE.format(min_value=self.min_value)
        self.max_value_error_message = self.MAX_VALUE_ERROR_MESSAGE.format(max_value=self.max_value)

        if self.input_type == InputType.FILE:
            self.invalid_format_message = self.INVALID_FORMAT_MESSAGE.format(
                allowed_formats=", ".join(self.allowed_values)
            )
            self.invalid_weight_message = self.INVALID_WEIGHT_ERROR_MESSAGE.format(
                max_value="".join(str(self.max_value))
            )


class InvalidEmailStrategy(InvalidDataStrategy):
    """Strategy for generating invalid email data."""

    async def generate_data(self):
        """Generates an invalid email."""
        invalid_value = self._get_value_or_custom(lambda: generate_random_string(10))
        if self.input_type in [InputType.SELECT2, InputType.SELECT2_MULTIPLE]:
            invalid_value = self.field_instance.convert_to_select2_format_value(invalid_value)
        await self.remove_type_attribute(self.field_selector, page=self.page)
        return invalid_value, self.INVALID_EMAIL_MESSAGE


class MaxLengthStrategy(InvalidDataStrategy):
    """Strategy for generating data exceeding max length."""

    async def generate_data(self):
        """Generates a value longer than allowed max length."""
        invalid_value = self._get_value_or_custom(
            lambda: (
                generate_random_email(self.max_length + 1)
                if self.input_type == InputType.EMAIL
                else generate_random_string(self.max_length + 1)
            )
        )

        if self.input_type not in [InputType.SELECT2, InputType.SELECT2_MULTIPLE]:
            await self.remove_max_length_attribute(self.field_selector)

        return invalid_value, self.max_length_error_message


class MinLengthStrategy(InvalidDataStrategy):
    """Strategy for generating data below min length."""

    async def generate_data(self):
        """Generates a value shorter than allowed min length."""
        invalid_value = self._get_value_or_custom(
            lambda: (
                generate_random_number_with_length(self.min_length - 1)
                if self.input_type == InputType.PHONE
                else generate_random_string(self.min_length - 1)
            )
        )

        if self.input_type not in [InputType.SELECT2, InputType.SELECT2_MULTIPLE]:
            await self.remove_min_length_attribute(self.field_selector)

        if self.input_type == InputType.PHONE:
            return invalid_value, self.INVALID_PHONE_MESSAGE
        else:
            return invalid_value, self.min_length_error_message


class RequiredFieldStrategy(InvalidDataStrategy):
    """Strategy for testing required fields with empty data."""

    async def generate_data(self):
        """Generates empty data for a required field."""
        invalid_value = ""
        if self.input_type in [InputType.SELECT2, InputType.SELECT2_MULTIPLE]:
            name_selector = self.name.lower().replace(" ", "_")
            await self.remove_required_attribute(f'select[name="{name_selector}"]')
        else:
            await self.remove_required_attribute(self.field_selector)
        if self.input_type == InputType.FILE:
            # Elimina el archivo que se ingresa al inicializar los valores
            await self.page.set_input_files(self.field_selector, [])
            invalid_value = []
        elif self.input_type == InputType.RADIO:
            await self.field_instance._remove_radio_option()
            invalid_value = None
        elif self.input_type == InputType.SELECT2_MULTIPLE:
            await self.field_instance.clear_multi_selector_options()
            invalid_value = []
        elif self.input_type == InputType.SELECT2:
            await self.field_instance.clear_select2_options()
            invalid_value = []
        elif self.input_type == InputType.SELECT:
            await self.field_instance.clear_select_option()
        return invalid_value, self.REQUIRED_FIELD_MESSAGE


class ReadOnlyStrategy(InvalidDataStrategy):
    """Strategy for testing read-only fields."""

    async def generate_data(self):
        """Attempts to modify a read-only field."""
        await self.remove_readonly_attribute(self.field_selector)
        self.generate_valid_data(True)
        return "", self.READONLY_ERROR_MESSAGE


class MinValueStrategy(InvalidDataStrategy):
    """Strategy for generating data below min value."""

    async def generate_data(self):
        """Generates a value less than allowed min value."""
        invalid_value = str(self._get_value_or_custom(lambda: self.min_value - 1))
        await self.remove_min_attribute(self.field_selector)
        return invalid_value, self.min_value_error_message


class MaxValueStrategy(InvalidDataStrategy):
    """Strategy for generating data above max value."""

    async def generate_data(self):
        """Generates a value greater than allowed max value."""
        invalid_value = str(self._get_value_or_custom(lambda: self.max_value + 1))
        await self.remove_max_attribute(self.field_selector)
        return invalid_value, self.max_value_error_message


class NoSpecialCharsStrategy(InvalidDataStrategy):
    """Strategy for testing no special characters constraint."""

    async def generate_data(self):
        """Generates data containing special characters."""
        invalid_value = self._get_value_or_custom(generate_special_char_string)
        return invalid_value, self.NO_SPECIAL_CHARS_ERROR_MESSAGE


class InvalidNumberStrategy(InvalidDataStrategy):
    """Strategy for testing invalid number input."""

    async def generate_data(self):
        """Generates invalid number data."""
        invalid_value = str(self._get_value_or_custom(lambda: generate_random_int(5, 10)))
        await self.remove_type_attribute(self.field_selector)
        return invalid_value, self.LETTERS_ERROR_MESSAGE


class InvalidLetterStrategy(InvalidDataStrategy):
    """Strategy for testing invalid letter input."""

    async def generate_data(self):
        """Generates invalid letter data."""
        invalid_value = self._get_value_or_custom(lambda: generate_random_string(10))
        await self.remove_type_attribute(self.field_selector)
        return invalid_value, self.NUMBER_DATA_TYPE_MESSAGE


class NegativeNumberStrategy(InvalidDataStrategy):
    """Strategy for testing negative number input."""

    async def generate_data(self):
        """Generates a negative number."""
        invalid_value = str(self._get_value_or_custom(generate_negative_number))
        await self.remove_type_attribute(self.field_selector)
        return invalid_value, self.NEGATIVE_NUMBER_ERROR_MESSAGE


class DuplicatedStrategy(InvalidDataStrategy):
    """Strategy for testing duplicated values."""

    async def generate_data(self):
        """Generates duplicated data."""
        await self.remove_type_attribute(self.field_selector)
        return self.custom_value, (
            self.DUPLICATED_EMAIL_MESSAGE if self.input_type == InputType.EMAIL else self.DUPLICATED_REGISTER_MESSAGE
        )


class WeakPasswordStrategy(InvalidDataStrategy):
    """Strategy for testing weak passwords."""

    async def generate_data(self):
        """Generates a weak password."""
        invalid_value = self._get_value_or_custom(lambda: generate_random_string(10))
        await self.remove_type_attribute(self.field_selector)
        return invalid_value, self.WEAK_PASSWORD_MESSAGE


class AlphanumericStrategy(InvalidDataStrategy):
    """Strategy for testing alphanumeric constraints."""

    async def generate_data(self):
        """Generates alphanumeric data."""
        invalid_value = self._get_value_or_custom(generate_special_char_string)
        await self.remove_type_attribute(self.field_selector)
        return invalid_value, (
            self.INVALID_PHONE_MESSAGE if self.input_type == InputType.PHONE else self.NO_SPECIAL_CHARS_ERROR_MESSAGE
        )


class DateDDMMYYYYStrategy(InvalidDataStrategy):
    """Strategy for testing invalid date format."""

    async def generate_data(self):
        """Generates invalid date data."""
        invalid_value = self._get_value_or_custom(lambda: generate_random_string(10))
        await self.remove_type_attribute(self.field_selector)
        return invalid_value, self.INVALID_DATE_ERROR_MESSAGE


class InvalidFileFormatStrategy(InvalidDataStrategy):
    """Strategy for testing invalid file formats."""

    async def generate_data(self):
        """Generates a file with an invalid format."""
        invalid_value = None
        if not self.custom_value:
            extension = "test"  # Extensión no permitida
            invalid_value = generate_base64_file(extension=extension)
        else:
            invalid_value = generate_base64_file(extension=self.custom_value)
        return invalid_value, self.invalid_format_message


class InvalidFileWeightStrategy(InvalidDataStrategy):
    """Strategy for testing invalid file weights."""

    async def generate_data(self):
        """Generates a file exceeding weight limit."""

        def generate_heavy_file():
            selected_extension = random.randint(1, len(self.allowed_values))
            extension = random.sample(self.allowed_values, selected_extension)
            weight = int(self.max_value + 1) if not isinstance(self.max_length, int) else self.max_value + 1
            return generate_base64_file(extension=extension[0], weight=weight)

        invalid_value = self._get_value_or_custom(generate_heavy_file)
        return invalid_value, self.invalid_weight_message


class InvalidRadioOptionStrategy(InvalidDataStrategy):
    """Strategy for testing invalid radio options."""

    async def generate_data(self):
        """Selects an invalid radio option."""
        # Obtener todos los radio buttons dentro del contenedor
        radio_options = await self.get_radio_options(self.name.lower())
        if not self.custom_value or self.custom_value == "":
            self.custom_value = generate_random_string(2).capitalize()
        # Cambiar el valor y deseleccionar el radio button
        await radio_options[0].evaluate(
            """(el, custom_value) => {
            el.value = custom_value;  // Cambiar el valor (aunque no tendrá efecto real)
            el.checked = false;      // Deseleccionar el radio button
        }""",
            self.custom_value,
        )  # Pasar self.custom_value como argumento

        self.field_value = self.custom_value
        self.field_selector = f"input[value={self.field_value}]"

        return f"Seleccione una opción válida. {self.custom_value} no es una de las opciones disponibles."


class InvalidCURPStrategy(InvalidDataStrategy):
    """Strategy for test invalid CURP."""

    async def generate_data(self):
        """Genera una CURP inválida para probar la validación."""
        invalid_value = self._get_value_or_custom(lambda: generate_random_string(18))
        return invalid_value, self.INVALID_CURP_MESSAGE


class InvalidRangeOfDates(InvalidDataStrategy):
    """Strategy for testing invalid date ranges."""

    async def generate_data(self):
        """Generates an invalid date range."""

        def generate_invalid_date():
            if self.input_type == InputType.DATE_START:
                return format_date_in_dd_mm_aaaa(self.date_now)
            elif self.input_type == InputType.DATE_MIDDLE:
                return format_date_in_dd_mm_aaaa(self.date_now + timedelta(days=-1))
            elif self.input_type == InputType.DATE_END:
                return format_date_in_dd_mm_aaaa(self.date_now + timedelta(days=-2))
            return None

        invalid_value = self._get_value_or_custom(generate_invalid_date)
        return invalid_value, self.WRONG_RANGE_OF_DATES_ERROR_MESSAGE


class BlankFieldStrategy(InvalidDataStrategy):
    """Strategy for testing blank fields."""

    async def generate_data(self):
        """Generates blank data for a field."""

        def generate_blank_value():
            if self.input_type in [InputType.SELECT2, InputType.SELECT2_MULTIPLE]:
                return {self.select2_search_selector: "  "}
            return "  "

        invalid_value = self._get_value_or_custom(generate_blank_value)
        return invalid_value, self.REQUIRED_FIELD_MESSAGE


class CustomInvalidDataStrategy(InvalidDataStrategy):
    """Strategy for testing custom invalid data."""

    async def generate_data(self):
        """Generates custom invalid data."""
        return self.custom_value, None
