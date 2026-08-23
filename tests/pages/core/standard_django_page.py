import re

from playwright.async_api import Page, expect

from tests.pages.core.base_page import BasePage


class StandardDjangoPage(BasePage):
    """A class that encapsulates interactions with a web page.

    Provides methods for form manipulation, data validation, and user interaction.

    This class is designed to facilitate the automation of web interactions using
    Playwright. Each method within this class operates on the current page context
    and assumes that the user is already on the appropriate page or form.

    Attributes:
        page (Page): An instance of the Playwright Page class, representing the current page.
    """

    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        self.cancel_button_selector = 'button:has-text("Cancelar")'
        self.cancel_anchor_selector = 'a:has-text("Cancelar")'
        self.filter_button_selector = 'button:has-text("Filtrar")'
        self.clear_filters_selector = 'a:has-text("Borrar filtros"), a:has-text("Borrar filtro")'
        self.edit_button_selector = 'a[title="Editar"]'
        self.error_message_selector = ".invalid-feedback"  # SE elimino la p debido a que habían invalid-feedback variable, de esta manera es más general
        self.disable_modal_title_selector = 'h4:has-text("Deshabilitar")'
        self.enable_modal_title_selector = 'h4:has-text("Habilitar")'
        self.create_form_button_selector = 'a[title="boton_crear"]'
        self.disabled_index_page_button_selector = 'a[title="boton_disabled"]'

        # Edit selectors - all possible variants
        self.edit_button_selector = 'button[title="Editar"]'
        self.edit_anchor_selector = 'a[title="Update"]'
        self.edit_span_selector = 'span[title="Editar"]'

        # Delete selectors - all possible variants
        self.delete_button_selector = 'button[title="Eliminar"]'
        self.delete_anchor_selector = 'a[title="Eliminar"]'
        self.delete_span_selector = 'span[title="Eliminar"]'
        self.input_checkbox_disable = 'input[title=" Deshabilitar "]'
        self.input_checkbox_enable = 'input[title=" Habilitar "]'

        # Enable/Disable selectors
        self.enable_button_selector = 'input[title="Habilitar"]'
        self.disable_button_selector = 'button:has-text("Deshabilitar")'

        # Detail selectors - all possible variants
        self.detail_anchor_selector = 'a[title="Show"]'
        self.detail_button_selector = 'button[title="Detalle"]'
        self.detail_span_selector = 'span[title="Detalle"]'

        # Additional comprehensive selectors for all actions
        self._init_comprehensive_selectors()

        self.modal_form_selector = 'div[role="dialog"]'
        self.submit_create_form_selector = 'button:has-text("Guardar")'
        # self.enable_confirm_button_selector = 'button:text("Habilitar")'
        self.confirm_disable_button_selector = 'button:text("Deshabilitar")'
        self.delete_confirm_button_selector = 'button:has-text("Eliminar")'
        self.double_confirm_button_selector = 'button.swal2-confirm:has-text("Guardar")'
        # self.cancel_modal_button_selector = 'button:has-text("Cancelar")'
        self.modal_message_selector = "#swal2-html-container"
        self.success_message_selector = "#swal2-title"
        self.justificacion_input_selector = 'textarea(title="Justificacion")'
        self.back_anchor_selector = 'a:has-text("Volver")'

        self.table_selector = "#ipi-table"
        self.not_found_filter_message_text = "No hay datos disponibles"

        self.success_create_message_text = "¡Elemento creado exitosamente!"
        self.success_edit_message_text = "¡Elemento actualizado exitosamente!"
        self.success_delete_message_text = "¡Elemento eliminado exitosamente!"
        self.success_restore_message_text = "¡Elemento restaurado exitosamente!"
        self.success_disable_message_text = "¡Elemento deshabilitado con éxito!"
        self.success_enable_message_text = "¡Elemento habilitado con éxito!"

        self.data_filters = {}
        self.data_validate = {}
        # Fields
        self.input_field_instances = {}

    def _init_comprehensive_selectors(self):
        """Initialize comprehensive selectors for all possible action variations."""
        # Edit action selectors - comprehensive list
        self.edit_selectors = [
            # Anchor variants
            'a[title="Editar"]',
            'a[title="Edit"]',
            'a[title="Update"]',
            'a[title="Modificar"]',
            'a:has-text("Editar")',
            'a:has-text("Edit")',
            'a:has-text("Modificar")',
            "a.edit-btn",
            "a.btn-edit",
            # Button variants
            'button[title="Editar"]',
            'button[title="Edit"]',
            'button[title="Update"]',
            'button[title="Modificar"]',
            'button:has-text("Editar")',
            'button:has-text("Edit")',
            'button:has-text("Modificar")',
            "button.edit-btn",
            "button.btn-edit",
            # Span variants
            'span[title="Editar"]',
            'span[title="Edit"]',
            'span[title="Update"]',
            'span[title="Modificar"]',
            'span:has-text("Editar")',
            'span:has-text("Edit")',
            "span.edit-btn",
            "span.btn-edit",
            # Icon variants
            "i.fa-edit",
            "i.fa-pencil",
            "i.fa-pencil-alt",
            "i.fas.fa-edit",
            "i.fas.fa-pencil-alt",
            # Generic class variants
            ".edit-action",
            '.btn-primary[title*="dit"]',
            '[data-action="edit"]',
            '[data-toggle="edit"]',
        ]

        # Delete action selectors - comprehensive list
        self.delete_selectors = [
            # Checkbox variants (disable/enable)
            'input[title=" Deshabilitar "]',
            'input[title=" Habilitar "]',
            'input[title="Deshabilitar"]',
            'input[title="Habilitar"]',
            'input[title="Disable"]',
            'input[title="Enable"]',
            # Anchor variants
            'a[title="Eliminar"]',
            'a[title="Delete"]',
            'a[title="Remove"]',
            'a:has-text("Eliminar")',
            'a:has-text("Delete")',
            'a:has-text("Remove")',
            "a.delete-btn",
            "a.btn-delete",
            "a.btn-danger",
            # Button variants
            'button[title="Eliminar"]',
            'button[title="Delete"]',
            'button[title="Remove"]',
            'button:has-text("Eliminar")',
            'button:has-text("Delete")',
            'button:has-text("Remove")',
            "button.delete-btn",
            "button.btn-delete",
            "button.btn-disable",
            # Span variants
            'span[title="Eliminar"]',
            'span[title="Delete"]',
            'span[title="Remove"]',
            'span[title="Deshabilitar"]',
            'span:has-text("Eliminar")',
            'span:has-text("Delete")',
            'span:has-text("Remove")',
            "span.delete-btn",
            "span.btn-delete",
            # Icon variants
            "i.fa-trash",
            "i.fa-trash-alt",
            "i.fa-remove",
            "i.fa-times",
            "i.fas.fa-trash",
            "i.fas.fa-trash-alt",
            # Generic class variants
            ".delete-action",
            '.btn-danger[title*="limin"]',
            '[data-action="delete"]',
            '[data-toggle="delete"]',
        ]

        # Detail/Show action selectors - comprehensive list
        self.detail_selectors = [
            # Anchor variants
            'a[title="Show"]',
            'a[title="Detalle"]',
            'a[title="Detail"]',
            'a[title="Ver"]',
            'a[title="View"]',
            'a[title="Mostrar"]',
            'a:has-text("Detalle")',
            'a:has-text("Detail")',
            # 'a:has-text("Ver")', Encuentra el botón "Volver"
            'a:has-text("View")',
            'a:has-text("Show")',
            "a.detail-btn",
            "a.btn-detail",
            "a.btn-info",
            # Button variants
            'button[title="Detalle"]',
            'button[title="Detail"]',
            'button[title="Show"]',
            'button[title="Ver"]',
            'button[title="View"]',
            'button[title="Mostrar"]',
            'button:has-text("Detalle")',
            'button:has-text("Detail")',
            'button:has-text("Ver")',
            'button:has-text("View")',
            'button:has-text("Show")',
            "button.detail-btn",
            "button.btn-detail",
            "button.btn-info",
            # Span variants
            'span[title="Detalle"]',
            'span[title="Detail"]',
            'span[title="Show"]',
            'span[title="Ver"]',
            'span[title="View"]',
            'span:has-text("Detalle")',
            'span:has-text("Detail")',
            # 'span:has-text("Ver")',
            'span:has-text("View")',
            "span.detail-btn",
            "span.btn-detail",
            # Icon variants
            "i.fa-eye",
            "i.fa-info",
            "i.fa-info-circle",
            "i.fas.fa-eye",
            "i.fas.fa-info",
            "i.fas.fa-info-circle",
            # Generic class variants
            ".detail-action",
            '.btn-info[title*="etall"]',
            '[data-action="show"]',
            '[data-action="detail"]',
            '[data-toggle="detail"]',
        ]

        # Enable action selectors - comprehensive list
        self.enable_selectors = [
            # Input/checkbox variants
            'input[title="Habilitar"]',
            'input[title=" Habilitar "]',
            'input[title="Habilitado"]',
            'input[title="Enable"]',
            'input[title=" Enable "]',
            'input[title="Activar"]',
            'input[title=" Activar "]',
            # Button variants
            # 'button[title="Habilitar"]',
            'button[title="Enable"]',
            'button[title="Activar"]',
            # 'button:has-text("Habilitar")',
            'button:has-text("Enable")',
            'button:has-text("Activar")',
            "button.enable-btn",
            "button.btn-enable",
            "button.btn-success",
            # Anchor variants
            'a[title="Habilitar"]',
            'a[title="Enable"]',
            'a[title="Activar"]',
            'a:has-text("Habilitar")',
            'a:has-text("Enable")',
            'a:has-text("Activar")',
            "a.enable-btn",
            "a.btn-enable",
            # Span variants
            'span[title="Habilitar"]',
            'span[title="Enable"]',
            'span[title="Activar"]',
            'span:has-text("Habilitar")',
            'span:has-text("Enable")',
            "span.enable-btn",
            # Icon variants
            "i.fa-check",
            "i.fa-check-circle",
            "i.fa-power-off",
            "i.fas.fa-check",
            "i.fas.fa-check-circle",
            # Generic class variants
            ".enable-action",
            '.btn-success[title*="abilit"]',
            '[data-action="enable"]',
            '[data-toggle="enable"]',
        ]

        # Cancel action selectors - comprehensive list
        self.cancel_selectors = [
            # Selector del boton cancelar del formulario de habilitar
            '#enableForm button:has-text("Cancelar")',
            # Button variants
            'button:has-text("Cancelar")',
            'button:has-text("Cancel")',
            # 'button:has-text("Cerrar")', Encuentra cerrar sesión
            'button:has-text("Close")',
            'button[title="Cancelar"]',
            'button[title="Cancel"]',
            'button[title="Cerrar"]',
            'button[title="Close"]',
            "button.cancel-btn",
            "button.btn-cancel",
            "button.btn-secondary",
            # Anchor variants
            'a:has-text("Cancelar")',
            'a:has-text("Cancel")',
            'a:has-text("Cerrar")',
            'a:has-text("Close")',
            'a[title="Cancelar"]',
            'a[title="Cancel"]',
            'a[title="Cerrar"]',
            'a[title="Close"]',
            "a.cancel-btn",
            "a.btn-cancel",
            # Span variants
            'span:has-text("Cancelar")',
            'span:has-text("Cancel")',
            # 'span:has-text("Cerrar")', Encuentra cerrar sesión
            "span.cancel-btn",
            # Modal specific
            'button[data-dismiss="modal"]',
            "button.swal2-cancel",
            '.modal-footer button:has-text("Cancelar")',
            '.modal-footer button:has-text("Cancel")',
            # Icon variants
            "i.fa-times",
            "i.fa-close",
            "i.fas.fa-times",
            # Generic class variants
            ".cancel-action",
            '[data-action="cancel"]',
            '[data-toggle="cancel"]',
        ]

        # Back/Return action selectors - comprehensive list
        self.back_selectors = [
            # Anchor variants
            'a:has-text("Volver")',
            'a:has-text("Back")',
            'a:has-text("Regresar")',
            'a:has-text("Return")',
            'a[title="Volver"]',
            'a[title="Back"]',
            'a[title="Regresar"]',
            'a[title="Return"]',
            "a.back-btn",
            "a.btn-back",
            # Button variants
            'button:has-text("Volver")',
            'button:has-text("Back")',
            'button:has-text("Regresar")',
            'button[title="Volver"]',
            'button[title="Back"]',
            "button.back-btn",
            "button.btn-back",
            # Icon variants
            "i.fa-arrow-left",
            "i.fa-chevron-left",
            "i.fas.fa-arrow-left",
            "i.fas.fa-chevron-left",
            # Generic class variants
            ".back-action",
            '[data-action="back"]',
            '[data-toggle="back"]',
        ]

    async def fill_data(self, data: dict, page: Page = None):
        """Fills out a form with the provided data and submits it.

        Args:
            data (dict): The data to be filled in the form.
            page (Page, optional): The browser page where the data is to be filled. Defaults to `self.page`.

        Steps:
            1. Uses the base class's `fill_data` method to fill the form with the provided data.
            2. Waits for the form's submit button to be visible.
            3. Clicks the submit button to submit the form.
        """
        page = page or self.page
        await super().fill_data(data, page=page)

    async def delete_item_with_justificacion(self, data_filters: dict, justificacion: str, page: Page = None):
        """Deletes an item after applying filters and providing a justification.

        Args:
            data_filters (dict): Criteria to locate the item to delete.
            justificacion (str): Justification text required for the deletion.
            page (Page, optional): The browser page to perform the action. Defaults to `self.page`.

        Steps:
            1. Filters the item using `data_filters`.
            2. Clicks the delete button for the located item.
            3. Fills in the required justification.
            4. Validates the deletion with a confirmation message.
        """
        page = page or self.page
        await self.search_records_with_filters(data_filters)

        await self.wait_for_selector(self.delete_button_selector, page=page)
        await page.locator(self.delete_button_selector).first.click()

        await self.wait_for_selector(self.justificacion_input_selector, page=page)
        await page.locator(self.justificacion_input_selector).fill(justificacion)

        await self.check_success_modal_message(self.success_delete_message_text, page=page)

    async def disable_item_with_toggle(self, data_filters: dict, page: Page = None):
        """Disables an item using a toggle button after applying filters.

        Args:
            data_filters (dict): Criteria to locate the item to disable.
            page (Page, optional): The browser page to perform the action. Defaults to `self.page`.

        Steps:
            1. Filters the item using the provided `data_filters`.
            2. Toggles the item's state using the base class's `disable_item` method.
            3. Waits for the confirmation dialog or button to appear.
            4. Clicks the confirmation button to complete the disable action.
            5. Validates the action by checking for a success message.
        """
        page = page or self.page
        await self.search_records_with_filters(data_filters)

        await super().disable_item(self.disable_button_selector, page=page)

        await self.wait_for_selector(self.disable_modal_title_selector, page=page)
        await page.click(self.disable_confirm_button_selector)

        modal_message = await self.page.locator(self.modal_message_selector).text_content()
        message = (
            modal_message
            if modal_message in [self.success_disable_message_text, self.success_delete_message_text]
            else None
        )
        await self.check_success_modal_message(message, page=page)

    async def enable_item(self, data_filters: dict, page: Page = None):
        """Enables an item after applying filters.

        Args:
            data_filters (dict): Criteria to locate the item to enable.
            page (Page, optional): The browser page to perform the action. Defaults to `self.page`.

        Steps:
            1. Filters the item using the provided `data_filters`.
            2. Enables the item using the base class's `enable_item` method.
            3. Waits for the confirmation dialog or button to appear.
            4. Clicks the confirmation button to complete the enable action.
            5. Validates the action by checking for a success message.
        """
        page = page or self.page
        await self.search_records_with_filters(data_filters)
        await super().enable_item(self.enable_button_selector, page=page)

        await self.wait_for_selector(self.enable_modal_title_selector, page=page)
        await page.click(self.enable_confirm_button_selector)

        await self.check_success_modal_message(self.success_enable_message_text, page=page)

    async def validate_record_information_in_edit_view(self, data_validate: dict, page: Page = None):
        """Validates that the item's information in the edit view matches the provided data.

        Args:
            data_validate (dict): The expected data to validate against the item's information.
            page (Page, optional): The browser page to perform the validation. Defaults to `self.page`.

        Steps:
            1. Uses the base class's `validate_record_information_in_edit_view` method to perform the validation.
            2. Ensures the validation is executed on the specified or default page.
        """
        page = page or self.page
        await super().validate_record_information_in_edit_view(data_validate, page=page)

    async def validate_record_information_in_details_view(self, data_validate: dict, page: Page = None):
        """Validates that the record's information in the details view matches the provided data.

        Args:
            data_validate (dict): The expected data to validate against the record's details.
            page (Page, optional): The browser page to perform the validation. Defaults to `self.page`.

        Steps:
            1. Uses the base class's `validate_record_information_in_details_view` method to perform the validation.
            2. Ensures the validation is executed on the specified or default page.
        """
        page = page or self.page
        await super().validate_record_information_in_details_view(data_validate, page=page)

    async def check_success_modal_message(self, message: str, page: Page = None):
        """Verifies the success message in a modal and handles the continue action.

        Args:
            message (str): The expected success message text displayed in the modal.
            page (Page, optional): The browser page where the check is performed. Defaults to `self.page`.

        Steps:
            1. Uses the base class's `check_success_message` method to validate the modal message.
            2. Handles the "Continue" action on the specified or default page.
        """
        page = page or self.page
        await super().validate_success_message_and_continue(
            self.modal_message_selector, self.continue_button_selector, message, page=page
        )

    async def validate_table_data(self, data_filters: dict, page: Page = None):
        """Verifies the visibility of table data based on the provided filters.

        Args:
            data_filters (dict): A dictionary containing key-value pairs to validate in the table rows.
            page (Page, optional): The browser page where the validation is to be performed. Defaults to `self.page`.

        Steps:
            1. Uses the `search_with_filters` method to filter the data in the table.
            2. Locates the table and iterates through each row.
            3. Verifies the visibility of each row.
            4. Checks if each filtered value is visible in the corresponding table cell.
        """
        page = page or self.page
        await self.search_records_with_filters(data_filters)

        table_locator = page.locator(self.table_selector)

        # iterate over the table rows
        for row in await table_locator.locator("tbody").locator("tr").all():
            await expect(row).to_be_visible()
            # validate based data
            for key, value in data_filters.items():
                await expect(row.locator("td", has_text=value)).to_be_visible()

    async def get_radio_options(self, selector_complement):
        """Retrieves all radio button option elements within a container.

        Uses the container identified by `#div_id_{selector_complement}`.

        Args:
            selector_complement (str): Suffix used to compose the container selector
                (`#div_id_{selector_complement}`) where the radio inputs reside.

        Returns:
            list[playwright.async_api.ElementHandle]: A list of element handles for the
            radio inputs found in the container.

        Raises:
            Exception: If no radio button options are found.
        """
        # Localizar el contenedor de los radio buttons
        radio_locator = self.page.locator(f'#div_id_{selector_complement} input[type="radio"]')

        # Cevuelve todos los radio buttons dentro del contenedor
        options = await radio_locator.element_handles()

        if not options:
            raise Exception("No se encontraron opciones del radio")

        return options

    async def get_first_visible_selector(self, selectors: list[str], type_selector) -> str:
        """Returns the first selector from `selectors` that is visible on the page.

        Checks each candidate in order using Playwright's locator API. If no selector
        is visible, logs a message including `type_selector` and returns `None`.

        Args:
            selectors (list[str]): Candidate CSS/XPath selectors to check in order.
            type_selector (str): Human-friendly label used only for logging when no
                selector is found (e.g., "editar", "detalle").

        Returns:
            Optional[str]: The first visible selector, or `None` if none are visible.
        """
        await self.page.wait_for_timeout(200)
        for selector in selectors:
            if await self.page.locator(selector).first.is_visible():
                return selector
        print(f"Ningún selector visible encontrado para {type_selector}.")
        return None

    async def get_detail_button_selector(self):
        """Resolves the selector for the 'detail' action.

        Returns the first visible candidate from a comprehensive list of detail/show selectors.

        Checks multiple variations including buttons, anchors, spans with different titles,
        text content, classes, icons, and data attributes in both Spanish and English.

        Returns:
            Optional[str]: The first visible detail selector, or `None` if none are visible.
        """
        return await self.get_first_visible_selector(self.detail_selectors, "detalle")

    async def get_edit_button_selector(self):
        """Resolves the selector for the 'edit' action.

        Returns the first visible candidate from a comprehensive list of edit/update selectors.

        Checks multiple variations including buttons, anchors, spans with different titles,
        text content, classes, icons, and data attributes in both Spanish and English.

        Returns:
            Optional[str]: The first visible edit selector, or `None` if none are visible.
        """
        return await self.get_first_visible_selector(self.edit_selectors, "editar")

    async def get_delete_button_selector(self):
        """Resolves the selector for the 'delete' action.

        Returns the first visible candidate from a comprehensive list of delete/remove selectors.

        Checks multiple variations including checkboxes, buttons, anchors, spans with different
        titles, text content, classes, icons, and data attributes in both Spanish and English.
        Also includes disable/enable checkboxes as they often serve as delete functionality.

        Returns:
            Optional[str]: The first visible delete-related selector, or `None` if none are visible.
        """
        return await self.get_first_visible_selector(self.delete_selectors, "eliminar")

    async def get_enable_button_selector(self):
        """Resolves the selector for the 'enable' action.

        Returns the first visible candidate from a comprehensive list of enable/activate selectors.

        Checks multiple variations including checkboxes, buttons, anchors, spans with different
        titles, text content, classes, icons, and data attributes in both Spanish and English.

        Returns:
            Optional[str]: The first visible "enable" selector, or `None` if none are visible.
        """
        return await self.get_first_visible_selector(self.enable_selectors, "habilitar")

    async def get_cancel_button_selector(self):
        """Resolves the selector for the 'cancel' action.

        Returns the first visible candidate from a comprehensive list of cancel/close selectors.

        Checks multiple variations including buttons, anchors, spans with different titles,
        text content, classes, modal-specific selectors, icons, and data attributes
        in both Spanish and English.

        Returns:
            Optional[str]: The first visible "cancel" selector, or `None` if none are visible.
        """
        return await self.get_first_visible_selector(self.cancel_selectors, "cancelar")

    async def get_back_button_selector(self):
        """Returns the selector for the back navigation control.

        Returns the first visible candidate from a comprehensive list of back/return selectors.

        Checks multiple variations including anchors, buttons with different titles,
        text content, classes, icons, and data attributes in both Spanish and English.

        Returns:
            Optional[str]: The first visible back-control selector, or `None` if not found.
        """
        return await self.get_first_visible_selector(self.back_selectors, "volver")

    async def submit_form(self, button_selector):
        """Submits a form by clicking the button indicated by `button_selector`.

        Behavior:
            1. Waits for `button_selector` to exist in the DOM.
            2. If the button is not visible, scrolls to the bottom of the page.
            3. Clicks the button once visible.

        Args:
            button_selector (str): CSS selector for the submit button.

        Raises:
            Exception: Any exception raised by `wait_for_selector` or `click` will propagate.
        """
        await self.wait_for_selector(button_selector)
        submit_button = self.page.locator(button_selector)
        if not await submit_button.is_visible():
            await self.scroll_to_bottom()
        if await submit_button.is_visible():
            await submit_button.click()

    async def scroll_to_bottom(self):
        """Scrolls the page to the very bottom using an incremental window scroll.

        Executes a small JavaScript routine that scrolls in steps until the total
        scroll height is reached.
        """
        await self.page.evaluate(
            """async () => {
            await new Promise((resolve) => {
                let totalHeight = 0;
                const distance = 100;
                const timer = setInterval(() => {
                    const scrollHeight = document.body.scrollHeight;
                    window.scrollBy(0, distance);
                    totalHeight += distance;

                    if (totalHeight >= scrollHeight) {
                        clearInterval(timer);
                        resolve();
                    }
                }, 100);
            });
        }"""
        )
        print("Scroll hasta el final de la página completado.")

    async def validate_many_filter_results(self, field_selector, field_value, validate_value, index=None):
        """Validates that one or more expected values appear in the table after applying a filter.

        Flow:
            1. Navigates to the index page.
            2. Fills the filter identified by `field_selector` with `field_value` and submits.
            3. For each expected value in `validate_value`, asserts it is present at least once
            by delegating to `compare_count_in_filters_with_many_restults`.

        Args:
            field_selector (str): Selector/key for the filter field to populate.
            field_value: Value to input into the filter field.
            validate_value (str | list | dict): Expected value(s) to verify in the results.
                - str: single value.
                - list: validate each value.
                - dict: if a value is a list, `index` selects which element to validate.
            index (int | None): Index used when `validate_value` contains lists within a dict.

        Raises:
            AssertionError: If any expected value is not found in the results.
        """
        await self.goto_index_page()
        await self.fill_data({field_selector: field_value})
        await self.page.click(self.filter_button_selector)
        if isinstance(validate_value, dict):
            for key, value in validate_value.items():
                if isinstance(value, list):
                    # for sub_value in value:
                    await self.compare_count_in_filters_with_many_restults(value[index], field_selector)
                else:
                    await self.compare_count_in_filters_with_many_restults(value, field_selector)
        elif isinstance(validate_value, list):
            for value in validate_value:
                await self.compare_count_in_filters_with_many_restults(value, field_selector)
        else:
            await self.compare_count_in_filters_with_many_restults(validate_value, field_selector)

    async def compare_count_in_filters_with_many_restults(self, validate_value, field_selector):
        """Asserts that `validate_value` appears at least once in the results table for the given field.

        Finds table cells whose accessible name matches `validate_value` exactly and
        asserts that the count is greater than zero.

        Args:
            validate_value (str): The exact cell text expected to be present.
            field_selector (str): Field/filter identifier used only for error messaging.

        Raises:
            AssertionError: If no matching cells are found.
        """
        field_locator = self.page.get_by_role("cell", name=f"{validate_value}", exact=True)
        field_count = await field_locator.count()
        assert field_count > 0, f"El valor {validate_value} no se encontró en el campo {field_selector}"

    async def get_cell_value_by_header_th(self, th_selector: str, *, row_selector: str = "tbody tr"):
        """Obtiene el valor de una celda (<td>) en una tabla HTML basándose en el encabezado (<th>).

        Obtiene el valor que corresponde a esa columna, sin importar la posición que ocupe en la tabla.

        Este método es útil cuando:
            - Solo conoces el selector del <th> (encabezado), pero no sabes el índice de la columna.
            - El orden de las columnas puede cambiar dinámicamente.
            - Después de filtrar, hay una sola fila en el <tbody> y quieres obtener el valor exacto
            que corresponde a esa columna.

        Flujo de funcionamiento:
            1. Espera a que el elemento <th> especificado esté presente en la página.
            2. Calcula el índice (posición) de esa columna dentro de su fila de encabezados.
            3. Busca la tabla contenedora de ese <th> para limitar el alcance de la búsqueda.
            4. Selecciona el <td> de esa misma columna en la primera fila encontrada (o la única fila
            si el filtro aplicado devuelve un solo resultado).
            5. Devuelve el texto de la celda.

        Args:
            page (Page): Instancia de Playwright Page en la que se ejecuta la búsqueda.
            th_selector (str): Selector CSS del encabezado (<th>) cuya columna deseas leer.
                            Ejemplo: "table thead th:nth-child(3)" o "th:has-text('Folio')"
            row_selector (str, opcional): Selector de la fila objetivo en el <tbody>.
                                        Por defecto es `"tbody tr"`, pero puedes usar otro si la
                                        fila tiene una clase especial (por ejemplo: `"tbody tr.filtered"`).

        Returns:
            str: Texto de la celda correspondiente en la primera fila de resultados.

        Raises:
            TimeoutError: Si el <th> o el <td> correspondiente no aparece antes del timeout.
            ValueError: Si no se encuentra la tabla o el índice de la columna.

        Ejemplo de uso:
            >>> valor_folio = await get_cell_value_by_header_th(
            ...     self.page,
            ...     "thead th:has-text('Folio')"
            ... )
            >>> print(valor_folio)
            'EVENTFOLIO0926'
        """
        # 1) Espera el <th> que conoces
        th = await self.page.wait_for_selector(th_selector, timeout=5000)

        # 2) Calcula el índice de la columna (1-based) dentro de su fila de headers
        col_index = await th.evaluate(
            """
            th => {
                const siblings = Array.from(th.parentElement.children)
                    .filter(el => el.matches('th,td'));  // por si la cabecera usa <td>
                return siblings.indexOf(th) + 1;        // 1-based para nth-child
            }
        """
        )

        # 3) Encuentra la tabla “dueña” de ese <th> para no confundir tablas
        table_handle = await th.evaluate_handle("th => th.closest('table')")
        table = table_handle.as_element()

        # 4) Toma el <td> de esa columna en la (única) fila filtrada
        cell = await table.wait_for_selector(f"{row_selector} td:nth-child({col_index})", timeout=5000)

        return (await cell.inner_text()).strip()

    def _extract_name_attribute(self, selector: str) -> str:
        """Extrae el valor del atributo name de un selector CSS.

        Args:
            selector: Puede ser "field", "input[name=field]", "input[name='field']"

        Returns:
            El valor extraído o el selector original si no tiene atributo name

        Examples:
            "input[name=song-0-theme]" -> "song-0-theme"
            "song-0-theme" -> "song-0-theme"
        """
        m = re.search(r"\[name\s*=\s*['\"]?([^\]'\"]+)['\"]?\]", selector)
        return m.group(1).strip() if m else selector.strip()

    def _parse_formset_structure(self, name: str) -> tuple[str, str, str]:
        """Parsea la estructura de un nombre de formset.

        Args:
            name: Formato "prefix-index-field" (ej: "activities-0-capacity")

        Returns:
            Tupla (prefix, index, field)
            Si no tiene el formato esperado, retorna ("", "", name)

        Examples:
            "activities-0-capacity" -> ("activities", "0", "capacity")
            "song-12-theme-color" -> ("song", "12", "theme-color")
            "simple" -> ("", "", "simple")
        """
        # Buscar patrón formset: prefix-index-field
        m = re.match(r"^([\w-]+)-(\d+|__prefix__)-([\w-]+)$", name)
        if m:
            return m.group(1), m.group(2), m.group(3)

        # Fallback: split simple
        if "-" in name:
            parts = name.split("-")
            if len(parts) >= 3:
                return parts[0], parts[1], "-".join(parts[2:])
            elif len(parts) == 2:
                return parts[0], "", parts[1]

        return "", "", name
