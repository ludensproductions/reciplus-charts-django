"""Bridge de autenticación con reciplus-djangoninja para las plataformas que NO
comparten cookies con el navegador donde se abre /graphs (Android/iOS/Desktop — ver
apps.graphs.auth_bridge_controller). La web NO pasa por aquí: usa sesión Django
compartida de verdad (mismo django_session, misma llave de firma — ver
reciplus-djangoninja apps.auth.api_controller.establish_session y
common/django/shared/session_backend.py).

Flujo nativo: la app manda el JWT (que ya tiene, de su login normal) a
POST /graphs/exchange-code. Se valida una vez aquí y se genera un código opaco de un
solo uso (EXCHANGE_CODE_TTL_SECONDS de vida, en cache/Redis). La app abre
reci.plus/graphs/?code=<codigo> en el navegador del sistema; ahí se canjea (se borra
al leerse, nunca se reusa) y se llama a django.contrib.auth.login() — de ahí en
adelante es sesión Django normal, igual que en web.
"""
from __future__ import annotations

import secrets

from django.conf import settings
from django.core.cache import cache
from jose import JWTError, jwt

from apps.graphs import consts as graphs_consts
from common.django.user.models import User

_EXCHANGE_CODE_CACHE_PREFIX = "graphs:exchange-code:"

# Igual que NINJA_JWT['ALGORITHM'] en reciplus-djangoninja — nunca cambia entre
# ambientes, así que va hardcodeado en ambos lados, no como variable de entorno.
_JWT_ALGORITHM = "HS256"


class AuthBridgeError(Exception):
    """Token inválido/expirado, usuario inexistente, o sin permiso."""


def _decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[_JWT_ALGORITHM],
        )
    except JWTError as exc:
        raise AuthBridgeError(graphs_consts.ERROR_INVALID_TOKEN) from exc

    if payload.get("token_type") != "access":
        raise AuthBridgeError(graphs_consts.ERROR_INVALID_TOKEN)

    return payload


def resolve_user_from_token(token: str) -> User:
    """Valida [token] y regresa el User compartido que representa. Levanta
    AuthBridgeError si el token es inválido, el usuario no existe, o no pertenece
    al grupo requerido."""
    payload = _decode_access_token(token)

    user_id = payload.get("user_id")
    if user_id is None:
        raise AuthBridgeError(graphs_consts.ERROR_INVALID_TOKEN)

    user = User.objects.filter(id=user_id, is_active=True).first()
    if user is None:
        raise AuthBridgeError(graphs_consts.ERROR_INVALID_TOKEN)

    if not user.groups.filter(name__in=graphs_consts.ALLOWED_GROUPS).exists():
        raise AuthBridgeError(graphs_consts.ERROR_FORBIDDEN)

    return user


def create_exchange_code(user: User) -> str:
    """Genera un código opaco de un solo uso que representa a [user]. Solo para
    plataformas nativas."""
    code = secrets.token_urlsafe(24)
    cache.set(
        f"{_EXCHANGE_CODE_CACHE_PREFIX}{code}",
        user.id,
        timeout=graphs_consts.EXCHANGE_CODE_TTL_SECONDS,
    )
    return code


def redeem_exchange_code(code: str) -> User | None:
    """Canjea [code] por el User que representa — de un solo uso, se borra al
    leerse exista o no. Regresa None si no existe / ya expiró / ya se usó."""
    cache_key = f"{_EXCHANGE_CODE_CACHE_PREFIX}{code}"
    user_id = cache.get(cache_key)
    cache.delete(cache_key)
    if user_id is None:
        return None
    return User.objects.filter(id=user_id, is_active=True).first()
