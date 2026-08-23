from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import TemplateView

from .consts import (
    USER_CARDS,
    USUARIOS_TEMPLATE,
    USUARIOS_TITLE,
)


class IndexView(PermissionRequiredMixin, TemplateView):
    """Render the user cards dashboard view."""

    template_name = USUARIOS_TEMPLATE
    all_cards = USER_CARDS
    permission_required = "users_module.view_users_module"

    def get_context_data(self, **kwargs):
        """Build context data for the users dashboard.

        Args:
            **kwargs: Context keyword arguments from the parent method.

        Returns:
            dict: Template context including title and filtered cards.
        """
        context = super().get_context_data(**kwargs)
        context["title"] = USUARIOS_TITLE
        context["cards"] = [card for card in self.all_cards if self.request.user.has_perm(card["perm"])]
        return context
