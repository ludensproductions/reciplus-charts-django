from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import TemplateView

from .consts import (
    CATALOG_CARDS,
    CATALOGOS_TEMPLATE,
    CATALOGOS_TITLE,
)


class IndexView(PermissionRequiredMixin, TemplateView):
    """Render the catalog cards dashboard view."""

    template_name = CATALOGOS_TEMPLATE
    all_cards = CATALOG_CARDS
    permission_required = "catalogos.view_catalogos"

    def get_context_data(self, **kwargs):
        """Build context data for the catalog dashboard.

        Args:
            **kwargs: Context keyword arguments from the parent method.

        Returns:
            dict: Template context including title and filtered cards.
        """
        context = super().get_context_data(**kwargs)
        context["title"] = CATALOGOS_TITLE
        context["cards"] = []
        for card in self.all_cards:
            if card["perm"] is None:
                context["cards"].append(card)
            if self.request.user.has_perm(card["perm"]):
                context["cards"].append(card)

        return context
