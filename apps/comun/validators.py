"""Reusable validators for files and Mexican identity/tax formats."""

import re

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.deconstruct import deconstructible

from apps.comun.consts import (
    CURP_FORMAT_REGEX,
    CURP_STRICT_REGEX,
    ERROR_CURP_INVALID,
    ERROR_FILE_TOO_LARGE,
    ERROR_LETTERS_ONLY,
    ERROR_RFC_INVALID,
    RFC_FORMAT_REGEX,
    RFC_STRICT_REGEX,
)


@deconstructible
class FileSizeValidator:
    """Validator for file size.

    Args:
        max_mb (int): Maximum allowed size in mebibytes (MiB).
    """

    def __init__(self, max_mb: int):
        """Initialize the file size validator.

        Args:
            max_mb (int): Maximum allowed size in mebibytes (MiB).
        """
        self.max_mb = max_mb
        self.max_bytes = max_mb * 1024 * 1024

    def __call__(self, value):
        """Validate file size against the configured limit.

        Args:
            value: File-like object with a `size` attribute in bytes.

        Raises:
            ValidationError: If the file exceeds the configured maximum size.
        """
        if value.size > self.max_bytes:
            raise ValidationError(
                ERROR_FILE_TOO_LARGE,
                params={"max_mb": self.max_mb},
            )

    def __eq__(self, other):
        """Needed so Django can compare validators when creating migrations."""
        return isinstance(other, FileSizeValidator) and self.max_mb == other.max_mb


# Only letters.
unicode_letter_validator = RegexValidator(
    re.compile(r"^[^\W\d_]+$"),
    ERROR_LETTERS_ONLY,
)

# Common mexican specific validators

rfc_format_validator = RegexValidator(
    RFC_FORMAT_REGEX,
    ERROR_RFC_INVALID,
)  # Ref: https://gist.github.com/gerardorochin/5718313


strict_rfc_validator = RegexValidator(
    RFC_STRICT_REGEX,
    ERROR_RFC_INVALID,
)  # Ref: https://gist.github.com/gerardorochin/5718313


curp_format_validator = RegexValidator(CURP_FORMAT_REGEX, ERROR_CURP_INVALID)


strict_curp_validator = RegexValidator(CURP_STRICT_REGEX, ERROR_CURP_INVALID)
