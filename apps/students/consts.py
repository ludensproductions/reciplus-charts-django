from django.utils.text import format_lazy
from django.utils.translation import gettext_lazy as _

# Base identifiers
APP_NAME = "students"
MODEL_NAME = "student"
MODULE_VERBOSE_NAME = _("Estudiantes")
MODULE_VERBOSE_NAME_SINGULAR = _("Estudiante")

# Permissions (built from APP_NAME and MODEL_NAME)
PERMISSION_VIEW = f"{APP_NAME}.view_{MODEL_NAME}"
PERMISSION_ADD = f"{APP_NAME}.add_{MODEL_NAME}"
PERMISSION_CHANGE = f"{APP_NAME}.change_{MODEL_NAME}"
PERMISSION_DELETE = f"{APP_NAME}.delete_{MODEL_NAME}"

# Navigation URLs
INDEX_URL = f"{APP_NAME}:index"
CREATE_URL = f"{APP_NAME}:create"
EDIT_URL = f"{APP_NAME}:edit"
DELETE_URL = f"{APP_NAME}:delete"
DETAIL_URL = f"{APP_NAME}:detail"
DISABLED_INDEX_URL = f"{APP_NAME}:disabled_index"
ENABLE_URL = f"{APP_NAME}:enable"
DASHBOARD_URL = "catalogos:index"

# Fields shown in views
INDEX_FIELDS = ["name", "last_name", "email", "phone", "address"]

DETAIL_FIELDS = ["name", "last_name", "email", "phone", "address", "image"]

# View titles
INDEX_TITLE = MODULE_VERBOSE_NAME
CREATE_TITLE = format_lazy(_("Crear {module_verbose}"), module_verbose=MODULE_VERBOSE_NAME_SINGULAR)
EDIT_TITLE = format_lazy(_("Editar {module_verbose}"), module_verbose=MODULE_VERBOSE_NAME_SINGULAR)
DETAIL_TITLE = format_lazy(_("Detalles del {module_verbose}"), module_verbose=MODULE_VERBOSE_NAME_SINGULAR)

# Default ordering
DEFAULT_ORDERING = ["name"]

# API tags and paths
API_TAG = MODULE_VERBOSE_NAME
API_PATH = f"/{APP_NAME}"

# API descriptions
API_CREATE_SUMMARY = format_lazy(
    _("Crear un nuevo {module_verbose}"),
    module_verbose=MODULE_VERBOSE_NAME_SINGULAR,
)
API_CREATE_DESCRIPTION = format_lazy(
    _("Crear un nuevo {module_verbose}"),
    module_verbose=MODULE_VERBOSE_NAME_SINGULAR,
)

# Model labels
STUDENT_NAME_LABEL = _("Nombre")
STUDENT_LAST_NAME_LABEL = _("Apellido")
STUDENT_EMAIL_LABEL = _("Correo electrónico")
STUDENT_PHONE_LABEL = _("Teléfono")
STUDENT_ADDRESS_LABEL = _("Dirección")
STUDENT_IMAGE_LABEL = _("Imagen")
STUDENT_COURSES_LABEL = _("Cursos")
COURSE_LABEL = _("Curso")
STUDENT_GRADE_LABEL = _("Calificación")

# Filter labels
STUDENT_NAME_FILTER_LABEL = STUDENT_NAME_LABEL
STUDENT_LAST_NAME_FILTER_LABEL = STUDENT_LAST_NAME_LABEL
STUDENT_EMAIL_FILTER_LABEL = STUDENT_EMAIL_LABEL
STUDENT_PHONE_FILTER_LABEL = STUDENT_PHONE_LABEL
STUDENT_ADDRESS_FILTER_LABEL = STUDENT_ADDRESS_LABEL

# Model verbose names
STUDENT_MODEL_VERBOSE_NAME = MODULE_VERBOSE_NAME_SINGULAR
STUDENT_MODEL_VERBOSE_NAME_PLURAL = MODULE_VERBOSE_NAME
STUDENT_COURSE_MODEL_VERBOSE_NAME = _("Curso de estudiante")
STUDENT_COURSE_MODEL_VERBOSE_NAME_PLURAL = _("Cursos de estudiantes")
