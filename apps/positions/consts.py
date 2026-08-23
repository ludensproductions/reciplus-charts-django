from django.utils.translation import gettext_lazy as _

APP_NAME = "positions"
MODEL_NAME = "puestodepartamento"
MODULE_VERBOSE_NAME = _("puesto")

INDEX_URL = f"{APP_NAME}:index"
EDIT_URL = f"{APP_NAME}:edit"
PERMISSIONS_URL = f"{APP_NAME}:permissions"
DASHBOARD_URL = "users_module:index"

INDEX_FIELDS = {
    "departamento": _("Departamento"),
    "puesto": _("Título"),
    "is_jefe_departamento": _("Jefe de departamento"),
}

# View Titles
INDEX_TITLE = _("Puestos")
EDIT_TITLE = _("Editar puesto")
PERMISSIONS_TITLE = _("Asignar grupos")

# Ordering
ORDERING = ["-id"]

# Permissions
PERMISSION_VIEW = "positions.view_puesto"
PERMISSION_CHANGE = "positions.change_puestodepartamento"
PERMISSION_ADD_GROUP = "positions.add_positiongroup"

# Error messages
ERROR_POSITION_EXISTS_IN_DEPARTMENT = _("El puesto ya existe dentro del departamento.")

# Form labels and placeholders
FORM_DEPARTAMENTO_PLACEHOLDER = _("Departamento")
FORM_PUESTO_LABEL = _("Nombre del puesto")
FORM_PUESTO_PLACEHOLDER = _("Nombre del puesto")
FORM_GROUPS_LABEL = _("Grupos")
FORM_GROUPS_PLACEHOLDER = _("Seleccionar")
