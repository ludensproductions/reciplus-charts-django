import os
from enum import Enum

from dotenv import load_dotenv
from playwright.async_api import Page

from tests.pages.core.constants import InputType
from tests.pages.core.fields_page import FieldsPage
from tests.pages.core.generic_page import GenericPage
from utils.utils_functions import generate_valid_password

load_dotenv()

url = os.getenv("URL_PROYECTO")


class FieldLoginEnum(Enum):
    """Enumeration of fields for the Login page."""

    USERNAME = "username"
    PASSWORD = "password"


class LoginPage(GenericPage):
    """Page object for the Login page."""

    def __init__(self, page: Page, username: str = None, password: str = None):
        super().__init__(page)
        self.input_field_instances = {
            FieldLoginEnum.USERNAME.value: FieldsPage(
                page=page,
                name=FieldLoginEnum.USERNAME.value,
            ),
            FieldLoginEnum.PASSWORD.value: FieldsPage(
                page=page,
                name=FieldLoginEnum.PASSWORD.value,
                input_type=InputType.PASSWORD,
            ),
        }
        self.login_button_selector = 'button[type="submit"]'
        self.menu_dropdown_selector = "#user-menu-toggle"
        self.logout_button_selector = 'button:has-text("Cerrar sesión")'
        self.username = username
        self.password = password
        self.error_message_selector = ".text-danger"
        self.hidden_password_error_message = "El campo 'Contraseña' debe estar oculto en la pantalla de Login."
        self.mismatched_credential_error_message = (
            "Nombre de usuario y/o contraseña no coinciden. Por favor intente nuevamente."
        )

    async def login(self, username: str = None, password: str = None):
        """Realiza el inicio de sesión con el nombre de usuario y la contraseña proporcionados.

        :param username: Nombre de usuario para iniciar sesión.
        :param password: Contraseña para iniciar sesión.
        """
        user = username or self.username
        pwd = password or self.password
        await self.page.goto(url)
        self.set_input_instance_value(**{FieldLoginEnum.USERNAME.value: user, FieldLoginEnum.PASSWORD.value: pwd})
        await self.fill_input_fields()
        await self.page.click(self.login_button_selector)
        return self.page

    async def logout(self):
        """Cierra la sesión del usuario logueado."""
        await self.page.click(self.menu_dropdown_selector)
        await self.wait_for_selector(self.logout_button_selector)
        await self.page.click(self.logout_button_selector)

    async def change_user(self, username: str, password: str):
        """Cambia el usuario logueado cerrando la sesión actual e iniciando sesión con las nuevas credenciales.

        :param username: Nuevo nombre de usuario para iniciar sesión.
        :param password: Nueva contraseña para iniciar sesión.
        """
        await self.logout()
        await self.login(username, password)

    async def validate_invalid_login(self):
        """Validates that the login attempt with invalid credentials shows the correct error message."""
        await self.page.goto(url)
        self.set_input_instance_value(**{FieldLoginEnum.PASSWORD.value: generate_valid_password(8)})
        await self.fill_input_fields()
        await self.page.click(self.login_button_selector)
        await self.page.wait_for_selector(self.error_message_selector)
        error_message = await self.page.text_content(self.error_message_selector)
        assert (
            error_message == self.mismatched_credential_error_message
        ), f"Expected error message not found: {error_message}"

    async def validate_password_field_is_hidden(self):
        """Valida que el campo 'Contraseña' esté oculto (type="password") en la pantalla de Login."""
        await self.page.goto(url)
        password_input = self.page.locator(self.input_field_instances[FieldLoginEnum.PASSWORD.value].field_selector)
        input_type = await password_input.get_attribute("type")
        assert input_type == "password", self.hidden_password_error_message
