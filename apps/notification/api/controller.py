from http import HTTPStatus

from django.core.handlers.asgi import ASGIRequest
from django.core.paginator import Paginator
from django_eventstream import send_event
from ninja.responses import Status
from ninja_extra import api_controller, http_patch, http_post
from ninja_extra.security import django_auth

from apps.notification.api.schemas import (
    ReadNotificationIn,
    ReadNotificationOut,
)
from apps.notification.consts import (
    NOTIFICATIONS_CHANNEL_PREFIX,
)
from apps.notification.models import Notification
from apps.notification.utils import render_notification


@api_controller("/notifications", tags=["notifications"], auth=django_auth)
class NotificationsController:
    """API controller responsible for managing user notifications.

    This controller provides endpoints to:
    - Mark a single notification as read.
    - Mark all unread notifications as read.
    - Retrieve paginated unread notifications rendered as HTML fragments.

    The controller assumes:
    - Requests are authenticated via Django authentication.
    - Notifications are user-scoped and must never be accessed across users.
    - Client-side state is partially synchronized via Server-Sent Events (SSE).

    Attributes:
        PAGE_LIMIT (int): Maximum number of notifications returned per page
            when retrieving notifications.
    """

    PAGE_LIMIT = 10

    @http_patch(
        path="/{notification_id}",
        response={
            HTTPStatus.OK: None,
            HTTPStatus.NOT_FOUND: None,
        },
    )
    def read_notification(self, request: ASGIRequest, notification_id: int):
        """Marks a single notification as read.

        The notification must:
        - Exist.
        - Belong to the authenticated user.

        If the notification does not exist or does not belong to the user,
        a NOT_FOUND response is returned to avoid leaking information.

        Upon successfully marking the notification as read, a server-sent
        event is emitted to notify the client about:
        - The updated unread notifications count.
        - The specific notification that was marked as read.

        Args:
            request (ASGIRequest): Incoming HTTP request containing the
                authenticated user.
            notification_id (int): Primary key of the notification to mark
                as read.

        Returns:
            Status: HTTP status indicating the outcome.
        """
        user = request.user
        try:
            notification = Notification.objects.get(pk=notification_id, user=user)
        except Notification.DoesNotExist:
            return Status(HTTPStatus.NOT_FOUND, None)

        notification.is_read = True
        notification.save(update_fields=["is_read"])

        send_event(
            f"{NOTIFICATIONS_CHANNEL_PREFIX}{user.pk}",
            "notification_read",
            {
                "count": Notification.objects.filter(user=user, is_read=False).count(),
                "notification_id": notification.id,
            },
        )

        return Status(HTTPStatus.OK, None)

    @http_patch(
        path="",
        response={
            HTTPStatus.OK: None,
        },
    )
    def read_all_notifications(self, request: ASGIRequest):
        """Marks all unread notifications for the authenticated user as read.

        If there are no unread notifications, the operation is a no-op and
        returns immediately.

        After updating the notifications, a server-sent event is emitted
        to notify the client that all notifications have been marked as
        read and to synchronize the unread notifications count.

        Args:
            request (ASGIRequest): Incoming HTTP request containing the
                authenticated user.

        Returns:
            Status: HTTP status indicating the operation
                completed successfully.
        """
        user = request.user
        notifications = Notification.objects.filter(user=user, is_read=False)

        if not notifications.exists():
            return Status(HTTPStatus.OK, None)

        notifications.update(is_read=True)

        send_event(
            f"{NOTIFICATIONS_CHANNEL_PREFIX}{user.pk}",
            "all_notifications_read",
            {
                "count": Notification.objects.filter(user=user, is_read=False).count(),
            },
        )

        return Status(HTTPStatus.OK, None)

    @http_post(
        path="",
        response={
            HTTPStatus.OK: ReadNotificationOut,
        },
    )
    def get_notifications(self, request: ASGIRequest, parameters: ReadNotificationIn):
        """Retrieves a paginated list of unread notifications for the authenticated user.

        Notifications are:
        - Filtered to unread only.
        - Ordered by creation date (newest first).
        - Paginated using a fixed page size.
        - Rendered server-side into HTML fragments.

        The endpoint also returns:
        - Whether additional pages exist.
        - The count of unread notifications excluding those already known
          by the client (used for incremental synchronization).

        Args:
            request (ASGIRequest): Incoming HTTP request containing the
                authenticated user.
            parameters (ReadNotificationIn): Input parameters containing:
                - page (int): Page number to retrieve.
                - new_notification_ids (list[int]): IDs already present on
                  the client to exclude from the count.

        Returns:
            Status: HTTP status and response payload containing:
                - notifications_html (list[str]): Rendered notification
                  HTML fragments.
                - has_next (bool): Whether additional pages are available.
                - count (int): Number of remaining unread notifications
                  excluding known IDs.
        """
        page = parameters.page
        exclude_ids = parameters.new_notification_ids

        notifications = (
            Notification.objects.only("id", "title", "content", "created_at", "is_read")
            .filter(user=request.user, is_read=False)
            .order_by("-created_at")
        )

        count = notifications.exclude(pk__in=exclude_ids).count()

        paginator = Paginator(notifications, self.PAGE_LIMIT)
        notifications = paginator.get_page(page)

        notifications_html = [
            render_notification(notification=notification) for notification in notifications.object_list
        ]

        return Status(
            HTTPStatus.OK,
            {
                "notifications_html": notifications_html,
                "has_next": notifications.has_next(),
                "count": count,
            },
        )
