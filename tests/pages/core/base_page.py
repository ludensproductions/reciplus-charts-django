import inspect
import logging
import os
import re
import time

from dotenv import load_dotenv
from playwright.async_api import Page, TimeoutError as PlaywrightTimeoutError, expect

from utils.catch_error_wrapper import catch_test_failures
from utils.strategies.inputs_class_strategies.input_strategy_factory import StrategyFactory

load_dotenv()

logger = logging.getLogger(__name__)


class BasePage:
    """Generic Playwright base page that centralizes shared behaviors for custom test automation.

    This class holds a Playwright `Page` instance, common UI selectors (e.g., a
    "remove all" control for Select2 widgets), and a `StrategyFactory` used by
    downstream interaction strategies. Subclasses benefit from an automatic
    error-handling wrapper applied to their coroutine methods at class creation time.

    Attributes:
        page (Page): The Playwright page used to drive UI interactions.
        remove_options_select2 (str): CSS selector for clearing all items in Select2.
        factory (StrategyFactory): Factory for building interaction/validation strategies.
        cleanup_tests_on_failure (bool): Class attribute that controls whether to cleanup on test failures.
    """

    # Atributo de clase: se lee una vez al cargar la clase
    cleanup_tests_on_failure = os.getenv("CLEANUP_TESTS_ON_FAILURE", "false").lower() == "true"

    def __init__(self, page: Page):
        """Initializes the BasePage with a Playwright `Page` instance.

        Args:
            page (Page): The Playwright page used to drive UI interactions.

        Side Effects:
            - Sets the Select2 "remove all items" selector.
            - Instantiates a `StrategyFactory` for strategy-based operations.
        """
        self.page = page
        self.remove_options_select2 = 'button[title="Remove all items"]'
        self.factory = StrategyFactory()

    def __init_subclass__(cls, **kwargs):
        """Class initialization hook that decorates coroutine methods on subclasses.

        When a subclass of `BasePage` is defined, all of its coroutine functions
        (`async def`) are automatically wrapped with `catch_test_failures` to provide
        consistent failure reporting—except for methods explicitly skipped in
        `functions_to_skip` (currently `["delete_record"]`).

        Args:
            **kwargs: Arbitrary keyword arguments provided by Python during subclass creation.

        Notes:
            - Decoration happens at class definition time (not at instance creation).
            - Only coroutine functions are wrapped; regular (sync) methods are left untouched.
        """
        functions_to_skip = ["delete_record"]
        if cls.cleanup_tests_on_failure:
            for name, func in inspect.getmembers(cls, inspect.iscoroutinefunction):
                if name not in functions_to_skip:
                    setattr(cls, name, catch_test_failures(func))

    async def fill_data(self, data: dict, page: Page = None):
        """Populates form fields with the provided data for creation, editing, or filtering.

        This method identifies the type of each field (input, select, checkbox, etc.) and fills
        the corresponding values based on the input data.

        Args:
            data (dict): A dictionary where keys are field selectors and values are the values to fill in.
            page (Page): Optional Playwright page instance. Uses self.page if not provided.

        Example:
            await fill_data({
                'input[name="username"]': 'john_doe',
                'input[name="accept_terms"]': True,
                'select[name="country"]': 'USA',
                'input[type="file"]': 'path/to/file.txt'
            })

            **This fills in the username, checks the terms acceptance, selects a country, and uploads a file.**

        The method performs the following actions for each field:
            - For file inputs, it sets the file to be uploaded.
            - For radio buttons, it checks the button if the value matches.
            - For checkboxes, it checks or unchecks based on the boolean value provided.
            - For buttons that require multiple clicks, it iterates over a list of values.
            - For select elements, it selects the appropriate option.
            - For text inputs, textareas, and date/time inputs, it fills in the provided value.
            - For any other input types, it attempts to click on the corresponding select2 options if applicable.

        Note:
            - This method assumes that the user is already on the form page where the fields are located.
            - Ensure that the provided keys in the `data` dictionary match the selectors for the fields on the form.
        """
        for field_name, value in data.items():
            logger.debug(f"Filling field '{field_name}' with value '{value}'")

            await self.wait_for_selector(field_name)
            field_input = self.page.locator(field_name)
            first_element = field_input.first

            tag_name = await first_element.evaluate("el => el.tagName")
            input_type = await first_element.evaluate("el => el.type")
            idselect2 = await first_element.evaluate(
                'el => el.getAttribute("data-select2-id") || (el.querySelector("[data-select2-id]") !== null)'
            )

            has_contenteditable = await first_element.evaluate(
                "el => el.querySelector(\"div[contenteditable='true']\") !== null"
            )
            has_multiple_attr = await first_element.evaluate(
                'el => el.hasAttribute("multiple") || el.querySelector("input[multiple]") !== null'
            )

            strategy = self.factory.get_strategy(
                input_type,
                tag_name,
                idselect2,
                has_contenteditable,
                has_multiple_attr,
            )

            await strategy.fill(
                field_input=field_input,
                value=value,
                page=self.page,
                field_name=field_name,
                fill_data_method=self.fill_data,
                remove_options_select2=self.remove_options_select2,
            )

    async def validate_record_information_in_edit_view(self, data_validate: dict, page: Page = None):
        """Validate record information in the edit view.

        Compares the expected values with the actual values displayed in the form fields.

        Args:
            data_validate (dict): A dictionary where keys are field selectors and values are
                                the expected values for validation.
            page (Page): Si manejas más de una pestaña puedes mandar el page de la página donde necesites aplicar este método.

        Example:
            data_validate = {
                'input[name="title"]': 'Test Title',
                'input[name="year"]': '2023',
                'input[name="is_active"]': True,
                'select[name="genre"]': 'Action'
            }

            **await validate_edit_view_item_information(data_validate)**

        This method performs the following checks:
            1. Iterates through the `data_validate` dictionary to validate each field.
            2. For each field, it retrieves the current value and compares it to the expected value:
                - For `<SELECT>` fields, it checks the selected option.
                - For `<INPUT>` fields:
                    - Checks if a checkbox or radio button is checked/unchecked based on expected value.
                    - For other input types, it checks the value against the expected value.
                - If the expected value is a list, it validates each item with a separate method.
                - If the expected value is a set, it checks the visibility of each option in a select dropdown.
            3. Raises an assertion error if the actual value does not match the expected value for any field.

        Note:
            - Ensure that the field selectors in the `data_validate` dictionary accurately correspond
            to the elements in the edit view.
            - This method assumes that the user is already on the edit view of the record.
        """
        page = page or self.page

        for field_name, expected_value in data_validate.items():
            field_input = page.locator(field_name)
            tag_name = await field_input.evaluate("el => el.tagName")
            logger.debug(f"Validating file field '{field_name}': expected '{expected_value}' in tag '{tag_name}'")

            if tag_name == "SELECT":
                await expect(
                    field_input, message=f"Error en {field_name}: se esperaba opción '{expected_value}' en el SELECT."
                ).to_contain_text(expected_value)

            elif tag_name == "INPUT":
                input_type = await field_input.evaluate("el => el.type")

                if input_type == "checkbox":
                    if expected_value:
                        await expect(
                            field_input,
                            message=f"Error en {field_name}: se esperaba que el checkbox estuviera seleccionado.",
                        ).to_be_checked()
                    else:
                        await expect(
                            field_input,
                            message=f"Error en {field_name}: se esperaba que el checkbox NO estuviera seleccionado.",
                        ).not_to_be_checked()

                elif input_type == "radio":
                    if expected_value:
                        await expect(
                            field_input,
                            message=f"Error en {field_name}: se esperaba que el radio button estuviera seleccionado.",
                        ).to_be_checked()
                    else:
                        await expect(
                            field_input,
                            message=f"Error en {field_name}: se esperaba que el radio button NO estuviera seleccionado.",
                        ).not_to_be_checked()

                elif input_type == "number":
                    actual_value = await field_input.input_value()
                    assert float(actual_value) == float(expected_value), (
                        f"Error en {field_name}: se esperaba número '{expected_value}', "
                        f"pero se encontró '{actual_value}'."
                    )

                elif input_type == "file":
                    # Para campos FILE, el valor está en un <a> adyacente dentro del contenedor padre
                    # Estructura: #div_id_X > div.input-group > div > span > a
                    import os

                    # Obtener el contenedor padre del input (usualmente tiene id="div_id_X")
                    parent_id = await field_input.evaluate("el => el.closest('[id^=\"div_id_\"]')?.id")

                    if parent_id:
                        # Buscar el enlace dentro del contenedor
                        file_link_selector = f"#{parent_id} a"
                        file_link = page.locator(file_link_selector)

                        if await file_link.count() > 0:
                            # Extraer el nombre del archivo del href
                            href = await file_link.get_attribute("href")
                            actual_filename = os.path.basename(href) if href else ""

                            assert expected_value in actual_filename or actual_filename in expected_value, (
                                f"Error en {field_name}: validación de archivo falló.\n"
                                f"Se esperaba: '{expected_value}'\n"
                                f"Se encontró: '{actual_filename}'\n"
                                f"Href completo: '{href}'"
                            )
                        else:
                            # No hay archivo cargado (campo vacío)
                            logger.warning(f"File field '{field_name}' has no file loaded (empty field)")
                    else:
                        logger.warning(f"Could not find parent container for file field '{field_name}'")

                else:
                    if isinstance(expected_value, list):
                        actual_value = await field_input.input_value()
                        for value in expected_value:
                            assert actual_value == value, (
                                f"Error en {field_name}: se esperaba uno de {expected_value}, "
                                f"pero se encontró '{actual_value}'."
                            )
                    else:
                        actual_value = await field_input.input_value()
                        await expect(
                            field_input,
                            message=f"Error en {field_name}: se esperaba '{expected_value}', pero se encontró '{actual_value}'.",
                        ).to_have_value(expected_value)

            elif tag_name == "SPAN" and isinstance(expected_value, set):
                for option in expected_value:
                    option_locator = page.locator(f'.select2-results__option:has-text("{option}")')
                    await expect(
                        option_locator,
                        message=f"Error en {field_name}: se esperaba que la opción '{option}' fuera visible en el dropdown.",
                    ).to_be_visible()

            elif isinstance(expected_value, list):
                for fila_data in expected_value:
                    await self.validate_record_information_in_edit_view({field_name: fila_data}, page=page)

    async def validate_record_information_in_details_view(self, data_validate: dict, page: Page = None):
        """Validate record information on the details view page.

        Compares the expected values with the actual values shown in the UI.

        Args:
            data_validate (dict): A dictionary where keys are selectors for the fields to validate
                                and values are the expected values.
            page (Page): Si manejas más de una pestaña puedes mandar el page de la página donde necesites aplicar este método.

        Example:
            data_validate = {
                'label[name="title"]': 'Test Title',
                'td[name="year"]': '2023',
                'p[name="status"]': {'Active', 'Pending'}
            }

            **await validate_record_information_in_details_view(data_validate)**

        This method performs the following checks:
            1. Iterates through the `data_validate` dictionary to validate each field's value.
            2. For each expected value:
                - If the expected value is a set, it checks that each value is present in the UI using various selectors.
                - Otherwise, it checks that the expected value is present in the UI for the corresponding selector.
            3. Raises an assertion error if the actual value does not match the expected value for any field.

        Note:
            - This method assumes that the user is already on the details view page of the record.
            - Ensure that the field selectors in the `data_validate` dictionary correspond accurately
            to the elements in the details view of the record.
        """
        page = page or self.page

        for field_name, expected_value in data_validate.items():
            logger.debug(
                f"Validating field '{field_name}' with expected value {expected_value} type {type(expected_value)}"
            )

            # Intentar validar como archivo/imagen primero
            # Intentamos extraer el nombre del archivo del href/src del elemento
            if isinstance(expected_value, str):
                file_validated = await self._try_validate_file_or_image(field_name, expected_value)
                if file_validated:
                    continue

            if isinstance(expected_value, (set, list)):
                for value in expected_value:
                    use_regex = bool(re.search(r"[^\w\s]", value))
                    if use_regex:
                        # Escapa caracteres especiales y usa una expresión regular
                        safe_value = re.escape(value)
                        await self.validate_value_with_regex(field_name, safe_value, value)
                    else:
                        await self.validate_values(field_name, value)

            # Case 2: If the value it's a dict, for the select2 cases
            elif isinstance(expected_value, dict):
                for sub_selector, sub_values in expected_value.items():
                    if isinstance(sub_values, list):
                        for value in sub_values:
                            use_regex = bool(re.search(r"[^\w\s]", value))

                            if use_regex:
                                # Escapa caracteres especiales y usa una expresión regular
                                safe_value = re.escape(value)
                                await self.validate_value_with_regex(field_name, safe_value, expected_value)
                            else:
                                await self.validate_values(field_name, value)
                    else:
                        # Verifica si expected_value contiene caracteres especiales
                        use_regex = bool(re.search(r"[^\w\s]", sub_values))

                        if use_regex:
                            # Escapa caracteres especiales y usa una expresión regular
                            safe_value = re.escape(sub_values)
                            await self.validate_value_with_regex(field_name, safe_value, expected_value)
                        else:
                            await self.validate_values(field_name, sub_values)

            # Case 3: If the value it's a normal input, like an string
            elif expected_value:
                # Verifica si expected_value contiene caracteres especiales
                use_regex = bool(re.search(r"[^\w\s]", expected_value))

                if use_regex:
                    # Escapa caracteres especiales y usa una expresión regular
                    safe_value = re.escape(expected_value)
                    await self.validate_value_with_regex(field_name, safe_value, expected_value)
                else:
                    await self.validate_values(field_name, expected_value)

    def get_label_locator(self, name, expected_value):
        """Builds a composite Playwright locator for a label/value pair across common HTML tags.

        The method generates a locator for each of the following tags—"label", "a", "span",
        "td", "p", "th", "li", "div"—using `get_selector_for_validate_locator(name, tag, expected_value)`
        and OR-combines them into a single locator that matches if any tag variant is present.

        Args:
            name (str): The field or label name used to construct each tag-specific locator.
            expected_value (str): The text expected to be associated with the label/name.

        Returns:
            playwright.async_api.Locator: A locator representing the OR-combination of all
            supported tag variants.
        """
        tags = ["label", "a", "span", "td", "p", "th", "li", "div", "img"]
        label_locator = self.get_selector_for_validate_locator(name, tags[0], expected_value)

        for tag in tags[1:]:
            label_locator = label_locator.or_(self.get_selector_for_validate_locator(name, tag, expected_value))
        return label_locator

    async def validate_value_with_regex(self, name, safe_value, expected_value):
        """Validates that the text associated with `name` contains `expected_value`.

        Builds the composite locator via `get_label_locator(name, expected_value)` and asserts,
        using Playwright's `expect(...).to_contain_text`, that the element's text includes
        the provided `expected_value`.

        Args:
            name (str): The field or label name used to resolve the target locator.
            safe_value (str): A pre-sanitized version of the expected value (reserved for future use).
            expected_value (str): The text (or pattern) expected to be contained in the element.

        Raises:
            AssertionError: If the resolved element does not contain `expected_value`.
        """
        # Obtener el texto del elemento y hacer strip
        actual_value = await self.get_label_locator(name, expected_value).inner_text()
        actual_value = actual_value.strip()
        logger.debug(f"Comparing expected '{expected_value}' with actual '{actual_value}'")
        # Comparar de forma case-insensitive
        assert expected_value.lower() in actual_value.lower(), (
            f"La prueba falló al validar en los detalles.\n"
            f"Expected value: '{expected_value}'\n"
            f"Actual value: '{actual_value}'"
        )

    async def _try_validate_file_or_image(self, field_name: str, expected_filename: str) -> bool:
        """Try to validate a file or image field by extracting the filename from href/src.

        Extracts the actual filename from the media URL and compares it with the expected filename.
        Example: <a href="/media/evidences/LrhWaKhIhk.ods">evidences/LrhWaKhIhk.ods</a>
        Extracts: LrhWaKhIhk.ods

        Args:
            field_name: Name/title of the field
            expected_filename: Expected filename to validate

        Returns:
            True if validation succeeded, False if this is not a file/image field
        """
        # Try to find an image with the filename in its src attribute
        img_selector = f'div[title="{field_name.lower()}"] img'
        img_locator = self.page.locator(img_selector)

        try:
            if await img_locator.count() > 0:
                # Extract filename from src attribute
                src = await img_locator.get_attribute("src")
                # Extract just the filename from the path (e.g., "/media/evidences/file.jpg" -> "file.jpg")
                actual_filename = os.path.basename(src) if src else ""

                assert expected_filename in actual_filename or actual_filename in expected_filename, (
                    f"Image validation failed for field '{field_name}'.\n"
                    f"Expected filename: '{expected_filename}'\n"
                    f"Actual filename from src: '{actual_filename}'\n"
                    f"Full src: '{src}'"
                )
                return True
        except AssertionError:
            raise
        except Exception:
            # Not an image, try as file link
            pass

        # Try to find a file link (anchor tag)
        link_selector = f'div[title="{field_name.lower()}"] a'
        link_locator = self.page.locator(link_selector)

        try:
            if await link_locator.count() > 0:
                # Extract filename from href attribute
                href = await link_locator.get_attribute("href")
                # Extract just the filename from the URL (e.g., "/media/evidences/file.ods" -> "file.ods")
                actual_filename = os.path.basename(href) if href else ""

                assert expected_filename in actual_filename or actual_filename in expected_filename, (
                    f"File validation failed for field '{field_name}'.\n"
                    f"Expected filename: '{expected_filename}'\n"
                    f"Actual filename from href: '{actual_filename}'\n"
                    f"Full href: '{href}'"
                )
                return True
        except AssertionError:
            raise
        except Exception:
            # Not a file link
            pass

        # This is not a file/image field
        return False

    async def validate_values(self, name, expected_value):
        """Asserts that the UI element associated with `name` contains `expected_value`.

        Builds a composite locator via `get_label_locator(name, expected_value)` and verifies,
        using Playwright's `expect(...).to_contain_text`, that the element's text includes
        the provided `expected_value`.

        Args:
            name (str): Logical field/label name used to resolve the target locator.
            expected_value (str): Text expected to be contained in the element.

        Raises:
            AssertionError: If the resolved element does not contain `expected_value`.
        """
        await expect(self.get_label_locator(name, expected_value)).to_contain_text(expected_value)

    def get_selector_for_validate_locator(self, name, tag, value):
        """Return a locator for an element of type `tag` matching title and text.

        The locator matches elements whose `title` attribute equals `name.lower()` and whose
        text contains `value`.

        Args:
            name (str): Field/label name; its lowercase form is matched against the `title` attribute.
            tag (str): HTML tag to target (e.g., "label", "span", "td").
            value (str): Text that must be contained within the element.

        Returns:
            playwright.async_api.Locator: Locator matching the specified tag, title, and text.
        """
        # if tag == "img":
        #     return self.page.locator(f'div[title="{name.lower()}"] {tag}[alt*="{value}"]')

        return self.page.locator(f'{tag}[title="{name.lower()}"]', has_text=value)

    async def validate_record_information_in_index_view(
        self, data_validate: dict, index_many_results: bool = False, page: Page = None
    ):
        """Validate that all scalar values from a validation payload are visible in the index table.

        Behavior:
            - Recursively traverses `data_validate` (dicts, lists, sets) to extract scalar
            values.
            - Ignores falsy scalars (e.g., None, "", 0).
            - For each extracted value, asserts that a table cell (`td`) containing that
            text is visible.

        Args:
            data_validate (dict): Nested structure of expected values to verify in the table.
            page (Page, optional): Playwright page instance. Defaults to `self.page`.
            index_many_results (bool, optional): If True, applies a row-level filter to find a single matching row before validating values.

        Raises:
            AssertionError: If any expected value is not visible in a `td` cell.

        Notes:
            - Matching uses Playwright's `has_text` filter against `td` elements.
        """
        page = page or self.page

        def extract_values(obj, parent_key=""):
            """Recursively extract all scalar values from nested lists/sets/dicts with their keys."""
            if isinstance(obj, dict):
                for k, v in obj.items():
                    full_key = f"{parent_key}.{k}" if parent_key else k
                    yield from extract_values(v, full_key)
            elif isinstance(obj, (list, set)):
                for idx, v in enumerate(obj):
                    full_key = f"{parent_key}[{idx}]" if parent_key else f"[{idx}]"
                    yield from extract_values(v, full_key)
            elif obj:
                yield (parent_key, obj)

        values = list(extract_values(data_validate))

        if index_many_results:
            row = page.locator("tr")
            for _, expected_value in values:
                row = row.filter(has_text=expected_value)
            # Use .first since multiple rows may still match (e.g. a repeated single-field value)
            matching_row = row.first
            for field_name, expected_value in values:
                logger.debug(f"Validating field '{field_name}' with value '{expected_value}' in row (many results)")
                await expect(
                    matching_row.locator("td", has_text=expected_value),
                    message=f"Campo '{field_name}': Valor esperado no encontrado en la fila correcta: '{expected_value}'",
                ).to_be_visible(timeout=6000)
        else:
            for field_name, expected_value in values:
                logger.debug(f"Validating field '{field_name}' with value '{expected_value}' in index view")
                await expect(
                    page.locator("td", has_text=expected_value),
                    message=f"Campo '{field_name}': Valor esperado no encontrado en la tabla: '{expected_value}'",
                ).to_be_visible(timeout=6000)

    async def check_error_message(
        self,
        error_selectors: list[str],
        error_message: str,
        continue_button_selector: str = None,
        page: Page = None,
        timeout: int = 4000,
    ):
        """Valida la aparición de un mensaje de error en la interfaz de usuario y maneja la interacción con el modal si es necesario.

        Este método busca el texto de error especificado (`error_message`) en los contenedores indicados (`error_selectors`).
        La validación se realiza leyendo el texto visible (`inner_text`) del contenedor, lo que permite detectar el mensaje
        incluso si se encuentra dentro de elementos anidados (por ejemplo, dentro de un `<span>` o `<p>`).

        Comportamiento:
        - Si el mensaje aparece en alguno de los contenedores, se valida correctamente y el método finaliza sin errores.
        - Si el mensaje aparece dentro de un modal (coincide con `self.modal_message_selector`), se realiza automáticamente
        un clic en el botón indicado por `continue_button_selector` para cerrar el modal y continuar con el flujo de la prueba.
        - Si el mensaje no se encuentra en ninguno de los contenedores dentro del tiempo límite (`timeout`), se lanza un
        `AssertionError` detallado con la información de diagnóstico.

        Args:
            error_selectors (list[str]): Lista de selectores CSS donde se espera que aparezca el mensaje de error.
                                        Generalmente incluye:
                                        - `self.error_message_selector` → errores mostrados en la página principal.
                                        - `self.modal_message_selector` → errores mostrados dentro de un modal.
            error_message (str): Texto esperado del mensaje de error. Se valida como subcadena dentro del texto visible del contenedor.
            continue_button_selector (str): Selector CSS del botón "Continuar"/"Aceptar" dentro del modal, en caso de que el mensaje aparezca ahí.
            page (Page, opcional): Instancia de la página de Playwright. Por defecto utiliza `self.page` si no se proporciona.
            timeout (int, opcional): Tiempo máximo de espera en milisegundos para que el mensaje de error aparezca. Por defecto es 4000 ms.

        Raises:
            AssertionError: Si el mensaje de error no aparece en ninguno de los contenedores proporcionados dentro del tiempo especificado.

        Ejemplo:
            >>> await self.check_error_message(
            ...     error_selectors=[self.error_message_selector, self.modal_message_selector],
            ...     error_message="La ubicación es obligatoria.",
            ...     continue_button_selector=self.continue_button_selector
            ... )
        """
        page = page or self.page
        found_texts = {}  # Almacena el texto encontrado en cada selector

        for selector in error_selectors:
            try:
                await page.wait_for_selector(selector, state="visible", timeout=timeout)
                text = await page.locator(selector).inner_text()
                found_texts[selector] = text.strip()  # Guarda el texto encontrado

                if error_message in text:
                    # Si el error está dentro del modal, continuar automáticamente
                    if selector == self.modal_message_selector:
                        await page.click(continue_button_selector)
                    return

            except PlaywrightTimeoutError:
                found_texts[selector] = "Selector no visible (timeout)"
            except Exception as e:
                found_texts[selector] = f"Error al leer selector: {str(e)}"

        # Construir mensaje de error detallado con lo que se encontró
        error_details = "\n".join([f"  • {selector}:\n    → '{text}'" for selector, text in found_texts.items()])

        raise AssertionError(
            f"\nNo se encontró el mensaje de error esperado.\n\n"
            f"Mensaje buscado:\n  → '{error_message}'\n\n"
            f"Textos encontrados en los selectores:\n{error_details}\n"
        )

    async def wait_for_selector(self, selector, time_sleep=0.05, page: Page = None):
        """Wait for an element to be visible on the page.

        Args:
            selector (str): Selector of the element to wait for.
            time_sleep (float): Time to sleep after the selector is found (default: 0.05 seconds).
            page (Page): Optional Playwright page instance. Uses self.page if not provided.
        """
        page = page or self.page
        await page.wait_for_selector(selector)
        time.sleep(time_sleep)

    async def remove_required_attribute(self, selector, page: Page = None):
        """Remove the 'required' attribute from the provided element.

        Args:
            selector (any): Identifier of the element from which the attribute needs to be removed.
            page (Page): Si manejas más de una pestaña puedes mandar el page de la página donde necesites aplicar este método.
        """
        page = page or self.page
        await self.wait_for_selector(selector, page=page)
        # await page.eval_on_selector(selector, "el => el.removeAttribute('required')")
        # Verifica si el atributo 'required' existe antes de intentar eliminarlo
        await page.eval_on_selector(
            selector,
            """el => {
                if (el.hasAttribute('required')) {
                    el.removeAttribute('required');
                    return true; // Indica que el atributo fue eliminado
                }
                return false; // Indica que el atributo no existía
            }""",
        )

    async def remove_max_length_attribute(self, selector, page: Page = None):
        """Remove the 'maxlength' attribute from the provided element.

        Args:
            selector (any): Identifier of the element from which the attribute needs to be removed.
            page (Page): Si manejas más de una pestaña puedes mandar el page de la página donde necesites aplicar este método.
        """
        page = page or self.page
        await self.wait_for_selector(selector, page=self.page)
        await page.eval_on_selector(selector, "el => el.removeAttribute('maxlength')")

    async def remove_min_length_attribute(self, selector, page: Page = None):
        """Remove the 'minlength' attribute from the provided element.

        Args:
            selector (any): Identifier of the element from which the attribute needs to be removed.
            page (Page): Si manejas más de una pestaña puedes mandar el page de la página donde necesites aplicar este método.
        """
        page = page or self.page
        await self.wait_for_selector(selector, page=page)
        await page.eval_on_selector(selector, "el => el.removeAttribute('minlength')")

    async def remove_max_attribute(self, selector, page: Page = None):
        """Remove the 'max' attribute from the provided element.

        Args:
            selector (any): Identifier of the element from which the attribute needs to be removed.
            page (Page): Si manejas más de una pestaña puedes mandar el page de la página donde necesites aplicar este método.
        """
        page = page or self.page
        await self.wait_for_selector(selector, page=page)
        await page.eval_on_selector(selector, "el => el.removeAttribute('max')")

    async def remove_accept_attribute(self, selector, page: Page = None):
        """Function that removes the 'accept' attribute from the provided element.

        Args:
            selector (any): Identifier of the element from which the attribute needs to be removed.
            page (Page): Si manejas más de una pestaña puedes mandar el page de la página donde necesites aplicar este método.
        """
        page = page or self.page
        await self.wait_for_selector(selector, page=page)
        await page.eval_on_selector(selector, "el => el.removeAttribute('accept')")

    async def remove_min_attribute(self, selector, page: Page = None):
        """Remove the 'min' attribute from the provided element.

        Args:
            selector (any): Identifier of the element from which the attribute needs to be removed.
            page (Page): Si manejas más de una pestaña puedes mandar el page de la página donde necesites aplicar este método.
        """
        page = page or self.page
        await self.wait_for_selector(selector, page=page)
        await self.page.eval_on_selector(selector, "el => el.removeAttribute('min')")

    async def remove_type_attribute(self, selector, page: Page = None):
        """Remove the 'type' attribute from the provided element.

        Args:
            selector (any): Identifier of the element from which the attribute needs to be removed.
            page (Page): Si manejas más de una pestaña puedes mandar el page de la página donde necesites aplicar este método.
        """
        page = page or self.page
        await self.wait_for_selector(selector, page=page)
        await page.eval_on_selector(selector, "el => el.removeAttribute('type')")

    async def remove_pattern_attribute(self, selector, page: Page = None):
        """Remove the 'pattern' attribute from the provided element.

        Args:
            selector (any): Identifier of the element from which the attribute needs to be removed.
            page (Page): Si manejas más de una pestaña puedes mandar el page de la página donde necesites aplicar este método.
        """
        page = page or self.page
        await self.wait_for_selector(selector, page=page)
        await page.eval_on_selector(selector, "el => el.removeAttribute('pattern')")

    async def remove_disabled_attribute(self, selector, page: Page = None):
        """Remove the 'disabled' attribute from the provided element.

        Args:
            selector (any): Identifier of the element from which the attribute needs to be removed.
            page (Page): Si manejas más de una pestaña puedes mandar el page de la página donde necesites aplicar este método.
        """
        page = page or self.page
        await self.wait_for_selector(selector, page=page)
        await page.eval_on_selector(selector, "el => el.removeAttribute('disabled')")

    async def remove_readonly_attribute(self, selector, page: Page = None):
        """Remove the 'readonly' attribute from the provided element.

        Args:
            selector (any): Identifier of the element from which the attribute needs to be removed.
            page (Page): Si manejas más de una pestaña puedes mandar el page de la página donde necesites aplicar este método.
        """
        page = page or self.page
        await self.wait_for_selector(selector, page=page)
        await page.eval_on_selector(selector, "el => el.removeAttribute('readonly')")

    async def change_type_attribute(self, selector, page: Page = None):
        """Change the value of the 'type' attribute of the provided element.

        Args:
            selector (any): Identifier of the element for which the attribute value needs to be changed.
            page (Page): Si manejas más de una pestaña puedes mandar el page de la página donde necesites aplicar este método.
        """
        page = page or self.page
        await self.wait_for_selector(selector, page=page)
        await page.eval_on_selector(selector, "el => el.setAttribute('type', 'text')")

    async def hold_click(self, locator):
        """Simulate a drag and drop operation for a permission element.

        Args:
            locator (Locator): The locator for the element to click and hold.
        """
        # Obtener la posición del elemento de permiso
        bounding_box = await locator.bounding_box()
        # Mover el mouse al permiso y mantener el clic
        await self.page.wait_for_timeout(3000)
        await self.page.mouse.move(
            bounding_box["x"] + bounding_box["width"] / 2, bounding_box["y"] + bounding_box["height"] / 2
        )
        await self.page.mouse.down()
        await self.page.wait_for_timeout(timeout=500)
        await self.page.mouse.up()
