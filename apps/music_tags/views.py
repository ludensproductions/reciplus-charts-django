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
    PERMISSION_ADD,
    PERMISSION_CHANGE,
    PERMISSION_DELETE,
    PERMISSION_VIEW,
)
from .forms import MusicTagsForm
from .models import MusicTags


class IndexView(PermissionRequiredMixin, GenericFilterView):
    """Vista de índice para listar etiquetas musicales."""

    permission_required = PERMISSION_VIEW
    model = MusicTags
    filter_fields = FILTER_FIELDS
    shown_fields = INDEX_FIELDS
    title = INDEX_TITLE
    ordering = DEFAULT_ORDERING
    can_disable = True

    create_url = CREATE_URL
    delete_url = DELETE_URL
    edit_url = EDIT_URL
    return_url = DASHBOARD_URL


class CreateView(PermissionRequiredMixin, GenericCreateView):
    """Vista para crear una nueva etiqueta musical."""

    permission_required = PERMISSION_ADD
    model = MusicTags
    form_class = MusicTagsForm
    success_url = reverse_lazy(INDEX_URL)
    title = CREATE_TITLE
    return_url = INDEX_URL


class EditView(PermissionRequiredMixin, GenericUpdateView):
    """Vista para editar una etiqueta musical existente."""

    permission_required = PERMISSION_CHANGE
    model = MusicTags
    form_class = MusicTagsForm
    success_url = reverse_lazy(INDEX_URL)
    title = EDIT_TITLE
    return_url = INDEX_URL


class DeleteView(PermissionRequiredMixin, GenericDeleteView):
    """Vista para eliminar una etiqueta musical."""

    permission_required = PERMISSION_DELETE
    model = MusicTags
    success_url = reverse_lazy(INDEX_URL)
    can_disable = True
