from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy

from apps.comun.views import (
    GenericCreateView,
    GenericDeleteView,
    GenericDetailView,
    GenericFilterView,
    GenericUpdateView,
)

from .const import (
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
    VEHICLE_CREATE_URL,
    VEHICLE_DELETE_URL,
    VEHICLE_DETAIL_URL,
    VEHICLE_EDIT_URL,
    VEHICLE_INDEX_URL,
    VEHICLE_SHOWN_FIELDS,
    VIEW_DELETED_OBJECTS,
)
from .filters import VehicleFilter
from .forms import VehicleForm
from .models import Vehicle


class IndexView(PermissionRequiredMixin, GenericFilterView):
    """Index view used to list and filter vehicles."""

    permission_required = PERMISSION_VIEW
    model = Vehicle
    filterset_class = VehicleFilter
    shown_fields = VEHICLE_SHOWN_FIELDS
    title = INDEX_TITLE
    ordering = DEFAULT_ORDERING

    create_url = VEHICLE_CREATE_URL
    delete_url = VEHICLE_DELETE_URL
    detail_url = VEHICLE_DETAIL_URL
    edit_url = VEHICLE_EDIT_URL
    return_url = RETURN_URL
    can_disable = False


class CreateView(PermissionRequiredMixin, GenericCreateView):
    """Create view used to add new vehicles."""

    permission_required = PERMISSION_ADD
    model = Vehicle
    form_class = VehicleForm
    success_url = reverse_lazy(VEHICLE_INDEX_URL)
    title = CREATE_TITLE
    return_url = VEHICLE_INDEX_URL


class EditView(PermissionRequiredMixin, GenericUpdateView):
    """Update view for existing vehicles."""

    permission_required = PERMISSION_CHANGE
    model = Vehicle
    form_class = VehicleForm
    success_url = reverse_lazy(VEHICLE_INDEX_URL)
    title = EDIT_TITLE
    return_url = VEHICLE_INDEX_URL

    def get_form_kwargs(self):
        """Provide form kwargs including the current user."""
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class DeleteView(PermissionRequiredMixin, GenericDeleteView):
    """Delete view for vehicles."""

    permission_required = PERMISSION_DELETE
    model = Vehicle
    success_url = reverse_lazy(VEHICLE_INDEX_URL)
    can_disable = False


class DetailView(PermissionRequiredMixin, GenericDetailView):
    """Detail view that displays vehicle information."""

    permission_required = PERMISSION_VIEW
    model = Vehicle
    context_object_name = CONTEXT_OBJECT_NAME
    shown_fields = VEHICLE_SHOWN_FIELDS
    return_url = VEHICLE_INDEX_URL
    success_url = reverse_lazy(VEHICLE_INDEX_URL)
    title = DETAIL_TITLE
    view_deleted_objects = VIEW_DELETED_OBJECTS
