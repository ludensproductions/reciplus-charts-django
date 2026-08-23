from enum import StrEnum


class ErrorType(StrEnum):
    """Enumeration of error classification types."""

    VALIDATION_ERROR = "VALIDATION_ERROR"
    PERMISSION_ERROR = "PERMISSION_ERROR"
    BUSINESS_RULE_ERROR = "BUSINESS_RULE_ERROR"
    INTEGRATION_ERROR = "INTEGRATION_ERROR"
    SYSTEM_ERROR = "SYSTEM_ERROR"
    API_ERROR = "API_ERROR"
