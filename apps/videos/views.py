from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.text import format_lazy

from apps.comun.consts import ERROR_CONTENT_TYPE_MISMATCH, ERROR_DISABLE_ALREADY_DISABLED
from apps.comun.views import (
    GenericDeleteView,
    GenericDetailView,
    GenericFilterView,
    GenericUpdateView,
)
from apps.contents.consts import ContentTypes
from apps.videos.models import Video

from .consts import (
    DASHBOARD_URL,
    DEFAULT_ORDERING,
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
    PERMISSION_CHANGE,
    PERMISSION_DELETE,
    PERMISSION_VIEW,
    VERBOSE_NAME,
)
from .forms import VideoForm


class IndexView(PermissionRequiredMixin, GenericFilterView):
    """Index view to list and filter videos."""

    permission_required = PERMISSION_VIEW
    model = Video
    filter_fields = FILTER_FIELDS
    shown_fields = INDEX_FIELDS
    title = INDEX_TITLE
    verbose_name = VERBOSE_NAME
    ordering = DEFAULT_ORDERING
    can_disable = True

    delete_url = DELETE_URL
    edit_url = EDIT_URL
    detail_url = DETAIL_URL
    return_url = DASHBOARD_URL

    def get_queryset(self):
        """Filter queryset to include only video content."""
        qs = super().get_queryset()
        qs = qs.filter(content__content_type=ContentTypes.VIDEO)
        return qs


class EditView(PermissionRequiredMixin, GenericUpdateView):
    """Edit view for existing videos."""

    permission_required = PERMISSION_CHANGE
    model = Video
    form_class = VideoForm
    success_url = reverse_lazy(INDEX_URL)
    title = EDIT_TITLE
    return_url = INDEX_URL

    def get_queryset(self):
        """Filter queryset to include only video content."""
        qs = super().get_queryset()
        qs = qs.filter(content__content_type=ContentTypes.VIDEO)
        return qs


class DeleteView(PermissionRequiredMixin, GenericDeleteView):
    """Delete or disable view for videos."""

    permission_required = PERMISSION_DELETE
    model = Video
    success_url = reverse_lazy(INDEX_URL)
    can_disable = True

    def get_queryset(self):
        """Filter queryset to include only video content."""
        qs = super().get_queryset()
        qs = qs.filter(content__content_type=ContentTypes.VIDEO)
        return qs

    def dispatch(self, request, *args, **kwargs):
        """Validate content type before processing the request."""
        self.object: Video = self.get_object()

        if not self.object.should_allow_delete_action():
            messages.error(request, ERROR_CONTENT_TYPE_MISMATCH)
            return redirect(self.get_success_url())

        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """Process delete or restore action for a video instance."""
        self.object = self.get_object()
        self.is_htmx = request.headers.get("HX-Request", False)
        self.is_delete = True if not self.object.deleted else False

        if self.is_delete:
            return self.delete(request, *args, **kwargs)

        if not self.can_disable:
            return self.handle_response(
                False,
                format_lazy(ERROR_DISABLE_ALREADY_DISABLED, object=self.object),
            )

        deleted, message = self.object.undelete()
        if self.object.content.deleted:
            self.object.content.undelete()

        return self.handle_response(deleted, message)

    def delete(self, request, *args, **kwargs):
        """Delete the video and its related content object."""
        self.object = self.get_object()
        deleted, message = self.object.delete()

        if not self.object.content.deleted:
            self.object.content.delete()

        return self.handle_response(deleted, message)


class DetailView(PermissionRequiredMixin, GenericDetailView):
    """Detail view to display video information."""

    permission_required = PERMISSION_VIEW
    model = Video
    shown_fields = DETAIL_FIELDS
    return_url = INDEX_URL
    title = DETAIL_TITLE
    view_deleted_objects = True

    def get_queryset(self):
        """Filter queryset to include only video content."""
        qs = super().get_queryset()
        qs = qs.filter(content__content_type=ContentTypes.VIDEO)
        return qs
