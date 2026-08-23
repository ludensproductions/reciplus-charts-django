import json
import os
import re
from pathlib import Path
from urllib.parse import urljoin

import pytest
from dotenv import load_dotenv
from pages import page_helper
from playwright.async_api import Page

from utils.eiu_generator_utils import (
    format_image_path,
    get_bar_info,
    get_button_info,
    get_element_info,
    get_special_elements_info,
    get_table_info,
    process_modal,
)

load_dotenv()

url_proyecto = os.getenv("URL_PROYECTO")
user_administrador = os.getenv("USER_ADMIN")
user_admin_password = os.getenv("PASSWORD_ADMIN")

path = Path(__file__).parent.resolve() / "urls_json" / "fixed_urls.json"
with open(path, "r", encoding="utf-8") as json_file:
    urls_data = json.load(json_file)

all_elements_data = {}


@pytest.mark.parametrize(
    "user, password",
    [
        pytest.param(user_administrador, user_admin_password, id="test"),
    ],
)
@pytest.mark.asyncio
async def test_eiu(page: Page, user: str, password: str):
    page = await page_helper.login_admin(page, user, password)

    for url in urls_data:
        process_other_elements = await process_url(page, url)
        if process_other_elements:
            await process_elements(page, url)
            await process_buttons(page, url)
            await process_tables(page, url)
            await process_bar(page, url)
            await process_special_items(page, url)
    path_elements = Path(__file__).parent.resolve() / "images" / "elements_data.json"
    with open(path_elements, "w", encoding="utf-8") as json_file:
        json.dump(all_elements_data, json_file, ensure_ascii=False, indent=4)


def add_element(
    url,
    elemento,
    tipo="N/A",
    longitud="N/A",
    nivel_acceso="L",
    descripcion="Descripción no encontrada",
    formulas="N/A",
    precisiones="N/A",
):
    if url not in all_elements_data:
        all_elements_data[url] = {"campos": []}
    all_elements_data[url]["campos"].append(
        {
            "Elemento": elemento,
            "Tipo": tipo,
            "Longitud": longitud,
            "Nivel de acceso": nivel_acceso,
            "Descripción del campo": descripcion,
            "Fórmulas": formulas,
            "Precisiones": precisiones,
        }
    )


async def process_action(page: Page, url: str, action: str, url_prefix: str):
    new_url = url.replace(f"/{url_prefix}/1", "").rstrip("/")
    destination_url = urljoin(url_proyecto, new_url)
    if action == "Habilitar":
        destination_url = destination_url.rstrip("/") + "/disabled"
    elif action == "Eliminar":
        destination_url = destination_url.rstrip("/")
    await page.goto(destination_url)
    link = page.locator(f'a[title="{action}"]').first
    await link.click()
    elements = await process_modal(page, url)
    if elements:
        for element in elements:
            add_element(*element)


async def process_url(page: Page, url: str):
    if "enable/1" in url:
        await process_action(page, url, "Habilitar", "enable")
        return False
    elif "delete/1" in url:
        await process_action(page, url, "Eliminar", "delete")
        return False
    else:
        formated_url = format_image_path(url)
        await page.goto(url_proyecto + url)
        await page.screenshot(path=formated_url)
        h1 = page.locator("h1")
        raw_text = await h1.text_content()
        clean_text = re.sub(r"\s+", " ", raw_text.strip())
        if clean_text:
            add_element(
                url,
                clean_text,
                tipo="Alfanumérico",
                nivel_acceso="L",
                descripcion="Texto que indica el título del formulario",
            )
        return True


async def process_elements(page, url):
    elements = page.locator("label, input, select, file, textarea, h2")

    for i in range(await elements.count()):
        element = elements.nth(i)
        data_processed = await get_element_info(page, element, url)
        if data_processed:
            add_element(*data_processed)


async def process_buttons(page, url):
    buttons = page.locator("button")
    for i in range(await buttons.count()):
        button = buttons.nth(i)
        data_processed = await get_button_info(button, url)
        if data_processed:
            add_element(*data_processed)


async def process_tables(page, url):
    index_table = page.locator("table")
    if index_table:
        table_columns = page.locator("th")
        for i in range(await table_columns.count()):
            column = table_columns.nth(i)
            data_processed = await get_table_info(column, url)
            if data_processed:
                add_element(*data_processed)


async def process_bar(page, url):
    links = page.locator("a")
    for i in range(await links.count()):
        link = links.nth(i)
        data_processed = await get_bar_info(link, url)
        if data_processed:
            add_element(*data_processed)


async def process_special_items(page, url):
    special_elements = await get_special_elements_info(page, url)
    for element in special_elements:
        if element:
            add_element(*element)
