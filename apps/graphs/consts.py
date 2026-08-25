"""Graphs module constants."""

# Nombres de grupo — mismos valores que utils.constants.Groups en reciplus-djangoninja.
GROUP_ADMINISTRATOR = "Administrator"
GROUP_DOCTOR = "Doctor"

# Grupos que pueden ver /graphs. Admin ve la plataforma completa; doctor ve solo lo suyo
# (ver apps.graphs.service.get_profits_and_losses).
ALLOWED_GROUPS = {GROUP_ADMINISTRATOR, GROUP_DOCTOR}

ERROR_INVALID_TOKEN = "Token inválido o expirado"
ERROR_NOT_AUTHENTICATED = "No has iniciado sesión"
ERROR_FORBIDDEN = "No tienes permiso para ver esta información"

MONTHS_BACK = 12

# Resumen de citas/cobros (get_doctor_summary) — mismos valores que apps.stats en
# reciplus-djangoninja.
STATS_DEFAULT_RANGE_DAYS = 30
PROVIDER_MERCADOPAGO = "mercado_pago"

# Código de intercambio (solo plataformas nativas — Android/iOS/Desktop, ver
# apps.graphs.auth_bridge). Corto a propósito: se canjea segundos después de emitirse.
EXCHANGE_CODE_TTL_SECONDS = 30
