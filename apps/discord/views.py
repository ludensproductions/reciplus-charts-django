from http import HTTPStatus
from urllib.parse import quote, urlencode

import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import RedirectView

from apps.discord.auth import DiscordAuthenticationBackend
from apps.discord.consts import (
    CONTENT_TYPE_FORM_URLENCODED,
    DISCORD_AUTH_BACKEND,
    ERROR_NO_PERMISSIONS,
    ERROR_NO_ROLES,
    GUILD_MEMBER_ENDPOINT,
    LOGIN_URL_NAME,
    OAUTH2_TOKEN_ENDPOINT,
    USER_ME_ENDPOINT,
)


class DiscordLoginView(RedirectView):
    """Maneja la redirección inicial a la página de autorización de Discord."""

    permanent = False
    query_string = True

    def get_redirect_url(self, *args, **kwargs):
        """Docstring for get_redirect_url."""
        params = {
            "client_id": settings.DISCORD_CLIENT_ID,
            "redirect_uri": settings.DISCORD_REDIRECT_URI,
            "response_type": settings.DISCORD_RESPONSE_TYPE,
        }
        scope_string = quote("+".join(settings.DISCORD_SCOPES), safe="+")
        auth_url = f"{settings.DISCORD_AUTH_URL}?{urlencode(params)}&scope={scope_string}"
        return auth_url


class DiscordLoginRedirectView(View):
    """Maneja el callback de Discord."""

    def get(self, request, *args, **kwargs):
        """Docstring for get."""
        code = request.GET.get("code")
        user_data = self._exchange_code(code)
        if not user_data:
            return redirect(reverse_lazy(LOGIN_URL_NAME))
        backend = DiscordAuthenticationBackend()
        discord_user = backend.authenticate(request, user=user_data)
        if not discord_user:
            error_msg = getattr(request, "discord_login_error", ERROR_NO_ROLES)
            messages.error(request, error_msg)
            return redirect(reverse_lazy(LOGIN_URL_NAME))
        
        

        login(request, discord_user, backend=DISCORD_AUTH_BACKEND)
        return redirect(reverse_lazy(settings.LOGIN_REDIRECT_URL))

    def _exchange_code(self, code: str):
        """Método auxiliar (privado) para manejar la lógica de la API de Discord."""
        data = {
            "client_id": settings.DISCORD_CLIENT_ID,
            "client_secret": settings.DISCORD_CLIENT_SECRET,
            "grant_type": settings.DISCORD_GRANT_TYPE,
            "code": code,
            "redirect_uri": settings.DISCORD_REDIRECT_URI,
            "scope": " ".join(settings.DISCORD_SCOPES),
        }
        headers = {"Content-Type": CONTENT_TYPE_FORM_URLENCODED}
        discord_api_url = settings.DISCORD_API_URL
        response = requests.post(f"{discord_api_url}{OAUTH2_TOKEN_ENDPOINT}", data=data, headers=headers)
        if response.status_code != HTTPStatus.OK:
            messages.error(self.request, ERROR_NO_PERMISSIONS)
            return None
        credentials = response.json()
        access_token = credentials.get("access_token")
        guild_response = requests.get(
            f"{discord_api_url}{GUILD_MEMBER_ENDPOINT.format(guild_id=settings.DISCORD_GUILD_ID)}",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        user_response = requests.get(
            f"{discord_api_url}{USER_ME_ENDPOINT}", headers={"Authorization": f"Bearer {access_token}"}
        )
        guild_data = guild_response.json()
        if "user" not in guild_data or guild_data["user"] is None:
            messages.error(self.request, ERROR_NO_ROLES)
            return None
        base_user_data = user_response.json()
        email = base_user_data.get("email")
        username = base_user_data.get("username")
        discriminator = base_user_data.get("discriminator")
        nickname = guild_data.get("nick") or username
        roles = guild_data.get("roles", [])
        avatar = base_user_data.get("avatar", None)
        return {
            "id": base_user_data["id"],
            "username": username,
            "email": email,
            "discriminator": discriminator,
            "nick": nickname,
            "roles": roles,
            "avatar": avatar,
        }
