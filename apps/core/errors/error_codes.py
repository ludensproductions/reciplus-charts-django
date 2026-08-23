from enum import StrEnum


class ErrorCode(StrEnum):
    """Enumeration of stable and documented error codes."""

    # Auth
    AUTH_001 = "AUTH_001"  # Unauthenticated user
    AUTH_002 = "AUTH_002"  # User without permissions

    # Validation
    VAL_001 = "VAL_001"  # Data validation failed
    VAL_002 = "VAL_002"  # Missing required parameter

    # Business rule
    BUS_001 = "BUS_001"  # Business rule violated
    BUS_002 = "BUS_002"  # Resource in invalid state

    # Integration
    INT_001 = "INT_001"  # Error with external service
    INT_002 = "INT_002"  # Integration timeout

    # System
    SYS_500 = "SYS_500"  # Unexpected system error

    # Ninja/API specific error codes
    API_001 = "API_001"  # Object not found
    API_002 = "API_002"  # Schema validation failed
    API_003 = "API_003"  # Custom value error
