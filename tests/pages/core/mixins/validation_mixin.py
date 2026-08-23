"""ValidationMixin for GenericPage.

This mixin encapsulates all validation methods (validate_*) for testing CRUD operations.

Required attributes from GenericPage:
    - page: Playwright Page instance
    - navigation: Navigation routes dictionary
    - data_validate: Dictionary with values to validate
    - edit_data_validate: Dictionary with values to validate in edit form
    - index_data_validate: Dictionary with values to validate in index view
    - data_filters: Dictionary with filter values
    - input_field_instances: Dictionary of FieldsPage instances
    - formset_fields: Dictionary of formset field definitions
    - formset_instances: Dictionary of formset instances
    - dependency_instances: Dictionary of dependency instances
    - delete_mode: DeleteModeEnum value (TOGGLE, DISABLE_INDEX, etc.)

Required selectors from GenericPage:
    - filter_button_selector
    - no_datos_selector
    - delete_button_selector
    - delete_modal_selector
    - delete_confirm_button_selector
    - confirm_disable_button_selector
    - confirm_enable_button_selector
    - enable_modal_selector
    - modal_message_selector
    - continue_button_selector
    - submit_create_form_selector
    - error_message_selector
    - index_page_title_selector
    - clear_filters_selector
    - cancel_modal_button_selector
    - cancel_alert_button_selector
    - swal2_confirm_button_selector
    - delete_row_formset_selector

Required messages from GenericPage:
    - not_found_filter_message_text
    - success_delete_message_text
    - success_restore_message_text
    - success_create_message_text
    - success_edit_message_text

Required methods from GenericPage:
    - wait_for_selector
    - goto_index_page
    - goto_disabled_index_page
    - goto_create_page
    - goto_detail_page
    - goto_edit_page
    - search_records_with_filters
    - validate_record_information_in_details_view
    - validate_record_information_in_edit_view
    - validate_record_information_in_index_view
    - fill_data
    - get_detail_button_selector
    - get_edit_button_selector
    - get_delete_button_selector
    - get_enable_button_selector
    - get_cancel_button_selector
    - get_back_button_selector
    - submit_form
    - check_error_message
    - create_record
    - delete_record
    - delete_dependencies
    - delete_formset_dependencies
    - generate_filters_and_validate_data
    - fill_input_fields
    - fill_formsets
    - generate_random_data
    - generate_formset_data
    - get_field_values
    - field_exists
    - get_input_instance_by_attribute
    - filter_by_specific_field
    - validate_many_filter_results
    - edit_record
"""

import logging
from typing import Optional
from urllib.parse import parse_qs, urlparse

from playwright.async_api import expect

from tests.pages.core.constants import DeleteModeEnum, InvalidDataType, ValidDataType
from tests.pages.core.fields_page import FieldsPage

logger = logging.getLogger(__name__)


class ValidationMixin:
    """Mixin that contains all validation methods for CRUD testing."""

    def _get_formset_field_values(self, field_name: str, mode: str = "create"):
        """Obtiene los valores de un campo de formset preservando orden de filas."""
        values = []

        for _, formset_modes in self.formset_instances.items():
            for row in formset_modes.get(mode, []) or []:
                for selector, field_object in row.items():
                    if self.get_formset_field_name(selector) != field_name:
                        continue
                    if isinstance(field_object, FieldsPage):
                        values.append(field_object.field_value)
                        break

        return values

    def _resolve_same_record_duplicate_value(
        self,
        field_name: str,
        custom_value=None,
        mode: str = "create",
        source_row_index: int = 0,
    ):
        """Resuelve el valor a duplicar dentro del mismo registro (formset actual).

        Args:
            field_name (str): Nombre lógico del campo en el formset.
            custom_value (Any, opcional): Valor explícito a reutilizar.
            mode (str): Modo de formset a consultar ("create" o "edit").
            source_row_index (int, opcional): Índice de la fila fuente cuyo valor se duplicará.
                Por defecto 0.

        Returns:
            Any: Valor listo para forzar duplicidad.

        Raises:
            ValueError: Si no existe valor suficiente para construir duplicado.
        """
        values = self._get_formset_field_values(field_name, mode=mode)

        if custom_value is not None:
            resolved_value = custom_value
        elif len(values) > source_row_index:
            resolved_value = values[source_row_index]
        elif values:
            resolved_value = values[0]
        else:
            resolved_value = None

        if resolved_value is None:
            raise ValueError(
                f"No se pudo construir duplicado en el mismo registro para '{field_name}'. "
                "Asegura al menos dos filas de formset para ese campo (ej. num_merch=2)."
            )
        return resolved_value

    def _get_formset_duplicate_value(self, field_name: str, mode: str = "create"):
        """Obtiene un valor existente de formset para provocar duplicado en el mismo registro.

        Args:
            field_name (str): Nombre lógico del campo en el formset.
            mode (str): Modo de formset a consultar ("create" o "edit").

        Returns:
            Any | None: Valor reutilizable para forzar duplicidad en otra fila,
            o None si no hay suficientes filas/valores.
        """
        values = self._get_formset_field_values(field_name, mode=mode)
        if len(values) >= 2:
            return values[1]
        if values:
            return values[0]
        return None

    async def validate_record(self, index_many_results=False):
        """Valida que los datos del registro coincidan con los valores esperados.

        Efectos:
            - Busca el registro usando los filtros actuales.
            - Si existe botón de detalle:
                * Navega a la vista de detalle.
                * Valida la información en `self.data_validate`.
            - En caso contrario:
                * Navega a la vista de edición.
                * Valida la información en `self.edit_data_validate`.

        Notas:
            - En formsets, la validación puede fallar si no están ordenados de forma ascendente.
              En ese caso se recomienda definir `ordering = ["id"]` en el modelo.
        """
        await self.search_records_with_filters(index_many_results=index_many_results)
        detail_button_selector = await self.get_detail_button_selector()
        edit_button_selector = await self.get_edit_button_selector()

        if detail_button_selector:
            logger.debug("Diccionario de validación: %s", self.data_validate)
            await self.validate_record_on_detail()

        elif edit_button_selector:
            logger.debug("Diccionario de validación (edit): %s", self.edit_data_validate)
            await self.validate_record_on_edit()

    async def validate_record_on_detail(self):
        """Valida los datos del registro desde la vista de detalle.

        Efectos:
            - Navega a la página de detalle.
            - Verifica que los campos coincidan con los valores en `self.data_validate`.
        """
        await self.goto_detail_page()
        await self.validate_record_information_in_details_view(self.data_validate)

    async def validate_record_on_edit(self):
        """Valida los datos del registro desde la vista de edición.

        Efectos:
            - Navega al formulario de edición.
            - Verifica que los campos coincidan con los valores en `self.edit_data_validate`.
        """
        await self.goto_edit_page()
        await self.validate_record_information_in_edit_view(self.edit_data_validate)

    async def validate_record_state(self, is_deleted=True):
        """Valida el estado del registro después de eliminar/deshabilitar o habilitar.

        Args:
            is_deleted (bool): True si el registro debe estar borrado/deshabilitado,
                               False si el registro debe estar habilitado/activo.

        Efectos:
            Valida que el registro esté en el estado esperado según delete_mode.
        """
        goto_method = (
            self.goto_disabled_index_page if self.delete_mode == DeleteModeEnum.DISABLE_INDEX else self.goto_index_page
        )
        await goto_method()
        await self.fill_data(self.data_filters)
        await self.page.click(self.filter_button_selector)
        if is_deleted:
            # Lógica para validar registro eliminado/deshabilitado

            if self.delete_mode == DeleteModeEnum.TOGGLE:
                enabled_button = await self.get_enable_button_selector()
                if enabled_button:
                    await self.wait_for_selector(enabled_button)
                    await expect(self.page.locator(enabled_button).first).to_be_visible()
                else:
                    await expect(self.page.locator(self.no_datos_selector)).to_contain_text(
                        self.not_found_filter_message_text
                    )
            elif self.delete_mode == DeleteModeEnum.DISABLE_INDEX:
                await self.validate_record_information_in_index_view(self.index_data_validate)
            else:
                await expect(self.page.locator(self.no_datos_selector)).to_contain_text(
                    self.not_found_filter_message_text
                )
        else:
            # Lógica para validar registro habilitado/activo

            if self.delete_mode == DeleteModeEnum.TOGGLE:
                delete_button = await self.get_delete_button_selector()
                if delete_button:
                    await self.wait_for_selector(delete_button)
                    await expect(self.page.locator(delete_button).first).to_be_visible()
                else:
                    await self.validate_record_information_in_index_view(self.index_data_validate)
            elif self.delete_mode == DeleteModeEnum.DISABLE_INDEX:
                await expect(self.page.locator(self.no_datos_selector)).to_contain_text(
                    self.not_found_filter_message_text
                )
            else:
                await self.validate_record_information_in_index_view(self.index_data_validate)

    async def validate_success_message_and_continue(
        self, message_selector: str, continue_button_selector: str, message: str, **kwargs
    ):
        """Valida que el mensaje de éxito mostrado coincida con el esperado y continúa el flujo.

        Args:
            message_selector (str): Selector del elemento que contiene el mensaje de éxito.
            continue_button_selector (str): Selector del botón para continuar después del mensaje.
            message (str): Texto esperado dentro del mensaje de éxito.
            kwargs: Parámetros adicionales (no utilizados).

        Efectos:
            - Espera la aparición del mensaje en la página.
            - Comprueba que el texto esperado esté presente en el mensaje.
            - Hace clic en el botón de continuar.
        """
        await self.wait_for_selector(message_selector)
        success_message = await self.page.text_content(message_selector)
        assert (
            message in success_message
        ), f"El mensaje de éxito no contiene el texto esperado: {message} mensaje obtenido: {success_message}"
        await self.page.click(continue_button_selector)

    async def validate_create_invalid_data(
        self,
        field_name: str,
        validate_type: InvalidDataType,
        custom_error_message: Optional[str] = None,
        custom_value: Optional[str] = None,
        **kwargs,
    ):
        """Valida que un campo muestre el comportamiento esperado al ingresar datos inválidos.

        Durante la creación de un registro.

        Args:
            field_name (str): Nombre del campo a validar.
            validate_type (InvalidDataType): Tipo de validación inválida a aplicar
                (ejemplo: duplicado, formato incorrecto, vacío, etc.).
            custom_error_message (str, opcional): Mensaje de error esperado, si se requiere uno específico.
            custom_value (str, opcional): Valor personalizado a usar como entrada inválida.
            **kwargs: Parámetros adicionales para generar datos o dependencias.

        Efectos:
            - Genera datos de prueba o crea un registro previo si la validación es de duplicados.
            - Navega al formulario de creación y llena los campos necesarios.
            - Aplica el valor inválido al campo especificado.
            - Cancela el formulario si aparece un modal de error.
            - Elimina el registro o dependencias creadas tras la validación.
            - Limpia formsets en caso de haberlos usado.
        """
        if not self.field_exists(field_name):
            raise ValueError(f"El campo '{field_name}' no existe en los campos de la página ni en formsets.")

        kwargs.update({"create_on_dependency_page": True})
        await self.generate_random_data(**kwargs)
        await self.generate_formset_data(**kwargs)

        duplicate_scope = kwargs.get("duplicate_scope", "database")
        duplicate_record_instance = None
        target_formset_row_index = kwargs.get("target_formset_row_index", 0)

        if validate_type == InvalidDataType.DUPLICATED and duplicate_scope == "same_record":
            # Opción 1: duplicar el valor de la primera fila en la segunda fila.
            target_formset_row_index = kwargs.get("target_formset_row_index", 1)
            custom_value = self._resolve_same_record_duplicate_value(
                field_name,
                custom_value,
                mode="create",
                source_row_index=0,
            )

            # Si el campo existe tanto en formulario principal como en formset
            # (ej. "title" en Álbum y en Canciones), priorizar el formset.
            field_exists_in_formset = any(
                field_name in formset_data.get("fields", {}) for formset_data in self.formset_fields.values()
            )
            if field_exists_in_formset:
                kwargs["lookup_formset"] = True

        elif validate_type == InvalidDataType.DUPLICATED:
            # Crear un registro duplicado para obtener el valor a duplicar
            duplicate_record_instance = self.__class__(self.page)
            await duplicate_record_instance.create_record(validate_record=False, **kwargs)
            duplicated_field_values = await duplicate_record_instance.get_field_values()

            # Buscar el valor correcto según si es campo normal o formset
            custom_value = None
            lookup_formset = kwargs.get("lookup_formset", False)

            # Caso 1: Campo normal (no formset)
            if field_name in duplicated_field_values and not lookup_formset:
                custom_value = duplicated_field_values[field_name]
            # Caso 2: Campo de formset - buscar por prefijo
            else:
                for name, value in duplicated_field_values.items():
                    formset_field = self.get_formset_field_name(name)
                    if formset_field == field_name:
                        custom_value = value
                        break

            if custom_value is None:
                raise ValueError(
                    f"No se pudo encontrar el valor duplicado para el campo '{field_name}'. "
                    f"Campos disponibles: {list(duplicated_field_values.keys())}"
                )

            self.generate_filters_and_validate_data()

        await self.goto_create_page()
        await self.fill_input_fields()
        await self.fill_formsets(**kwargs)

        lookup_formset = kwargs.pop("lookup_formset", False)
        await self._fill_field_with_data(
            field_name,
            validate_type,
            is_valid=False,
            custom_message=custom_error_message,
            custom_value=custom_value,
            lookup_formset=lookup_formset,
            target_formset_row_index=target_formset_row_index,
            **kwargs,
        )

        if duplicate_record_instance:
            await duplicate_record_instance.delete_record()

        await self.delete_dependencies()
        await self.delete_formset_dependencies()

    async def validate_edit_invalid_data(
        self,
        field_name: str,
        validate_type: InvalidDataType,
        custom_error_message: Optional[str] = None,
        custom_value: Optional[str] = None,
        **kwargs,
    ):
        """Valida que un campo muestre el comportamiento esperado al ingresar datos inválidos.

        Durante la edición de un registro.

        Args:
            field_name (str): Nombre del campo a validar.
            validate_type (InvalidDataType): Tipo de validación inválida a aplicar
                (ejemplo: duplicado, formato incorrecto, vacío, etc.).
            custom_error_message (str, opcional): Mensaje de error esperado, si se requiere uno específico.
            custom_value (str, opcional): Valor personalizado a usar como entrada inválida.
            **kwargs: Parámetros adicionales para generar datos o dependencias.

        Efectos:
            - Crea un registro inicial para poder editarlo.
            - Si la validación es de duplicados:
                * Crea un segundo registro duplicado para forzar la colisión.
                * Obtiene el valor a usar como entrada duplicada.
            - Navega al formulario de edición y aplica el valor inválido en el campo.
            - Elimina los registros y dependencias creados tras la validación.
            - Limpia formsets en caso de haberlos usado.
        """
        if not self.field_exists(field_name):
            raise ValueError(f"El campo '{field_name}' no existe en los campos de la página ni en formsets.")

        is_duplicate_allowed = validate_type == InvalidDataType.DUPLICATED
        duplicate_scope = kwargs.get("duplicate_scope", "database")
        duplicate_record_instance = None
        target_formset_row_index = kwargs.get("target_formset_row_index", 0)

        lookup_formset = kwargs.get("lookup_formset", False)
        if not lookup_formset and field_name in self.input_field_instances:
            field_exists_in_formset = any(
                field_name in formset_data.get("fields", {}) for formset_data in self.formset_fields.values()
            )
            if field_exists_in_formset:
                lookup_formset = True

        await self.create_record(**kwargs)

        if is_duplicate_allowed and duplicate_scope == "same_record":
            # Opción 1: duplicar el valor de la primera fila en la segunda fila.
            target_formset_row_index = kwargs.get("target_formset_row_index", 1)
            custom_value = self._resolve_same_record_duplicate_value(
                field_name,
                custom_value,
                mode="create",
                source_row_index=0,
            )

        elif is_duplicate_allowed:
            duplicate_record_instance = self.__class__(self.page)
            await duplicate_record_instance.create_record(validate_record=False, **kwargs)
            field_instance_value = await duplicate_record_instance.get_field_values()
            # Buscar el valor correcto según si es campo normal o formset
            custom_value = None

            # Caso 1: Campo normal (no formset)
            if field_name in field_instance_value and not lookup_formset:
                custom_value = field_instance_value[field_name]
            # Caso 2: Campo de formset - buscar por prefijo
            else:
                for name, value in field_instance_value.items():
                    if lookup_formset and name in self.input_field_instances:
                        continue
                    formset_field = self.get_formset_field_name(name)
                    if formset_field == field_name:
                        custom_value = value
                        break

            if custom_value is None:
                raise ValueError(
                    f"No se pudo encontrar el valor duplicado para el campo '{field_name}'. "
                    f"Campos disponibles: {list(field_instance_value.keys())}"
                )

        await self.goto_edit_page()

        await self._fill_field_with_data(
            field_name,
            validate_type,
            is_valid=False,
            custom_message=custom_error_message,
            custom_value=custom_value,
            lookup_formset=lookup_formset,
            target_formset_row_index=target_formset_row_index,
        )

        if duplicate_record_instance:
            await duplicate_record_instance.delete_record()

        await self.delete_record()
        await self.delete_formset_dependencies()

    async def validate_create_valid_data(
        self,
        field_name: str,
        validate_data_type: ValidDataType,
        custom_value: Optional[str] = None,
        delete_record=True,
        **kwargs,
    ):
        """Valida que un campo acepte datos correctos durante la creación de un registro.

        Args:
            field_name (str): Nombre del campo a validar.
            validate_data_type (ValidDataType): Tipo de validación válida a aplicar
                (ejemplo: texto, número, caracteres especiales, duplicado permitido, etc.).
            custom_value (str, opcional): Valor personalizado a usar como entrada válida.
            delete_record (bool, opcional): Si es True (por defecto), elimina el registro
                después de la validación.
            **kwargs: Parámetros adicionales para generar datos o dependencias.

        Efectos:
            - Genera datos de prueba y navega al formulario de creación.
            - Llena los campos principales y formsets si existen.
            - Aplica el valor válido en el campo especificado.
            - Valida el mensaje de éxito y los datos en el registro creado.
            - Elimina el registro si `delete_record` es True.
        """
        if not self.field_exists(field_name):
            raise ValueError(f"El campo '{field_name}' no existe en los campos de la página ni en formsets.")

        if self.formset_fields:
            await self.generate_formset_data(**kwargs)
        await self.generate_random_data(**kwargs)

        await self.goto_create_page()
        await self.fill_input_fields()
        await self.fill_formsets(**kwargs)

        await self._fill_field_with_data(
            field_name, validate_data_type, is_valid=True, custom_value=custom_value, **kwargs
        )

        await self.validate_success_message_and_continue(
            self.modal_message_selector, self.continue_button_selector, self.success_create_message_text
        )
        self.generate_filters_and_validate_data()
        await self.validate_record()
        if delete_record:
            await self.delete_record()

    async def validate_edit_valid_data(
        self, field_name: str, validate_data_type: ValidDataType, custom_value: Optional[str] = None, **kwargs
    ):
        """Valida que un campo acepte datos correctos durante la edición de un registro.

        Args:
            field_name (str): Nombre del campo a validar.
            validate_data_type (ValidDataType): Tipo de validación válida a aplicar
                (ejemplo: texto, número, caracteres especiales, duplicado permitido, etc.).
            custom_value (str, opcional): Valor personalizado a usar como entrada válida.
            **kwargs: Parámetros adicionales para generar datos o dependencias.

        Efectos:
            - Crea un registro inicial para editarlo.
            - Si el tipo de validación permite duplicados:
                * Crea un segundo registro para obtener un valor duplicado válido.
            - Navega al formulario de edición y aplica el valor válido al campo.
            - Valida el mensaje de éxito y actualiza los diccionarios de validación.
            - Elimina el registro editado y, si corresponde, las dependencias o registros duplicados.
            - Limpia formsets en caso de haberlos usado.
        """
        if not self.field_exists(field_name):
            raise ValueError(f"El campo '{field_name}' no existe en los campos de la página ni en formsets.")

        is_duplicate_allowed = validate_data_type == ValidDataType.ALLOW_DUPLICATES
        await self.create_record(validate_record=False, **kwargs)
        if is_duplicate_allowed:
            duplicate_record_instance = self.__class__(self.page)
            await duplicate_record_instance.create_record(validate_record=False, **kwargs)
            field_instance_value = (await duplicate_record_instance.get_field_values()).get(field_name)

        await self.goto_edit_page()

        if is_duplicate_allowed:
            await self._fill_field_with_data(
                field_name, validate_data_type, is_valid=True, custom_value=field_instance_value
            )
        else:
            await self._fill_field_with_data(
                field_name, validate_data_type, is_valid=True, custom_value=custom_value, **kwargs
            )

        await self.validate_success_message_and_continue(
            self.modal_message_selector, self.continue_button_selector, self.success_edit_message_text
        )
        self.generate_filters_and_validate_data(True)

        if is_duplicate_allowed:
            duplicate_record_instance.generate_filters_and_validate_data(True)
            await duplicate_record_instance.delete_record(delete_dependencies=False)
        await self.delete_record()

        if is_duplicate_allowed:
            await duplicate_record_instance.delete_dependencies()

        if self.formset_fields:
            await self.delete_formset_dependencies()

    async def validate_no_results_on_filters(self, field_name=None, disabled_index=False):
        """Verifica que la búsqueda con filtros no arroje resultados.

        Args:
            field_name (str, opcional): Nombre de un campo específico para aplicar y validar el filtro.
                Si no se proporciona, utiliza `self.data_filters`.
            disabled_index (bool, opcional): Si navegar al índice de deshabilitados.

        Efectos:
            - Navega a la vista de índice normal o deshabilitados.
            - Aplica el filtro (del campo específico o los filtros por defecto).
            - Valida que la tabla muestre el mensaje de "sin resultados".
        """
        # Paso 1: Navegar al índice apropiado
        if disabled_index:
            await self.goto_disabled_index_page()
        else:
            await self.goto_index_page()

        # Paso 2: Aplicar filtros según el modo
        if field_name:
            # Modo 1: Filtro de campo único - genera valor inexistente para ese campo
            await self.filter_by_specific_field(field_name)
        else:
            # Modo 2: Todos los filtros - siempre genera valores nuevos que no existen en la BD
            filters_to_apply = {}

            for field_instance in self.input_field_instances.values():
                if not getattr(field_instance, "is_filter", False):
                    continue
                selector = field_instance.filter_selector
                if not selector or not selector.startswith("input"):
                    continue
                field_instance.generate_valid_data(ignore_generated_fields=False)
                if field_instance.filter_value is not None:
                    filters_to_apply[selector] = field_instance.filter_value

            # Aplicar los filtros regenerados
            await self.fill_data(filters_to_apply)

        # Paso 3: Ejecutar búsqueda y validar mensaje de sin resultados
        await self.page.click(self.filter_button_selector)
        await expect(self.page.locator(self.no_datos_selector)).to_contain_text(self.not_found_filter_message_text)

    async def validate_cancel_create_form_returns_to_index(self, **kwargs):
        """Valida que el botón Cancelar del formulario de creación regrese a la vista de índice.

        Efectos:
            - Navega a la página de creación.
            - Obtiene y espera el selector del botón Cancelar.
            - Hace clic en Cancelar.
            - Verifica que el título de la página de índice sea visible.

        Notas:
            - `**kwargs` se acepta por consistencia con otras validaciones, aunque no se utiliza.
        """
        await self.goto_create_page()
        await self.page.wait_for_timeout(200)
        cancel_selector = await self.get_cancel_button_selector()
        await self.wait_for_selector(cancel_selector)
        await self.page.click(cancel_selector)
        await expect(self.page.locator(self.index_page_title_selector)).to_be_visible()

    async def validate_cancel_edit_form_returns_to_index(self, **kwargs):
        """Valida que el botón Cancelar del formulario de edición regrese a la vista de índice.

        Efectos:
            - Crea un registro de prueba.
            - Navega al formulario de edición.
            - Obtiene y espera el selector del botón Cancelar.
            - Hace clic en Cancelar.
            - Verifica que el título de la página de índice sea visible.
            - Elimina el registro creado.

        Notas:
            - `**kwargs` se pasa a `create_record` para personalizar la data del registro de prueba.
        """
        await self.create_record(**kwargs)
        await self.goto_edit_page()
        cancel_selector = await self.get_cancel_button_selector()
        await self.wait_for_selector(cancel_selector)
        await self.page.click(cancel_selector)
        await expect(self.page.locator(self.index_page_title_selector)).to_be_visible()
        await self.delete_record()

    async def validate_back_button_on_create(self):
        """Valida que el botón Volver del formulario de creación redirija a la página de índice.

        Efectos:
            - Navega al formulario de creación.
            - Obtiene y espera el selector del botón Volver.
            - Hace clic en el botón.
            - Espera la visibilidad del título de la página de índice.
        """
        await self.goto_create_page()
        back_button_selector = await self.get_back_button_selector()
        await self.wait_for_selector(back_button_selector)
        await self.page.click(back_button_selector)
        await self.wait_for_selector(self.index_page_title_selector)

    async def validate_back_button_on_edit(self):
        """Valida que el botón Volver del formulario de edición redirija a la página de índice.

        Efectos:
            - Crea un registro de prueba y navega al formulario de edición.
            - Obtiene y espera el selector del botón Volver.
            - Hace clic en el botón.
            - Espera la visibilidad del título de la página de índice.
            - Elimina el registro creado.
        """
        await self.create_record()
        await self.goto_edit_page()
        back_button_selector = await self.get_back_button_selector()
        await self.wait_for_selector(back_button_selector)
        await self.page.click(back_button_selector)
        await self.wait_for_selector(self.index_page_title_selector)
        await self.delete_record()

    async def validate_back_button_on_detail(self):
        """Valida que el botón Volver de la vista de detalle redirija a la página de índice.

        Efectos:
            - Crea un registro de prueba y navega a la vista de detalle.
            - Obtiene y espera el selector del botón Volver.
            - Hace clic en el botón.
            - Espera la visibilidad del título de la página de índice.
            - Elimina el registro creado.
        """
        await self.create_record()
        await self.goto_detail_page()
        back_button_selector = await self.get_back_button_selector()
        await self.wait_for_selector(back_button_selector)
        await self.page.click(back_button_selector)
        await self.wait_for_selector(self.index_page_title_selector)
        await self.delete_record()

    async def validate_back_button_on_disabled_index(self):
        """Valida que el botón Volver del índice de deshabilitados redirija al índice normal.

        Efectos:
            - Crea un registro de prueba y lo deshabilita.
            - Navega a la vista índice de registros deshabilitados.
            - Obtiene y espera el selector del botón Volver.
            - Hace clic en el botón.
            - Espera la visibilidad del título de la página de índice normal.
            - Elimina las dependencias creadas.
        """
        await self.create_record()
        await self.delete_record(delete_dependencies=False)
        await self.goto_disabled_index_page()
        back_button_selector = await self.get_back_button_selector()
        await self.wait_for_selector(back_button_selector)
        await self.page.click(back_button_selector)
        await self.wait_for_selector(self.index_page_title_selector)
        await self.delete_dependencies()

    async def validate_clear_filters_button(self, **kwargs):
        """Valida que el botón de limpiar filtros borre los valores de los campos de filtro.

        Efectos:
            - Crea un registro de prueba y aplica filtros en la vista índice normal.
            - Hace clic en el botón de limpiar filtros.
            - Verifica que los campos de filtro queden vacíos.
            - Elimina el registro creado.

        Notas:
            - `**kwargs` se pasa a `create_record` para personalizar los datos del registro de prueba.
        """
        await self.create_record(**kwargs)
        await self.search_records_with_filters(self.data_filters)
        await self.wait_for_selector(self.clear_filters_selector)
        await self.page.click(self.clear_filters_selector)
        for field, instance in self.input_field_instances.items():
            if instance.is_filter:
                await expect(self.page.locator(instance.filter_selector)).to_contain_text("")
        await self.delete_record()

    async def validate_clear_filters_button_in_disabled_index(self, **kwargs):
        """Valida el botón de limpiar filtros en la vista índice de registros deshabilitados.

        Efectos:
            - Crea un registro de prueba y lo deshabilita.
            - Navega a la vista índice de registros deshabilitados.
            - Aplica filtros en la vista índice.
            - Hace clic en el botón de limpiar filtros.
            - Verifica que los campos de filtro queden vacíos.
            - Elimina las dependencias creadas.

        Notas:
            - `**kwargs` se pasa a `create_record` para personalizar los datos del registro de prueba.
        """
        await self.create_record(**kwargs)
        await self.delete_record(delete_dependencies=False)
        await self.search_records_with_filters(search_disabled=True)
        await self.wait_for_selector(self.clear_filters_selector)
        await self.page.click(self.clear_filters_selector)
        for field, instance in self.input_field_instances.items():
            if instance.is_filter:
                await expect(self.page.locator(instance.filter_selector)).to_contain_text("")
        await self.delete_dependencies()

    async def validate_cancel_double_validation_modal(self, field_name):
        """Valida el flujo de cancelación en un modal de doble confirmación.

        Al intentar eliminar una dependencia relacionada.

        Args:
            field_name (str): Clave usada para localizar las instancias de dependencia
                dentro de `self.dependency_instances`.

        Efectos:
            - Crea un registro de prueba.
            - Abre el flujo de eliminación en cada dependencia creada (modo "create").
            - Si existe una segunda confirmación (doble validación), la cancela.
            - Cancela el alerta principal de eliminación.
            - Elimina el registro de prueba creado al inicio.
        """
        await self.create_record()
        dependency_instance = self.dependency_instances[field_name]
        for dependency in dependency_instance.get("create", {}):
            await dependency.search_records_with_filters()
            await dependency.wait_for_selector(dependency.delete_button_selector)
            await dependency.page.click(dependency.delete_button_selector)
            await dependency.wait_for_selector(dependency.delete_confirm_button_selector)
            await dependency.page.click(dependency.delete_confirm_button_selector)
            # Doble verificacion
            if await dependency.page.locator(dependency.swal2_confirm_button_selector).count() > 0:
                await dependency.page.click(dependency.cancel_modal_button_selector)
            await dependency.page.click(dependency.cancel_alert_button_selector)

        await self.delete_record()

    async def validate_many_results_on_filter(self, field_name):
        """Valida que un filtro produzca múltiples coincidencias en la tabla índice.

        Args:
            field_name (str): Nombre del campo cuyo filtro se aplicará.

        Efectos:
            - Obtiene el `filter_value` del campo indicado.
            - Si el valor es una lista, valida cada elemento con su índice esperado.
            - Si el valor es único, realiza una validación única.
        """
        if not self.field_exists(field_name):
            raise ValueError(f"El campo '{field_name}' no existe en los campos de la página ni en formsets.")

        search_field = self.input_field_instances[field_name]
        if isinstance(search_field.filter_value, list):
            for index, sub_value in enumerate(search_field.filter_value):
                await self.validate_many_filter_results(
                    search_field.filter_selector, sub_value, search_field.validate_value, index
                )
        else:
            await self.validate_many_filter_results(
                search_field.filter_selector, search_field.filter_value, search_field.validate_value
            )

    async def validate_cancel_delete_modal(self):
        """Valida que al cancelar el modal de eliminación no se modifique la tabla.

        Efectos:
            - Busca el registro con los filtros actuales.
            - Abre el modal de eliminación.
            - Hace clic en Cancelar en el modal.
            - Verifica que la información en la vista índice permanezca correcta e intacta.
        """
        await self.create_record()
        await self.search_records_with_filters()
        delete_button = await self.get_delete_button_selector()
        await self.page.click(delete_button)
        await self.wait_for_selector(self.cancel_alert_button_selector)
        await self.page.click(self.cancel_alert_button_selector)
        # Valida que se canceló la eliminación
        await self.validate_record_information_in_index_view(self.index_data_validate)
        await self.delete_record()

    async def validate_cancel_enable_modal(self, create_record=True, delete_record=True, delete_dependencies=True):
        """Valida que al cancelar el modal de habilitación no se modifique la tabla.

        Efectos:
            - Busca el registro con los filtros actuales.
            - Abre el modal de habilitar.
            - Hace clic en Cancelar en el modal.
            - Verifica que la información en la vista índice permanezca correcta e intacta.
        """
        if create_record:
            await self.create_record()

        if delete_record:
            await self.delete_record(delete_dependencies=False)

        if self.delete_mode == DeleteModeEnum.DISABLE_INDEX:
            await self.search_records_with_filters(search_disabled=True)
        else:
            await self.search_records_with_filters()
        enable_button = await self.get_enable_button_selector()
        await self.page.click(enable_button)
        cancel_button = await self.get_cancel_button_selector()
        await self.wait_for_selector(cancel_button)
        await self.page.click(cancel_button)
        # Valida que se canceló la habilitación
        await self.validate_record_information_in_index_view(self.index_data_validate)

        if delete_dependencies:
            await self.delete_dependencies()

    async def validate_edit_without_changes(self, delete_record=True):
        """Valida que enviar el formulario de edición sin realizar cambios produzca un éxito y mantenga los datos.

        Efectos:
            - Crea un registro de prueba y navega al formulario de edición.
            - Envía el formulario sin modificar campos.
            - Verifica el mensaje de éxito de edición.
            - Valida que el registro conserve la información esperada.
            - Elimina el registro creado.
        """
        await self.create_record()
        await self.goto_edit_page()
        await self.wait_for_selector(self.submit_create_form_selector)
        await self.page.click(self.submit_create_form_selector)
        await self.validate_success_message_and_continue(
            self.modal_message_selector,
            self.continue_button_selector,
            self.success_edit_message_text,
        )
        await self.validate_record()
        if delete_record:
            await self.delete_record()

    async def validate_delete_formset_row_on_create(self, formset_name, num_delete_rows, **kwargs):
        """Valida la eliminación de filas de un formset durante la creación de un registro.

        Args:
            formset_name (str): Nombre del formset a validar.
            num_delete_rows (int): Número de filas a eliminar.
            **kwargs: Parámetros opcionales (por ejemplo, `num_<formset_name>` para definir
                la cantidad inicial de filas).

        Efectos:
            - Ajusta la cantidad inicial de filas según si el formset es requerido.
            - Crea un registro de prueba sin enviarlo.
            - Elimina las filas indicadas en modo "create".
            - Elimina las dependencias generadas.
        """
        is_required = self.formset_fields[formset_name].get("is_required", False)
        if not kwargs.get(f"num_{formset_name}"):
            kwargs.update({f"num_{formset_name}": num_delete_rows if not is_required else num_delete_rows + 1})
        await self.create_record(submit=False, **kwargs)
        await self.delete_formset_rows(formset_name, num_delete_rows, mode="create", **kwargs)
        await self.delete_dependencies()

    async def validate_delete_formset_row_on_edit(self, formset_name, num_delete_rows, **kwargs):
        """Valida la eliminación de filas de un formset durante la edición de un registro.

        Args:
            formset_name (str): Nombre del formset a validar.
            num_delete_rows (int): Número de filas a eliminar.
            **kwargs: Parámetros opcionales (por ejemplo, `num_<formset_name>` para definir
                la cantidad inicial de filas).

        Efectos:
            - Ajusta la cantidad inicial de filas según si el formset es requerido.
            - Crea y valida un registro de prueba.
            - Entra al formulario de edición sin enviar.
            - Elimina las filas indicadas en modo "edit".
            - Envía el formulario y valida el mensaje de éxito.
            - Valida nuevamente el registro y lo elimina al final.
        """
        is_required = self.formset_fields[formset_name].get("is_required", False)
        if not kwargs.get(f"num_{formset_name}"):
            kwargs.update({f"num_{formset_name}": num_delete_rows if not is_required else num_delete_rows + 1})
        await self.create_record(**kwargs)
        await self.validate_record()
        await self.edit_record(submit=False, **kwargs)
        await self.delete_formset_rows(formset_name, num_delete_rows, mode="edit", **kwargs)
        await self.submit_form(self.submit_create_form_selector)
        await self.validate_success_message_and_continue(
            self.modal_message_selector,
            self.continue_button_selector,
            self.success_edit_message_text,
        )
        await self.validate_record()
        await self.delete_record()

    async def validate_enable_record(self, **kwargs):
        """Valida que sea posible habilitar un registro previamente deshabilitado.

        Efectos:
            - Crea un registro de prueba.
            - Lo deshabilita/elimina según el modo configurado (sin borrar dependencias).
            - Ejecuta la acción de habilitar.
            - Valida que el registro activo coincida con los datos esperados.
            - Elimina el registro al finalizar.

        Notas:
            - `**kwargs` se pasa a `create_record` para personalizar la creación del registro.
        """
        await self.create_record(**kwargs)
        await self.delete_record(delete_dependencies=False)
        await self.enable_record()
        await self.validate_record()
        await self.delete_record()

    async def validate_empty_filters(self, disabled_index=False):
        """Valida que todos los parámetros de la URL de filtros estén vacíos.

        Efectos:
            - Navega a la página de índice y ejecuta la búsqueda.
            - Analiza la URL resultante para verificar que cada parámetro esté vacío.
            - Falla la prueba (pytest.fail) si alguno contiene un valor no vacío.
        """
        if disabled_index:
            await self.goto_disabled_index_page()
        else:
            await self.goto_index_page()
        await self.page.click(self.filter_button_selector)
        url = self.page.url

        # Parse URL
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)

        # Validar que todos los parámetros estén vacíos
        for param, values in query_params.items():
            if any(values):
                raise AssertionError(f"El parámetro de filtro '{param}' no está vacío. Valores encontrados: {values}")

    # Private methods
    async def _fill_field_with_data(
        self,
        field_name: str,
        validate_type,
        is_valid: bool = True,
        custom_message: Optional[str] = None,
        custom_value: Optional[str] = None,
        lookup_formset: bool = False,
        **kwargs,
    ):
        """Rellena un campo con datos válidos o inválidos para testing.

        Método unificado que maneja tanto validaciones exitosas como fallidas.

        Args:
            field_name (str): Nombre del campo a afectar.
            validate_type: Tipo de validación (ValidDataType o InvalidDataType).
            is_valid (bool): True para datos válidos, False para datos inválidos. Por defecto True.
            custom_message (str, opcional): Mensaje de error esperado (solo para is_valid=False).
            custom_value (Any, opcional): Valor personalizado a ingresar.
            lookup_formset (bool, opcional): Si buscar el campo en formsets.
            **kwargs: Parámetros adicionales para el llenado.

        Efectos:
            - Si el campo existe en `input_field_instances`, delega al método específico del campo.
            - En caso contrario, intenta rellenarlo dentro de un formset mediante `_fill_formset_field`.

        Raises:
            ValueError: Si el campo no existe en los campos de la página ni en formsets.
        """
        if not self.field_exists(field_name):
            raise ValueError(f"El campo '{field_name}' no existe en las instancias de campos o formsets.")

        field_instance: FieldsPage = self.input_field_instances.get(field_name)

        # When lookup_formset is requested, only route to the formset path if the
        # field actually exists in a formset.  If the field lives only in the main
        # form (e.g. "year" or "artist"), fall back to the main-form path so that
        # the form is filled and submitted correctly.
        field_in_any_formset = any(
            field_name in formset_data.get("fields", {}) for formset_data in self.formset_fields.values()
        )
        use_main_form = field_instance and (not lookup_formset or not field_in_any_formset)

        if use_main_form:
            if is_valid:
                await self.fill_specific_field_with_valid_data(field_instance, validate_type, custom_value)
            else:
                await self.fill_specific_field_with_invalid_data(
                    field_instance, validate_type, custom_message, custom_value
                )
        else:
            await self._fill_formset_field(
                field_name,
                is_valid=is_valid,
                validate_type=validate_type,
                custom_value=custom_value,
                custom_message=custom_message if not is_valid else None,
                target_formset_row_index=kwargs.get("target_formset_row_index", 0),
            )

        if field_instance and is_valid:
            self.input_field_instances[field_name] = field_instance
