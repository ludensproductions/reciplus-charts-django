from datetime import datetime, timezone
from http import HTTPStatus

from django.core.handlers.asgi import ASGIRequest
from ninja.responses import Status
from ninja_extra import api_controller, http_post
from ninja_extra.security import django_auth

from apps.activity_feed.utils import emit_activity


@api_controller("/activity-feed", tags=["Activity Feed"], auth=django_auth)
class ActivityFeedController:
    """API controller responsible for managing activity feed actions.

    This controller provides endpoints to:
    - Trigger an emit activity action.
    """

    @http_post(
        path="/emit-activity",
        response={
            HTTPStatus.OK: None,
        },
    )
    def trigger_emit_activity(self, request: ASGIRequest):
        """Triggers a test event.

        Args:
            request (ASGIRequest): Incoming HTTP request containing the
                authenticated user.

        Returns:
            Tuple[HTTPStatus, None]: HTTP status indicating the outcome.
        """
        emit_activity(f"[INFO {datetime.now(timezone.utc)}]: This is a test event.")
        return Status(HTTPStatus.OK, None)
