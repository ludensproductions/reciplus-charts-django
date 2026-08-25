"""Helpers de autorización para los endpoints/vistas de gráficas.

Funciona igual sin importar cómo se autenticó el usuario — sesión compartida real en
web, o código de intercambio canjeado en nativo (ver apps.graphs.auth_bridge): ambos
caminos terminan en un django.contrib.auth.login() real, así que esto solo mira
request.user, el mecanismo estándar de Django.
"""
from __future__ import annotations

from ninja.errors import HttpError

from apps.graphs import consts as graphs_consts


def bearer_token(request) -> str | None:
    """Extrae el token del header Authorization: Bearer <token>, o None si no viene."""
    header = request.headers.get("Authorization", "")
    if not header.startswith("Bearer "):
        return None
    return header.removeprefix("Bearer ").strip() or None


def has_graphs_access(user) -> bool:
    return user.is_authenticated and user.groups.filter(name__in=graphs_consts.ALLOWED_GROUPS).exists()


def session_doctor_scope(request) -> int | None:
    """Levanta 401 si no hay sesión válida o el usuario no pertenece a un grupo
    permitido. Regresa None (admin, ve todo) o el id del doctor de la sesión
    (doctor, ve solo lo suyo)."""
    if not has_graphs_access(request.user):
        raise HttpError(401, graphs_consts.ERROR_NOT_AUTHENTICATED)
    is_admin = request.user.groups.filter(name=graphs_consts.GROUP_ADMINISTRATOR).exists()
    return None if is_admin else request.user.id
