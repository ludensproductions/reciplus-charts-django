from django.utils.translation import gettext_lazy as _

APP_NAME = "event_planner"
MODEL_NAME = "event"

# Model verbose names
EVENT_VERBOSE_NAME = _("Evento")
EVENT_VERBOSE_NAME_PLURAL = _("Eventos")
EVENT_ACTIVITY_VERBOSE_NAME = _("Actividad del Evento")
EVENT_ACTIVITY_VERBOSE_NAME_PLURAL = _("Actividades del Evento")
EVENT_ATTENDEE_VERBOSE_NAME = _("Asistente al Evento")
EVENT_ATTENDEE_VERBOSE_NAME_PLURAL = _("Asistentes al Evento")

# Field labels
EVENT_TITLE_LABEL = _("Título")
EVENT_DATE_START_LABEL = _("Fecha de inicio")
EVENT_LOCATION_LABEL = _("Ubicación")
EVENT_RESPONSIBLE_LABEL = _("Responsable")
EVENT_FOLIO_LABEL = _("Folio")
EVENT_ACTIVITY_LABEL = _("Actividad")
EVENT_ACTIVITY_CAPACITY_LABEL = _("Aforo")
EVENT_ACTIVITY_CODE_LABEL = _("Código")
ATTENDEE_FULL_NAME_LABEL = _("Nombre completo")
ATTENDEE_EMAIL_LABEL = _("Correo electrónico")
ATTENDEE_PHONE_LABEL = _("Teléfono")
ATTENDEE_NOTES_LABEL = _("Notas")

# Placeholders
EVENT_TITLE_PLACEHOLDER = _("Título del evento")
EVENT_LOCATION_PLACEHOLDER = EVENT_LOCATION_LABEL
EVENT_ACTIVITY_CAPACITY_PLACEHOLDER = EVENT_ACTIVITY_CAPACITY_LABEL
EVENT_ACTIVITY_CODE_PLACEHOLDER = EVENT_ACTIVITY_CODE_LABEL
ATTENDEE_FULL_NAME_PLACEHOLDER = ATTENDEE_FULL_NAME_LABEL
ATTENDEE_EMAIL_PLACEHOLDER = ATTENDEE_EMAIL_LABEL
ATTENDEE_PHONE_PLACEHOLDER = ATTENDEE_PHONE_LABEL
ATTENDEE_NOTES_PLACEHOLDER = ATTENDEE_NOTES_LABEL

# Display labels
ACTIVITY_LABEL_WITH_LOCATION = _("{name} - {location}")
CLONE_TITLE_PREFIX = _("Copia de ")
ACTIVITY_LABEL_WITH_PIPE = _("{name} | {location}")
RESPONSIBLE_LABEL_WITH_DASH = _("{first_name} - {last_name}")

# Display formats
RESPONSIBLE_DISPLAY_PIPE = _("{first_name} | {last_name}")
RESPONSIBLE_DISPLAY_COMMA = _("{first_name}, {last_name}")
EVENT_DISPLAY = _("{title} - {date}")
EVENT_ACTIVITY_DISPLAY = _("{event} - {activity} (aforo: {capacity})")
EVENT_ACTIVITIES_JOINER = _(" | ")
EVENT_ACTIVITY_INDEX_ITEM = _("{activity}, {location}")
VALUE_NOT_AVAILABLE = _("N/D")

INDEX_URL = f"{APP_NAME}:index"
CREATE_URL = f"{APP_NAME}:create"
EDIT_URL = f"{APP_NAME}:edit"
DELETE_URL = f"{APP_NAME}:delete"
DETAIL_URL = f"{APP_NAME}:detail"
DASHBOARD_URL = "catalogos:index"
EVENT_REGISTER_TO_EVENT_URL = f"{APP_NAME}:event-attendees"
EVENT_DOWNLOAD_MAP_URL = f"{APP_NAME}:download-map"
EVENT_CLONE_EVENT_URL = f"{APP_NAME}:clone-event"


INDEX_FIELDS = {
    "folio": _("Folio"),
    "title": _("Título"),
    "date_start": _("Fecha inicio"),
    "location": _("Ubicación"),
    "get_index_activities": _("Actividades"),
    "get_responsible_name_index": _("Responsable"),
}

DETAIL_FIELDS = {
    "folio": _("Folio"),
    "title": _("Título"),
    "date_start": _("Fecha inicio"),
    "location": _("Ubicación"),
    "get_index_activities": _("Actividades"),
    "get_responsible_name_index": _("Responsable"),
}

CHILDREN_ENTITIES = {
    "event_activities": {
        "activity": _("Nombre"),
        "capacity": _("Aforo"),
        "code": _("Código"),
    },
    "attendees": {
        "full_name": _("Nombre"),
        "email": _("Correo electrónico"),
        "phone": _("Teléfono"),
        "notes": _("Notas"),
    },
}

TABLE_TITLES = {
    "event_activities": _("Actividades"),
}

EVENT_ACTIVITY_FORMSET_CONFIG = {
    "title": _("Actividades"),
    "form": "EventActivityForm",
    "prefix": "activities",
    "related_name": "event",
}

# View Titles
INDEX_TITLE = _("Eventos")
CREATE_TITLE = _("Crear evento")
EDIT_TITLE = _("Editar evento")
DELETE_TITLE = _("Eliminar evento")
DETAIL_TITLE = _("Detalle del evento")
ATTENDEES_TITLE = _("Añadir asistentes al evento")
CLONE_TITLE = _("Clonar evento")

# Ordering
ORDERING = ["-id"]

# Custom button and form IDs
CUSTOM_BUTTON_TITLE = _("Eliminar fila")
FORM_ID = "form_id"

# Extra actions tooltips and icons
TOOLTIP_REGISTER_ATTENDEES = _("Registrar asistentes al evento")
TOOLTIP_DOWNLOAD_MAP = _("Descargar mapa del evento")
TOOLTIP_CLONE_EVENT = _("Clonar evento")
ICON_REGISTER_ATTENDEES = "fas fa-user-plus"
ICON_DOWNLOAD_MAP = "fas fa-map"
ICON_CLONE_EVENT = "fas fa-clone"
COLOR_INFO = "text-info"
COLOR_DANGER = "text-danger"
COLOR_PRIMARY = "text-primary"

# Formset prefixes
ATTENDEES_PREFIX = "attendees"
ATTENDEES_FORMSET_TITLE = _("Asistentes")
ACTIVITIES_FORMSET_TITLE = _("Actividades")

# PDF file paths
PDF_FILENAME = "map.pdf"
PDF_STATIC_PATH = "static/assets/pdfs/mapa.pdf"

# Form field names
FIELD_LOCATION = "location"
FIELD_PK = "pk"
FORMSET_KEY_ACTIVITIES = "activities"

# Error messages
ERROR_LOCATION_REQUIRED = _("La ubicación es obligatoria.")
ERROR_ACTIVITY_REQUIRED = _("Debe agregar al menos una actividad.")
ERROR_FIELD_REQUIRED = _("Este campo es requerido.")
ERROR_CODE_ALPHANUMERIC = _("El código debe ser alfanumérico.")
ERROR_ACTIVITY_CODE_DUPLICATE = _("Esta actividad ya tiene este código en el formulario.")
ERROR_CODE_DUPLICATE = _("El código ya está repetido en el formulario.")
ERROR_CODE_ALREADY_EXISTS = _("El código ya existe en otro registro.")

# Filter labels
FILTER_TITLE_LABEL = EVENT_TITLE_LABEL
FILTER_DATE_START_LABEL = _("Fecha inicio")
FILTER_LOCATION_LABEL = EVENT_LOCATION_LABEL
FILTER_ACTIVITY_CAPACITY_LABEL = EVENT_ACTIVITY_CAPACITY_LABEL
FILTER_ACTIVITY_NAME_LABEL = _("Nombre de actividad")
FILTER_ACTIVITY_LABEL = _("Actividad")
FILTER_ACTIVITY_TYPE_LABEL = _("Tipo actividad")
FILTER_RESPONSIBLE_LABEL = EVENT_RESPONSIBLE_LABEL
FILTER_FOLIO_LABEL = EVENT_FOLIO_LABEL

# Permissions
PERMISSION_VIEW = f"{APP_NAME}.view_{MODEL_NAME}"
PERMISSION_ADD = f"{APP_NAME}.add_{MODEL_NAME}"
PERMISSION_CHANGE = f"{APP_NAME}.change_{MODEL_NAME}"
PERMISSION_DELETE = f"{APP_NAME}.delete_{MODEL_NAME}"

# View types
VIEW_TYPE_CLONE = "clone"
from django.utils.translation import gettext_lazy as _

# Constantes para Event

EVENT_SHOWN_FIELDS = {
    "folio": _("Folio"),
    "title": _("Título"),
    "date_start": _("Fecha inicio"),
    "location": _("Ubicación"),
    "get_index_activities": _("Actividades"),
    "get_responsible_name_index": _("Responsable"),
}

EVENT_CREATE_URL = "event_planner:create"
EVENT_EDIT_URL = "event_planner:edit"
EVENT_DELETE_URL = "event_planner:delete"
EVENT_DETAIL_URL = "event_planner:detail"
EVENT_INDEX_URL = "event_planner:index"
EVENT_REGISTER_TO_EVENT_URL = "event_planner:event-attendees"
EVENT_DOWNLOAD_MAP_URL = "event_planner:download-map"
EVENT_CLONE_EVENT_URL = "event_planner:clone-event"

EVENT_CHILDREN_ENTITIES = {
    "event_activities": {
        "activity": _("Nombre"),
        "capacity": _("Aforo"),
        "code": _("Código"),
    },
    "attendees": {
        "full_name": _("Nombre"),
        "email": _("Email"),
        "phone": _("Teléfono"),
        "notes": _("Notas"),
    },
}

EVENT_TABLE_TITLE = {
    "event_activities": _("Actividades"),
}
