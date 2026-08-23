from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class IndexView(LoginRequiredMixin, TemplateView):
    """View responsible for rendering the main chat page.

    Access to this view is restricted to authenticated users. It renders
    a static template and injects minimal context data required by the
    UI.
    """

    template_name = "chat/index.html"

    def get_context_data(self, **kwargs):
        """Adds additional context data for the chat template.

        Args:
            **kwargs: Keyword arguments passed from the URL configuration.

        Returns:
            dict: Template context including the page title.
        """
        context = super().get_context_data(**kwargs)
        context["title"] = "Chat"
        return context
