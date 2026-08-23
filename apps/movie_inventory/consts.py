from django.utils.translation import gettext_lazy as _

APP_NAME = "movie_inventory"

INDEX_URL = f"{APP_NAME}:index"
CREATE_URL = f"{APP_NAME}:create"
EDIT_URL = f"{APP_NAME}:edit"
DELETE_URL = f"{APP_NAME}:delete"
DETAIL_URL = f"{APP_NAME}:detail"
DISABLED_INDEX_URL = f"{APP_NAME}:disabled_index"
ENABLE_URL = f"{APP_NAME}:enable"
DASHBOARD_URL = "catalogos:index"

QUERY_FIELD = "created_by"

INDEX_FIELDS = {
    "movie_title": _("Título"),
    "productor": _("Productor"),
    "quantity": _("Cantidad"),
}

DETAIL_FIELDS = [
    "movie",
    "productor",
    "quantity",
    "email",
    "registration_date",
    "modification_date",
    "phone",
    "billing_file",
    "movie_cover",
]

SPECIAL_ATTRIBUTES = {
    "movie_cover": {
        "classes": "col-12 pb-4",
    }
}

# View titles
INDEX_TITLE = _("Inventario de películas")
CREATE_TITLE = _("Añadir inventario de película")
EDIT_TITLE = _("Editar inventario de película")
DETAIL_TITLE = _("Detalles del inventario de la película")
DISABLED_INDEX_TITLE = _("Inventario de películas deshabilitadas")

# Filter fields
FILTER_FIELDS = {"movie": _("Película")}

# Ordering
ORDERING = ["-id"]

# Permissions
PERMISSION_VIEW = f"{APP_NAME}.view_movieinventory"
PERMISSION_ADD = f"{APP_NAME}.add_movieinventory"
PERMISSION_CHANGE = f"{APP_NAME}.change_movieinventory"
PERMISSION_DELETE = f"{APP_NAME}.delete_movieinventory"
PERMISSION_ENABLE = f"{APP_NAME}.enable_movieinventory"

# Form labels and messages
ERROR_DUPLICATE_MOVIE_INVENTORY = _("Ya existe un inventario para esta película.")
SUCCESS_MOVIE_INVENTORY_ENABLED = _("Inventario habilitado correctamente.")

# Model verbose names
MODEL_MOVIE_INVENTORY_VERBOSE_NAME = _("Inventario de película")
MODEL_MOVIE_INVENTORY_VERBOSE_NAME_PLURAL = _("Inventarios de películas")

# Field labels
FIELD_MOVIE_LABEL = _("Película")
FIELD_PRODUCTOR_LABEL = _("Productor")
FIELD_QUANTITY_LABEL = _("Cantidad")
FIELD_EMAIL_LABEL = _("Correo electrónico")
FIELD_PASSWORD_LABEL = _("Contraseña")
FIELD_REGISTRATION_DATE_LABEL = _("Fecha de registro")
FIELD_MODIFICATION_DATE_LABEL = _("Fecha de modificación")
FIELD_PHONE_LABEL = _("Teléfono")
FIELD_BILLING_FILE_LABEL = _("Archivo de facturación")
FIELD_MOVIE_COVER_LABEL = _("Portada de la película")
FIELD_JUSTIFICATION_LABEL = _("Justificación")

# Validation messages
ERROR_PASSWORD_COMPLEXITY = _(
    "La contraseña debe contener al menos un caracter especial, un número, una letra mayúscula, "
    "una letra minúscula y tener al menos 10 caracteres de longitud."
)
ERROR_REGISTRATION_DATE_REQUIRED_BEFORE_MODIFICATION = _(
    "Debe proporcionar una fecha de registro antes de establecer una fecha de modificación."
)
ERROR_MODIFICATION_DATE_BEFORE_REGISTRATION = _("La fecha de modificación no puede ser menor a la fecha de registro.")
ERROR_PHONE_INVALID_LENGTH = _("El número de teléfono debe tener 10 dígitos.")
ERROR_BILLING_FILE_REQUIRED = _("Este campo es requerido.")
ERROR_BILLING_FILE_EXTENSION = _("El archivo de facturación debe ser un archivo pdf o zip.")
ERROR_MOVIE_COVER_REQUIRED = _("Este campo es requerido.")
ERROR_MOVIE_COVER_EXTENSION = _("La portada de la película debe ser un archivo png o jpg.")

# Form labels and placeholders
FORM_MOVIE_LABEL = _("Película")
FORM_PRODUCTOR_LABEL = _("Productor")
FORM_QUANTITY_LABEL = _("Cantidad")
FORM_EMAIL_LABEL = _("Correo")
FORM_PASSWORD_LABEL = _("Contraseña")
FORM_REGISTRATION_DATE_LABEL = _("Fecha de registro")
FORM_MODIFICATION_DATE_LABEL = _("Fecha de modificación")
FORM_PHONE_LABEL = _("Teléfono")
FORM_BILLING_FILE_LABEL = _("Archivo de facturación")
FORM_MOVIE_COVER_LABEL = _("Portada de la película")
FORM_CURP_LABEL = _("CURP")
FORM_RFC_LABEL = _("RFC")
FORM_MOVIE_LABEL_FORMAT = _("{year} - {title}")
FORM_CURP_PLACEHOLDER = _("CURP")
FORM_RFC_PLACEHOLDER = _("RFC")
FORM_JUSTIFICATION_LABEL = _("Justificación")
FORM_JUSTIFICATION_PLACEHOLDER = _("Agregar justificación...")
