from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy

from apps.comun.mixins import AutoAccessMixin
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
    DISABLED_INDEX_TITLE,
    EDIT_TITLE,
    EDIT_URL,
    ENABLE_URL,
    INDEX_FIELDS,
    INDEX_TITLE,
    INDEX_URL,
    PERMISSION_ADD,
    PERMISSION_CHANGE,
    PERMISSION_DELETE,
    PERMISSION_ENABLE,
    PERMISSION_VIEW,
)
from .filters import GenreFilter
from .forms import GenreForm
from .models import Genre


class IndexView(PermissionRequiredMixin, GenericFilterView):
    """List and filter genres."""

    permission_required = PERMISSION_VIEW
    model = Genre
    filterset_class = GenreFilter
    shown_fields = INDEX_FIELDS
    title = INDEX_TITLE
    ordering = DEFAULT_ORDERING
    can_disable = True
    create_url = CREATE_URL
    edit_url = EDIT_URL
    delete_url = DELETE_URL
    detail_url = DETAIL_URL
    return_url = DASHBOARD_URL


class CreateView(PermissionRequiredMixin, GenericCreateView):
    """Create new genres."""

    permission_required = PERMISSION_ADD
    model = Genre
    form_class = GenreForm
    success_url = reverse_lazy(INDEX_URL)
    title = CREATE_TITLE
    return_url = INDEX_URL


class EditView(PermissionRequiredMixin, AutoAccessMixin, GenericUpdateView):
    """Edit existing genres."""

    permission_required = PERMISSION_CHANGE
    model = Genre
    form_class = GenreForm
    success_url = reverse_lazy(INDEX_URL)
    title = EDIT_TITLE
    return_url = INDEX_URL

    def get_form_kwargs(self):
        """Build form kwargs with the current user.

        Returns:
            dict: Keyword arguments passed to the form instance.
        """
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class DeleteView(PermissionRequiredMixin, AutoAccessMixin, GenericDeleteView):  # Default created_by field.
    """Delete or disable genres."""

    permission_required = PERMISSION_DELETE
    model = Genre
    success_url = reverse_lazy(INDEX_URL)
    can_disable = True


class DetailView(PermissionRequiredMixin, AutoAccessMixin, GenericDetailView):  # Default created_by field.
    """Display details for a genre."""

    permission_required = PERMISSION_VIEW
    model = Genre
    shown_fields = DETAIL_FIELDS
    return_url = INDEX_URL
    success_url = reverse_lazy(INDEX_URL)
    title = DETAIL_TITLE
    view_deleted_objects = True


class DisabledIndexView(PermissionRequiredMixin, GenericFilterView):
    """List disabled genres."""

    model = Genre
    permission_required = PERMISSION_ENABLE
    title = DISABLED_INDEX_TITLE
    ordering = DEFAULT_ORDERING
    backward = INDEX_URL
    is_disabled_view = True
    queryset = Genre.deleted_objects.all()
    delete_url = ENABLE_URL
    return_url = INDEX_URL

    shown_fields = INDEX_FIELDS


class EnableView(PermissionRequiredMixin, GenericDeleteView):
    """Enable disabled genres."""

    permission_required = PERMISSION_ENABLE
    model = Genre
    success_url = reverse_lazy(INDEX_URL)
    can_disable = True
    is_delete = False
