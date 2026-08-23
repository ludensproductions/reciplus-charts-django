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
    DISABLED_INDEX_TITLE,
    DISABLED_INDEX_URL,
    EDIT_TITLE,
    EDIT_URL,
    FILTER_FIELDS,
    INDEX_FIELDS,
    INDEX_TITLE,
    INDEX_URL,
    PERMISSION_ADD,
    PERMISSION_CHANGE,
    PERMISSION_DELETE,
    PERMISSION_VIEW,
)

# from .filters import CategoryFilter
from .forms import CategoryForm
from .models import Category


class IndexView(PermissionRequiredMixin, GenericFilterView):
    """Vista de índice para listar categorías."""

    permission_required = PERMISSION_VIEW
    model = Category
    filter_fields = FILTER_FIELDS
    shown_fields = INDEX_FIELDS
    title = INDEX_TITLE
    ordering = DEFAULT_ORDERING
    create_url = CREATE_URL
    delete_url = DELETE_URL
    edit_url = EDIT_URL
    return_url = DASHBOARD_URL
    disable_url = DISABLED_INDEX_URL


class CreateView(PermissionRequiredMixin, GenericCreateView):
    """Vista para crear una nueva categoría."""

    permission_required = PERMISSION_ADD
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy(INDEX_URL)
    title = CREATE_TITLE


class EditView(PermissionRequiredMixin, GenericUpdateView):
    """Vista para editar una categoría existente."""

    permission_required = PERMISSION_CHANGE
    model = Category
    form_class = CategoryForm
    success_url = reverse_lazy(INDEX_URL)
    title = EDIT_TITLE


class DeleteView(PermissionRequiredMixin, GenericDeleteView):
    """Vista para eliminar una categoría."""

    permission_required = PERMISSION_DELETE
    model = Category
    success_url = reverse_lazy(INDEX_URL)
    can_disable = True


class DisabledIndexView(PermissionRequiredMixin, GenericFilterView):
    """Vista de índice para listar categorías deshabilitadas."""

    permission_required = PERMISSION_VIEW
    model = Category
    filter_fields = FILTER_FIELDS
    shown_fields = INDEX_FIELDS
    title = DISABLED_INDEX_TITLE
    ordering = DEFAULT_ORDERING
    create_url = CREATE_URL
    delete_url = DELETE_URL
    return_url = INDEX_URL
    is_disabled_view = True
