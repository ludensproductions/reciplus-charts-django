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
    DEFAULT_ORDERING,
    DELETE_URL,
    DETAIL_FIELDS,
    DETAIL_TITLE,
    DETAIL_URL,
    EDIT_TITLE,
    EDIT_URL,
    INDEX_FIELDS,
    INDEX_TITLE,
    INDEX_URL,
    PERMISSION_ADD,
    PERMISSION_CHANGE,
    PERMISSION_DELETE,
    PERMISSION_VIEW,
)
from .filters import StudentFilter
from .forms import StudentForm
from .models import Student


class IndexView(PermissionRequiredMixin, GenericFilterView):
    """List view for Student with filtering and pagination.

    Displays all active Student records with options to create, edit,
    view details, and soft delete. Supports filtering through StudentFilter.
    """

    permission_required = PERMISSION_VIEW
    model = Student
    filterset_class = StudentFilter
    shown_fields = INDEX_FIELDS
    title = INDEX_TITLE
    ordering = DEFAULT_ORDERING
    can_disable = True
    create_url = CREATE_URL
    delete_url = DELETE_URL
    detail_url = DETAIL_URL
    edit_url = EDIT_URL
    return_url = DASHBOARD_URL


class CreateView(PermissionRequiredMixin, GenericCreateView):
    """Create view for new Student instances.

    Handles the creation of new Student records using StudentForm.
    """

    permission_required = PERMISSION_ADD
    model = Student
    form_class = StudentForm
    success_url = reverse_lazy(INDEX_URL)
    title = CREATE_TITLE
    return_url = INDEX_URL


class DetailView(PermissionRequiredMixin, GenericDetailView):
    """Detail view for Student instances.

    Displays detailed information for a single Student record,
    including soft-deleted records if permitted.
    """

    permission_required = PERMISSION_VIEW
    model = Student
    shown_fields = DETAIL_FIELDS
    return_url = INDEX_URL
    success_url = reverse_lazy(INDEX_URL)
    title = DETAIL_TITLE
    view_deleted_objects = True


class EditView(PermissionRequiredMixin, GenericUpdateView):
    """Update view for existing Student instances.

    Allows editing of Student records using StudentForm.
    """

    permission_required = PERMISSION_CHANGE
    model = Student
    form_class = StudentForm
    success_url = reverse_lazy(INDEX_URL)
    title = EDIT_TITLE
    return_url = INDEX_URL


class DeleteView(PermissionRequiredMixin, GenericDeleteView):
    """Delete view for Student instances.

    Handles soft deletion of Student records.
    """

    permission_required = PERMISSION_DELETE
    model = Student
    success_url = reverse_lazy(INDEX_URL)
    can_disable = True
