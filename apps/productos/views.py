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
from .filters import ProductosFilter
from .forms import ProductoForm
from .models import Producto


class IndexView(PermissionRequiredMixin, GenericFilterView):
    """Vista de índice para listar y filtrar productos."""

    permission_required = PERMISSION_VIEW
    model = Producto
    filterset_class = ProductosFilter
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
    """Vista para crear nuevos productos."""

    permission_required = PERMISSION_ADD
    model = Producto
    form_class = ProductoForm
    success_url = reverse_lazy(INDEX_URL)
    title = CREATE_TITLE
    return_url = INDEX_URL


class EditView(PermissionRequiredMixin, GenericUpdateView):
    """Vista para editar productos existentes."""

    permission_required = PERMISSION_CHANGE
    model = Producto
    form_class = ProductoForm
    success_url = reverse_lazy(INDEX_URL)
    title = EDIT_TITLE
    return_url = INDEX_URL


class DeleteView(PermissionRequiredMixin, GenericDeleteView):
    """Vista para eliminar o deshabilitar productos."""

    permission_required = PERMISSION_DELETE
    model = Producto
    success_url = reverse_lazy(INDEX_URL)
    can_disable = True


class DetailView(PermissionRequiredMixin, GenericDetailView):
    """Vista de detalle para visualizar información de un producto."""

    permission_required = PERMISSION_VIEW
    model = Producto
    shown_fields = DETAIL_FIELDS
    return_url = INDEX_URL
    success_url = reverse_lazy(INDEX_URL)
    title = DETAIL_TITLE
    view_deleted_objects = True
