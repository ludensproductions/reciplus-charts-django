from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy

from apps.comun.consts import (
    HistoriasUsuario,
)
from apps.comun.views import (
    GenericCreateView,
    GenericDeleteView,
    GenericDetailView,
    GenericFilterView,
    GenericUpdateView,
)
from apps.movies.models import Movie

from .consts import (
    CONTEXT_OBJECT_NAME,
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
    SPECIAL_ATTRIBUTES,
)
from .filters import MoviesFilter
from .forms import InventarioForm


class IndexView(PermissionRequiredMixin, GenericFilterView):
    """Vista de índice para listar y filtrar películas."""

    permission_required = PERMISSION_VIEW
    model = Movie
    filterset_class = MoviesFilter
    shown_fields = INDEX_FIELDS
    field_attributes = SPECIAL_ATTRIBUTES
    title = INDEX_TITLE
    ordering = ORDERING
    can_disable = True

    create_url = CREATE_URL
    delete_url = DELETE_URL
    detail_url = DETAIL_URL
    edit_url = EDIT_URL
    return_url = DASHBOARD_URL

    class Meta:
        """Metadatos de la vista IndexView."""

        HUs = [HistoriasUsuario.HU004]


class CreateView(PermissionRequiredMixin, GenericCreateView):
    """Vista para crear nuevas películas."""

    permission_required = PERMISSION_ADD
    model = Movie
    template_name = "movies/form.html"
    form_class = InventarioForm
    success_url = reverse_lazy(INDEX_URL)
    title = CREATE_TITLE
    return_url = INDEX_URL

    class Meta:
        """Metadatos de la vista CreateView."""

        HUs = [HistoriasUsuario.HU004, HistoriasUsuario.HU005]


class EditView(PermissionRequiredMixin, GenericUpdateView):
    """Vista para editar películas existentes."""

    permission_required = PERMISSION_CHANGE
    model = Movie
    template_name = "movies/form.html"
    form_class = InventarioForm
    success_url = reverse_lazy(INDEX_URL)
    title = EDIT_TITLE
    return_url = INDEX_URL

    class Meta:
        """Metadatos de la vista EditView."""

        HUs = [HistoriasUsuario.HU004]

    def get_form_kwargs(self):
        """Obtiene los argumentos para la instancia del formulario."""
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class DeleteView(PermissionRequiredMixin, GenericDeleteView):
    """Vista para eliminar o deshabilitar películas."""

    permission_required = PERMISSION_DELETE
    model = Movie
    success_url = reverse_lazy(INDEX_URL)
    can_disable = True

    class Meta:
        """Metadatos de la vista DeleteView."""

        HUs = [HistoriasUsuario.HU004]


class DetailView(PermissionRequiredMixin, GenericDetailView):
    """Vista de detalle para visualizar información de una película."""

    permission_required = PERMISSION_VIEW
    model = Movie
    context_object_name = CONTEXT_OBJECT_NAME
    shown_fields = DETAIL_FIELDS
    field_attributes = SPECIAL_ATTRIBUTES
    return_url = INDEX_URL
    success_url = reverse_lazy(INDEX_URL)
    title = DETAIL_TITLE
    view_deleted_objects = True

    class Meta:
        """Metadatos de la vista DetailView."""

        HUs = [HistoriasUsuario.HU004]
