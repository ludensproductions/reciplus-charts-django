import json
import re
from pathlib import Path


def format_image_path(url: str) -> str:
    """Generates a file path for saving a screenshot based on a given URL.

    The method extracts relevant parts of the URL and constructs a structured path
    where the image will be stored. If the URL contains specific keywords like
    'create', 'edit', 'detail', etc., the image name corresponds to that section.

    Args:
        url (str): The URL to be converted into an image path.

    Returns:
        str: The formatted file path for storing the screenshot.

    Examples:
        format_image_path("https://example.com/dashboard/create")
        -> "images/dashboard/create.png"

        format_image_path("https://example.com/users/edit")
        -> "images/users/edit.png"

        format_image_path("https://example.com/settings")
        -> "images/settings/index.png"
    """
    parts = url.strip("/").split("/")

    for keyword in ["create", "edit", "detail", "disabled", "delete", "enable"]:
        if keyword in parts:
            idx = parts.index(keyword)
            return f"images/{'/'.join(parts[:idx])}/{keyword}.png"

    if len(parts) == 2:
        return f"images/{'/'.join(parts)}/index.png"

    if len(parts) == 1:
        return f"images/{parts[0]}/index.png"

    return f"images/{url}.png"


async def evaluate_hidden(element):
    """Checks if an element is hidden."""
    return await element.is_hidden()


async def get_element_info(page, element, url):
    """Retrieves information about a page element."""
    tag_name = await element.evaluate("(el) => el.tagName.toLowerCase()")

    if await evaluate_hidden(element):
        return None

    if tag_name == "h2" and "detail" in url:
        return await get_h2_info(element, url)

    if tag_name == "label" and ("detail" in url or "edit" in url):
        return await get_label_info(element, url)

    input_id = await element.get_attribute("id")
    if tag_name == "input":
        return await get_input_info(page, element, url, input_id)

    if tag_name == "select":
        return await get_select_info(page, element, url, input_id)

    if tag_name == "textarea":
        return await get_textarea_info(page, element, url, input_id)


async def get_h2_info(element, url):
    """Extracts information from an h2 element."""
    h2_text = (await element.text_content() or "Etiqueta no encontrada").strip()
    element_class = await element.get_attribute("class")
    element_class_id = await element.get_attribute("id")
    if "form-label mb-3 text-break" not in element_class and element_class_id != "logoutModalLabel":
        return (
            url,
            h2_text,
            "Alfanumérico",
            "N/A",
            "L",
            f"Título de la tabla informativa de {h2_text.lower()}",
        )
    return None


async def get_label_info(label, url):
    """Extracts information from a label element."""
    label_text = (await label.text_content() or "Etiqueta no encontrada").strip()
    element_class = await label.get_attribute("class")
    if "form-label mb-3 text-break" in element_class or ("edit" in url and await label.get_attribute("for")):
        return None
    return (
        url,
        label_text,
        "Alfanumérico",
        "N/A",
        "L",
        f"Campo que muestra el campo {label_text.lower()}",
    )


async def get_input_info(page, input_element, url, input_id):
    """Extracts information from an input element."""
    label_for = await page.query_selector(f'label[for="{input_id}"]')
    input_display_name = (
        (await label_for.text_content() or "").strip().replace("*", "").replace(":", "")
        if label_for
        else await input_element.get_attribute("placeholder")
    )
    input_type = await input_element.get_attribute("type")
    input_name = await input_element.get_attribute("name")

    # configs custom
    if input_type == "hidden" or input_name in ["csrfmiddlewaretoken"] or input_display_name is None:
        return None
    if input_type == "checkbox" and input_id == "Habilitado":
        return None

    input_type_map = {
        "text": ("Alfanumérico", "255"),
        "checkbox": ("Checkbox", "N/A"),
        "date": ("Fecha", "N/A"),
        "number": ("Númerico", "N/A"),
    }
    input_type, longitud = input_type_map.get(input_type, (input_type, "N/A"))
    input_nivel_acceso = "S" if input_type == "Checkbox" else "E"
    action = "filtrar por" if "index" in url else "ingresar"
    return (
        url,
        input_display_name,
        input_type,
        longitud,
        input_nivel_acceso,
        f"Campo que permite {action} {input_display_name.lower()}",
    )


async def get_select_info(page, select, url, input_id):
    """Extracts information from a select element."""
    select_name = await select.get_attribute("name")
    if select_name:
        # configs custom
        if select_name == "status":
            input_display_name = "Estado"
        else:
            label_for = await page.query_selector(f'label[for="{input_id}"]')
            if label_for:
                input_display_name = (await label_for.text_content() or "").strip().replace("*", "").replace(":", "")
            else:
                input_display_name = await select.get_attribute("placeholder")
            select_id = await select.get_attribute("id")
            input_display_name = await format_name_with_no_placeholder(
                page, input_display_name, select_name, select_id
            )
        action = "filtrar por" if "index" in url else "seleccionar"
        return (
            url,
            input_display_name,
            "Select",
            "N/A",
            "S",
            f"Campo que permite {action} {input_display_name.lower()}",
        )


async def get_textarea_info(page, textarea, url, input_id):
    """Extracts information from a textarea element."""
    label_for = await page.query_selector(f'label[for="{input_id}"]')
    if label_for:
        textarea_name = (await label_for.text_content() or "").strip().replace("*", "").replace(":", "")
    else:
        textarea_name = await textarea.get_attribute("placeholder")
    if textarea_name:
        if re.search(r"[^a-zA-Z0-9\s]", textarea_name):
            return None
        return (
            url,
            textarea_name,
            "Select",
            "65535",
            "S",
            f"Campo que permite ingresar {textarea_name.lower()}",
        )


async def get_special_elements_info(page, url):
    """Retrieves information about special elements on the page."""
    parts = url.strip("/").split("/")
    if len(parts) != 2 and "disabled" not in parts:
        return None, None, None, None, None, None, None

    # configs custom
    elements_info = {
        "Habilitado": (
            "#Habilitado",
            "Checkbox",
            "Campo que permite habilitar o deshabilitar",
        ),
        "Habilitar": ("#Habilitar", "Botón", "Campo que permite habilitar"),
        "Habilitar (link)": (
            'a[title="Habilitar"]',
            "Botón",
            "Campo que permite habilitar",
        ),
        "Detalles": ('a[title="Detalle"]', "Botón", "Botón que permite ver el detalle"),
        "Editar": ('a[title="Editar"]', "Botón", "Botón que permite editar"),
        "Eliminar": ('a[title="Eliminar"]', "Botón", "Botón que permite eliminar"),
        "Deshabilitar": (
            'a[title="Deshabilitar"]',
            "Botón",
            "Botón que permite eliminar",
        ),
        "Configurar carril": (
            'a[title="Configurar carril"]',
            "Botón",
            "Botón que permite ingresar a configurar carril",
        ),
        "Desconectar usuarios del kiosko": (
            'button[title="Desconectar usuarios del kiosko"]',
            "Botón",
            "Botón que permite desconectar usuarios del kiosko",
        ),
    }

    results = []
    for name, (selector, element_type, description) in elements_info.items():
        element = await page.query_selector(selector)
        if element:
            results.append((url, name, element_type, "N/A", "S", description))
        else:
            results.append(None)

    return tuple(results)


async def get_button_info(button, url):
    """Extracts information from a button element."""
    if await evaluate_hidden(button):
        return None
    omit_buttons = {"Cerrar sesión", "0", ">", ">>"}
    raw_text = (await button.text_content() or "").strip()
    clean_text = re.sub(r"\s+", " ", raw_text)
    boton_id = await button.get_attribute("id")
    if boton_id == "plus_button":
        return url, "+", "Botón", "N/A", "S", "Botón que permite agregar un registro"
    if (
        clean_text
        and clean_text not in omit_buttons
        and clean_text.isalpha()
        and not re.match(r"Página 1 de", clean_text)
        and not re.match(r"[^a-zA-Z0-9\s]", clean_text)
    ):
        return (
            url,
            raw_text,
            "Botón",
            "N/A",
            "S",
            f"Botón que permite {clean_text.lower()}",
        )


async def get_table_info(column, url):
    """Extracts information from a table column."""
    if await evaluate_hidden(column):
        return None
    raw_text = await column.text_content()
    clean_text = re.sub(r"\s+", " ", raw_text.strip())
    if clean_text:
        return (
            url,
            raw_text.strip(),
            "Alfanumérico",
            "N/A",
            "L",
            f"Campo que muestra {clean_text.lower()} en la tabla",
        )


async def get_bar_info(link, url):
    """Extracts information from a bar link."""
    if await evaluate_hidden(link):
        return None
    # configs custom
    path = Path(__file__).parent.parent.resolve() / "urls_json" / "omit.json"
    with open(path, "r", encoding="utf-8") as f:
        config = json.load(f)
        omit_links = config.get("omit_links", [])
    raw_text = await link.text_content()
    clean_text = re.sub(r"\s+", " ", raw_text.strip())

    if (
        clean_text
        and clean_text not in omit_links
        and not re.match(r"Página 1 de", clean_text)
        and not re.match(r"[^a-zA-Z0-9\s]", clean_text)
    ):
        parts = url.strip("/").split("/")
        return (
            url,
            raw_text.strip(),
            "Botón",
            "N/A",
            "S",
            f"Botón que permite {'ingresar a ' if len(parts) == 1 else ''}{clean_text.lower()}",
        )


async def format_name_with_no_placeholder(page, input_display_name, select_name, select_id):
    """Formats the name of an element when no placeholder is available."""
    if not input_display_name:
        element = await page.query_selector(f"#{select_id}")
        if not element:
            return select_name

        label = await element.evaluate_handle("(el) => el.previousElementSibling")
        if label:
            label_text = await label.text_content()
            return label_text.strip().replace("*", "").replace(":", "")
        else:
            return select_name
    return input_display_name


async def process_modal(page, url: str):
    """Processes a modal and extracts its elements."""
    await page.wait_for_timeout(3000)
    formated_url = format_image_path(url)
    await page.screenshot(path=formated_url)

    modal_content = page.locator(".modal-content").filter(has_not=page.locator("[hidden]")).first

    modal_elements = await extract_modal_elements(modal_content, url)
    return modal_elements


async def extract_modal_elements(modal_content, url):
    """Extracts elements from a modal content."""
    elements = []

    h2 = modal_content.locator("h2").first
    modal_title = await h2.text_content()
    clean_modal_title = re.sub(r"\s+", " ", modal_title.strip())
    elements.append(
        (
            url,
            clean_modal_title,
            "Alfanumérico",
            "N/A",
            "L",
            "Texto que indica el título del modal",
        )
    )

    label_justificacion = modal_content.locator('label[for="id_justificacion"]')
    if await label_justificacion.count() > 0:
        justificacion_text = await label_justificacion.text_content()
        clean_justificacion_text = re.sub(r"\s+", " ", justificacion_text.strip())
        elements.append(
            (
                url,
                clean_justificacion_text,
                "Texto largo",
                "N/A",
                "S",
                "Campo de justificación del modal",
            )
        )

    botones_modal = modal_content.locator("button")
    for i in range(await botones_modal.count()):
        boton = botones_modal.nth(i)
        boton_text = await boton.text_content()
        clean_boton_text = re.sub(r"\s+", " ", boton_text.strip())
        if await boton.get_attribute("class") == "btn-close":
            elements.append((url, "X", "Botón", "N/A", "S", "Botón que cierra el modal"))
        else:
            elements.append(
                (
                    url,
                    clean_boton_text,
                    "Botón",
                    "N/A",
                    "S",
                    f"Botón que permite {clean_boton_text.lower()} en el modal",
                )
            )

    return elements
