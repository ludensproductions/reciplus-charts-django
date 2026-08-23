import pandas as pd
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import View
from django_select2.views import AutoResponseView

from apps.comun.views import (
    GenericCreateView,
    GenericDeleteView,
    GenericDetailView,
    GenericFilterView,
    GenericUpdateView,
)
from apps.notification.mixins import SuccessNotificationMixin

from .consts import (
    CREATE_TITLE,
    CREATE_URL,
    CSV_FILENAME,
    DASHBOARD_URL,
    DELETE_URL,
    DETAIL_FIELDS,
    DETAIL_TITLE,
    DETAIL_URL,
    EDIT_TITLE,
    EDIT_URL,
    EXPORT_BUTTON_CLASS,
    EXPORT_BUTTON_ICON,
    EXPORT_BUTTON_TITLE,
    EXPORT_CSV_URL,
    INDEX_FIELDS,
    INDEX_TITLE,
    INDEX_URL,
    MODAL_INDEX_TITLE,
    ORDERING,
    PERMISSION_ADD,
    PERMISSION_CHANGE,
    PERMISSION_DELETE,
    PERMISSION_VIEW,
    PERMISSION_VIEW_SONG,
    SUCCESS_REVIEW_CREATED_MESSAGE,
    SUCCESS_REVIEW_CREATED_TITLE,
    SUCCESS_REVIEW_UPDATED_MESSAGE,
    SUCCESS_REVIEW_UPDATED_TITLE,
    VERBOSE_NAME,
)
from .filters import SongReviewFilter
from .forms import SongReviewForm
from .models import SongReview


class SongSelect2responseView(PermissionRequiredMixin, AutoResponseView):
    """Serve Select2 responses for song lookups."""

    permission_required = PERMISSION_VIEW_SONG


class IndexView(PermissionRequiredMixin, GenericFilterView):
    """List and filter song reviews in the index view."""

    template_name = "song_reviews/index.html"
    permission_required = PERMISSION_VIEW
    model = SongReview
    filterset_class = SongReviewFilter
    shown_fields = INDEX_FIELDS
    title = INDEX_TITLE
    ordering = ORDERING
    can_disable = True
    verbose_name = VERBOSE_NAME

    return_url = DASHBOARD_URL
    create_url = CREATE_URL
    edit_url = EDIT_URL
    delete_url = DELETE_URL
    detail_url = DETAIL_URL

    def get_general_extra_actions(self):
        """Build the header-level extra actions.

        Returns:
            list[dict]: Action configurations for the index header.
        """
        return [
            {
                "title_button": EXPORT_BUTTON_TITLE,
                "icon": EXPORT_BUTTON_ICON,
                "url": EXPORT_CSV_URL,
                "class": EXPORT_BUTTON_CLASS,
            },
        ]


class CreateView(PermissionRequiredMixin, SuccessNotificationMixin, GenericCreateView):
    """Create new song reviews."""

    permission_required = PERMISSION_ADD
    model = SongReview
    form_class = SongReviewForm
    success_url = reverse_lazy(INDEX_URL)
    title = CREATE_TITLE
    return_url = INDEX_URL

    notification_message = SUCCESS_REVIEW_CREATED_MESSAGE
    notification_title = SUCCESS_REVIEW_CREATED_TITLE
    # To notify certain users, you need to specify a queryset in the `notification_users` variable.
    # notification_users = None # Here goes a queryset


class EditView(PermissionRequiredMixin, SuccessNotificationMixin, GenericUpdateView):
    """Edit existing song reviews."""

    permission_required = PERMISSION_CHANGE
    model = SongReview
    form_class = SongReviewForm
    title = EDIT_TITLE
    success_url = reverse_lazy(INDEX_URL)
    return_url = INDEX_URL

    notification_message = SUCCESS_REVIEW_UPDATED_MESSAGE
    notification_title = SUCCESS_REVIEW_UPDATED_TITLE
    # To notify certain users, you need to specify a queryset in the `notification_users` variable.
    # notification_users = None # Here goes a queryset

    def get_form_kwargs(self):
        """Build form kwargs with the current user.

        Returns:
            dict: Keyword arguments passed to the form instance.
        """
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class DeleteView(PermissionRequiredMixin, GenericDeleteView):
    """Delete or disable song reviews."""

    permission_required = PERMISSION_DELETE
    model = SongReview
    success_url = reverse_lazy(INDEX_URL)
    can_disable = True


class DetailView(PermissionRequiredMixin, GenericDetailView):
    """Display details for a song review."""

    permission_required = PERMISSION_VIEW
    model = SongReview
    shown_fields = DETAIL_FIELDS
    return_url = INDEX_URL
    success_url = reverse_lazy(INDEX_URL)
    title = DETAIL_TITLE
    view_deleted_objects = True


class ExportCSVView(View):
    """Export song reviews as a CSV file."""

    model = SongReview

    def get_queryset(self):
        """Return the data used for the CSV export.

        Returns:
            QuerySet: A queryset of values for the CSV output.
        """
        return self.model.objects.all().values(
            "album__title",
            "song__title",
            "score",
        )

    def get_filename(self):
        """Return the name of the exported file.

        Returns:
            str: The CSV file name.
        """
        return CSV_FILENAME

    def get(self, request, *args, **kwargs):
        """Generate and return the song reviews CSV file.

        Args:
            request: The incoming HTTP request.
            *args: Positional arguments provided by the framework.
            **kwargs: Keyword arguments provided by the framework.

        Returns:
            HttpResponse: A CSV file response with song reviews.
        """
        df = pd.DataFrame(list(self.get_queryset()))

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = f'attachment; filename="{self.get_filename()}"'

        df.to_csv(path_or_buf=response, index=False)
        return response


class ModalIndexView(PermissionRequiredMixin, GenericFilterView):
    """List and filter song reviews in a modal index view."""

    template_name = "song_reviews/modal_index.html"
    permission_required = PERMISSION_VIEW
    model = SongReview
    filterset_class = SongReviewFilter
    shown_fields = INDEX_FIELDS
    title = MODAL_INDEX_TITLE
    ordering = ORDERING

    edit_url = EDIT_URL
    detail_url = DETAIL_URL
