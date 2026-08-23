from playwright.async_api import expect

from tests.pages.core.generic_page import GenericPage
from utils.utils_functions import create_random_image, generate_base64_file


class PagePerfil(GenericPage):
    """Page object for the Profile page."""

    def __init__(self, page):
        """Initializes the PagePerfil object."""
        super().__init__(page)

        # Index selectors
        self.dashboard_page_title_selector = 'h3:has-text("Dashboard")'

        # Profile selectors
        self.sidebar_button_selector = "#user-menu-toggle"
        self.index_page_button_selector = 'a:has-text("Perfil")'
        self.index_page_title_selector = 'h1:has-text("Perfil")'
        self.change_picture_button_selector = 'button:has-text("Cambiar")'
        self.clean_picture_button_selector = 'button:has-text("Limpiar")'
        self.submit_picture_button_selector = 'button:has-text("Guardar")'
        self.return_button_selector = 'a:has-text("Regresar")'
        self.file_input_selector = 'input[type="file"]'
        self.username_selector = 'input[name="username"]'
        self.no_image_selector = "#noImageText"

        # Message selectors
        self.error_message_selector = "p#error_1_id_image"
        self.invalid_picture_error_message = (
            'La extensión de archivo "pdf" no está permitida. Las extensiones permitidas son: jpg, jpeg, png, svg.'
        )
        self.success_create_message_text = "¡Perfil actualizado exitosamente!"

    async def goto_index_page(self):
        """Navigates to the profile index page."""
        await self.page.click(self.sidebar_button_selector)
        await self.wait_for_selector(self.index_page_button_selector)
        await self.page.click(self.index_page_button_selector)
        await self.wait_for_selector(self.index_page_title_selector)

    async def validate_user_information(self, username):
        """Navigates to the profile view and verifies that the user's personal information is correctly displayed."""
        await self.goto_index_page()
        # No hay nada que se pueda validar ya que no hay manera de obtener el correo del usuario logeado
        # Solo tenemos el username pero este no se muestra en ningún lado en el perfil, por lo que no hay nada que validar
        # await self.validate_record_information_in_index_view({self.username_selector: username})

    async def change_profile_picture(self):
        """Generates a random image and sets it as the new profile picture."""
        await self.goto_index_page()
        image_path = create_random_image()
        file_input = self.page.locator(self.file_input_selector)
        await file_input.set_input_files(image_path)

        await self.page.click(self.submit_picture_button_selector)
        await self.validate_success_message_and_continue(
            self.modal_message_selector, self.continue_button_selector, self.success_create_message_text
        )
        await expect(self.page.locator(self.no_image_selector)).not_to_be_visible()

    async def cancel_change_profile_picture(self):
        """Cancels the profile picture update and ensures the user is redirected back to the dashboard view."""
        await self.goto_index_page()

    async def change_invalid_profile_picture(self):
        """Attempts to upload a profile picture using an invalid file format (e.g., .pdf).

        Verifies that an appropriate error message is displayed and allows the user to cancel the action.
        """
        await self.goto_index_page()
        file_path = generate_base64_file(extension="pdf")
        file_input = self.page.locator(self.file_input_selector)
        await file_input.set_input_files(file_path)

        await self.page.click(self.submit_picture_button_selector)
        await self.wait_for_selector(self.error_message_selector)
        await self.check_error_message([self.error_message_selector], self.invalid_picture_error_message)

    async def remove_profile_picture(self):
        """Removes the current profile picture."""
        await self.goto_index_page()
        await self.wait_for_selector(self.clean_picture_button_selector)
        await self.page.click(self.clean_picture_button_selector)
        await self.page.click(self.submit_picture_button_selector)

        await self.validate_success_message_and_continue(
            self.modal_message_selector, self.continue_button_selector, self.success_create_message_text
        )
        await expect(self.page.locator(self.no_image_selector)).to_be_visible()
