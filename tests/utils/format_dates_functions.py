from datetime import datetime

months_in_spanish = [
    "Enero",
    "Febrero",
    "Marzo",
    "Abril",
    "Mayo",
    "Junio",
    "Julio",
    "Agosto",
    "Septiembre",
    "Octubre",
    "Noviembre",
    "Diciembre",
]


def format_date_dd_mm_aa(date: str, date_separator: str = "/") -> str:
    """Recibe una fecha en formato YYYY-MM-DD (ej: '2025-09-05') y la transforma a 'DD/MM/AA' (ej: '05/09/25').

    El separador entre día, mes y año puede ser personalizado.
    """
    formatted_date = datetime.strptime(date, "%Y-%m-%d")
    return formatted_date.strftime(f"%d{date_separator}%m{date_separator}%y")


def format_date_mm_dd_aa(date: str, date_separator: str = "/") -> str:
    """Recibe una fecha en formato YYYY-MM-DD (ej: '2025-09-05') y la transforma a 'MM/DD/AA' (ej: '09/05/25').

    El separador entre mes, día y año puede ser personalizado.
    """
    formatted_date = datetime.strptime(date, "%Y-%m-%d")
    return formatted_date.strftime(f"%m{date_separator}%d{date_separator}%y")


def format_date_aa_mm_dd(date: str, date_separator: str = "/") -> str:
    """Recibe una fecha en formato YYYY-MM-DD (ej: '2025-09-05') y la transforma a 'AA/MM/DD' (ej: '25/09/05').

    El separador entre año, mes y día puede ser personalizado.
    """
    formatted_date = datetime.strptime(date, "%Y-%m-%d")
    return formatted_date.strftime(f"%y{date_separator}%m{date_separator}%d")


def format_date_aa_dd_mm(date: str, date_separator: str = "/") -> str:
    """Recibe una fecha en formato YYYY-MM-DD (ej: '2025-09-05') y la transforma a 'AA/DD/MM' (ej: '25/05/09').

    El separador entre año, día y mes puede ser personalizado.
    """
    formatted_date = datetime.strptime(date, "%Y-%m-%d")
    return formatted_date.strftime(f"%y{date_separator}%d{date_separator}%m")


def format_date_dd_mm_aaaa(date: str, date_separator: str = "/") -> str:
    """Recibe una fecha en formato YYYY-MM-DD (ej: '2025-09-05') y la transforma a 'DD/MM/AAAA' (ej: '05/09/2025').

    El separador entre día, mes y año puede ser personalizado.
    """
    formatted_date = datetime.strptime(date, "%Y-%m-%d")
    return formatted_date.strftime(f"%d{date_separator}%m{date_separator}%Y")


def format_date_mm_dd_aaaa(date: str, date_separator: str = "/") -> str:
    """Recibe una fecha en formato YYYY-MM-DD (ej: '2025-09-05') y la transforma a 'MM/DD/AAAA' (ej: '09/05/2025').

    El separador entre mes, día y año puede ser personalizado.
    """
    formatted_date = datetime.strptime(date, "%Y-%m-%d")
    return formatted_date.strftime(f"%m{date_separator}%d{date_separator}%Y")


def format_date_aaaa_dd_mm(date: str, date_separator: str = "/") -> str:
    """Recibe una fecha en formato YYYY-MM-DD (ej: '2025-09-05') y la transforma a 'AAAA/DD/MM' (ej: '2025/05/09').

    El separador entre año, día y mes puede ser personalizado.
    """
    formatted_date = datetime.strptime(date, "%Y-%m-%d")
    return formatted_date.strftime(f"%Y{date_separator}%d{date_separator}%m")


def format_date_aaaa_mm_dd(date: str, date_separator: str = "/") -> str:
    """Recibe una fecha en formato YYYY-MM-DD (ej: '2025-09-05') y la transforma a 'AAAA/MM/DD' (ej: '2025/09/05').

    El separador entre año, mes y día puede ser personalizado.
    """
    formatted_date = datetime.strptime(date, "%Y-%m-%d")
    return formatted_date.strftime(f"%Y{date_separator}%m{date_separator}%d")


def format_time_hh_mm_ss(time: str, time_separator: str = ":") -> str:
    """Recibe una hora en formato HH:MM:SS o HH:MM (ej: '14:30:00' o '14:30') y la transforma a 'HH:MM:SS' (ej: '14:30:00').

    Si se recibe HH:MM, agrega ':00' al final automáticamente.
    El separador entre horas, minutos y segundos puede ser personalizado.
    """
    # Intentar primero con el formato completo HH:MM:SS
    try:
        formatted_time = datetime.strptime(time, "%H:%M:%S")
    except ValueError:
        # Si falla, intentar con HH:MM y agregar segundos
        formatted_time = datetime.strptime(time, "%H:%M")
    return formatted_time.strftime(f"%H{time_separator}%M{time_separator}%S")


def format_time_hh_mm(time: str, time_separator: str = ":") -> str:
    """Recibe una hora en formato HH:MM o HH:MM:SS (ej: '14:30' o '14:30:00') y la transforma a 'HH:MM' (ej: '14:30').

    El separador entre horas y minutos puede ser personalizado.
    """
    # Intentar primero con el formato completo HH:MM:SS
    try:
        formatted_time = datetime.strptime(time, "%H:%M:%S")
    except ValueError:
        # Si falla, intentar con HH:MM
        formatted_time = datetime.strptime(time, "%H:%M")
    return formatted_time.strftime(f"%H{time_separator}%M")


def format_time_hh_mm_am_pm(time: str, time_separator: str = ":") -> str:
    """Recibe una hora en formato HH:MM o HH:MM:SS (ej: '14:30' o '14:30:00') y la transforma a 'HH:MM AM/PM' (ej: '02:30 PM').

    El separador entre horas y minutos puede ser personalizado.
    Convierte automáticamente el formato 24h a 12h con indicador AM/PM.
    """
    # Intentar primero con el formato completo HH:MM:SS
    try:
        formatted_time = datetime.strptime(time, "%H:%M:%S")
    except ValueError:
        # Si falla, intentar con HH:MM
        formatted_time = datetime.strptime(time, "%H:%M")
    return formatted_time.strftime(f"%I{time_separator}%M %p")


def format_time_hh_mm_ss_am_pm(time: str, time_separator: str = ":") -> str:
    """Recibe una hora en formato HH:MM:SS o HH:MM (ej: '14:30:00' o '14:30') y la transforma a 'HH:MM:SS AM/PM' (ej: '02:30:45 PM').

    Si se recibe HH:MM, agrega ':00' al final automáticamente.
    El separador entre horas, minutos y segundos puede ser personalizado.
    Convierte automáticamente el formato 24h a 12h con indicador AM/PM.
    """
    # Intentar primero con el formato completo HH:MM:SS
    try:
        formatted_time = datetime.strptime(time, "%H:%M:%S")
    except ValueError:
        # Si falla, intentar con HH:MM y agregar segundos
        formatted_time = datetime.strptime(time, "%H:%M")
    return formatted_time.strftime(f"%I{time_separator}%M{time_separator}%S %p")


def format_date_dd_mm_aa_hh_mm_ss(
    date: str, date_separator: str = "/", datetime_separator: str = " ", time_separator: str = ":"
) -> str:
    """Recibe una fecha y hora en formato ISO y la transforma a 'DD/MM/AA HH:MM:SS'.

    Formatos de entrada: 'YYYY-MM-DDTHH:MM:SS', 'YYYY-MM-DDTHH:MM', 'YYYY-MM-DD HH:MM:SS' o 'YYYY-MM-DD HH:MM'.
    """
    # Intentamos con diferentes formatos
    try:
        formatted_date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        try:
            formatted_date = datetime.strptime(date, "%Y-%m-%dT%H:%M")
        except ValueError:
            try:
                formatted_date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                formatted_date = datetime.strptime(date, "%Y-%m-%d %H:%M")

    return formatted_date.strftime(
        f"%d{date_separator}%m{date_separator}%y{datetime_separator}%H{time_separator}%M{time_separator}%S"
    )


def format_date_mm_dd_aa_hh_mm_ss(
    date: str, date_separator: str = "/", datetime_separator: str = " ", time_separator: str = ":"
) -> str:
    """Recibe una fecha y hora en formato ISO y la transforma a 'MM/DD/AA HH:MM:SS'.

    Formatos de entrada: 'YYYY-MM-DDTHH:MM:SS', 'YYYY-MM-DDTHH:MM', 'YYYY-MM-DD HH:MM:SS' o 'YYYY-MM-DD HH:MM'.
    """
    # Intentamos con diferentes formatos
    try:
        formatted_date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        try:
            formatted_date = datetime.strptime(date, "%Y-%m-%dT%H:%M")
        except ValueError:
            try:
                formatted_date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                formatted_date = datetime.strptime(date, "%Y-%m-%d %H:%M")

    return formatted_date.strftime(
        f"%m{date_separator}%d{date_separator}%y{datetime_separator}%H{time_separator}%M{time_separator}%S"
    )


def format_date_aa_mm_dd_hh_mm_ss(
    date: str, date_separator: str = "/", datetime_separator: str = " ", time_separator: str = ":"
) -> str:
    """Recibe una fecha y hora en formato ISO y la transforma a 'AA/MM/DD HH:MM:SS'.

    Formatos de entrada: 'YYYY-MM-DDTHH:MM:SS', 'YYYY-MM-DDTHH:MM', 'YYYY-MM-DD HH:MM:SS' o 'YYYY-MM-DD HH:MM'.
    """
    # Intentamos con diferentes formatos
    try:
        formatted_date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        try:
            formatted_date = datetime.strptime(date, "%Y-%m-%dT%H:%M")
        except ValueError:
            try:
                formatted_date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                formatted_date = datetime.strptime(date, "%Y-%m-%d %H:%M")

    return formatted_date.strftime(
        f"%y{date_separator}%m{date_separator}%d{datetime_separator}%H{time_separator}%M{time_separator}%S"
    )


def format_date_aa_dd_mm_hh_mm_ss(
    date: str, date_separator: str = "/", datetime_separator: str = " ", time_separator: str = ":"
) -> str:
    """Recibe una fecha y hora en formato ISO y la transforma a 'AA/DD/MM HH:MM:SS'.

    Formatos de entrada: 'YYYY-MM-DDTHH:MM:SS', 'YYYY-MM-DDTHH:MM', 'YYYY-MM-DD HH:MM:SS' o 'YYYY-MM-DD HH:MM'.
    """
    # Intentamos con diferentes formatos
    try:
        formatted_date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        try:
            formatted_date = datetime.strptime(date, "%Y-%m-%dT%H:%M")
        except ValueError:
            try:
                formatted_date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                formatted_date = datetime.strptime(date, "%Y-%m-%d %H:%M")

    return formatted_date.strftime(
        f"%y{date_separator}%d{date_separator}%m{datetime_separator}%H{time_separator}%M{time_separator}%S"
    )


def format_date_dd_mm_aaaa_hh_mm_ss(
    date: str, date_separator: str = "/", datetime_separator: str = " ", time_separator: str = ":"
) -> str:
    """Recibe una fecha y hora en formato ISO y la transforma a 'DD/MM/AAAA HH:MM:SS'.

    Formatos de entrada: 'YYYY-MM-DDTHH:MM:SS', 'YYYY-MM-DDTHH:MM', 'YYYY-MM-DD HH:MM:SS' o 'YYYY-MM-DD HH:MM'.
    """
    # Intentamos con diferentes formatos
    try:
        formatted_date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        try:
            formatted_date = datetime.strptime(date, "%Y-%m-%dT%H:%M")
        except ValueError:
            try:
                formatted_date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                formatted_date = datetime.strptime(date, "%Y-%m-%d %H:%M")

    return formatted_date.strftime(
        f"%d{date_separator}%m{date_separator}%Y{datetime_separator}%H{time_separator}%M{time_separator}%S"
    )


def format_date_mm_dd_aaaa_hh_mm_ss(
    date: str, date_separator: str = "/", datetime_separator: str = " ", time_separator: str = ":"
) -> str:
    """Recibe una fecha y hora en formato ISO y la transforma a 'MM/DD/AAAA HH:MM:SS'.

    Formatos de entrada: 'YYYY-MM-DDTHH:MM:SS', 'YYYY-MM-DDTHH:MM', 'YYYY-MM-DD HH:MM:SS' o 'YYYY-MM-DD HH:MM'.
    """
    # Intentamos con diferentes formatos
    try:
        formatted_date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        try:
            formatted_date = datetime.strptime(date, "%Y-%m-%dT%H:%M")
        except ValueError:
            try:
                formatted_date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                formatted_date = datetime.strptime(date, "%Y-%m-%d %H:%M")

    return formatted_date.strftime(
        f"%m{date_separator}%d{date_separator}%Y{datetime_separator}%H{time_separator}%M{time_separator}%S"
    )


def format_date_aaaa_dd_mm_hh_mm_ss(
    date: str, date_separator: str = "/", datetime_separator: str = " ", time_separator: str = ":"
) -> str:
    """Recibe una fecha y hora en formato ISO y la transforma a 'AAAA/DD/MM HH:MM:SS'.

    Formatos de entrada: 'YYYY-MM-DDTHH:MM:SS', 'YYYY-MM-DDTHH:MM', 'YYYY-MM-DD HH:MM:SS' o 'YYYY-MM-DD HH:MM'.
    """
    # Intentamos con diferentes formatos
    try:
        formatted_date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        try:
            formatted_date = datetime.strptime(date, "%Y-%m-%dT%H:%M")
        except ValueError:
            try:
                formatted_date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                formatted_date = datetime.strptime(date, "%Y-%m-%d %H:%M")

    return formatted_date.strftime(
        f"%Y{date_separator}%d{date_separator}%m{datetime_separator}%H{time_separator}%M{time_separator}%S"
    )


def format_date_aaaa_mm_dd_hh_mm_ss(
    date: str, date_separator: str = "/", datetime_separator: str = " ", time_separator: str = ":"
) -> str:
    """Recibe una fecha y hora en formato ISO y la transforma a 'AAAA/MM/DD HH:MM:SS'.

    Formatos de entrada: 'YYYY-MM-DDTHH:MM:SS', 'YYYY-MM-DDTHH:MM', 'YYYY-MM-DD HH:MM:SS' o 'YYYY-MM-DD HH:MM'.
    """
    # Intentamos con diferentes formatos
    try:
        formatted_date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        try:
            formatted_date = datetime.strptime(date, "%Y-%m-%dT%H:%M")
        except ValueError:
            try:
                formatted_date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                formatted_date = datetime.strptime(date, "%Y-%m-%d %H:%M")

    return formatted_date.strftime(
        f"%Y{date_separator}%m{date_separator}%d{datetime_separator}%H{time_separator}%M{time_separator}%S"
    )


def format_date_dd_mm_aa_hh_mm(
    date: str, date_separator: str = "/", datetime_separator: str = " ", time_separator: str = ":"
) -> str:
    """Recibe una fecha y hora en formato ISO y la transforma a 'DD/MM/AA HH:MM'.

    Formatos de entrada: 'YYYY-MM-DDTHH:MM', 'YYYY-MM-DDTHH:MM:SS', 'YYYY-MM-DD HH:MM' o 'YYYY-MM-DD HH:MM:SS'.
    """
    # Intentamos con diferentes formatos
    try:
        formatted_date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        try:
            formatted_date = datetime.strptime(date, "%Y-%m-%dT%H:%M")
        except ValueError:
            try:
                formatted_date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                formatted_date = datetime.strptime(date, "%Y-%m-%d %H:%M")

    return formatted_date.strftime(f"%d{date_separator}%m{date_separator}%y{datetime_separator}%H{time_separator}%M")


def format_date_mm_dd_aa_hh_mm(
    date: str, date_separator: str = "/", datetime_separator: str = " ", time_separator: str = ":"
) -> str:
    """Recibe una fecha y hora en formato ISO y la transforma a 'MM/DD/AA HH:MM'.

    Formatos de entrada: 'YYYY-MM-DDTHH:MM', 'YYYY-MM-DDTHH:MM:SS', 'YYYY-MM-DD HH:MM' o 'YYYY-MM-DD HH:MM:SS'.
    """
    # Intentamos con diferentes formatos
    try:
        formatted_date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        try:
            formatted_date = datetime.strptime(date, "%Y-%m-%dT%H:%M")
        except ValueError:
            try:
                formatted_date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                formatted_date = datetime.strptime(date, "%Y-%m-%d %H:%M")

    return formatted_date.strftime(f"%m{date_separator}%d{date_separator}%y{datetime_separator}%H{time_separator}%M")


def format_date_aa_mm_dd_hh_mm(
    date: str, date_separator: str = "/", datetime_separator: str = " ", time_separator: str = ":"
) -> str:
    """Recibe una fecha y hora en formato ISO y la transforma a 'AA/MM/DD HH:MM'.

    Formatos de entrada: 'YYYY-MM-DDTHH:MM', 'YYYY-MM-DDTHH:MM:SS', 'YYYY-MM-DD HH:MM' o 'YYYY-MM-DD HH:MM:SS'.
    """
    # Intentamos con diferentes formatos
    try:
        formatted_date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        try:
            formatted_date = datetime.strptime(date, "%Y-%m-%dT%H:%M")
        except ValueError:
            try:
                formatted_date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                formatted_date = datetime.strptime(date, "%Y-%m-%d %H:%M")

    return formatted_date.strftime(f"%y{date_separator}%m{date_separator}%d{datetime_separator}%H{time_separator}%M")


def format_date_aa_dd_mm_hh_mm(
    date: str, date_separator: str = "/", datetime_separator: str = " ", time_separator: str = ":"
) -> str:
    """Recibe una fecha y hora en formato ISO y la transforma a 'AA/DD/MM HH:MM'.

    Formatos de entrada: 'YYYY-MM-DDTHH:MM', 'YYYY-MM-DDTHH:MM:SS', 'YYYY-MM-DD HH:MM' o 'YYYY-MM-DD HH:MM:SS'.
    """
    # Intentamos con diferentes formatos
    try:
        formatted_date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        try:
            formatted_date = datetime.strptime(date, "%Y-%m-%dT%H:%M")
        except ValueError:
            try:
                formatted_date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                formatted_date = datetime.strptime(date, "%Y-%m-%d %H:%M")

    return formatted_date.strftime(f"%y{date_separator}%d{date_separator}%m{datetime_separator}%H{time_separator}%M")


def format_date_dd_mm_aaaa_hh_mm(
    date: str, date_separator: str = "/", datetime_separator: str = " ", time_separator: str = ":"
) -> str:
    """Recibe una fecha y hora en formato ISO y la transforma a 'DD/MM/AAAA HH:MM'.

    Formatos de entrada: 'YYYY-MM-DDTHH:MM', 'YYYY-MM-DDTHH:MM:SS', 'YYYY-MM-DD HH:MM' o 'YYYY-MM-DD HH:MM:SS'.
    """
    # Intentamos con diferentes formatos
    try:
        formatted_date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        try:
            formatted_date = datetime.strptime(date, "%Y-%m-%dT%H:%M")
        except ValueError:
            try:
                formatted_date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                formatted_date = datetime.strptime(date, "%Y-%m-%d %H:%M")

    return formatted_date.strftime(f"%d{date_separator}%m{date_separator}%Y{datetime_separator}%H{time_separator}%M")


def format_date_mm_dd_aaaa_hh_mm(
    date: str, date_separator: str = "/", datetime_separator: str = " ", time_separator: str = ":"
) -> str:
    """Recibe una fecha y hora en formato ISO y la transforma a 'MM/DD/AAAA HH:MM'.

    Formatos de entrada: 'YYYY-MM-DDTHH:MM', 'YYYY-MM-DDTHH:MM:SS', 'YYYY-MM-DD HH:MM' o 'YYYY-MM-DD HH:MM:SS'.
    """
    # Intentamos con diferentes formatos
    try:
        formatted_date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        try:
            formatted_date = datetime.strptime(date, "%Y-%m-%dT%H:%M")
        except ValueError:
            try:
                formatted_date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                formatted_date = datetime.strptime(date, "%Y-%m-%d %H:%M")

    return formatted_date.strftime(f"%m{date_separator}%d{date_separator}%Y{datetime_separator}%H{time_separator}%M")


def format_date_aaaa_dd_mm_hh_mm(
    date: str, date_separator: str = "/", datetime_separator: str = " ", time_separator: str = ":"
) -> str:
    """Recibe una fecha y hora en formato ISO y la transforma a 'AAAA/DD/MM HH:MM'.

    Formatos de entrada: 'YYYY-MM-DDTHH:MM', 'YYYY-MM-DDTHH:MM:SS', 'YYYY-MM-DD HH:MM' o 'YYYY-MM-DD HH:MM:SS'.
    """
    # Intentamos con diferentes formatos
    try:
        formatted_date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        try:
            formatted_date = datetime.strptime(date, "%Y-%m-%dT%H:%M")
        except ValueError:
            try:
                formatted_date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                formatted_date = datetime.strptime(date, "%Y-%m-%d %H:%M")

    return formatted_date.strftime(f"%Y{date_separator}%d{date_separator}%m{datetime_separator}%H{time_separator}%M")


def format_date_aaaa_mm_dd_hh_mm(
    date: str, date_separator: str = "/", datetime_separator: str = " ", time_separator: str = ":"
) -> str:
    """Recibe una fecha y hora en formato ISO y la transforma a 'AAAA/MM/DD HH:MM'.

    Formatos de entrada: 'YYYY-MM-DDTHH:MM', 'YYYY-MM-DDTHH:MM:SS', 'YYYY-MM-DD HH:MM' o 'YYYY-MM-DD HH:MM:SS'.
    """
    # Intentamos con diferentes formatos
    try:
        formatted_date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        try:
            formatted_date = datetime.strptime(date, "%Y-%m-%dT%H:%M")
        except ValueError:
            try:
                formatted_date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                formatted_date = datetime.strptime(date, "%Y-%m-%d %H:%M")

    return formatted_date.strftime(f"%Y{date_separator}%m{date_separator}%d{datetime_separator}%H{time_separator}%M")


def format_date_date_in_spanish(date: str) -> str:
    """Recibe una fecha en formato YYYY-MM-DD (ej: '2025-09-05') y la transforma al formato 'D de Mes de AAAA'.

    Ejemplo: '5 de Septiembre de 2025'.
    """
    formatted_date = datetime.strptime(date, "%Y-%m-%d")

    day = formatted_date.day
    month = months_in_spanish[formatted_date.month - 1]
    year = formatted_date.year
    return f"{day} de {month} de {year}"


def format_date_datetime_in_spanish(date: str) -> str:
    """Recibe una fecha y hora en formato ISO (ej: '2025-09-05T14:30:00' o '2025-09-05T14:30') y la transforma al formato 'D de Mes de AAAA a las HH:MM'.

    Ejemplo: '5 de Septiembre de 2025 a las 14:30'.
    """
    # Intentamos con diferentes formatos
    try:
        formatted_date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        try:
            formatted_date = datetime.strptime(date, "%Y-%m-%dT%H:%M")
        except ValueError:
            try:
                formatted_date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                formatted_date = datetime.strptime(date, "%Y-%m-%d %H:%M")

    day = formatted_date.day
    month = months_in_spanish[formatted_date.month - 1]
    year = formatted_date.year
    time = formatted_date.strftime("%H:%M")
    return f"{day} de {month} de {year} a las {time}"


def format_date_dd_complete_month_yyyy(date: str) -> str:
    """Recibe una fecha en formato YYYY-MM-DD (ej: '2025-09-05') y la transforma a 'DD Mes YYYY' (ej: '05 Septiembre 2025')."""
    formatted_date = datetime.strptime(date, "%Y-%m-%d")
    day = formatted_date.day
    month = months_in_spanish[formatted_date.month - 1]
    year = formatted_date.year
    return f"{day} {month} {year}"


def format_date_dd_abbreviate_month_yyyy(date: str) -> str:
    """Recibe una fecha en formato YYYY-MM-DD (ej: '2025-09-05') y la transforma a 'DD Mon YYYY' (ej: '05 Sep 2025')."""
    formatted_date = datetime.strptime(date, "%Y-%m-%d")
    return formatted_date.strftime("%d %b %Y")


def parse_date_to_datetime(date_string: str, date_format=None, separators=None) -> datetime:
    """Convierte una fecha en cualquier formato a un objeto datetime de Python.

    Args:
        date_string: String con la fecha en cualquier formato soportado
        date_format: AllowedDatesFormates opcional para especificar el formato esperado
        separators: Dict opcional con separadores personalizados {'date': '/', 'time': ':', 'datetime': ' '}

    Returns:
        datetime: Objeto datetime de Python

    Raises:
        ValueError: Si no se puede parsear la fecha con ningún formato conocido

    Ejemplos:
        >>> parse_date_to_datetime("2026-02-09")
        datetime.datetime(2026, 2, 9, 0, 0)
        >>> parse_date_to_datetime("09/02/2026")
        datetime.datetime(2026, 2, 9, 0, 0)
        >>> parse_date_to_datetime("09/02/2026 11:15", AllowedDatesFormates.DD_MM_AAAA_HH_MM)
        datetime.datetime(2026, 2, 9, 11, 15)
    """
    from tests.pages.core.constants import AllowedDatesFormates

    if separators is None:
        separators = {"date": "/", "time": ":", "datetime": " "}

    # Mapeo de formatos de AllowedDatesFormates a patrones strptime
    format_mapping = {
        # Formatos de fecha - año 2 dígitos
        AllowedDatesFormates.DD_MM_AA: ["%d/%m/%y", "%d-%m-%y"],
        AllowedDatesFormates.MM_DD_AA: ["%m/%d/%y", "%m-%d-%y"],
        AllowedDatesFormates.AA_MM_DD: ["%y/%m/%d", "%y-%m-%d"],
        AllowedDatesFormates.AA_DD_MM: ["%y/%d/%m", "%y-%d-%m"],
        # Formatos de fecha - año 4 dígitos
        AllowedDatesFormates.DD_MM_AAAA: ["%d/%m/%Y", "%d-%m-%Y"],
        AllowedDatesFormates.MM_DD_AAAA: ["%m/%d/%Y", "%m-%d-%Y"],
        AllowedDatesFormates.AAAA_MM_DD: ["%Y/%m/%d", "%Y-%m-%d"],
        AllowedDatesFormates.AAAA_DD_MM: ["%Y/%d/%m", "%Y-%d-%m"],
        # Formatos de hora
        AllowedDatesFormates.HH_MM: ["%H:%M"],
        AllowedDatesFormates.HH_MM_SS: ["%H:%M:%S"],
        # Formatos de fecha+hora con segundos - año 2 dígitos
        AllowedDatesFormates.DD_MM_AA_HH_MM_SS: ["%d/%m/%y %H:%M:%S", "%d-%m-%y %H:%M:%S"],
        AllowedDatesFormates.MM_DD_AA_HH_MM_SS: ["%m/%d/%y %H:%M:%S", "%m-%d-%y %H:%M:%S"],
        AllowedDatesFormates.AA_MM_DD_HH_MM_SS: ["%y/%m/%d %H:%M:%S", "%y-%m-%d %H:%M:%S"],
        AllowedDatesFormates.AA_DD_MM_HH_MM_SS: ["%y/%d/%m %H:%M:%S", "%y-%d-%m %H:%M:%S"],
        # Formatos de fecha+hora con segundos - año 4 dígitos
        AllowedDatesFormates.DD_MM_AAAA_HH_MM_SS: ["%d/%m/%Y %H:%M:%S", "%d-%m-%Y %H:%M:%S"],
        AllowedDatesFormates.MM_DD_AAAA_HH_MM_SS: ["%m/%d/%Y %H:%M:%S", "%m-%d-%Y %H:%M:%S"],
        AllowedDatesFormates.AAAA_DD_MM_HH_MM_SS: ["%Y/%d/%m %H:%M:%S", "%Y-%d-%m %H:%M:%S"],
        AllowedDatesFormates.AAAA_MM_DD_HH_MM_SS: ["%Y/%m/%d %H:%M:%S", "%Y-%m-%d %H:%M:%S"],
        # Formatos de fecha+hora sin segundos - año 2 dígitos
        AllowedDatesFormates.DD_MM_AA_HH_MM: ["%d/%m/%y %H:%M", "%d-%m-%y %H:%M"],
        AllowedDatesFormates.MM_DD_AA_HH_MM: ["%m/%d/%y %H:%M", "%m-%d-%y %H:%M"],
        AllowedDatesFormates.AA_MM_DD_HH_MM: ["%y/%m/%d %H:%M", "%y-%m-%d %H:%M"],
        AllowedDatesFormates.AA_DD_MM_HH_MM: ["%y/%d/%m %H:%M", "%y-%d-%m %H:%M"],
        # Formatos de fecha+hora sin segundos - año 4 dígitos
        AllowedDatesFormates.DD_MM_AAAA_HH_MM: ["%d/%m/%Y %H:%M", "%d-%m-%Y %H:%M"],
        AllowedDatesFormates.MM_DD_AAAA_HH_MM: ["%m/%d/%Y %H:%M", "%m-%d-%Y %H:%M"],
        AllowedDatesFormates.AAAA_DD_MM_HH_MM: ["%Y/%d/%m %H:%M", "%Y-%d-%m %H:%M"],
        AllowedDatesFormates.AAAA_MM_DD_HH_MM: ["%Y/%m/%d %H:%M", "%Y-%m-%d %H:%M"],
    }

    # Lista de patrones a intentar
    patterns_to_try = []

    # Añadir formatos ISO estándar al principio
    patterns_to_try.extend(
        [
            "%Y-%m-%d",
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%dT%H:%M",
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%d %H:%M",
        ]
    )

    # Si se especificó un formato, intentar primero con ese
    if date_format and date_format in format_mapping:
        patterns_to_try = format_mapping[date_format] + patterns_to_try

    # Si no se especificó formato, intentar con todos los formatos
    if not date_format:
        for patterns in format_mapping.values():
            patterns_to_try.extend(patterns)

    # Intentar cada patrón
    for pattern in patterns_to_try:
        try:
            # Reemplazar separadores si son personalizados
            test_pattern = pattern
            if separators.get("date") and separators["date"] != "/":
                test_pattern = test_pattern.replace("/", separators["date"]).replace("-", separators["date"])
            if separators.get("time") and separators["time"] != ":":
                test_pattern = test_pattern.replace(":", separators["time"])
            if separators.get("datetime") and separators["datetime"] != " ":
                test_pattern = test_pattern.replace(" ", separators["datetime"])

            return datetime.strptime(date_string, test_pattern)
        except ValueError:
            continue

    # Si ningún formato funcionó, lanzar error
    raise ValueError(
        f"No se pudo parsear la fecha '{date_string}'. "
        f"Formatos soportados: DD/MM/YYYY, DD/MM/YYYY HH:MM, YYYY-MM-DD, etc."
    )
