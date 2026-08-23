import logging

from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db import OperationalError, connection
from django.shortcuts import redirect

from apps.comun.consts import ERROR_NO_PERMISSION_ACCESS

logger = logging.getLogger(__name__)


class AutoAccessMixin(UserPassesTestMixin):
    """Mixin that checks access automatically based on a query and a field.

    - When `query` is not provided, `created_by` is used as the default.
    - When `field` is not provided, `self.request.user` is used directly.
    - Supports one-to-many relations, specific fields and many-to-many relations.
    """

    query = "created_by"  # Default value: 'created_by'
    field = None  # When None, self.request.user is used directly
    return_url = None  # URL to redirect to when access is denied
    success_url = None  # Alternative URL to redirect to when access is denied

    def test_func(self):  # noqa: D102
        # Get the object from the view
        obj = self.get_object()

        # When no query is provided, fall back to created_by
        if self.query == "created_by":
            model_field_value = getattr(obj, self.query)
            if self.field is not None:
                user_field_value = getattr(self.request.user, self.field)
            else:
                user_field_value = self.request.user
            return model_field_value == user_field_value

        # When a query is provided, check relations or specific fields
        if self.field is not None:
            # Case: compare specific fields (for example, aduana)
            model_field_value = getattr(obj, self.query)
            user_field_value = getattr(self.request.user, self.field)
            return model_field_value == user_field_value
        else:
            # Case: one-to-many or many-to-many relations
            filter_kwargs = {
                "id": obj.id,  # Filter by the object ID
                self.query: self.request.user,  # Filter by the relation
            }
            return self.model.objects.filter(**filter_kwargs).exists()

    def handle_no_permission(self):  # noqa: D102
        if self.return_url or self.success_url:
            # Add an error message
            messages.error(self.request, ERROR_NO_PERMISSION_ACCESS)

            redirect_url = self.success_url if self.success_url else self.return_url

            # Redirect to the given URL
            return redirect(redirect_url)
        else:
            # Without a return_url, defer to the base class handle_no_permission
            return super().handle_no_permission()


class EnsureDatabaseConnectionMixin:
    """Mixin that forces a database connection check before handling the request.

    It runs in `dispatch` so it covers every HTTP method (GET, POST, etc.).
    """

    def dispatch(self, request, *args, **kwargs):
        """Check the database connection before delegating to the base dispatch.

        When the database is unavailable, log the error and let the
        OperationalError propagate instead of failing later inside the view.
        """
        try:
            connection.ensure_connection()
        except OperationalError:
            logger.exception("Database unavailable while handling the request")
            raise
        return super().dispatch(request, *args, **kwargs)
