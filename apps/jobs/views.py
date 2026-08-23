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
    DELETE_PERMISSION,
    DELETE_URL,
    DETAIL_FIELDS,
    DETAIL_TITLE,
    DETAIL_URL,
    EDIT_TITLE,
    EDIT_URL,
    FILTER_FIELDS,
    INDEX_FIELDS,
    INDEX_TITLE,
    INDEX_URL,
    ORDERING,
    RETURN_URL,
    VIEW_PERMISSION,
)
from .forms import JobForm
from .models import Job


class IndexView(PermissionRequiredMixin, GenericFilterView):
    """List and filter job records."""

    permission_required = VIEW_PERMISSION
    model = Job
    shown_fields = INDEX_FIELDS
    filter_fields = FILTER_FIELDS
    title = INDEX_TITLE
    ordering = ORDERING
    can_disable = True

    create_url = CREATE_URL
    delete_url = DELETE_URL
    detail_url = DETAIL_URL
    edit_url = EDIT_URL
    return_url = RETURN_URL


class CreateView(PermissionRequiredMixin, GenericCreateView):
    """Create new job records."""

    permission_required = ADD_PERMISSION
    model = Job
    form_class = JobForm
    success_url = reverse_lazy(INDEX_URL)
    title = CREATE_TITLE
    return_url = INDEX_URL


class EditView(PermissionRequiredMixin, GenericUpdateView):
    """Edit existing job records."""

    permission_required = CHANGE_PERMISSION
    model = Job
    form_class = JobForm
    success_url = reverse_lazy(INDEX_URL)
    title = EDIT_TITLE
    return_url = INDEX_URL


class DeleteView(PermissionRequiredMixin, GenericDeleteView):
    """Delete or disable job records."""

    permission_required = DELETE_PERMISSION
    model = Job
    success_url = reverse_lazy(INDEX_URL)
    can_disable = True


class DetailView(PermissionRequiredMixin, GenericDetailView):
    """Display job details."""

    permission_required = VIEW_PERMISSION
    model = Job
    shown_fields = list(DETAIL_FIELDS.keys())
    return_url = INDEX_URL
    success_url = reverse_lazy(INDEX_URL)
    title = DETAIL_TITLE
    view_deleted_objects = True
