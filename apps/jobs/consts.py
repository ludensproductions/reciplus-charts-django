from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _

APP_NAME = "jobs"
MODEL_NAME = "job"

INDEX_URL = f"{APP_NAME}:index"
CREATE_URL = f"{APP_NAME}:create"
DELETE_URL = f"{APP_NAME}:delete"
DETAIL_URL = f"{APP_NAME}:detail"
EDIT_URL = f"{APP_NAME}:edit"
RETURN_URL = "catalogos:index"

INDEX_TITLE = _("Trabajos")
CREATE_TITLE = _("Crear trabajo")
EDIT_TITLE = _("Editar trabajo")
DETAIL_TITLE = _("Detalles del trabajo")


# Model verbose names
MODEL_JOB_VERBOSE_NAME = _("Trabajo")
MODEL_JOB_VERBOSE_NAME_PLURAL = _("Trabajos")

# Field labels
FIELD_TITLE_LABEL = _("Título")
FIELD_COMPANY_LABEL = _("Compañía")
FIELD_LOCATION_LABEL = _("Ubicación")
FIELD_JOB_TYPE_LABEL = _("Tipo de trabajo")
FIELD_MIN_SALARY_LABEL = _("Salario mínimo")
FIELD_MAX_SALARY_LABEL = _("Salario máximo")
FIELD_IS_REMOTE_LABEL = _("Es remoto")
FIELD_IS_ACTIVE_LABEL = _("Está activo")

# Fields
INDEX_FIELDS = {
    "title": FIELD_TITLE_LABEL,
    "company": FIELD_COMPANY_LABEL,
    "location": FIELD_LOCATION_LABEL,
    "job_type": FIELD_JOB_TYPE_LABEL,
    "min_salary": FIELD_MIN_SALARY_LABEL,
    "max_salary": FIELD_MAX_SALARY_LABEL,
    "is_remote": FIELD_IS_REMOTE_LABEL,
    "is_active": FIELD_IS_ACTIVE_LABEL,
}

DETAIL_FIELDS = INDEX_FIELDS.copy()

FILTER_FIELDS = INDEX_FIELDS.copy()

# Ordering
ORDERING = ["-id"]

# Permissions
VIEW_PERMISSION = "jobs.view_job"
ADD_PERMISSION = "jobs.add_job"
CHANGE_PERMISSION = "jobs.change_job"
DELETE_PERMISSION = "jobs.delete_job"


class JobTypes(TextChoices):
    """Define job type choices."""

    FULL_TIME = ("FT", _("Tiempo completo"))
    PART_TIME = ("PT", _("Medio tiempo"))
    CONTRACT = ("CT", _("Contrato"))


COMPANY_BLACKLIST = {"EvilCorp", "FakeJobs Inc."}
ACTIVE_JOB_COMPANY_RESTRICTION_VALUE = "Acme"
VALID_REMOTE_LOCATION_VALUES = {"remote", "remoto", "home office"}

# API configuration
API_JOBS_PATH = "/jobs"
API_JOBS_TAG = _("Trabajos")

# Validation messages
ERROR_SALARY_RANGE_INVALID = _("El salario mínimo no puede ser mayor que el máximo.")
ERROR_REMOTE_LOCATION_INVALID = _("Los trabajos remotos deben tener ubicación 'Remoto'.")
ERROR_COMPANY_INACTIVE_RESTRICTION = _("La compañía 'Acme' no puede publicar trabajos inactivos.")
ERROR_TITLE_INVALID = _("El título debe tener al menos 5 caracteres y contener un espacio.")
ERROR_COMPANY_NOT_ALLOWED = _("Esta compañía no está permitida.")

# Form labels and placeholders
FORM_TITLE_LABEL = FIELD_TITLE_LABEL
FORM_COMPANY_LABEL = FIELD_COMPANY_LABEL
FORM_LOCATION_LABEL = FIELD_LOCATION_LABEL
FORM_JOB_TYPE_LABEL = FIELD_JOB_TYPE_LABEL
FORM_MIN_SALARY_LABEL = FIELD_MIN_SALARY_LABEL
FORM_MAX_SALARY_LABEL = FIELD_MAX_SALARY_LABEL
FORM_IS_REMOTE_LABEL = FIELD_IS_REMOTE_LABEL
FORM_IS_ACTIVE_LABEL = FIELD_IS_ACTIVE_LABEL
FORM_TITLE_PLACEHOLDER = FIELD_TITLE_LABEL
FORM_COMPANY_PLACEHOLDER = FIELD_COMPANY_LABEL
FORM_LOCATION_PLACEHOLDER = FIELD_LOCATION_LABEL
FORM_JOB_TYPE_PLACEHOLDER = FIELD_JOB_TYPE_LABEL
FORM_MIN_SALARY_PLACEHOLDER = FIELD_MIN_SALARY_LABEL
FORM_MAX_SALARY_PLACEHOLDER = FIELD_MAX_SALARY_LABEL
