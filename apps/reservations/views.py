from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy

from apps.comun.views import (
    GenericCreateView,
    GenericDeleteView,
    GenericDetailView,
    GenericFilterView,
    GenericUpdateView,
)
from apps.reservations.models import Reservation

from .consts import (
    CONTEXT_OBJECT_NAME,
    CREATE_TITLE,
    CREATE_URL,
    CUSTOM_BUTTON_TITLE,
    DASHBOARD_URL,
    DEFAULT_ORDERING,
    DELETE_URL,
    DETAIL_FIELDS,
    DETAIL_TITLE,
    DETAIL_URL,
    DISABLED_INDEX_FIELDS,
    DISABLED_INDEX_TITLE,
    EDIT_TITLE,
    EDIT_URL,
    FIELD_ATTRIBUTES,
    FILTER_FIELDS,
    INDEX_FIELDS,
    INDEX_TITLE,
    INDEX_URL,
    PERMISSION_ADD,
    PERMISSION_CHANGE,
    PERMISSION_DELETE,
    PERMISSION_VIEW,
    RESERVATION_FORM_JS,
)
from .filters import ReservationFilter
from .forms import (
    ReservationForm,
)


class IndexView(PermissionRequiredMixin, GenericFilterView):
    """Vista de índice para listar y filtrar reservaciones."""

    permission_required = PERMISSION_VIEW
    model = Reservation
    filter_fields = FILTER_FIELDS
    shown_fields = INDEX_FIELDS
    title = INDEX_TITLE
    ordering = DEFAULT_ORDERING

    create_url = CREATE_URL
    delete_url = DELETE_URL
    detail_url = DETAIL_URL
    edit_url = EDIT_URL
    return_url = DASHBOARD_URL

    field_attributes = FIELD_ATTRIBUTES


class DisableIndexView(PermissionRequiredMixin, GenericFilterView):
    """Vista de índice para listar reservaciones deshabilitadas."""

    permission_required = PERMISSION_VIEW
    model = Reservation
    filterset_class = ReservationFilter
    is_disabled_view = True

    shown_fields = DISABLED_INDEX_FIELDS
    title = DISABLED_INDEX_TITLE
    ordering = DEFAULT_ORDERING

    delete_url = DELETE_URL
    return_url = INDEX_URL

    field_attributes = FIELD_ATTRIBUTES


class CreateView(PermissionRequiredMixin, GenericCreateView):
    """Vista para crear nuevas reservaciones."""

    permission_required = PERMISSION_ADD
    model = Reservation
    form_class = ReservationForm
    success_url = reverse_lazy(INDEX_URL)
    title = CREATE_TITLE
    return_url = INDEX_URL
    custom_js_files = RESERVATION_FORM_JS

    def get_context_data(self, **kwargs):
        """Obtiene el contexto incluyendo el título personalizado del botón."""
        context = super().get_context_data(**kwargs)
        # Custom button title (if specified it won't grab the title from the view)
        context["custom_button_title"] = CUSTOM_BUTTON_TITLE
        return context


class EditView(PermissionRequiredMixin, GenericUpdateView):
    """Vista para editar reservaciones existentes."""

    permission_required = PERMISSION_CHANGE
    model = Reservation
    form_class = ReservationForm
    success_url = reverse_lazy(INDEX_URL)
    title = EDIT_TITLE
    return_url = INDEX_URL
    custom_js_files = RESERVATION_FORM_JS

    def get_context_data(self, **kwargs):
        """Obtiene el contexto incluyendo el título personalizado del botón."""
        context = super().get_context_data(**kwargs)
        # Custom button title (if specified it won't grab the title from the view)
        context["custom_button_title"] = CUSTOM_BUTTON_TITLE
        return context


class DeleteView(PermissionRequiredMixin, GenericDeleteView):
    """Vista para eliminar o deshabilitar reservaciones."""

    permission_required = PERMISSION_DELETE
    model = Reservation
    success_url = reverse_lazy(INDEX_URL)
    can_disable = True


class DetailView(PermissionRequiredMixin, GenericDetailView):
    """Vista de detalle para visualizar información de una reservación."""

    permission_required = PERMISSION_VIEW
    model = Reservation
    context_object_name = CONTEXT_OBJECT_NAME
    return_url = INDEX_URL
    success_url = reverse_lazy(INDEX_URL)
    title = DETAIL_TITLE
    queryset = Reservation.all_objects.all()

    shown_fields = DETAIL_FIELDS
    field_attributes = FIELD_ATTRIBUTES
