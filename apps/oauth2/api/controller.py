from http import HTTPStatus

from django.core.handlers.wsgi import WSGIRequest
from django.utils import timezone
from ninja.responses import Status
from ninja_extra import api_controller, http_post

from apps.oauth2.const import ERROR_USER_NOT_FOUND, SUCCESS_LOGOUT
from apps.oauth2.schema import LogoutResponseOut, LogoutUser
from apps.oauth2.utils import delete_all_unexpired_sessions_for_user
from apps.users.models import User
from djangoproject.middleware import ApiKeyMiddleware

api_key_middleware = ApiKeyMiddleware()


@api_controller(
    "/o",
    tags=["Oauth2"],
    auth=api_key_middleware,
)
class Oauth2APIController:
    """API controller for OAuth2 centralized logout from the provider."""

    @http_post(
        path="/logout",
        response={
            HTTPStatus.OK: LogoutResponseOut,
            HTTPStatus.NOT_FOUND: LogoutResponseOut,
        },
    )
    def logout(self, request: WSGIRequest, payload: LogoutUser):
        """Logs out a user by deleting all their active sessions.

        Args:
            request: The incoming HTTP request.
            payload: LogoutUser schema with user_id (username or id from provider).

        Returns:
            Tuple[HTTPStatus, LogoutResponseOut]: Status and response message.
        """
        user_id = payload.user_id
        user = User.objects.filter(username=user_id).first()

        if not user and user_id.isdigit():
            user = User.objects.filter(id=int(user_id)).first()

        if not user:
            return Status(
                HTTPStatus.NOT_FOUND, LogoutResponseOut(message=ERROR_USER_NOT_FOUND)
            )

        user.force_logout_at = timezone.now()
        user.save(update_fields=["force_logout_at"])

        delete_all_unexpired_sessions_for_user(user)

        return Status(HTTPStatus.OK, LogoutResponseOut(message=SUCCESS_LOGOUT))

