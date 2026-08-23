import re


def regex_flags_to_str(flags: int) -> str:
    """Converts re flags into a compact string representation (HTML-safe).

    Args:
        flags (int): The regex flags as an integer.

    Returns:
        str: A string representing the active regex flags.
    """
    mapping = {
        re.IGNORECASE: "I",
        re.MULTILINE: "M",
        re.DOTALL: "S",
        re.UNICODE: "U",
        re.ASCII: "A",
        re.VERBOSE: "X",
    }
    return "".join(letter for flag, letter in mapping.items() if flags & flag)


class RegexValidator:
    """Validator for regex patterns with named presets."""

    patterns = {
        "postal_code": r"^\d{5}$",  # Solo 5 dígitos numéricos  # US ZIP codes: 12345 or 12345-6789
    }

    @classmethod
    def validate(cls, pattern_name: str, value: str) -> bool:
        """Validates a value against a named regex pattern.

        Args:
            pattern_name (str): The name of the pattern to use.
            value (str): The value to validate.

        Returns:
            bool: True if the value matches the pattern, False otherwise.

        Raises:
            ValueError: If the pattern name does not exist.
        """
        pattern = cls.patterns.get(pattern_name)
        if not pattern:
            raise ValueError(f"No pattern found for '{pattern_name}'")
        return re.match(pattern, value) is not None
