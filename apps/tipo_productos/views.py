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
    ADD_PERMISSION,
    CHANGE_PERMISSION,
    CREATE_TITLE,
    CREATE_URL,
    DEFAULT_ORDERING,
    DELETE_PERMISSION,
    DELETE_URL,
    DETAIL_FIELDS,
    DETAIL_TITLE,
    DETAIL_URL,
    EDIT_TITLE,
    EDIT_URL,
    INDEX_FIELDS,
    INDEX_TITLE,
    INDEX_URL,
    RETURN_URL,
    VIEW_PERMISSION,
)
from .filters import TipoProductosFilter
from .forms import TipoProductoForm
from .models import TipoProducto


class IndexView(PermissionRequiredMixin, GenericFilterView):
    """Page to list and filter product types.

    Displays all product types with filtering and sorting capabilities.
    Requires view_tipo_productos.tipoproducto permission.
    """

    permission_required = VIEW_PERMISSION
    model = TipoProducto
    filterset_class = TipoProductosFilter
    shown_fields = INDEX_FIELDS
    title = INDEX_TITLE
    ordering = DEFAULT_ORDERING
    can_disable = True

    create_url = CREATE_URL
    delete_url = DELETE_URL
    detail_url = DETAIL_URL
    edit_url = EDIT_URL
    return_url = RETURN_URL


class CreateView(PermissionRequiredMixin, GenericCreateView):
    """Page to create a new product type.

    Displays a form to create a new product type entry.
    Requires add_tipo_productos.tipoproducto permission.
    """

    permission_required = ADD_PERMISSION
    model = TipoProducto
    form_class = TipoProductoForm
    success_url = reverse_lazy(INDEX_URL)
    title = CREATE_TITLE
    return_url = INDEX_URL


class EditView(PermissionRequiredMixin, GenericUpdateView):
    """Page to edit an existing product type.

    Displays a form to update product type information.
    Requires change_tipo_productos.tipoproducto permission.
    """

    permission_required = CHANGE_PERMISSION
    model = TipoProducto
    form_class = TipoProductoForm
    success_url = reverse_lazy(INDEX_URL)
    title = EDIT_TITLE
    return_url = INDEX_URL


class DeleteView(PermissionRequiredMixin, GenericDeleteView):
    """Page to delete or disable a product type.

    Soft-deletes (disables) a product type record, optionally supporting
    hard deletion based on permission settings.
    Requires delete_tipo_productos.tipoproducto permission.
    """

    permission_required = DELETE_PERMISSION
    model = TipoProducto
    success_url = reverse_lazy(INDEX_URL)
    can_disable = True


class DetailView(PermissionRequiredMixin, GenericDetailView):
    """Page displaying detailed information about a product type.

    Shows comprehensive details of a single product type.
    Includes option to view soft-deleted entries if permitted.
    Requires view_tipo_productos.tipoproducto permission.
    """

    permission_required = VIEW_PERMISSION
    model = TipoProducto
    shown_fields = list(DETAIL_FIELDS.keys())
    return_url = INDEX_URL
    success_url = reverse_lazy(INDEX_URL)
    title = DETAIL_TITLE
    view_deleted_objects = True
