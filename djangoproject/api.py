from http import HTTPStatus

from django.core.exceptions import ObjectDoesNotExist
from ninja_extra import NinjaExtraAPI
from ninja_extra.exceptions import ValidationError

# Security / Authentication endpoints
from ninja_jwt.controller import NinjaJWTDefaultController

# Importing API Controllers
from apps.comun.api.exceptions import CustomValueError
from apps.graphs.api_controller import GraphsController
from apps.graphs.auth_bridge_controller import GraphsAuthBridgeController
from apps.comun.consts import (
    ERROR_BAD_REQUEST,
    ERROR_INTERNAL_SERVER,
    ERROR_INTERNAL_SERVER_DETAIL,
    ERROR_OBJECT_DOES_NOT_EXIST,
    ERROR_VALIDATION_FAILED,
)
from apps.core.errors.error_codes import ErrorCode
from apps.core.errors.error_types import ErrorType

# Utils
from utils.json_logger import get_error_log, log_error, log_warning


def _parse_validation_errors(errors):
    """Converts ErrorDetail objects from validation errors into plain strings."""
    return [{"loc": [str(l) for l in e["loc"]], "msg": str(e["msg"])} for e in errors]


# Registration of API Controllers
api = NinjaExtraAPI(csrf=False)  # CSRF Protection

api.register_controllers(
    NinjaJWTDefaultController,  # JWT Authentication Endpoints
    GraphsController,
    GraphsAuthBridgeController,
)


# Error handling
@api.exception_handler(ObjectDoesNotExist)
def handle_object_does_not_exist(request, exc):
    """Handles Django `ObjectDoesNotExist` exceptions.

    This handler is triggered when a requested database object cannot
    be found. It returns a standardized NOT FOUND response without
    exposing internal model details.

    Args:
        request (HttpRequest): Incoming HTTP request that caused the
            exception.
        exc (ObjectDoesNotExist): Raised exception instance.

    Returns:
        HttpResponse: JSON response with HTTP 404 status containing
        error metadata.
    """
    log_warning(
        {"code": ErrorCode.API_001, "type": ErrorType.API_ERROR, "log_message": str(exc), **get_error_log(request)}
    )
    return api.create_response(
        request,
        {
            "status": HTTPStatus.NOT_FOUND,
            "message": ERROR_OBJECT_DOES_NOT_EXIST,
            "detail": str(exc),
        },
        status=HTTPStatus.NOT_FOUND,
    )


@api.exception_handler(ValidationError)
def handle_validation_error(request, exc):
    """Handles validation errors raised during request parsing or schema validation.

    This handler supports validation errors coming from different
    sources (e.g., Django, Pydantic, ninja_extra), normalizing their
    structure into a consistent error format.

    The resulting error payload:
    - Uses HTTP 422 (Unprocessable Entity).
    - Groups validation errors by field and nested structure.
    - Preserves array indices for list-based inputs.

    Args:
        request (HttpRequest): Incoming HTTP request that caused the
            validation error.
        exc (ValidationError): Validation exception instance.

    Returns:
        HttpResponse: JSON response with HTTP 422 status containing
            structured validation errors.
    """
    # ninja_extra ValidationError uses .detail instead of .errors
    errors = exc.detail if hasattr(exc, "detail") else exc.errors if hasattr(exc, "errors") else []
    log_warning(
        {
            "code": ErrorCode.API_002,
            "type": ErrorType.API_ERROR,
            "log_message": _parse_validation_errors(errors),
            **get_error_log(request),
        }
    )
    return api.create_response(
        request,
        {
            "status": "error",
            "code": HTTPStatus.UNPROCESSABLE_ENTITY.value,
            "message": ERROR_VALIDATION_FAILED,
            "errors": process_validation_errors(errors),
        },
        status=HTTPStatus.UNPROCESSABLE_ENTITY,
    )


@api.exception_handler(CustomValueError)
def handle_custom_value_error(request, exc):
    """Handles application-specific value errors.

    This handler is used for domain-level validation failures that do
    not fit schema validation but still represent client-side errors.

    Args:
        request (HttpRequest): Incoming HTTP request that caused the
            exception.
        exc (CustomValueError): Raised custom exception.

    Returns:
        HttpResponse: JSON response with HTTP 400 status describing the
            validation issue.
    """
    log_warning(
        {"code": ErrorCode.API_003, "type": ErrorType.API_ERROR, "log_message": str(exc), **get_error_log(request)}
    )
    return api.create_response(
        request,
        {
            "status": "error",
            "code": HTTPStatus.BAD_REQUEST.value,
            "message": ERROR_BAD_REQUEST,
            "detail": str(exc),
        },
        status=HTTPStatus.BAD_REQUEST,
    )


@api.exception_handler(Exception)
def handle_internal_server_error(request, exc):
    """Handles uncaught exceptions and internal server errors.

    This is a catch-all handler intended to:
    - Prevent unhandled exceptions from leaking stack traces.
    - Log unexpected errors for later investigation.
    - Return a generic error message to the client.

    Args:
        request (HttpRequest): Incoming HTTP request that caused the
            exception.
        exc (Exception): Unhandled exception instance.

    Returns:
        HttpResponse: JSON response with HTTP 500 status and a generic
            error message.
    """
    log_error(
        {
            "code": ErrorCode.SYS_500,
            "type": ErrorType.SYSTEM_ERROR,
            "user_message": "An unexpected error occurred",
            "log_message": str(exc),
            **get_error_log(request),
        }
    )
    return api.create_response(
        request,
        {
            "status": HTTPStatus.INTERNAL_SERVER_ERROR,
            "message": ERROR_INTERNAL_SERVER,
            "detail": ERROR_INTERNAL_SERVER_DETAIL,
        },
        status=HTTPStatus.INTERNAL_SERVER_ERROR,
    )


def process_validation_errors(exc_errors):
    """Transforms raw validation errors into a nested, client-friendly structure.

    This function processes validation error entries containing
    location paths (`loc`) and messages (`msg`), converting them into
    a hierarchical dictionary that mirrors the input payload structure.

    Features:
    - Supports nested objects.
    - Supports arrays with index-based error grouping.
    - Skips technical wrapper keys such as `body` and `payload`.
    - Preserves error context for deeply nested fields.

    Args:
        exc_errors (list[dict]): List of validation error objects.
            Each error is expected to contain:
                - "loc" (list): Location path of the error.
                - "msg" (str): Error message.

    Returns:
        dict: Structured dictionary of validation errors suitable for
            frontend consumption.
    """

    def process_location(loc, msg, target_dict):
        if not loc:
            return

        current = target_dict
        for i, key in enumerate(loc[:-1]):
            if isinstance(key, int):
                # Handle array elements
                if "objetos" not in current:
                    current["objetos"] = []

                # Ensure we have enough elements in the array
                while len(current["objetos"]) <= key:
                    current["objetos"].append({"index": len(current["objetos"]), "errors": {}})

                current = current["objetos"][key]["errors"]
            else:
                # Handle nested objects
                if key not in ("body", "payload"):
                    if key not in current:
                        current[key] = {}
                    current = current[key]

        # Set the final error message
        last_key = loc[-1]
        if isinstance(last_key, int):
            if "objetos" not in current:
                current["objetos"] = []
            while len(current["objetos"]) <= last_key:
                current["objetos"].append({"index": len(current["objetos"]), "errors": {}})
            current["objetos"][last_key]["errors"] = msg
        else:
            current[last_key] = msg

    errors = {}
    for error in exc_errors:
        process_location(error["loc"], error["msg"], errors)

    return errors
