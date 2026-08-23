import logging
from urllib.parse import urlencode

import httpx
from django.conf import settings
from django.contrib.auth import login, logout
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic.base import RedirectView
from ninja import Status

from djangoproject.backends import OAuth2Backend

from .const import (
    ERROR_ACCESS_DENIED,
    ERROR_GENERIC,
    ERROR_KEY_ACCESS_DENIED,
    OAUTH2_BACKEND,
    OAUTH2_SCOPE,
    PROVIDER_PATH_AUTHORIZE,
    PROVIDER_PATH_LOGOUT,
    PROVIDER_PATH_REVOKE,
    PROVIDER_PATH_TOKEN,
    PROVIDER_PATH_USERINFO,
    SESSION_KEY_ACCESS_TOKEN,
    SESSION_KEY_CODE_VERIFIER,
    SESSION_KEY_ID_TOKEN,
    SESSION_KEY_LOGIN_AT,
    TEMPLATE_LOGOUT,
    URL_DASHBOARD_INDEX,
    URL_OAUTH2_AUTHORIZE,
)
from .utils import generate_code_challenge, generate_code_verifier

logger = logging.getLogger(__name__)


class OAuthLogoutView(View):
    """Logs out the user locally and on the OAuth2 provider."""

    def post(self, request, *args, **kwargs):
        """Clears the local session, revokes token, and redirects to provider logout.

        Args:
            request: The incoming HTTP request.

        Returns:
            HttpResponseRedirect: Redirect to the provider's logout URL.
        """
        return self._perform_logout(request)

    def get(self, request, *args, **kwargs):
        """Handles GET logout (e.g. direct URL access)."""
        return self._perform_logout(request)

    def _perform_logout(self, request):
        """Revokes the OAuth2 token, clears local session, and redirects to provider logout.

        Args:
            request: The incoming HTTP request.

        Returns:
            HttpResponseRedirect: Redirect to the provider's logout or authorize URL.
        """
        access_token = request.session.get(SESSION_KEY_ACCESS_TOKEN, "")
        id_token = request.session.get(SESSION_KEY_ID_TOKEN, "")
        if access_token:
            self._revoke_token(access_token)
        logout(request)

        provider_url = settings.PROVIDER_URL_EXTERNAL
        redirect_uri_logout = settings.REDIRECT_URI_LOGOUT
        if provider_url and redirect_uri_logout:
            params = {"post_logout_redirect_uri": redirect_uri_logout}
            if id_token:
                params["id_token_hint"] = id_token
            return redirect(f"{provider_url}{PROVIDER_PATH_LOGOUT}?{urlencode(params)}")
        return redirect(reverse_lazy(URL_OAUTH2_AUTHORIZE))

    def _revoke_token(self, access_token):
        """Revokes the access token on the OAuth2 provider.

        Args:
            access_token: The OAuth2 access token to revoke.
        """
        try:
            provider_url = settings.PROVIDER_URL_INTERNAL
            revoke_url = f"{provider_url}{PROVIDER_PATH_REVOKE}"
            data = {
                "token": access_token,
                "client_id": settings.CLIENT_ID,
                "client_secret": settings.CLIENT_SECRET,
            }
            with httpx.Client() as client:
                client.post(revoke_url, data=data)
        except Exception:
            logger.exception("Error revoking OAuth2 token on provider")


class SuccessfulLogoutView(View):
    """Landing page after provider logout redirects back to this app."""

    def get(self, request, *args, **kwargs):
        """Renders the logout confirmation page.

        Args:
            request: The incoming HTTP request.

        Returns:
            HttpResponse: The logout template.
        """
        return redirect(reverse_lazy(URL_OAUTH2_AUTHORIZE))


class OAuthAuthorizeView(RedirectView):
    """Redirects to the OAuth2 provider authorization endpoint with PKCE."""

    def get_redirect_url(self, *args, **kwargs):
        """Builds the authorization URL with PKCE challenge parameters.

        Generates a new code verifier per login attempt, stores it in the session,
        and derives the code challenge from it.

        Returns:
            str: Full authorization URL for the OAuth2 provider.
        """
        code_challenge_method = settings.CODE_CHALLENGER_METHOD
        code_verifier = generate_code_verifier()
        self.request.session[SESSION_KEY_CODE_VERIFIER] = code_verifier
        code_challenge = generate_code_challenge(code_verifier)

        client_id = settings.CLIENT_ID
        redirect_uri = settings.REDIRECT_URI_EXTERNAL
        provider_url = settings.PROVIDER_URL_EXTERNAL

        authorization_url = (
            f"{provider_url}{PROVIDER_PATH_AUTHORIZE}"
            f"?response_type=code"
            f"&code_challenge={code_challenge}"
            f"&code_challenge_method={code_challenge_method}"
            f"&client_id={client_id}"
            f"&redirect_uri={redirect_uri}"
            f"&scope={OAUTH2_SCOPE}"
        )

        return authorization_url


class OAuthCallbackView(View):
    """Handles the OAuth2 callback: exchanges code for token and logs in."""

    def get(self, request, *args, **kwargs):
        """Processes the OAuth2 callback from the provider.

        Args:
            request: The incoming HTTP request with authorization code.

        Returns:
            HttpResponse: Redirect to dashboard on success, or error page.
        """
        error = request.GET.get("error", None)
        if error:
            dict_error = {
                ERROR_KEY_ACCESS_DENIED: ERROR_ACCESS_DENIED,
            }
            message = dict_error.get(error, ERROR_GENERIC)
            return render(request, TEMPLATE_LOGOUT, {"message": message})

        code = request.GET.get("code")
        client_id = settings.CLIENT_ID
        client_secret = settings.CLIENT_SECRET
        redirect_uri = settings.REDIRECT_URI_EXTERNAL
        provider_url = settings.PROVIDER_URL_INTERNAL
        token_url = f"{provider_url}{PROVIDER_PATH_TOKEN}"
        code_verifier = request.session.get(SESSION_KEY_CODE_VERIFIER)

        if not code_verifier:
            logger.warning("PKCE code_verifier missing from session during OAuth2 callback")
            return redirect(reverse_lazy(URL_OAUTH2_AUTHORIZE))

        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": redirect_uri,
            "client_id": client_id,
            "client_secret": client_secret,
            "code_verifier": code_verifier,
        }

        try:
            token_data, user_info = self._fetch_token_and_user_info(token_url, data, provider_url)
        except Exception:
            logger.exception("Error during OAuth2 token exchange")
            return redirect(reverse_lazy(URL_OAUTH2_AUTHORIZE))

        if not token_data or not user_info:
            return redirect(reverse_lazy(URL_OAUTH2_AUTHORIZE))

        backend = OAuth2Backend()
        user = backend.authenticate(request, user_data=user_info, token_data=token_data)

        if not user:
            ban_error = getattr(request, "oauth2_login_error", None)
            if ban_error:
                return render(request, TEMPLATE_LOGOUT, {"message": ban_error})
            return redirect(reverse_lazy(URL_OAUTH2_AUTHORIZE))

        login(request, user, backend=OAUTH2_BACKEND)
        request.session.pop(SESSION_KEY_CODE_VERIFIER, None)
        request.session[SESSION_KEY_LOGIN_AT] = timezone.now().isoformat()
        request.session[SESSION_KEY_ACCESS_TOKEN] = token_data.get("access_token", "")
        request.session[SESSION_KEY_ID_TOKEN] = token_data.get("id_token", "")

        return redirect(reverse_lazy(URL_DASHBOARD_INDEX))

    def _fetch_token_and_user_info(self, token_url, data, provider_url):
        """Exchanges authorization code for tokens and fetches user info.

        Args:
            token_url: URL to exchange the authorization code.
            data: POST data for the token request.
            provider_url: Base URL of the OAuth2 provider.

        Returns:
            tuple: (token_data, user_info) dicts, or (None, None) on failure.
        """
        with httpx.Client() as client:
            token_response = client.post(token_url, data=data)
            token_data = token_response.json()

            if token_response.status_code != Status.OK:
                return None, None

            access_token = token_data.get("access_token")
            user_info_url = f"{provider_url}{PROVIDER_PATH_USERINFO}"
            headers = {"Authorization": f"Bearer {access_token}"}
            user_info_response = client.get(user_info_url, headers=headers)
            user_info = user_info_response.json()

            return token_data, user_info
