from django.utils.translation import gettext_lazy as _

INDEX_TEMPLATE = "dashboard/dashboard.html"
USUARIOS_TEMPLATE = "dashboard/usuarios.html"

USUARIOS_TITLE = _("Usuarios")
APP_NAME = "users_module"

# Permissions
PERMISSION_VIEW = _("Ver módulo de usuarios")

# Model metadata
MODEL_VERBOSE_NAME = _("Módulo de usuarios")
MODEL_VERBOSE_NAME_PLURAL = _("Módulo de usuarios")


USER_CARDS = [
    {"perm": "departments.view_departamento", "catalogo_url": "departments:index", "title": _("Departamentos")},
    {"perm": "groups.view_customgroup", "catalogo_url": "groups:index", "title": _("Grupos de permisos")},
    {"perm": "positions.view_puesto", "catalogo_url": "positions:index", "title": _("Puestos")},
    {"perm": "users.view_user", "catalogo_url": "users:index", "title": _("Usuarios")},
]
