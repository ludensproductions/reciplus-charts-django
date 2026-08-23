from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView


class IndexView(LoginRequiredMixin, TemplateView):  # noqa: D101
    template_name = "activity_feed/index.html"

    def get_context_data(self, **kwargs):  # noqa: D102
        context = super().get_context_data(**kwargs)
        context["title"] = "Activity feed"
        context["title_button"] = "Emit activity"
        context["icon"] = "fas fa-broadcast-tower"
        return context
