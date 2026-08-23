from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _

APP_NAME = "reservations"
MODEL_NAME = "reservation"
MODULE_VERBOSE_NAME = _("Reservaciones")

INDEX_URL = f"{APP_NAME}:index"
CREATE_URL = f"{APP_NAME}:create"
EDIT_URL = f"{APP_NAME}:edit"
DELETE_URL = f"{APP_NAME}:delete"
DETAIL_URL = f"{APP_NAME}:detail"
DASHBOARD_URL = "catalogos:index"

# Permissions
PERMISSION_VIEW = f"{APP_NAME}.view_{MODEL_NAME}"
PERMISSION_ADD = f"{APP_NAME}.add_{MODEL_NAME}"
PERMISSION_CHANGE = f"{APP_NAME}.change_{MODEL_NAME}"
PERMISSION_DELETE = f"{APP_NAME}.delete_{MODEL_NAME}"

# Titles
INDEX_TITLE = MODULE_VERBOSE_NAME
CREATE_TITLE = _("Crear reservación")
EDIT_TITLE = _("Editar reservación")
DETAIL_TITLE = _("Detalles de la reservación")
DISABLED_INDEX_TITLE = _("Reservaciones deshabilitadas")

# Default ordering
DEFAULT_ORDERING = ["-id"]

# Field labels (reusable strings)
RESERVADOR = _("Reservador")
FECHA_INICIO_CANCELACION = _("Fecha de inicio de cancelación")
FECHA_FIN_CANCELACION = _("Fecha de fin de cancelación")
TIEMPO_CANCELACION = _("Tiempo de cancelación")
FECHA_HORA_LLEGADA = _("Fecha y hora de llegada")
FECHAS_RESERVACION = _("Fechas de reservación")
RANGO = _("Rango")
CANCELACION_INICIO = _("Cancelación inicio")
CANCELACION_FIN = _("Cancelación fin")
CARGO_EXTRA = _("Cargo extra")
PUNTOS_PROMOCION = _("Puntos de promoción")
TIPO_RESERVACION = _("Tipo de reservación")
TIEMPO_LIMITE_CANCELACION = _("Tiempo límite de cancelación")

# Reservation type labels
RESERVATION_TYPE_STANDARD_LABEL = _("Estándar")
RESERVATION_TYPE_UNEXPECTED_LABEL = _("Sin anticipación")

# Placeholders
PLACEHOLDER_NOMBRE_RESERVADOR = _("Nombre del reservador")

# Validation messages
ERROR_CANCEL_START_AFTER_END = _("La fecha de inicio de cancelación no puede ser posterior a la fecha de fin.")

INDEX_FIELDS = {
    "guest": RESERVADOR,
    "cancel_start": FECHA_INICIO_CANCELACION,
    "cancel_end": FECHA_FIN_CANCELACION,
    "cancel_time": TIEMPO_CANCELACION,
    "scheduled_arrive": FECHA_HORA_LLEGADA,
}

DISABLED_INDEX_FIELDS = {
    "guest": RESERVADOR,
    "booking_range": FECHAS_RESERVACION,
    "cancel_start": FECHA_INICIO_CANCELACION,
    "cancel_end": FECHA_FIN_CANCELACION,
    "scheduled_arrive": FECHA_HORA_LLEGADA,
}

DETAIL_FIELDS = {
    "guest": RESERVADOR,
    "booking_range": RANGO,
    "cancel_start": CANCELACION_INICIO,
    "cancel_end": CANCELACION_FIN,
    "cancel_time": TIEMPO_CANCELACION,
    "scheduled_arrive": FECHA_HORA_LLEGADA,
    "extra_fee": CARGO_EXTRA,
    "promotion_points": PUNTOS_PROMOCION,
}

FILTER_FIELDS = {
    "guest": {"label": RESERVADOR, "placeholder": RESERVADOR},
}

# Field attributes for formatting
FIELD_ATTRIBUTES = {
    "cancel_start": {
        "format": "d-m-Y",
    },
    "cancel_end": {
        "format": "j F Y",
    },
    "scheduled_arrive": {
        "format": "d/m/Y H:i",
    },
    "booking_range": {
        "format": "d M Y",  # applies to both lower/upper
        "separator": "|",
    },
    "cancel_time": {
        "format": "H:i",
    },
}

# Custom JS files
RESERVATION_FORM_JS = ["assets/js/events/examples/reservation_events.js"]

# Context object name
CONTEXT_OBJECT_NAME = "reservation"

# Custom button title for form
CUSTOM_BUTTON_TITLE = _("Eliminar fila")

# Filter labels
RESERVATION_FILTER_FIELDS = {
    "guest": {"label": RESERVADOR},
    "booking_range": {"label": FECHAS_RESERVACION},
    "cancel_start": {"label": FECHA_INICIO_CANCELACION},
    "cancel_end": {"label": FECHA_FIN_CANCELACION},
    "scheduled_arrive": {"label": FECHA_HORA_LLEGADA},
}


class ReservationTypes(TextChoices):
    """Define reservation type choices for bookings."""

    STANDARD = "standard", RESERVATION_TYPE_STANDARD_LABEL
    UNEXPECTED = "unexpected", RESERVATION_TYPE_UNEXPECTED_LABEL


# Model labels and verbose names
MODEL_RESERVATION_VERBOSE_NAME = _("Reservación")
MODEL_RESERVATION_VERBOSE_NAME_PLURAL = MODULE_VERBOSE_NAME
MODEL_GUEST_LABEL = RESERVADOR
MODEL_SCHEDULED_ARRIVE_LABEL = FECHA_HORA_LLEGADA
MODEL_RESERVATION_TYPE_LABEL = TIPO_RESERVACION
MODEL_EXTRA_FEE_LABEL = CARGO_EXTRA
MODEL_PROMOTION_POINTS_LABEL = PUNTOS_PROMOCION
MODEL_BOOKING_RANGE_LABEL = FECHAS_RESERVACION
MODEL_CANCEL_START_LABEL = _("Inicio de cancelación")
MODEL_CANCEL_END_LABEL = _("Fin de cancelación")
MODEL_CANCEL_TIME_LABEL = TIEMPO_LIMITE_CANCELACION


SPECIAL_ATTRIBUTES = {
    "cancel_start": {
        "format": "d-m-Y",
    },
    "cancel_end": {
        "format": "j F Y",
    },
    "scheduled_arrive": {
        "format": "d/m/Y H:i",
    },
    "booking_range": {
        "format": "d M Y",  # applies to both lower/upper
    },
}
