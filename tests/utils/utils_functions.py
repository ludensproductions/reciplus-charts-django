import base64
import random
import re
import string
import tempfile
import zipfile
from datetime import datetime, timedelta
from io import BytesIO
from pathlib import Path
from types import SimpleNamespace

import rstr
from dotenv import dotenv_values, load_dotenv
from pages.core.constants import RegexFlag
from PIL import Image, ImageDraw

# File extension constants for file generation
TEXT_EXTENSIONS = ["txt", "csv", "log", "json", "xml", "svg"]
BINARY_EXTENSIONS = ["doc", "docx", "ppt", "pptx", "rar", "pdf", "odt", "xls", "xlsx", "ods", "odp", "zip", "7z"]
IMAGE_EXTENSIONS = ["jpg", "jpeg", "png", "gif", "bmp", "webp"]


def generate_random_string(length, chars=None):
    """Generates a random string of a specified length using a given set of characters.

    Args:
        length: The length of the random string to be generated.
        chars: The set of characters to use for generating the string (default is ASCII letters).

    Returns:
        A random string of the specified length.
    """
    return "".join(random.choice(chars or string.ascii_letters) for _ in range(length))


def generate_special_char_string(length=10):
    """Generates a random string containing special characters."""
    return "".join(random.choice(r"""#!"$%&'()*+,-./:<=>?@[\]^_`|~;""") for _ in range(length))


def generate_random_int(min_value: int, max_value: int):
    """Generates a random integer between the specified minimum and maximum values (inclusive).

    Args:
        min_value (int): The minimum value for the random integer.
        max_value (int): The maximum value for the random integer.

    Returns:
        A random integer between min_value and max_value (inclusive).
    """
    return random.randint(min_value, max_value)


def generate_random_float(minimo: int, maximo: int):
    """Generates a random float between the specified minimum and maximum values (inclusive), rounded to two decimal places.

    Args:
        minimo (int): The minimum value for the random float.
        maximo (int): The maximum value for the random float.

    Returns:
        float: A random float between min_value and max_value (inclusive), formatted to two decimal places.
    """
    flotante = round(random.uniform(minimo, maximo), 2)
    return format(flotante, ".2f")


def generate_custom_random_float(minimo: int, maximo: int, allowed_values: list = None):
    """Genera un número flotante aleatorio entre 'start' y 'end' con decimales restringidos a .25, .50 o .75.

    Args:
        minimo (int): Límite inferior (entero).
        maximo (int): Límite superior (entero).
        allowed_values (list): Lista de valores decimales permitidos.

    Returns:
        float: Número flotante aleatorio con decimales restringidos.
    """
    whole_number = random.randint(minimo, maximo)  # Genera la parte entera
    decimal_part = random.choice(allowed_values)  # Selecciona un decimal permitido
    return whole_number + decimal_part


def generate_random_email(length=10):
    """Generates a random email address."""
    return f"{generate_random_string(length)}@{generate_random_string(5).lower()}.com"


def generate_random_ip():
    """Generates a random IP address.

    Returns:
        A random IP address in the format 'xxx.xxx.xxx.xxx', where each 'xxx' is a number between 0 and 255.
    """
    return ".".join(str(random.randint(0, 255)) for _ in range(4))


def generate_random_mac():
    """Generates a random MAC address.

    Returns:
        A random MAC address in the format 'XX:XX:XX:XX:XX:XX', where each 'XX' is a two-digit hexadecimal number.
    """

    def random_mac_part():
        return "".join(random.choice("0123456789ABCDEF") for _ in range(2))

    return ":".join(random_mac_part() for _ in range(6))


def format_date_in_dd_mm_aaaa(date_obj: datetime):
    """Formats a given datetime object into a date string in the format "YYYY-MM-DD".

    Args:
        date_obj (datetime): The datetime object to be formatted.

    Returns:
        The formatted date string in the format "YYYY-MM-DD".
    """
    return date_obj.strftime("%Y-%m-%d")


def format_date_in_spanish(date_obj: datetime):
    """Formats a given datetime object into a date string in Spanish.

    Args:
        date_obj (datetime): The datetime object to be formatted.

    Returns:
        The formatted date string in the format "day de month de year", where month is the Spanish name of the month.
    """
    meses = {
        1: "Enero",
        2: "Febrero",
        3: "Marzo",
        4: "Abril",
        5: "Mayo",
        6: "Junio",
        7: "Julio",
        8: "Agosto",
        9: "Septiembre",
        10: "Octubre",
        11: "Noviembre",
        12: "Diciembre",
    }
    dia = date_obj.day
    mes = meses[date_obj.month]
    año = date_obj.year
    return f"{dia} de {mes} de {año}"


def generate_datetime() -> str:
    """Generates the current date and time in the format required for an input type='datetime-local'.

    Returns:
        The current date and time formatted as "YYYY-MM-DDTHH:MM".
    """
    now = datetime.now()
    return now.strftime("%Y-%m-%dT%H:%M")


def create_random_image() -> str:
    """Creates a random image of 100x100 pixels with a random background color and some random text.

    The image is saved as a PNG file to a temporary location, and the path to this file is returned.

    Returns:
        str: The file path to the saved PNG image.
    """
    img = Image.new("RGB", (100, 100), color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
    draw = ImageDraw.Draw(img)
    text = "".join(random.choices(string.ascii_uppercase + string.digits, k=5))
    draw.text((10, 10), text, fill=(255, 255, 255))

    with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
        img.save(temp_file, format="PNG")
        temp_file_path = temp_file.name
    return temp_file_path


def generate_valid_password(min_length=10, max_length=None):
    """Genera una contraseña aleatoria que cumple con los siguientes requisitos.

    - Al menos un carácter especial.
    - Al menos un número.
    - Al menos una letra mayúscula.
    - Al menos una letra minúscula.
    - Longitud mínima de 8 caracteres.

    Args:
        min_length (int): Longitud mínima de la contraseña.
        max_length (int): Longitud máxima de la contraseña.

    Returns:
        str: Contraseña generada.
    """
    if max_length is not None and max_length < min_length:
        raise ValueError("La longitud máxima no puede ser menor que la longitud mínima.")

    # Determinar la longitud real de la contraseña
    length = random.randint(min_length, max_length) if max_length else min_length

    # Caracteres requeridos
    special_char = random.choice("!@#$%^&*()_+-=[]{}|;:,.<>?/")  # Al menos un carácter especial
    number = random.choice(string.digits)  # Al menos un número
    uppercase = random.choice(string.ascii_uppercase)  # Al menos una letra mayúscula
    lowercase = random.choice(string.ascii_lowercase)  # Al menos una letra minúscula

    # Rellenar el resto de la contraseña con caracteres aleatorios
    remaining_length = length - 4
    all_characters = string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?/"
    remaining_chars = "".join(random.choices(all_characters, k=remaining_length))

    # Combinar todos los caracteres y mezclarlos
    password_list = [special_char, number, uppercase, lowercase] + list(remaining_chars)
    random.shuffle(password_list)

    # Convertir la lista a una cadena
    return "".join(password_list)


def generate_random_phone_number(min_length=10, max_length=10):
    """Generates a random phone number with a length between 10 and 15 digits.

    Returns:
        A random phone number with a length between 10 and 15 digits.
    """
    return "".join(random.choices(string.digits, k=random.randint(min_length, max_length)))


def generate_random_number_with_length(length):
    """Generates a random string of numbers of a specified length."""
    return "".join(random.choice(string.digits) for _ in range(length))


def generate_base64_file(content=None, extension="txt", output_filename=None, weight=None):
    """Genera un archivo en base64 con una extensión personalizada y un tamaño específico en MB.

    Args:
        content (str, optional): Contenido en base64 del archivo. Si no se proporciona, se genera automáticamente.
        extension (str): Extensión deseada para el archivo (por ejemplo, 'jpg', 'pdf', 'txt', 'zip').
        output_filename (str): Nombre base del archivo sin la extensión (por defecto, 'file').
        weight (float, optional): Tamaño deseado del archivo en MB. Si no se proporciona, se usa el contenido predeterminado.

    Returns:
        dict: Diccionario con el nombre del archivo, tipo MIME y contenido en memoria.
    """
    extension = extension.lstrip(".")
    file_name = f"{output_filename}.{extension}" if output_filename else f"{generate_random_string(10)}.{extension}"

    mime_types = {
        "txt": "text/plain",
        "csv": "text/csv",
        "log": "text/plain",
        "json": "application/json",
        "xml": "application/xml",
        "doc": "application/msword",
        "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "ppt": "application/vnd.ms-powerpoint",
        "pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        "svg": "image/svg+xml",
        "rar": "application/x-rar-compressed",
        "jpg": "image/jpeg",
        "jpeg": "image/jpeg",
        "png": "image/png",
        "gif": "image/gif",
        "pdf": "application/pdf",
        "zip": "application/zip",
        "xls": "application/vnd.ms-excel",
        "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "test": "application/octet-stream",  # MIME genérico para archivos no reconocidos
    }
    mime_type = mime_types.get(extension, "application/octet-stream")

    try:
        if content is None:
            target_size = int(weight * 1024 * 1024) if weight else None

            if extension in TEXT_EXTENSIONS:
                text_content = "A" * target_size if target_size else f"Archivo de prueba {extension}"
                content = base64.b64encode(text_content.encode("utf-8")).decode("utf-8")
            elif extension in BINARY_EXTENSIONS:
                # Contenido dummy binario
                bin_content = ("0" * (target_size if target_size else 1024)).encode("utf-8")
                content = base64.b64encode(bin_content).decode("utf-8")
            elif extension in IMAGE_EXTENSIONS:
                image_format = "JPEG" if extension in ["jpg", "jpeg"] else extension.upper()
                img = (
                    Image.new("RGB", (1000, 1000), color=(255, 0, 0))
                    if target_size
                    else Image.new("RGB", (100, 100), color=(255, 0, 0))
                )
                buffer = BytesIO()
                img.save(buffer, format=image_format)
                content = base64.b64encode(buffer.getvalue()).decode("utf-8")
            elif extension == "pdf":
                pdf_content = (
                    "%PDF-1.4\n1 0 obj\n<<\n>>\nendobj\n" * (target_size // 20)
                    if target_size
                    else b"%PDF-1.4\n1 0 obj\n<<\n>>\nendobj"
                )
                content = base64.b64encode(
                    pdf_content.encode("utf-8") if isinstance(pdf_content, str) else pdf_content
                ).decode("utf-8")
            elif extension in ["xls", "xlsx"]:
                xls_content = "PK\x03\x04" * (target_size // 3) if target_size else b"PK\x03\x04"
                content = base64.b64encode(
                    xls_content.encode("utf-8") if isinstance(xls_content, str) else xls_content
                ).decode("utf-8")
            elif extension == "zip":
                buffer = BytesIO()
                with zipfile.ZipFile(buffer, "w") as zipf:
                    zipf.writestr("archivo_prueba.txt", "A" * target_size if target_size else "Contenido de prueba")
                buffer.seek(0)
                content = base64.b64encode(buffer.read()).decode("utf-8")
            elif extension == "test":
                # Generar un archivo con formato no permitido para pruebas de validación de formato
                content = base64.b64encode(b"Contenido de prueba para formato no permitido").decode("utf-8")
            else:
                raise ValueError(f"No se puede generar contenido automático para la extensión: {extension}")

        file_data = base64.b64decode(content)
        return {
            "name": file_name,
            "mimeType": mime_type,
            "buffer": BytesIO(file_data).getvalue(),
        }
    except Exception:
        return None


def get_random_unaccepted_format(format_list, allowed_values):
    """Retorna un formato aleatorio que no esté en la lista de formatos aceptados.

    Args:
        format_list (list): Lista completa de formatos disponibles.
        allowed_values (list): Lista de formatos aceptados.

    Returns:
        str: Un formato no aceptado, seleccionado aleatoriamente. Retorna None si no hay formatos no aceptados.
    """
    normalized_allowed_values = {value.lower().lstrip(".") for value in (allowed_values or [])}
    normalized_format_list = [fmt.lower().lstrip(".") for fmt in (format_list or [])]

    # Crear una lista con los formatos que no están en los aceptados
    unaccepted_formats = [fmt for fmt in normalized_format_list if fmt not in normalized_allowed_values]

    # Si hay formatos no aceptados, devolver uno aleatorio
    if unaccepted_formats:
        return random.choice(unaccepted_formats)

    # Si no hay formatos no aceptados, retorna None
    return None


def get_format_file_list():
    """Retorna una lista de formatos de archivo comunes.

    Returns:
        list: Lista de formatos de archivo.
    """
    return [
        ".txt",
        ".csv",
        ".log",
        ".pdf",
        ".doc",
        ".docx",
        ".odt",
        ".xls",
        ".xlsx",
        ".ods",
        ".ppt",
        ".pptx",
        ".odp",
        ".jpg",
        ".jpeg",
        ".png",
        ".gif",
        ".bmp",
        ".webp",
        ".zip",
        ".rar",
        ".7z",
    ]


def generate_custom_date(dias: int) -> str:
    """Genera una fecha sumando o restando un número específico de días a la fecha actual.

    Args:
        dias (int): Número de días a agregar a la fecha actual.

    Returns:
        str: La fecha futura en formato 'YYYY-MM-DD'.
    """
    # Obtener la fecha actual
    fecha_actual = datetime.now()

    # Sumar el número de días a la fecha actual
    fecha_modificada = fecha_actual + timedelta(days=dias)

    return fecha_modificada


def get_random_boolean():
    """Generates a random boolean value."""
    return random.choice([True, False])


def generate_random_rfc():
    """Generates a random RFC."""
    rfc_first_part = "".join(random.choices(string.ascii_uppercase, k=3))
    rfc_date_part = f"{random.randint(50, 99):02d}{random.randint(1, 12):02d}{random.randint(1, 31):02d}"
    rfc_homoclave = "".join(random.choices(string.ascii_uppercase + string.digits, k=3))
    return f"{rfc_first_part}{rfc_date_part}{rfc_homoclave}"


def generate_random_curp():
    """Generates a random CURP."""
    first_part = "".join(random.choices(string.ascii_uppercase, k=4))
    date_part = f"{random.randint(50, 99):02d}{random.randint(1, 12):02d}{random.randint(1, 31):02d}"
    homoclave = "".join(random.choices(string.ascii_uppercase + string.digits, k=8))
    return f"{first_part}{date_part}{homoclave}"


def generate_negative_number() -> int:
    """Genera un número negativo aleatorio.

    :return: Un número negativo aleatorio.
    """
    return random.randint(-1000, -1)


def generate_time_with_format(format="%H:%M:%S") -> str:
    """Genera la hora actual en formato HH:MM.

    Retorna:
        str: La hora actual en formato de cadena (HH:MM).
    """
    hora_actual = datetime.now()
    return hora_actual.strftime(format)


def get_dotenv():
    """Loads and returns environment variables."""
    load_dotenv()
    env_path = Path(__file__).parent.parent / ".env"
    variables_entorno = dotenv_values(env_path)
    config = {variable: value for variable, value in variables_entorno.items()}
    objeto = SimpleNamespace(**config)
    return objeto


def plural_to_singular(palabra: str) -> str:
    """Converts a Spanish word from plural to singular."""
    palabra = palabra.lower()

    # Reglas comunes (de más específicas a más generales)
    if palabra.endswith("iones"):
        return re.sub("iones$", "ión", palabra)
    elif palabra.endswith("ciones"):
        return re.sub("ciones$", "ción", palabra)
    elif palabra.endswith("eres"):
        return re.sub("eres$", "er", palabra)
    elif palabra.endswith("ces"):
        return re.sub("ces$", "z", palabra)
    elif palabra.endswith("es") and len(palabra) > 4 and not palabra.endswith("ses"):
        return palabra[:-2]
    elif palabra.endswith("s") and not palabra.endswith("is") and len(palabra) > 3:
        return palabra[:-1]
    return palabra


def generate_random_state():
    """Returns a random state."""
    estados = [
        "Sonora",
    ]

    return random.choice(estados)


def generate_random_municipio(estado):
    """Returns a random municipality for the given state."""
    municipios = {
        "Sonora": ["Agua prieta"],
    }

    return random.choice(municipios[estado])


def get_random_postal_code(municipio):
    """Returns a postal code for the given municipality."""
    codigos_postales = {"Agua prieta": ["84269"]}

    return random.choice(codigos_postales[municipio])


def camel_to_snake(s: str) -> str:
    """Converts a camelCase string to snake_case."""
    return re.sub(r"(?<!^)(?=[A-Z])", "_", s).lower()


def get_random_value_from_list(values: list):
    """Returns a random value from the provided list."""
    return random.choice(values)


def get_prioritized_value_from_list(
    allowed_values: list, prioritized_values: list = None, priority_percentage: float = 0.7
):
    """Selecciona un valor de la lista allowed_values con priorización opcional.

    Args:
        allowed_values (list): Lista de valores permitidos
        prioritized_values (list, optional): Lista de valores que tienen prioridad
        priority_percentage (float): Probabilidad (0.0-1.0) de seleccionar un valor priorizado

    Returns:
        str: Valor seleccionado de la lista

    Examples:
        >>> # Sin priorización (comportamiento normal)
        >>> get_prioritized_value_from_list(['A', 'B', 'C'])
        'B'  # aleatorio

        >>> # Con priorización
        >>> get_prioritized_value_from_list(['A', 'B', 'C'], ['A'], 0.8)
        'A'  # 80% de probabilidad de ser 'A'
    """
    if not allowed_values:
        raise ValueError("La lista allowed_values no puede estar vacía")

    # Si no hay valores priorizados o están vacíos, usar selección aleatoria normal
    if not prioritized_values:
        return random.choice(allowed_values)

    # Filtrar valores priorizados que existen en allowed_values
    valid_prioritized = [val for val in prioritized_values if val in allowed_values]

    # Si no hay valores priorizados válidos, usar selección aleatoria normal
    if not valid_prioritized:
        return random.choice(allowed_values)

    # Decidir si usar valor priorizado o aleatorio
    if random.random() < priority_percentage:
        return random.choice(valid_prioritized)
    else:
        return random.choice(allowed_values)


def generate_value_from_pattern(pattern: str, flags: int = 0) -> str:
    r"""Generates a random value that matches a given regex pattern.

    Args:
        pattern (str): The regex pattern (e.g., r'^[A-Z]{3}\d{3}$').
        flags (int): Regex flags (re.IGNORECASE, re.MULTILINE, etc.).

    Returns:
        str: A generated string that matches the pattern.
    """
    # Remove anchors (^ and $) if they exist, for more flexibility
    pattern_without_anchors = re.sub(r"^\^|\$$", "", pattern)

    # Apply flags to the pattern by compiling it first
    try:
        if flags:
            # Compile pattern with flags, then use the compiled regex
            compiled_pattern = re.compile(pattern_without_anchors, flags)
            value = rstr.xeger(compiled_pattern.pattern)
        else:
            value = rstr.xeger(pattern_without_anchors)
        return value
    except Exception as e:
        raise ValueError(f"Could not generate a value for the pattern {pattern!r} with flags {flags}: {e}")


def regex_flags_from_str(flags_str: str) -> int:
    """Convierte un string de flags en el valor int combinado de re flags.

    Args:
        flags_str (str): String con letras de flags (ej: "IM" para IGNORECASE + MULTILINE)

    Returns:
        int: Valor combinado de flags de re (usando OR bit a bit)

    Examples:
        >>> regex_flags_from_str("I")
        2  # re.IGNORECASE
        >>> regex_flags_from_str("IM")
        10  # re.IGNORECASE | re.MULTILINE
        >>> regex_flags_from_str("")
        0  # Sin flags
    """
    if not flags_str:
        return 0

    mapping = {
        RegexFlag.I: re.IGNORECASE,
        RegexFlag.M: re.MULTILINE,
        RegexFlag.S: re.DOTALL,
        RegexFlag.U: re.UNICODE,
        RegexFlag.A: re.ASCII,
        RegexFlag.X: re.VERBOSE,
    }

    result = 0
    for char in flags_str.upper():
        if char in mapping:
            result |= mapping[char]
    return result


def generate_random_url():
    """Generates a random URL.

    Returns:
        str: A randomly generated URL.
    """
    domains = ["com", "org", "net", "io", "tech"]
    domain_name = generate_random_string(8).lower()
    domain_extension = random.choice(domains)
    return f"https://www.{domain_name}.{domain_extension}"
