import re

from django.apps import apps
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView, ListView, TemplateView
from django_filters.views import FilterView

from apps.users.models import User

from .filters import GenericFilter, create_dynamic_filter

# Create your views here.

LABELS_DICT = {
    # 'created_by': 'Creado por',
    # 'created_at': 'Fecha de creación',
    # 'updated_by': 'Actualizado por',
    # 'updated_at': 'Fecha de actualización',
    # 'deleted': 'Fecha de eliminación',
    # 'history_date': 'Fecha cambio',
    # 'history_type': 'Tipo de cambio',
    # 'history_user': 'Usuario',
}

QUANTITY_TO_DELETE = 1000

IGNORE_MODELS = [
    "HistoricalSeccion",
]


class IndexView(PermissionRequiredMixin, TemplateView):
    permission_required = "admin.view_logentry"
    template_name = "history/logs.html"


# App 'Users'
class UserLogsView(PermissionRequiredMixin, ListView):
    permission_required = "admin.view_logentry"
    model = User
    template_name = "history/users.html"
    context_object_name = "history"
    paginate_by = 20
    queryset = User.history.all()


class UserRollbackView(PermissionRequiredMixin, View):
    permission_required = "admin.view_logentry"
    model = User
    success_url = reverse_lazy("history:users")

    def post(self, request, pk, *args, **kwargs):
        history = self.model.history.get(pk=pk)
        history.save()
        return redirect(self.success_url)


# Generic LOGS


class GenericIndexview(PermissionRequiredMixin, TemplateView):
    template_name = "history/generic_index.html"
    permission_required = "admin.view_logentry"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        models = [
            model
            for model in apps.get_models()
            if model.__name__.startswith("Historical") and model.__name__ not in IGNORE_MODELS
        ]
        models.sort(key=lambda x: x.__name__)  # Sort models alphabetically by name
        context["models"] = models
        return context


class GenericLogsView(PermissionRequiredMixin, FilterView):
    permission_required = "admin.view_logentry"
    template_name = "history/generic_logs.html"
    context_object_name = "logs"
    paginate_by = 20
    filterset_class = GenericFilter

    def get_queryset(self):
        order_by = "-id"
        if hasattr(self.model, "updated_at"):
            order_by = "-updated_at"
        elif hasattr(self.model, "created_at"):
            order_by = "-created_at"

        if hasattr(self.model, "all_objects"):
            return self.model.all_objects.all().order_by(order_by)

        return self.model.objects.all().order_by(order_by)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["app"] = self.kwargs["app"]
        context["model"] = self.kwargs["model"]
        model_name = self.kwargs["model"].replace("Historical", "")
        model_name = re.sub(r"(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])", " ", model_name)
        context["model_name"] = model_name
        return context

    def get_filterset_class(self):
        self.model = apps.get_model(app_label=self.kwargs["app"], model_name=self.kwargs["model"])

        if self.model is None:
            return super().get_filterset_class()

        return create_dynamic_filter(self.model)


class DetailView(PermissionRequiredMixin, DetailView):
    template_name = "history/modals/generic_show.html"
    permission_required = "admin.view_logentry"
    context_object_name = "log"

    def get_context_data(self, *args, **kwargs):
        context = super(DetailView, self).get_context_data(*args, **kwargs)
        context["app"] = self.kwargs["app"]
        context["model"] = self.kwargs["model"]
        model_name = self.kwargs["model"].replace("Historical", "")
        model_name = re.sub(r"(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])", " ", model_name)
        context["model_name"] = model_name
        return context

    def get_object(self):
        model_class = apps.get_model(app_label=self.kwargs["app"], model_name=self.kwargs["model"])
        model = model_class.objects.get(history_id=self.kwargs["pk"])
        return model


class GenericRollbackView(PermissionRequiredMixin, View):
    permission_required = "admin.view_logentry"

    def post(self, request, *args, **kwargs):
        model_class = apps.get_model(app_label=self.kwargs["app"], model_name=self.kwargs["model"])

        history = model_class.history.get(pk=self.kwargs["pk"])
        history.instance.save()
        return redirect(
            reverse_lazy(
                "history:generic-log-model",
                kwargs={
                    "app": self.kwargs["app"],
                    "model": "Historical" + self.kwargs["model"],
                },
            )
        )
