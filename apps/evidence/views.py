from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy

from apps.comun.views import (
    GenericCreateView,
    GenericDeleteView,
    GenericFilterView,
    GenericUpdateView,
)

from .consts import (
    CREATE_TITLE,
    CREATE_URL,
    DASHBOARD_URL,
    DEFAULT_ORDERING,
    DELETE_URL,
    EDIT_TITLE,
    EDIT_URL,
    FILTER_FIELDS,
    INDEX_FIELDS,
    INDEX_TITLE,
    INDEX_URL,
    MODEL_NAME,
    PERMISSION_ADD,
    PERMISSION_CHANGE,
    PERMISSION_DELETE,
    PERMISSION_VIEW,
)
from .forms import EvidenceForm
from .models import Evidence


class IndexView(PermissionRequiredMixin, GenericFilterView):
    """Vista de índice para listar evidencias."""

    permission_required = PERMISSION_VIEW
    model = Evidence
    filter_fields = FILTER_FIELDS
    shown_fields = INDEX_FIELDS
    title = INDEX_TITLE
    verbose_name = MODEL_NAME.capitalize()
    ordering = DEFAULT_ORDERING
    can_disable = True
    create_url = CREATE_URL
    delete_url = DELETE_URL
    edit_url = EDIT_URL
    return_url = DASHBOARD_URL


class CreateView(PermissionRequiredMixin, GenericCreateView):
    """Vista para crear una nueva evidencia."""

    permission_required = PERMISSION_ADD
    model = Evidence
    form_class = EvidenceForm
    success_url = reverse_lazy(INDEX_URL)
    title = CREATE_TITLE
    return_url = INDEX_URL


class EditView(PermissionRequiredMixin, GenericUpdateView):
    """Vista para editar una evidencia existente."""

    permission_required = PERMISSION_CHANGE
    model = Evidence
    form_class = EvidenceForm
    success_url = reverse_lazy(INDEX_URL)
    title = EDIT_TITLE
    return_url = INDEX_URL


class DeleteView(PermissionRequiredMixin, GenericDeleteView):
    """Vista para eliminar una evidencia."""

    permission_required = PERMISSION_DELETE
    model = Evidence
    success_url = reverse_lazy(INDEX_URL)
    can_disable = True
