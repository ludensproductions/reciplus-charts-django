import logging
import os
from datetime import datetime
from functools import wraps
from http import HTTPStatus

import httpx
import jwt
from django.conf import settings
from django.contrib.auth import logout
from django.http import HttpRequest, JsonResponse
from django.shortcuts import redirect
from django.utils import timezone
from ninja.security import HttpBasicAuth, HttpBearer
from ninja_jwt.authentication import JWTAuth

from apps.comun.consts import ERROR_AUTH_CREDENTIALS_MISSING, ERROR_PERMISSION_DENIED
from apps.oauth2.const import (
    PROVIDER_CHECK_INTERVAL,
    PROVIDER_PATH_USERINFO,
    SESSION_KEY_ACCESS_TOKEN,
    SESSION_KEY_LOGIN_AT,
)

logger = logging.getLogger(__name__)


class ForceLogoutMiddleware:
    """Middleware that forces logout when the provider session is no longer valid.

    Two checks are performed for each authenticated request:

    1. **Centralized logout flag** — if PUMA called the ``/api/o/logout``
       endpoint, the user's ``force_logout_at`` field is set.  Any session
       created *before* that timestamp is immediately invalidated.

    2. **Periodic provider session validation** — every
       ``PROVIDER_CHECK_INTERVAL`` seconds the middleware hits the
       provider's ``/o/userinfo/`` endpoint with the stored access token.
       If the token is rejected (provider session expired / user logged
       out), the local session is terminated.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated:
            return self.get_response(request)

        # Skip checks for API and OAuth2 callback paths
        path = request.path
        if path.startswith("/api/") or path.startswith("/oauth2/"):
            return self.get_response(request)

        # --- Check 0: banned user ---
        if getattr(request.user, "is_banned", False):
            logout(request)
            return redirect(settings.LOGIN_URL)

        # --- Check 1: centralized logout flag ---
        if hasattr(request.user, "force_logout_at"):
            force_logout_at = request.user.force_logout_at
            if force_logout_at:
                session_login_at = request.session.get(SESSION_KEY_LOGIN_AT)
                should_logout = True
                if session_login_at:
                    login_dt = datetime.fromisoformat(session_login_at)
                    if timezone.is_naive(login_dt):
                        login_dt = timezone.make_aware(login_dt)
                    if login_dt >= force_logout_at:
                        should_logout = False

                if should_logout:
                    logout(request)
                    return redirect(settings.LOGIN_URL)

        # OAuth2-specific checks only when OAuth2 login is enabled
        if not settings.ENABLE_OAUTH2_LOGIN:
            return self.get_response(request)

        # --- Check 2: require OAuth2 session ---
        access_token = request.session.get(SESSION_KEY_ACCESS_TOKEN)
        if not access_token:
            # Session was not created via OAuth2; force re-authentication
            logout(request)
            return redirect(settings.LOGIN_URL)

        # --- Check 3: periodic provider session validation ---
        now = timezone.now().timestamp()
        last_check = request.session.get("_provider_last_check", 0)

        if now - last_check >= PROVIDER_CHECK_INTERVAL:
            request.session["_provider_last_check"] = now

            if not self._is_provider_session_active(access_token):
                logout(request)
                return redirect(settings.LOGIN_URL)

        return self.get_response(request)

    @staticmethod
    def _is_provider_session_active(access_token):
        """Validates the access token against the provider's userinfo endpoint.

        Args:
            access_token: The OAuth2 access token stored in the session.

        Returns:
            bool: True if the provider considers the token valid.
        """
        provider_url = settings.PROVIDER_URL_INTERNAL
        if not provider_url:
            return True

        try:
            response = httpx.get(
                f"{provider_url}{PROVIDER_PATH_USERINFO}",
                headers={"Authorization": f"Bearer {access_token}"},
                timeout=5,
            )
            return response.status_code == HTTPStatus.OK
        except Exception:
            logger.warning("Could not reach provider for session validation")
            return True

        return self.get_response(request)


class CustomJWTAuth(JWTAuth):  # noqa: D101
    """Custom JWT-based authentication backend extending the default JWTAuth.

    This class acts as a thin wrapper around the base JWT authentication
    mechanism, delegating token validation to the parent implementation
    while providing an explicit permission-checking helper.

    It is intended to be used in contexts where:
    - Authentication is performed via JWT tokens.
    - Authorization is enforced through Django's permission system.
    """

    def authenticate(self, request: HttpRequest, token: str):
        """Authenticates a request using a JWT token.

        This method delegates authentication to the underlying
        `jwt_authenticate` implementation provided by the parent class.

        Args:
            request (HttpRequest): Incoming HTTP request.
            token (str): JWT token extracted from the request.

        Returns:
            Optional[User]: Authenticated user if the token is valid;
                otherwise None.
        """
        user = self.jwt_authenticate(request, token)
        return user

    def has_permission(self, user, permission_code: str) -> bool:
        """Checks whether an authenticated user has a specific permission.

        This method uses Django's permission system and safely handles
        unexpected errors to avoid leaking authorization failures.

        Args:
            user (User): Authenticated user instance.
            permission_code (str): Django permission codename to check
                (e.g., "app_label.permission_name").

        Returns:
            bool: True if the user is authenticated and has the specified
                permission; False otherwise.
        """
        if not user.is_authenticated:
            return False
        try:
            return user.has_perms([permission_code])
        except Exception:
            return False


class BearerAuth(HttpBearer):
    """HTTP Bearer authentication backend based on raw JWT validation.

    This class validates Bearer tokens by:
    - Decoding the JWT using a secret key and algorithm provided via
      environment variables.
    - Rejecting expired or invalid tokens.

    Unlike full JWT authentication backends, this implementation:
    - Does NOT resolve a Django user.
    - Only validates the token's cryptographic integrity.

    It is suitable for service-to-service authentication or lightweight
    authorization checks where user context is not required.
    """

    def authenticate(self, request, token):
        """Authenticates a request using a Bearer token.

        The token is decoded using the secret key and algorithm defined
        in environment variables. If decoding succeeds, the token is
        considered valid.

        Environment Variables:
            SECRET_KEY (str): Secret key used to verify the JWT signature.
            JWT_ALGORITHM (str): Algorithm used to decode the JWT.

        Args:
            request (HttpRequest): Incoming HTTP request.
            token (str): Bearer token extracted from the Authorization
                header.

        Returns:
            Optional[str]: The token if it is valid; None otherwise.
        """
        SECRET_KEY = os.environ.get("SECRET_KEY")
        JWT_ALGORITHM = os.environ.get("JWT_ALGORITHM")

        if not SECRET_KEY or not JWT_ALGORITHM:
            return None

        try:
            # Decode the token using the secret key and algorithm
            jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
            # If decoding succeeds, return the token or any identifier
            return token
        except jwt.ExpiredSignatureError:
            # Token has expired
            return None
        except jwt.InvalidTokenError:
            # Token is invalid for other reasons
            return None


def permission_required(permission_code: str):
    """Method that authorizes the user based on its permissions.

    Args:
        permission_code (str): The codename of the permission.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            user = request.user
            if not user.is_authenticated:
                return JsonResponse(
                    {"detail": ERROR_AUTH_CREDENTIALS_MISSING},
                    status=401,
                )

            # Check permissions
            if not CustomJWTAuth().has_permission(user, permission_code):
                return JsonResponse({"detail": ERROR_PERMISSION_DENIED}, status=403)

            return func(request, *args, **kwargs)

        return wrapper

    return decorator


class HeaderAuthMiddleware(HttpBasicAuth):
    """Authentication middleware that validates credentials passed through custom HTTP headers.

    This middleware expects credentials to be provided via:
    - `User` header
    - `Password` header

    The credentials are validated against environment variables and are
    intended for internal or trusted-system authentication rather than
    end-user login.

    This mechanism should NOT be exposed to untrusted clients.
    """

    def __call__(self, request):
        """Extracts and validates authentication credentials from HTTP headers.

        If the required headers are missing or invalid, authentication
        fails silently and returns None.

        Args:
            request (HttpRequest): Incoming HTTP request.

        Returns:
            Optional[str]: Authenticated identifier if credentials are
            valid; None otherwise.
        """
        user = request.headers.get("User")
        password = request.headers.get("Password")

        if not user or not password:
            return None

        if user != os.getenv("AXXON_USER") or password != os.getenv("AXXON_PASSWORD"):
            return None

        return self.authenticate(request, user, password)

    def authenticate(self, request, username, password):
        """Validates the provided username and password against environment variables.

        Args:
            request (HttpRequest): Incoming HTTP request.
            username (str): Username extracted from request headers.
            password (str): Password extracted from request headers.

        Returns:
            Optional[str]: Username if credentials are valid; None
                otherwise.
        """
        if username != os.getenv("AXXON_USER") or password != os.getenv("AXXON_PASSWORD"):
            return None

        return username


class ApiKeyMiddleware(HttpBasicAuth):
    """Middleware to validate API key in incoming requests.

    Expects an Authorization header with format: ``Api-Key <key>``.
    The key is compared against ``settings.API_KEY_OAUTH2_PROVIDER``.
    """

    def __call__(self, request):
        """Extracts and validates the API key from the Authorization header.

        Args:
            request (HttpRequest): Incoming HTTP request.

        Returns:
            Optional[str]: The API key if valid; None otherwise.
        """
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return None

        parts = auth_header.split(" ", 1)
        if len(parts) < 2 or parts[0] != "Api-Key":
            return None

        api_key = parts[1]
        return self.authenticate(request, api_key)

    def authenticate(self, request, api_key):
        """Validates the API key against the configured setting.

        Args:
            request (HttpRequest): Incoming HTTP request.
            api_key (str): API key extracted from the header.

        Returns:
            Optional[str]: The API key if valid; None otherwise.
        """
        if api_key != settings.API_KEY_OAUTH2_PROVIDER:
            return None

        return api_key
