import random
from abc import ABC, abstractmethod

from tests.pages.core.constants import HtmlTagEnum


class InputStrategy(ABC):
    """Base class for input strategies."""

    @abstractmethod
    async def fill(self, field_input, value, page, **kwargs):
        """Fills the input field with the given value."""
        raise NotImplementedError("Subclasses must implement the fill method.")


class FileStrategy(InputStrategy):
    """Strategy for filling file inputs."""

    async def fill(self, field_input, value, page, **kwargs):
        """Sets input files for a file input."""
        await field_input.set_input_files(value)


class RadioStrategy(InputStrategy):
    """Strategy for filling radio inputs."""

    async def fill(self, field_input, value, page, **kwargs):
        """Checks the radio button if its value matches."""
        if await field_input.evaluate("el => el.value") == value:
            await field_input.check()


class CheckboxStrategy(InputStrategy):
    """Strategy for filling checkbox inputs."""

    async def fill(self, field_input, value, page, **kwargs):
        """Checks or unchecks checkboxes based on value."""
        field_name = kwargs.get("field_name")
        if isinstance(value, list):
            for sub_value in value:
                await page.locator(f'{field_name}[value="{sub_value}"]').check()
        else:
            if value:
                await field_input.check()
            else:
                await field_input.uncheck()


class ButtonStrategy(InputStrategy):
    """Strategy for clicking buttons."""

    async def fill(self, field_input, value, page, **kwargs):
        """Clicks the button, potentially handling row data."""
        fill_data_method = kwargs.get("fill_data_method")
        if isinstance(value, list):
            for fila_data in value:
                row_exists = any([await page.locator(selector).is_visible() for selector in fila_data.keys()])
                if not row_exists:
                    await field_input.click()
                if fill_data_method:
                    await fill_data_method(fila_data)
        else:
            await field_input.click()


class SelectStrategy(InputStrategy):
    """Strategy for filling select inputs."""

    async def fill(self, field_input, value, page, **kwargs):
        """Selects an option by value or label."""
        await field_input.select_option(value)


class TextInputStrategy(InputStrategy):
    """Strategy for filling text inputs."""

    async def fill(self, field_input, value, page, **kwargs):
        """Fills the text input with a value."""
        # Si el value es una lista, elegir uno al azar
        if isinstance(value, list) and value:
            selected_value = random.choice(value)
        else:
            selected_value = value

        await field_input.fill(str(selected_value))


class Select2Strategy(InputStrategy):
    """Strategy for filling Select2 inputs."""

    async def fill(self, field_input, value, page, **kwargs):
        """Interacts with Select2 components to select values."""
        if not isinstance(value, dict):
            raise ValueError("Select2Strategy expects value in dict format: {selector: value|[values]}.")

        if not value:
            return

        # El dict contiene {search_input_selector: value|[values]}
        search_selector, input_values = next(iter(value.items()))

        # Asegura que input_values sea una lista
        if not isinstance(input_values, list):
            input_values = [input_values]

        select2_type = await field_input.get_attribute("class")
        tag_name = await field_input.evaluate("el => el.tagName")
        if tag_name == HtmlTagEnum.DIV.value:
            select_tag = field_input.locator("select")
            is_disabled = await select_tag.get_attribute("disabled") is not None
            if is_disabled:
                await page.wait_for_timeout(100)

        # Abre el Select2
        await field_input.click()
        await page.wait_for_timeout(200)

        for input_value in input_values:
            try:
                search_field = page.locator(search_selector).first
                await search_field.wait_for(state="visible", timeout=2000)
                await search_field.fill(input_value)
            except Exception as e:
                print(f"[handle_option] Error al escribir en campo de búsqueda: {e}")

            options_container = page.locator("ul.select2-results__options")
            exact_option_locator = options_container.get_by_role("option", name=rf"{input_value}", exact=True).first
            partial_option_locator = options_container.get_by_role("option", name=rf"{input_value}", exact=False).first
            first_selectable_locator = page.locator(
                "li.select2-results__option.select2-results__option--selectable"
            ).first

            option_locator = None
            if input_value != "":
                try:
                    await exact_option_locator.wait_for(state="visible", timeout=2000)
                    option_locator = exact_option_locator
                except Exception:
                    try:
                        await partial_option_locator.wait_for(state="visible", timeout=2000)
                        option_locator = partial_option_locator
                    except Exception:
                        await first_selectable_locator.wait_for(state="visible", timeout=4000)
                        option_locator = first_selectable_locator

            if input_value == "":
                remove_locator = page.locator(
                    kwargs.get("remove_options_select2", "button[title='Remove all items']")
                ).first
                if await remove_locator.is_visible():
                    await remove_locator.click()
                    await field_input.press("Escape")
                else:
                    await page.keyboard.press("Escape")
            elif option_locator and await option_locator.is_visible():
                if "select2-selection--single" in select2_type or "mb-3" in select2_type:
                    await option_locator.click()
                    if await option_locator.is_visible():
                        await option_locator.click()
                else:
                    await option_locator.click()
            else:
                await page.keyboard.press("Enter")
                container_id = await field_input.get_attribute("id")
                if container_id:
                    select_id = container_id.replace("div_", "")
                    await page.evaluate(
                        """(selectId) => {
							const select = document.getElementById(selectId);
							if (select) {
								// Opción 1: Evento nativo
								select.dispatchEvent(new Event('change', { bubbles: true }));
								// Opción 2: jQuery/Select2 (si está disponible)
								if (typeof jQuery !== 'undefined') {
									$(select).trigger('select2:select');
								}
							}
						}""",
                        select_id,
                    )


class WYSIWYGStrategy(InputStrategy):
    """Strategy for filling WYSIWYG text areas (TipTap, TinyMCE, etc.).

    The field_input received is the outer Django wrapper div (e.g. #div_id_description).
    TipTap hides the native <textarea> and mounts a div[contenteditable="true"]
    next to it, so this strategy navigates into that inner element before filling.
    """

    async def fill(self, field_input, value, page, **kwargs):
        """Locates the contenteditable div inside the wrapper and fills it.

        Args:
            field_input: Playwright Locator pointing to the outer wrapper div.
            value: Text value to type into the editor.
            page: The Playwright Page instance.
            **kwargs: Additional keyword arguments (not used).
        """
        editor = field_input.locator("div[contenteditable='true']")
        await editor.click()
        await editor.fill(str(value))


class MultipleFilesStrategy(InputStrategy):
    """Strategy for filling multiple file inputs.

    The field_input received is the outer Django wrapper div (e.g. #div_id_files).
    The actual file input lives inside that wrapper, so this strategy navigates
    into it before calling set_input_files — the same approach used by
    WYSIWYGStrategy to locate the contenteditable div.
    """

    async def fill(self, field_input, value, page, **kwargs):
        """Locates the file input inside the wrapper div and sets the files.

        Args:
            field_input: Playwright Locator pointing to the outer wrapper div.
            value: List of file paths or a single file path.
            page: The Playwright Page instance.
            **kwargs: Additional keyword arguments (not used).
        """
        file_input = field_input.locator('input[type="file"]').first
        files = value if isinstance(value, list) else [value]
        await file_input.set_input_files(files)
