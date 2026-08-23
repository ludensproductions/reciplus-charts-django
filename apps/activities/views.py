from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy

from apps.comun.views import (
    GenericCreateView,
    GenericDeleteView,
    GenericDetailView,
    GenericFilterView,
    GenericUpdateView,
)

from .consts import (
    CONTEXT_OBJECT_NAME,
    CREATE_TITLE,
    CREATE_URL,
    DASHBOARD_URL,
    DEFAULT_ORDERING,
    DELETE_URL,
    DETAIL_FIELDS,
    DETAIL_TITLE,
    DETAIL_URL,
    EDIT_TITLE,
    EDIT_URL,
    INDEX_FIELDS,
    INDEX_TITLE,
    INDEX_URL,
    PERMISSION_ADD,
    PERMISSION_CHANGE,
    PERMISSION_DELETE,
    PERMISSION_VIEW,
)
from .filters import ActivityFilter
from .forms import ActivityForm
from .models import Activity


class IndexView(PermissionRequiredMixin, GenericFilterView):
    """Vista de índice para listar y filtrar actividades."""

    permission_required = PERMISSION_VIEW
    model = Activity
    filterset_class = ActivityFilter
    shown_fields = INDEX_FIELDS
    title = INDEX_TITLE
    ordering = DEFAULT_ORDERING
    can_disable = True
    create_url = CREATE_URL
    delete_url = DELETE_URL
    detail_url = DETAIL_URL
    edit_url = EDIT_URL
    return_url = DASHBOARD_URL


class CreateView(PermissionRequiredMixin, GenericCreateView):
    """Vista para crear nuevas actividades."""

    permission_required = PERMISSION_ADD
    model = Activity
    form_class = ActivityForm
    success_url = reverse_lazy(INDEX_URL)
    title = CREATE_TITLE
    return_url = INDEX_URL


class EditView(PermissionRequiredMixin, GenericUpdateView):
    """Vista para editar actividades existentes."""

    permission_required = PERMISSION_CHANGE
    model = Activity
    form_class = ActivityForm
    success_url = reverse_lazy(INDEX_URL)
    title = EDIT_TITLE
    return_url = INDEX_URL

    def get_form_kwargs(self):
        """Obtiene los argumentos para la instancia del formulario."""
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class DeleteView(PermissionRequiredMixin, GenericDeleteView):
    """Vista para eliminar o deshabilitar actividades."""

    permission_required = PERMISSION_DELETE
    model = Activity
    success_url = reverse_lazy(INDEX_URL)
    can_disable = True


class DetailView(PermissionRequiredMixin, GenericDetailView):
    """Vista de detalle para visualizar información de una actividad."""

    permission_required = PERMISSION_VIEW
    model = Activity
    context_object_name = CONTEXT_OBJECT_NAME
    shown_fields = DETAIL_FIELDS
    return_url = INDEX_URL
    success_url = reverse_lazy(INDEX_URL)
    title = DETAIL_TITLE
    view_deleted_objects = True
