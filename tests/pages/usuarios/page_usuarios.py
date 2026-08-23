from enum import Enum

from tests.pages.core.constants import InputType
from tests.pages.core.fields_page import FieldsPage
from tests.pages.core.generic_page import GenericPage
from utils.utils_functions import generate_random_email


class FieldUsuariosEnum(Enum):
    """Enumeration of fields for the Usuarios page."""

    NOMBRES = "first_name"
    APELLIDO_PATERNO = "last_name"
    APELLIDO_MATERNO = "second_last_name"
    EMAIL = "email"


class PageUsuarios(GenericPage):
    """Page object for the Usuarios catalog page."""

    def __init__(self, page):
        super().__init__(page, module_name="Usuarios", navigation=["Usuarios", "Usuarios"])

        self.sidebar_button_selector = 'a:has-text("Usuarios")'
        self.index_page_button_selector = 'a[title="Usuarios"]'

        self.input_field_instances = {
            FieldUsuariosEnum.NOMBRES.value: FieldsPage(
                page=page,
                name=FieldUsuariosEnum.NOMBRES.value,
                max_length=255,
            ),
            FieldUsuariosEnum.APELLIDO_PATERNO.value: FieldsPage(
                page=page,
                name=FieldUsuariosEnum.APELLIDO_PATERNO.value,
                max_length=255,
                is_filter=False,
                is_indexable=False,
            ),
            FieldUsuariosEnum.APELLIDO_MATERNO.value: FieldsPage(
                page=page,
                name=FieldUsuariosEnum.APELLIDO_MATERNO.value,
                max_length=255,
                is_filter=False,
                is_indexable=False,
            ),
            FieldUsuariosEnum.EMAIL.value: FieldsPage(
                page=page,
                name=FieldUsuariosEnum.EMAIL.value,
                input_type=InputType.EMAIL,
                max_length=254,
                is_filter=False,
                is_indexable=False,
                allowed_values=[generate_random_email().lower()],
            ),
        }

    async def goto_index_page(self):
        """Navigates to the Usuarios index page."""
        await self.page.wait_for_selector(self.sidebar_button_selector)
        await self.page.click(self.sidebar_button_selector)
        await self.page.wait_for_selector(self.index_page_button_selector)
        await self.page.click(self.index_page_button_selector)
        await self.page.wait_for_selector(self.index_page_title_selector)
