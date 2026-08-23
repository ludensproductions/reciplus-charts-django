"""Error handling middleware."""

import os

from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render

from apps.core.errors.error_codes import ErrorCode
from apps.core.errors.error_types import ErrorType
from apps.core.errors.exceptions import AppError
from utils import consts as utils_consts

from .json_logger import get_error_log, log_error, log_warning


class ExceptionErrorHandler:
    """Handle exceptions and present safe responses to the user."""

    def __init__(self, get_response):
        """Initialize the middleware with the downstream handler.

        Args:
            get_response (Callable): Next middleware or view.
        """
        self.get_response = get_response

    def __call__(self, request):
        """Invoke the middleware and return the response.

        Args:
            request (HttpRequest): Incoming request.

        Returns:
            HttpResponse: Response from downstream handler.
        """
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        """Handle exceptions with safe fallbacks and logging.

        Args:
            request (HttpRequest): Incoming request.
            exception (Exception): Raised exception.

        Returns:
            HttpResponse | None: Response when handled or None to continue default handling.
        """
        # This method is responsible for safe exception handling.
        if isinstance(exception, PermissionDenied):
            # Check if the templates folder and 403 template exist.
            if os.path.exists("templates"):
                if "403.html" in os.listdir("templates"):
                    return render(request=request, template_name="403.html", status=403)

            messages.error(request, utils_consts.ERROR_PERMISSION_DENIED)
            return HttpResponseRedirect("/")

        if isinstance(exception, AppError):
            log_warning(
                {
                    "code": exception.code,
                    "type": exception.type,
                    "user_message": exception.user_message,
                    "log_message": exception.log_message,
                    "context": exception.context,
                    **get_error_log(request),
                }
            )
            if "application/json" in request.headers.get("Accept", ""):
                return JsonResponse(
                    {"error": {"code": exception.code, "message": exception.user_message}},
                    status=exception.status_code,
                )
            return None

        log_error(
            {
                "code": ErrorCode.SYS_500,
                "type": ErrorType.SYSTEM_ERROR,
                "user_message": "An unexpected error occurred",
                "log_message": str(exception),
                **get_error_log(request),
            }
        )
        return None
