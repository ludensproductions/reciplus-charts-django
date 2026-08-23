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
    DEFAULT_ORDERING,
    DETAIL_TITLE,
    EDIT_TITLE,
    INDEX_TITLE,
    PERMISSION_ADD,
    PERMISSION_CHANGE,
    PERMISSION_DELETE,
    PERMISSION_VIEW,
    RETURN_URL,
    VEHICLE_TYPE_CREATE_URL,
    VEHICLE_TYPE_DELETE_URL,
    VEHICLE_TYPE_DETAIL_URL,
    VEHICLE_TYPE_EDIT_URL,
    VEHICLE_TYPE_INDEX_URL,
    VEHICLE_TYPE_SHOWN_FIELDS,
    VIEW_DELETED_OBJECTS,
)
from .filters import VehicleTypeFilter
from .forms import VehicleTypeForm
from .models import VehicleType


class IndexView(PermissionRequiredMixin, GenericFilterView):
    """Vista de índice para listar y filtrar tipos de vehículos."""

    permission_required = PERMISSION_VIEW
    model = VehicleType
    filterset_class = VehicleTypeFilter
    shown_fields = VEHICLE_TYPE_SHOWN_FIELDS
    title = INDEX_TITLE
    ordering = DEFAULT_ORDERING

    create_url = VEHICLE_TYPE_CREATE_URL
    delete_url = VEHICLE_TYPE_DELETE_URL
    detail_url = VEHICLE_TYPE_DETAIL_URL
    edit_url = VEHICLE_TYPE_EDIT_URL
    return_url = RETURN_URL
    can_disable = False


class CreateView(PermissionRequiredMixin, GenericCreateView):
    """Vista para crear nuevos tipos de vehículos."""

    permission_required = PERMISSION_ADD
    model = VehicleType
    form_class = VehicleTypeForm
    success_url = reverse_lazy(VEHICLE_TYPE_INDEX_URL)
    title = CREATE_TITLE
    return_url = VEHICLE_TYPE_INDEX_URL


class EditView(PermissionRequiredMixin, GenericUpdateView):
    """Vista para editar tipos de vehículos existentes."""

    permission_required = PERMISSION_CHANGE
    model = VehicleType
    form_class = VehicleTypeForm
    success_url = reverse_lazy(VEHICLE_TYPE_INDEX_URL)
    title = EDIT_TITLE
    return_url = VEHICLE_TYPE_INDEX_URL

    def get_form_kwargs(self):
        """Obtiene los argumentos para la instancia del formulario."""
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class DeleteView(PermissionRequiredMixin, GenericDeleteView):
    """Vista para eliminar tipos de vehículos."""

    permission_required = PERMISSION_DELETE
    model = VehicleType
    success_url = reverse_lazy(VEHICLE_TYPE_INDEX_URL)
    can_disable = False


class DetailView(PermissionRequiredMixin, GenericDetailView):
    """Vista de detalle para visualizar información de un tipo de vehículo."""

    permission_required = PERMISSION_VIEW
    model = VehicleType
    context_object_name = CONTEXT_OBJECT_NAME
    shown_fields = VEHICLE_TYPE_SHOWN_FIELDS
    return_url = VEHICLE_TYPE_INDEX_URL
    success_url = reverse_lazy(VEHICLE_TYPE_INDEX_URL)
    title = DETAIL_TITLE
    view_deleted_objects = VIEW_DELETED_OBJECTS
