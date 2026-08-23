from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import RedirectView, TemplateView

from .auth import MicrosoftAuthenticationBackend
from .auth_helper import get_sign_in_flow, get_token_from_code
from .consts import (
    ERROR_AUTH_FAILED,
    ERROR_PROFILE_FAILED,
    ERROR_SESSION_EXPIRED,
    ERROR_TOKEN_FAILED,
    LOGIN_URL_NAME,
    MICROSOFT_AUTH_BACKEND,
    MSG_SESSION_CLOSED,
    TEMPLATE_NAME_INVALID_LOGIN,
)
from .graph_helper import get_user


class InvalidLoginView(TemplateView):
    """Docstring for class InvalidLoginView."""

    template_name = TEMPLATE_NAME_INVALID_LOGIN


class MicrosoftSignInView(RedirectView):
    """
    Inicia el flujo de autenticación obteniendo la URL de Microsoft
    y guardando el estado en la sesión.
    """

    permanent = False
    query_string = False

    def get_redirect_url(self, *args, **kwargs):
        """Docstring for get_redirect_url."""
        flow = get_sign_in_flow()
        self.request.session["auth_flow"] = flow
        return flow["auth_uri"]


class MicrosoftSignOutView(RedirectView):
    """Cierra la sesión del usuario y redirige."""

    permanent = False

    def get_redirect_url(self, *args, **kwargs):
        """Docstring for get_redirect_url."""
        logout(self.request)
        messages.success(self.request, MSG_SESSION_CLOSED)
        return reverse_lazy(LOGIN_URL_NAME)


class MicrosoftCallbackView(View):
    """Maneja la respuesta de Microsoft, valida el token y crea la sesión."""

    def get(self, request, *args, **kwargs):
        """Docstring for get."""
        try:
            result = get_token_from_code(request)
        except ValueError:
            messages.error(request, ERROR_SESSION_EXPIRED)
            return redirect(LOGIN_URL_NAME)
        if not result or "access_token" not in result:
            messages.error(request, ERROR_TOKEN_FAILED)
            return redirect(LOGIN_URL_NAME)
        user_data = get_user(result["access_token"])
        if not user_data:
            messages.error(request, ERROR_PROFILE_FAILED)
            return redirect(LOGIN_URL_NAME)
        backend = MicrosoftAuthenticationBackend()
        microsoft_user = backend.authenticate(request, user=user_data)
        if not microsoft_user:
            error_msg = getattr(request, "microsoft_login_error", ERROR_AUTH_FAILED)
            messages.error(request, error_msg)
            return redirect(LOGIN_URL_NAME)
        login(request, microsoft_user, backend=MICROSOFT_AUTH_BACKEND)
        return redirect(settings.LOGIN_REDIRECT_URL)
