from django.utils.translation import gettext_lazy as _

APP_NAME = "groups"
MODEL_NAME = "customgroup"

INDEX_URL = f"{APP_NAME}:index"
CREATE_URL = f"{APP_NAME}:create"
EDIT_URL = f"{APP_NAME}:edit"
DELETE_URL = f"{APP_NAME}:delete"

INDEX_FIELDS = {
    "display_name": _("Grupo"),
}

USERS_CATALOG_URL = "users_module:index"

# View titles
INDEX_TITLE = _("Grupos")
CREATE_TITLE = _("Crear grupo")
EDIT_TITLE = _("Editar grupo")
DELETE_TITLE = _("Eliminar grupo")

# Ordering
ORDERING = ["-id"]

# Permissions
PERMISSION_VIEW = f"{APP_NAME}.view_{MODEL_NAME}"
PERMISSION_ADD = f"{APP_NAME}.add_{MODEL_NAME}"
PERMISSION_CHANGE = f"{APP_NAME}.change_{MODEL_NAME}"
PERMISSION_DELETE = f"{APP_NAME}.delete_{MODEL_NAME}"


class UserGroups:
    """Define built-in user group for code references."""

    ADMINISTRADOR = "Administrador"


# Form labels and placeholders
FORM_GROUP_LABEL = _("Grupo")
FORM_GROUP_PLACEHOLDER = _("Grupo")

# Validation messages
ERROR_GROUP_EXISTS = _("Ya existe un grupo con esta clave.")
ERROR_GROUP_INVALID = _("Ingrese un grupo válido. Solo se aceptan letras y números.")

# Action and message labels
ACTION_DELETE_LABEL = _("eliminar")
ACTION_RESTORE_LABEL = _("restaurar")
ACTION_DELETED_LABEL = _("eliminado")
ACTION_RESTORED_LABEL = _("restaurado")
LIST_CONJUNCTION_AND = _("y")
