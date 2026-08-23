import msal
from django.conf import settings

from apps.microsoft.consts import SESSION_KEY_AUTH_FLOW, SESSION_KEY_TOKEN_CACHE, SESSION_KEY_USER

AUTHORITY = f"{settings.MICROSOFT_AUTHORITY_URL}/{settings.MICROSOFT_TENANT_ID}"


def load_cache(request):
    """Docstring for load_cache."""
    cache = msal.SerializableTokenCache()
    if request.session.get(SESSION_KEY_TOKEN_CACHE):
        cache.deserialize(request.session[SESSION_KEY_TOKEN_CACHE])
    return cache


def save_cache(request, cache):
    """Docstring for save_cache."""
    if cache.has_state_changed:
        request.session[SESSION_KEY_TOKEN_CACHE] = cache.serialize()


def get_msal_app(cache=None):
    """Docstring for get_msal_app."""
    auth_app = msal.ConfidentialClientApplication(
        settings.MICROSOFT_APP_ID, authority=AUTHORITY, client_credential=settings.MICROSOFT_APP_SECRET, token_cache=cache
    )
    return auth_app


def get_sign_in_flow():
    """Docstring for get_sign_in_flow."""
    auth_app = get_msal_app()
    return auth_app.initiate_auth_code_flow(settings.MICROSOFT_SCOPES, redirect_uri=settings.MICROSOFT_REDIRECT_URI)


def get_token_from_code(request):
    """Docstring for get_token_from_code."""
    cache = load_cache(request)
    auth_app = get_msal_app(cache)
    flow = request.session.pop(SESSION_KEY_AUTH_FLOW, {})
    result = auth_app.acquire_token_by_auth_code_flow(flow, request.GET)
    save_cache(request, cache)
    return result


def get_token(request):
    """Docstring for get_token."""
    cache = load_cache(request)
    auth_app = get_msal_app(cache)
    accounts = auth_app.get_accounts()
    if accounts:
        result = auth_app.acquire_token_silent(settings.MICROSOFT_SCOPES, account=accounts[0])
        save_cache(request, cache)
        return result["access_token"]


def remove_user_and_token(request):
    """Docstring for remove_user_and_token."""
    if SESSION_KEY_TOKEN_CACHE in request.session:
        del request.session[SESSION_KEY_TOKEN_CACHE]
    if SESSION_KEY_USER in request.session:
        del request.session[SESSION_KEY_USER]
