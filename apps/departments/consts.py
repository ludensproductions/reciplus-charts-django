from django.utils.translation import gettext_lazy as _

APP_NAME = "departments"
MODEL_NAME = "departamento"

INDEX_URL = f"{APP_NAME}:index"
CREATE_URL = f"{APP_NAME}:create"
EDIT_URL = f"{APP_NAME}:edit"
DELETE_URL = f"{APP_NAME}:delete"
DETAIL_URL = f"{APP_NAME}:detail"
DISABLED_URL = f"{APP_NAME}:disabled_index"
ENABLE_URL = f"{APP_NAME}:enable"
GROUPS_URL = f"{APP_NAME}:groups"
DASHBOARD_URL = "users_module:index"

FILTER_FIELDS = {
    "nombre_departamento": {"label": _("Departamento"), "placeholder": _("Departamento")},
    "departamento_superior": {"label": _("Departamento superior")},
}

INDEX_FIELDS = {
    "nombre_departamento": _("Departamento"),
    "departamento_superior": _("Departamento superior"),
}

DETAIL_FIELDS = {
    "nombre_departamento": _("Nombre del departamento"),
    "departamento_superior": _("Departamento superior"),
}

CHILDREN_ENTITIES = {
    "puestos_departamentos": {"puesto": _("Puesto"), "is_jefe_departamento": _("¿Es jefe de departamento?")},
}

TABLE_TITLES = {
    "puestos_departamentos": _("Puestos"),
}

POSITION_FORMSET_CONFIG = {
    "title": _("Puestos"),
    "form": "PositionForm",  # String name to avoid circular import
    "prefix": "position",
    "related_name": "departamento",
}

# View titles
INDEX_TITLE = _("Departamentos")
CREATE_TITLE = _("Agregar departamento")
EDIT_TITLE = _("Editar departamento")
DETAIL_TITLE = _("Detalles del departamento")
DISABLED_INDEX_TITLE = _("Inventario de departamentos deshabilitados")
GROUPS_TITLE = _("Grupos del departamento")

# Field labels
DEPARTMENT_NAME_LABEL = _("Nombre del departamento")
PARENT_DEPARTMENT_LABEL = _("Departamento superior")
POSITION_LABEL = _("Puesto")
IS_DEPARTMENT_HEAD_LABEL = _("¿Es jefe de departamento?")
GROUPS_LABEL = _("Grupos")

# Placeholders
DEPARTMENT_NAME_PLACEHOLDER = DEPARTMENT_NAME_LABEL
EMPTY_SELECT_PLACEHOLDER = _("---------")

# Ordering
ORDERING = ["-id"]

# Context
CONTEXT_OBJECT_NAME = "department"

# Custom button title
CUSTOM_BUTTON_TITLE = _("Eliminar fila")

# Permissions
PERMISSION_VIEW = f"{APP_NAME}.view_{MODEL_NAME}"
PERMISSION_ADD = f"{APP_NAME}.add_{MODEL_NAME}"
PERMISSION_CHANGE = f"{APP_NAME}.change_{MODEL_NAME}"
PERMISSION_DELETE = f"{APP_NAME}.delete_{MODEL_NAME}"
PERMISSION_ENABLE = f"{APP_NAME}.enable_{MODEL_NAME}"
PERMISSION_ADD_GROUPS = f"{APP_NAME}.add_gruposdepartamento"
PERMISSION_VIEW_POSITION = "positions.view_puesto"

ERROR_AT_LEAST_ONE_BOSS = _("Debe haber al menos un jefe seleccionado.")
ERROR_SINGLE_BOSS = _("Solo puede haber un jefe por departamento.")
ERROR_BOSS_REQUIRED = _("Debe haber un jefe seleccionado.")
