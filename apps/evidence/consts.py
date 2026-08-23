from django.utils.text import format_lazy
from django.utils.translation import gettext_lazy as _

# Base identifiers
APP_NAME = "evidence"
MODEL_NAME = "evidence"
MODULE_VERBOSE_NAME = _("Evidencia")
MODULE_VERBOSE_NAME_PLURAL = _("Evidencias")

# Model verbose names
MODEL_VERBOSE_NAME = MODULE_VERBOSE_NAME
MODEL_VERBOSE_NAME_PLURAL = MODULE_VERBOSE_NAME_PLURAL

# Navigation URLs (built from APP_NAME)
INDEX_URL = f"{APP_NAME}:index"
CREATE_URL = f"{APP_NAME}:create"
EDIT_URL = f"{APP_NAME}:edit"
DELETE_URL = f"{APP_NAME}:delete"
DETAIL_URL = f"{APP_NAME}:detail"
DASHBOARD_URL = "catalogos:index"
DISABLED_INDEX_URL = f"{APP_NAME}:disabled_index"
ENABLE_URL = f"{APP_NAME}:enable"

# Field labels
CASE_NAME_LABEL = _("Nombre del caso")
TEXT_FILE_EVIDENCE_LABEL = _("Archivo TXT")
CSV_FILE_EVIDENCE_LABEL = _("Archivo CSV")
LOG_FILE_EVIDENCE_LABEL = _("Archivo LOG")
PDF_FILE_EVIDENCE_LABEL = _("Archivo PDF")
DOC_FILE_EVIDENCE_LABEL = _("Archivo DOC")
DOCX_FILE_EVIDENCE_LABEL = _("Archivo DOCX")
ODT_FILE_EVIDENCE_LABEL = _("Archivo ODT")
XLS_FILE_EVIDENCE_LABEL = _("Archivo XLS")
XLSX_FILE_EVIDENCE_LABEL = _("Archivo XLSX")
ODS_FILE_EVIDENCE_LABEL = _("Archivo ODS")
PPT_FILE_EVIDENCE_LABEL = _("Archivo PPT")
PPTX_FILE_EVIDENCE_LABEL = _("Archivo PPTX")
ODP_FILE_EVIDENCE_LABEL = _("Archivo ODP")
JPG_FILE_EVIDENCE_LABEL = _("Archivo JPG")
JPEG_FILE_EVIDENCE_LABEL = _("Archivo JPEG")
PNG_FILE_EVIDENCE_LABEL = _("Archivo PNG")
GIF_FILE_EVIDENCE_LABEL = _("Archivo GIF")
BMP_FILE_EVIDENCE_LABEL = _("Archivo BMP")
WEBP_FILE_EVIDENCE_LABEL = _("Archivo WEBP")
ZIP_FILE_EVIDENCE_LABEL = _("Archivo ZIP")
RAR_FILE_EVIDENCE_LABEL = _("Archivo RAR")
SEVENZIP_FILE_EVIDENCE_LABEL = _("Archivo 7Z")
MISC_FILE_EVIDENCE_LABEL = _("Archivo misceláneo")

# Form labels
CASE_NAME_PLACEHOLDER = CASE_NAME_LABEL
TEXT_FILE_EVIDENCE_FORM_LABEL = _("Evidencia en texto")
CSV_FILE_EVIDENCE_FORM_LABEL = _("Evidencia en CSV")
LOG_FILE_EVIDENCE_FORM_LABEL = _("Evidencia en LOG")
PDF_FILE_EVIDENCE_FORM_LABEL = _("Evidencia en PDF")
DOC_FILE_EVIDENCE_FORM_LABEL = _("Evidencia en DOC")
DOCX_FILE_EVIDENCE_FORM_LABEL = _("Evidencia en DOCX")
ODT_FILE_EVIDENCE_FORM_LABEL = _("Evidencia en ODT")
XLS_FILE_EVIDENCE_FORM_LABEL = _("Evidencia en XLS")
XLSX_FILE_EVIDENCE_FORM_LABEL = _("Evidencia en XLSX")
ODS_FILE_EVIDENCE_FORM_LABEL = _("Evidencia en ODS")
PPT_FILE_EVIDENCE_FORM_LABEL = _("Evidencia en PPT")
PPTX_FILE_EVIDENCE_FORM_LABEL = _("Evidencia en PPTX")
ODP_FILE_EVIDENCE_FORM_LABEL = _("Evidencia en ODP")
JPG_FILE_EVIDENCE_FORM_LABEL = _("Evidencia en JPG")
JPEG_FILE_EVIDENCE_FORM_LABEL = _("Evidencia en JPEG")
PNG_FILE_EVIDENCE_FORM_LABEL = _("Evidencia en PNG")
GIF_FILE_EVIDENCE_FORM_LABEL = _("Evidencia en GIF")
BMP_FILE_EVIDENCE_FORM_LABEL = _("Evidencia en BMP")
WEBP_FILE_EVIDENCE_FORM_LABEL = _("Evidencia en WEBP")
ZIP_FILE_EVIDENCE_FORM_LABEL = _("Archivo comprimido ZIP")
RAR_FILE_EVIDENCE_FORM_LABEL = _("Archivo comprimido RAR")
SEVENZIP_FILE_EVIDENCE_FORM_LABEL = _("Archivo comprimido 7Z")

# Fields shown in views
INDEX_FIELDS = {
    "case_name": CASE_NAME_LABEL,
}

# Filter fields
FILTER_FIELDS = {
    "case_name": {"label": CASE_NAME_LABEL, "placeholder": CASE_NAME_LABEL},
}

# View titles (used in CRUD)
INDEX_TITLE = MODULE_VERBOSE_NAME_PLURAL
CREATE_TITLE = format_lazy(_("Crear {module_verbose}"), module_verbose=MODULE_VERBOSE_NAME)
EDIT_TITLE = format_lazy(_("Editar {module_verbose}"), module_verbose=MODULE_VERBOSE_NAME)
DETAIL_TITLE = format_lazy(_("Detalles de la {module_verbose}"), module_verbose=MODULE_VERBOSE_NAME)

# Default ordering
DEFAULT_ORDERING = ["-id"]

# Permissions (built from APP_NAME and MODEL_NAME)
PERMISSION_VIEW = f"{APP_NAME}.view_{MODEL_NAME}"
PERMISSION_ADD = f"{APP_NAME}.add_{MODEL_NAME}"
PERMISSION_CHANGE = f"{APP_NAME}.change_{MODEL_NAME}"
PERMISSION_DELETE = f"{APP_NAME}.delete_{MODEL_NAME}"
