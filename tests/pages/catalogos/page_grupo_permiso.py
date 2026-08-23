from enum import Enum

from playwright.async_api import expect

from tests.pages.core.constants import DeleteModeEnum
from tests.pages.core.fields_page import FieldsPage
from tests.pages.core.generic_page import GenericPage


class FieldGrupoPermisoEnum(Enum):
    """Campos disponibles en el formulario de grupos de permisos."""

    DISPLAY_NAME = "display_name"


class PageGrupoPermiso(GenericPage):
    """Page object para el módulo Grupos de permisos."""

    def __init__(self, page):
        super().__init__(page, module_name="Grupos", navigation=["Usuarios", "Grupos de permisos"])
        self.delete_mode = DeleteModeEnum.TOGGLE
        self.edit_form_title_selector = 'h1:has-text("Editar grupo")'

        # Selectores específicos de la UI dual-list de permisos
        self.available_permission_option_selector = "#all-permission p#id_add_option"
        self.current_permission_option_selector = "#current-permission p#id_remove_option"
        self.add_permission_button_selector = "#move-to-current"
        self.remove_permission_button_selector = "#move-to-all"
        self.current_permissions_container_selector = "#current-permission"
        self.available_permissions_container_selector = "#all-permission"

        self.input_field_instances = {
            FieldGrupoPermisoEnum.DISPLAY_NAME.value: FieldsPage(
                page=page,
                name=FieldGrupoPermisoEnum.DISPLAY_NAME.value,
                max_length=150,
                min_length=1,
            ),
        }

    async def _move_first_permission(self, source_option_selector: str, action_button_selector: str) -> str:
        """Marca y mueve el primer permiso visible desde una lista a otra."""
        await self.wait_for_selector(source_option_selector)
        source_option = self.page.locator(source_option_selector).first
        permission_text = ((await source_option.inner_text()) or "").strip()
        await source_option.evaluate("el => el.closest('li').classList.add('item-selected')")
        await self.page.click(action_button_selector)
        return permission_text

    async def add_first_available_permission(self) -> str:
        """Mueve un permiso disponible hacia la lista de permisos actuales."""
        permission_text = await self._move_first_permission(
            self.available_permission_option_selector, self.add_permission_button_selector
        )
        await expect(self.page.locator(self.current_permissions_container_selector)).to_contain_text(permission_text)
        return permission_text

    async def remove_first_current_permission(self) -> str:
        """Quita un permiso de la lista de permisos actuales."""
        permission_text = await self._move_first_permission(
            self.current_permission_option_selector, self.remove_permission_button_selector
        )
        await expect(self.page.locator(self.available_permissions_container_selector)).to_contain_text(permission_text)
        return permission_text

    async def create_record_with_permission(self, validate_record=True):
        """Crea un grupo asignando un permiso desde la UI dual-list."""
        await self.generate_random_data()
        await self.goto_create_page()
        await self.fill_input_fields()
        permission_text = await self.add_first_available_permission()

        await self.submit_form(self.submit_create_form_selector)
        await self.validate_success_message_and_continue(
            self.modal_message_selector,
            self.continue_button_selector,
            self.success_create_message_text,
        )

        self.generate_filters_and_validate_data()

        if validate_record:
            await self.goto_edit_page()
            await expect(self.page.locator(self.current_permissions_container_selector)).to_contain_text(
                permission_text
            )

    async def validate_edit_add_permission(self):
        """Valida que se pueda agregar un permiso en edición."""
        await self.create_record(validate_record=False)
        await self.goto_edit_page()
        permission_text = await self.add_first_available_permission()
        await self.submit_form(self.submit_create_form_selector)
        await self.validate_success_message_and_continue(
            self.modal_message_selector,
            self.continue_button_selector,
            self.success_edit_message_text,
        )

        await self.goto_edit_page()
        await expect(self.page.locator(self.current_permissions_container_selector)).to_contain_text(permission_text)
        await self.delete_record()

    async def validate_edit_remove_permission(self):
        """Valida que se pueda quitar un permiso en edición."""
        await self.create_record_with_permission(validate_record=False)
        await self.goto_edit_page()
        permission_text = await self.remove_first_current_permission()
        await self.submit_form(self.submit_create_form_selector)
        await self.validate_success_message_and_continue(
            self.modal_message_selector,
            self.continue_button_selector,
            self.success_edit_message_text,
        )

        await self.goto_edit_page()
        await expect(self.page.locator(self.current_permissions_container_selector)).not_to_contain_text(
            permission_text
        )
        await self.delete_record()
