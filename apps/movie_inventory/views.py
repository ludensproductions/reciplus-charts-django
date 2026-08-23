from datetime import datetime

from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpRequest
from django.shortcuts import redirect
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
    DELETE_URL,
    DETAIL_FIELDS,
    DETAIL_TITLE,
    DETAIL_URL,
    DISABLED_INDEX_TITLE,
    DISABLED_INDEX_URL,
    EDIT_TITLE,
    EDIT_URL,
    ERROR_DUPLICATE_MOVIE_INVENTORY,
    FILTER_FIELDS,
    INDEX_FIELDS,
    INDEX_TITLE,
    INDEX_URL,
    ORDERING,
    PERMISSION_ADD,
    PERMISSION_CHANGE,
    PERMISSION_DELETE,
    PERMISSION_ENABLE,
    PERMISSION_VIEW,
    QUERY_FIELD,
    SPECIAL_ATTRIBUTES,
    SUCCESS_MOVIE_INVENTORY_ENABLED,
)
from .filters import MovieInventoryFilter
from .forms import EnableMovieInventaryForm, MovieInventoryForm
from .models import MovieInventory


class IndexView(PermissionRequiredMixin, GenericFilterView):
    """List and filter movie inventory records."""

    model = MovieInventory
    permission_required = PERMISSION_VIEW
    filterset_class = MovieInventoryFilter
    title = INDEX_TITLE
    ordering = ORDERING
    shown_fields = INDEX_FIELDS
    filter_fields = FILTER_FIELDS
    create_url = CREATE_URL
    delete_url = DELETE_URL
    detail_url = DETAIL_URL
    edit_url = EDIT_URL
    disable_url = DISABLED_INDEX_URL
    return_url = DASHBOARD_URL


class CreateView(PermissionRequiredMixin, GenericCreateView):
    """Create new movie inventory records."""

    permission_required = PERMISSION_ADD
    model = MovieInventory
    form_class = MovieInventoryForm
    success_url = reverse_lazy(INDEX_URL)
    title = CREATE_TITLE
    return_url = INDEX_URL


class EditView(PermissionRequiredMixin, AutoAccessMixin, GenericUpdateView):
    """Edit existing movie inventory records."""

    permission_required = PERMISSION_CHANGE
    model = MovieInventory
    form_class = MovieInventoryForm
    success_url = reverse_lazy(INDEX_URL)
    title = EDIT_TITLE
    return_url = INDEX_URL
    query = QUERY_FIELD  # Field name in the MovieInventory model.

    def get_form_kwargs(self):
        """Build form kwargs with the current user.

        Returns:
            dict: Keyword arguments passed to the form instance.
        """
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class DeleteView(PermissionRequiredMixin, AutoAccessMixin, GenericDeleteView):
    """Delete or disable movie inventory records."""

    permission_required = PERMISSION_DELETE
    model = MovieInventory
    success_url = reverse_lazy(INDEX_URL)
    can_disable = True
    query = QUERY_FIELD  # Field name in the MovieInventory model.


class DetailView(PermissionRequiredMixin, GenericDetailView):
    """Display details for a movie inventory record."""

    permission_required = PERMISSION_VIEW
    model = MovieInventory
    shown_fields = DETAIL_FIELDS
    field_attributes = SPECIAL_ATTRIBUTES

    return_url = INDEX_URL
    success_url = reverse_lazy(INDEX_URL)
    title = DETAIL_TITLE
    query = QUERY_FIELD  # Field name in the MovieInventory model.


class DisabledIndexView(PermissionRequiredMixin, GenericFilterView):
    """List disabled movie inventory records."""

    model = MovieInventory
    permission_required = PERMISSION_DELETE
    filterset_class = MovieInventoryFilter
    title = DISABLED_INDEX_TITLE
    ordering = ORDERING
    backward = INDEX_URL
    is_disabled_view = True
    shown_fields = INDEX_FIELDS
    delete_url = DELETE_URL
    return_url = INDEX_URL

    def get_filterset_kwargs(self, filterset_class):
        """Build filterset kwargs including disabled view flag.

        Args:
            filterset_class: Filterset class passed by the view.

        Returns:
            dict: Filterset keyword arguments.
        """
        kwargs = super().get_filterset_kwargs(filterset_class)
        kwargs["is_disabled_view"] = self.is_disabled_view
        return kwargs


class EnableView(PermissionRequiredMixin, GenericUpdateView):
    """Enable a disabled movie inventory record."""

    model = MovieInventory
    permission_required = PERMISSION_ENABLE

    def post(self, request: HttpRequest, *args: str, **kwargs):
        """Process enabling a disabled movie inventory record.

        Args:
            request (HttpRequest): Incoming HTTP request.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            HttpResponseRedirect: Redirect to the disabled inventory list.
        """
        movie_inventory_id = self.kwargs["pk"]
        movie_inventory = self.model.deleted_objects.filter(pk=movie_inventory_id).first()

        if self.model.objects.filter(movie=movie_inventory.movie).exists():
            messages.error(request, ERROR_DUPLICATE_MOVIE_INVENTORY)
            return redirect(reverse_lazy(DISABLED_INDEX_URL))

        form = EnableMovieInventaryForm(request.POST, instance=movie_inventory)
        if form.is_valid():
            movie_inventory.deleted = None
            movie_inventory.updated_by = request.user
            movie_inventory.modification_date = datetime.now()
            movie_inventory.justification = form.cleaned_data["justification"]
            movie_inventory.save()

        messages.success(request, SUCCESS_MOVIE_INVENTORY_ENABLED)
        return redirect(reverse_lazy(DISABLED_INDEX_URL))
