from django.utils.translation import gettext_lazy as _

# Error messages
ERROR_INVALID_IMAGE = _(
    "Sube una imagen con extensión válida: jpg, jpeg, png, svg. "
    "El archivo que cargó no era una imagen o estaba corrupta"
)
ERROR_INVALID_IMAGE_EXTENSION = _(
    'La extensión de archivo "%(extension)s" no está permitida. '
    "Las extensiones permitidas son: %(allowed_extensions)s."
)
ERROR_INVALID_EMAIL = _("Ingrese un correo electrónico válido")
ERROR_PASSWORD_FIELDS_REQUIRED = _("Debe completar ambos campos de contraseña")
ERROR_PASSWORD_MISMATCH = _("Las contraseñas no coinciden")
ERROR_PASSWORD_MIN_LENGTH = _("La contraseña debe tener al menos 8 caracteres")
ERROR_PASSWORD_SPECIAL_CHAR = _('La contraseña debe contener al menos un carácter especial (!@#$%^&*(),.?":{}|<>)')
ERROR_USERNAME_TAKEN = _("Este nombre de usuario ya está en uso")
ERROR_EMAIL_TAKEN = _("Este correo electrónico ya está registrado")
ERROR_USER_EMAIL_EXISTS = _("Ya existe un usuario con este correo")
ERROR_INVALID_POSTAL_CODE = _("Código postal inválido")
ERROR_INVALID_MUNICIPIO = _("Municipio inválido")

# App configuration
APP_NAME = "users"

# URLs
INDEX_URL = f"{APP_NAME}:index"
CREATE_URL = f"{APP_NAME}:create"
DELETE_URL = f"{APP_NAME}:delete"
EDIT_URL = f"{APP_NAME}:edit"
GROUPS_URL = f"{APP_NAME}:groups"
BAN_URL = f"{APP_NAME}:ban"
RETURN_URL = "users_module:index"

# Fields
INDEX_FIELDS = {
    "username": _("Nombre de usuario"),
    "first_name": _("Nombre"),
    "departamento": _("Departamento"),
    "puesto": _("Puesto"),
}

FILTER_FIELDS = {
    "username": {"label": _("Nombre de usuario"), "placeholder": _("Nombre de usuario")},
    "first_name": {"label": _("Nombre"), "placeholder": _("Nombre")},
    "departamento": {"label": _("Departamento")},
    "puesto": {"label": _("Puesto")},
}

# Permissions
VIEW_PERMISSION = "users.view_user"
ADD_PERMISSION = "users.add_user"
CHANGE_PERMISSION = "users.change_user"
DELETE_PERMISSION = "users.delete_user"
ADD_GROUP_PERMISSION = "users.add_usergroup"
BAN_PERMISSION = "users.ban_user"

# View titles
INDEX_TITLE = _("Usuarios")
CREATE_TITLE = _("Agregar usuario")
EDIT_TITLE = _("Editar usuario")
GROUPS_TITLE = _("Grupos del usuario")

# Ordering
ORDERING = ["-id"]

# Model verbose names
MODEL_USER_VERBOSE_NAME = _("Usuario")
MODEL_USER_VERBOSE_NAME_PLURAL = _("Usuarios")
MODEL_RESPONSIVA_VERBOSE_NAME = _("Responsiva")
MODEL_RESPONSIVA_VERBOSE_NAME_PLURAL = _("Responsivas")
MODEL_PAIS_VERBOSE_NAME = _("País")
MODEL_PAIS_VERBOSE_NAME_PLURAL = _("Países")
MODEL_ESTADO_VERBOSE_NAME = _("Estado")
MODEL_ESTADO_VERBOSE_NAME_PLURAL = _("Estados")
MODEL_DOMICILIO_VERBOSE_NAME = _("Domicilio")
MODEL_DOMICILIO_VERBOSE_NAME_PLURAL = _("Domicilios")
MODEL_MUNICIPIO_VERBOSE_NAME = _("Municipio")
MODEL_MUNICIPIO_VERBOSE_NAME_PLURAL = _("Municipios")
MODEL_CODIGO_POSTAL_VERBOSE_NAME = _("Código postal")
MODEL_CODIGO_POSTAL_VERBOSE_NAME_PLURAL = _("Códigos postales")
MODEL_USER_GROUP_VERBOSE_NAME = _("Grupo de usuario")
MODEL_USER_GROUP_VERBOSE_NAME_PLURAL = _("Grupos de usuario")

# Field labels
FIELD_FIRST_NAME_LABEL = _("Nombre")
FIELD_LAST_NAME_LABEL = _("Apellido paterno")
FIELD_SECOND_LAST_NAME_LABEL = _("Apellido materno")
FIELD_IMAGE_LABEL = _("Imagen")
FIELD_DEPARTAMENTO_LABEL = _("Departamento")
FIELD_PUESTO_LABEL = _("Puesto")
FIELD_WORK_PHONE_LABEL = _("Teléfono del trabajo")
FIELD_MOBILE_PHONE_LABEL = _("Celular")
FIELD_CITY_LABEL = _("Ciudad")
FIELD_STATE_LABEL = _("Estado")
FIELD_COUNTRY_LABEL = _("País")
FIELD_ADDRESS_LABEL = _("Dirección")
FIELD_DARK_MODE_LABEL = _("Modo oscuro")
FIELD_DOMICILIO_LABEL = _("Domicilio")
FIELD_EMAIL_LABEL = _("Correo electrónico")
FIELD_USER_LABEL = _("Usuario")
FIELD_RESPONSIVA_FILE_LABEL = _("Archivo de responsiva")
FIELD_PAIS_LABEL = _("País")
FIELD_CLAVE_LABEL = _("Clave")
FIELD_ESTADO_LABEL = _("Estado")
FIELD_MUNICIPIO_LABEL = _("Municipio")
FIELD_COLONIA_LABEL = _("Colonia")
FIELD_CODIGO_POSTAL_LABEL = _("Código postal")
FIELD_CALLE_LABEL = _("Calle")
FIELD_NUMERO_EXTERIOR_LABEL = _("Número exterior")
FIELD_NUMERO_INTERIOR_LABEL = _("Número interior")
FIELD_GRUPO_LABEL = _("Grupo")

# Form labels and placeholders
FORM_PROFILE_EMAIL_LABEL_HTML = _("<b>Correo electrónico</b>")
FORM_PROFILE_PASSWORD_LABEL_HTML = _("<b>Contraseña</b>")
FORM_PROFILE_PASSWORD_CONFIRM_LABEL_HTML = _("<b>Confirmar contraseña</b>")
FORM_PROFILE_PASSWORD_LABEL = _("Contraseña")
FORM_PROFILE_PASSWORD_PLACEHOLDER = _("Contraseña")
FORM_PROFILE_PASSWORD_CONFIRM_LABEL = _("Confirmar contraseña")
FORM_PROFILE_PASSWORD_CONFIRM_PLACEHOLDER = _("Confirmar contraseña")
FORM_PROFILE_EMAIL_PLACEHOLDER = _("Correo electrónico")

FORM_NEW_USER_EMAIL_PLACEHOLDER = _("Correo electrónico")
FORM_NEW_USER_USERNAME_PLACEHOLDER = _("Nombre de usuario")
FORM_NEW_USER_PASSWORD_LABEL = _("Contraseña")
FORM_NEW_USER_PASSWORD_PLACEHOLDER = _("Contraseña")
FORM_NEW_USER_PASSWORD_CONFIRM_LABEL = _("Confirmar contraseña")
FORM_NEW_USER_FIRST_NAME_PLACEHOLDER = _("Nombre")
FORM_NEW_USER_LAST_NAME_PLACEHOLDER = _("Apellido")

FORM_USER_HAS_DOMICILE_LABEL = _("Tiene domicilio")
FORM_USER_FIRST_NAME_LABEL = _("Nombres")
FORM_USER_LAST_NAME_LABEL = _("Apellido paterno")
FORM_USER_SECOND_LAST_NAME_LABEL = _("Apellido materno")
FORM_USER_EMAIL_LABEL = _("Correo electrónico")
FORM_USER_MOBILE_LABEL = _("Celular")
FORM_USER_WORK_PHONE_LABEL = _("Teléfono de trabajo")
FORM_USER_DEPARTAMENTO_LABEL = _("Departamento")
FORM_USER_PUESTO_LABEL = _("Puesto")

FORM_DOMICILIO_ESTADO_LABEL = _("Estado")
FORM_DOMICILIO_MUNICIPIO_LABEL = _("Municipio")
FORM_DOMICILIO_COLONIA_LABEL = _("Colonia")
FORM_DOMICILIO_CODIGO_POSTAL_LABEL = _("Código Postal")
FORM_DOMICILIO_CALLE_LABEL = _("Calle")
FORM_DOMICILIO_NUMERO_EXTERIOR_LABEL = _("Número exterior")
FORM_DOMICILIO_NUMERO_INTERIOR_LABEL = _("Número interior")
FORM_DOMICILIO_COLONIA_PLACEHOLDER = _("Colonia")
FORM_DOMICILIO_CALLE_PLACEHOLDER = _("Calle")
FORM_DOMICILIO_NUMERO_EXTERIOR_PLACEHOLDER = _("Número exterior")
FORM_DOMICILIO_NUMERO_INTERIOR_PLACEHOLDER = _("Número interior")

FORM_GROUPS_LABEL = _("Grupos")
FORM_GROUPS_PLACEHOLDER = _("Seleccionar")

# Messages
PROFILE_SUCCESSFUL_UPDATE_MESSAGE = _("¡Perfil actualizado exitosamente!")
ERROR_USER_DELETED = _("El usuario ha sido eliminado.")
ERROR_USER_INACTIVE = _("El usuario está inactivo.")
ERROR_USER_BANNED = _("Tu cuenta ha sido suspendida. No es posible iniciar sesión.")
SUCCESS_USER_BANNED = _("Usuario baneado exitosamente.")
SUCCESS_USER_UNBANNED = _("Usuario desbaneado exitosamente.")

# Password Reset
FORGOT_PASSWORD_TITLE = _("¿Olvidaste tu contraseña?")
FORGOT_PASSWORD_SUBTITLE = _("Ingresa tu correo electrónico y te enviaremos un enlace para restablecer tu contraseña.")
FORGOT_PASSWORD_EMAIL_PLACEHOLDER = _("Ingresa tu correo electrónico")
FORGOT_PASSWORD_SUCCESS_TITLE = _("Correo enviado")
FORGOT_PASSWORD_SUCCESS_MESSAGE = _(
    "Si existe una cuenta con ese correo electrónico, recibirás un enlace para restablecer tu contraseña."
)
PASSWORD_RESET_TITLE = _("Restablecer contraseña")
PASSWORD_RESET_COMPLETE_TITLE = _("Contraseña restablecida")
PASSWORD_RESET_COMPLETE_MESSAGE = _("Tu contraseña ha sido restablecida exitosamente. Ya puedes iniciar sesión.")
PASSWORD_RESET_INVALID_LINK_TITLE = _("Enlace inválido")
PASSWORD_RESET_INVALID_LINK_MESSAGE = _("El enlace de recuperación es inválido o ha expirado. Solicita uno nuevo.")
PASSWORD_RESET_EMAIL_SUBJECT = _("Recuperación de contraseña")
PASSWORD_ERROR_MISMATCH = _("Las contraseñas no coinciden.")
USER_WELCOME_EMAIL_SUBJECT = _("Tu cuenta ha sido creada")
USER_WELCOME_EMAIL_TITLE = _("Bienvenido a Issirmax")
USER_WELCOME_EMAIL_GREETING = _("Hola")
USER_WELCOME_EMAIL_BODY = _("Se ha creado una cuenta para ti con las siguientes credenciales de acceso.")
USER_WELCOME_EMAIL_USERNAME_LABEL = _("Usuario")
USER_WELCOME_EMAIL_PASSWORD_LABEL = _("Contraseña")
USER_WELCOME_EMAIL_FOOTER = _("Por seguridad, te recomendamos cambiar tu contraseña después de iniciar sesión.")
USER_WELCOME_EMAIL_SUPPORT = _("Si no reconoces este acceso, comunícate con el administrador del sistema.")
USER_USERNAME_RESERVED_SUFFIX_ERROR = _(
    "El correo es demasiado largo para generar un nombre de usuario reutilizable. Máximo permitido: {max_length} caracteres."
)

LABEL_EMAIL = _("Correo electrónico")
MSG_FIELD_REQUIRED = _("Este campo es obligatorio.")
MSG_EMAIL_INVALID = _("Ingrese un correo electrónico válido.")

# Password validation error map (Django built-in validator codes)
PASSWORD_VALIDATION_ERROR_MAP = {
    "password_too_similar": _("La contraseña es muy similar a tu información personal."),
    "password_too_short": _("La contraseña debe tener al menos 8 caracteres."),
    "password_too_common": _("La contraseña es demasiado común."),
    "password_entirely_numeric": _("La contraseña no puede ser completamente numérica."),
}

# Email template texts
PASSWORD_RESET_EMAIL_GREETING = _("Hola")
PASSWORD_RESET_EMAIL_BODY = _(
    "Recibiste este correo porque solicitaste restablecer tu contraseña. "
    "Haz clic en el siguiente enlace para crear una nueva contraseña:"
)
PASSWORD_RESET_EMAIL_BUTTON = _("Restablecer contraseña")
PASSWORD_RESET_EMAIL_IGNORE = _("Si no solicitaste esto, puedes ignorar este correo de forma segura.")
PASSWORD_RESET_EMAIL_EXPIRY = _("Este enlace expirará en 1 hora.")

# Form labels & placeholders
LABEL_NEW_PASSWORD = _("Nueva contraseña")
LABEL_REPEAT_PASSWORD = _("Repita la contraseña")
PLACEHOLDER_NEW_PASSWORD = _("Nueva contraseña")
PLACEHOLDER_REPEAT_PASSWORD = _("Repita la contraseña")
