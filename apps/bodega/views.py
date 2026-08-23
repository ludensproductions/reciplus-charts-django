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
    CREATE_TITLE,
    CREATE_URL,
    DASHBOARD_URL,
    DELETE_URL,
    DETAIL_FIELDS,
    DETAIL_TITLE,
    DETAIL_URL,
    EDIT_TITLE,
    EDIT_URL,
    INDEX_FIELDS,
    INDEX_TITLE,
    INDEX_URL,
    ORDERING,
    PERMISSION_ADD,
    PERMISSION_CHANGE,
    PERMISSION_DELETE,
    PERMISSION_VIEW,
)
from .filters import BodegaFilter
from .forms import BodegaForm
from .models import Bodega


class IndexView(PermissionRequiredMixin, GenericFilterView):
    """Vista de índice para listar y filtrar bodegas."""

    permission_required = PERMISSION_VIEW
    model = Bodega
    filterset_class = BodegaFilter
    shown_fields = INDEX_FIELDS
    title = INDEX_TITLE
    ordering = ORDERING
    can_disable = True

    create_url = CREATE_URL
    delete_url = DELETE_URL
    detail_url = DETAIL_URL
    edit_url = EDIT_URL
    return_url = DASHBOARD_URL


class CreateView(PermissionRequiredMixin, GenericCreateView):
    """Vista para crear nuevas bodegas."""

    permission_required = PERMISSION_ADD
    model = Bodega
    form_class = BodegaForm
    success_url = reverse_lazy(INDEX_URL)
    title = CREATE_TITLE
    return_url = INDEX_URL


class EditView(PermissionRequiredMixin, GenericUpdateView):
    """Vista para editar bodegas existentes."""

    permission_required = PERMISSION_CHANGE
    model = Bodega
    form_class = BodegaForm
    success_url = reverse_lazy(INDEX_URL)
    title = EDIT_TITLE
    return_url = INDEX_URL


class DeleteView(PermissionRequiredMixin, GenericDeleteView):
    """Vista para eliminar o deshabilitar bodegas."""

    permission_required = PERMISSION_DELETE
    model = Bodega
    success_url = reverse_lazy(INDEX_URL)
    can_disable = True


class DetailView(PermissionRequiredMixin, GenericDetailView):
    """Vista de detalle para visualizar información de una bodega."""

    permission_required = PERMISSION_VIEW
    model = Bodega
    shown_fields = DETAIL_FIELDS
    return_url = INDEX_URL
    success_url = reverse_lazy(INDEX_URL)
    title = DETAIL_TITLE
    view_deleted_objects = True
