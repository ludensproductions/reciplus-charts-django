from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

# Utils
from utils.json_logger import log

from .consts import (
    INDEX_TEMPLATE,
)


class IndexView(LoginRequiredMixin, TemplateView):
    """Render the main dashboard index page."""

    template_name = INDEX_TEMPLATE

    def get(self, request, *args, **kwargs):
        """Handle GET requests for the dashboard index.

        Args:
            request (HttpRequest): Incoming HTTP request.
            *args: Positional arguments passed to the parent method.
            **kwargs: Keyword arguments passed to the parent method.

        Returns:
            HttpResponse: Rendered index page response.
        """
        log({"status_code": 200, "message": "log de prueba"})
        return super().get(request, *args, **kwargs)
