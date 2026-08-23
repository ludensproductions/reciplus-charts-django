"""Mixin que encapsula toda la lógica relacionada con formsets.

Este mixin contiene métodos para generar, llenar, validar y eliminar filas de formsets.
"""

import logging
from enum import Enum
from typing import Dict, Optional

from playwright.async_api import expect

from tests.pages.core.constants import DependencyAction, InputType
from tests.pages.core.fields_page import FieldsPage
from tests.utils.selectors.selector_builder import FieldSelectorBuilder

logger = logging.getLogger(__name__)


class FillFormsetOptions(Enum):
    """Estrategias para manejar las filas de un formset al llenar/editar formularios.

    Opciones:
        KEEP_AND_ADD   : Conserva las filas existentes y agrega nuevas al final.
        REPLACE_ALL    : Reemplaza (recrea) todas las filas existentes.
        EDIT_AND_ADD   : Edita las filas existentes y agrega filas adicionales.
    """

    KEEP_AND_ADD = "keep_and_add"
    REPLACE_ALL = "replace_all"
    EDIT_AND_ADD = "edit_and_add"


class FormsetMixin:
    """Mixin que encapsula toda la lógica relacionada con formsets."""

    def __init__(self, *args, **kwargs):
        """Inicializa los atributos relacionados con formsets."""
        super().__init__(*args, **kwargs)
        # Inicializar atributos de formsets si no existen
        self.formset_fields = {}
        self.formset_instances = {}
        self.formset_dependecy_instances = {}
        self.delete_row_formset_selector = "button.delete-formset"

    # ===============================================
    # Sección 1: Generación de datos de formsets
    # ===============================================

    async def generate_formset_data(self, create_on_dependency_page=True, mode="create", **kwargs):
        """Genera automáticamente las filas de cada formset según la metadata de dependencias.

        Args:
            create_on_dependency_page (bool, opcional): Si crear dependencias desde su propia página.
                Por defecto False.
            mode (str, opcional): Modo de operación, "create" o "edit". Por defecto "create".
            **kwargs: Puede incluir:
                - num_<formset_name> (int): Cantidad de filas a generar por formset.
                - formset_mode (FillFormsetOptions): Estrategia de llenado en modo edit.

        Efectos:
            - Por cada formset en `self.formset_fields`:
                * Genera las filas requeridas según kwargs.
                * Crea instancias de dependencias según `create_on_dependency_page`.
                * Almacena las filas en `self.formset_instances[formset_name][mode]`.
            - Si está en modo `edit` y `formset_mode = KEEP_AND_ADD / EDIT_AND_ADD`, preserva
              las filas de `create`.
        """
        formset_mode = kwargs.get("formset_mode", FillFormsetOptions.REPLACE_ALL)

        for formset_name, formset_data in self.formset_fields.items():
            # Inicializar modo si no existe
            if formset_name not in self.formset_instances:
                self.formset_instances[formset_name] = {"create": [], "edit": []}

            num_formsets = kwargs.get(f"num_{formset_name}", 1)

            # Determinar cuántas filas generar según el modo
            total_create = len(self.formset_instances[formset_name].get("create", []))

            if mode == "edit":
                if formset_mode == FillFormsetOptions.REPLACE_ALL:
                    self.formset_instances[formset_name]["edit"] = []
                    range_formsets = range(num_formsets)
                elif formset_mode == FillFormsetOptions.KEEP_AND_ADD:
                    # Preservar las filas de create, agregar nuevas
                    self.formset_instances[formset_name]["edit"] = self.formset_instances[formset_name][
                        "create"
                    ].copy()
                    range_formsets = range(num_formsets)
                elif formset_mode == FillFormsetOptions.EDIT_AND_ADD:
                    # Editar las filas existentes, agregar nuevas
                    self.formset_instances[formset_name]["edit"] = self.formset_instances[formset_name][
                        "create"
                    ].copy()
                    range_formsets = range(num_formsets - total_create)
                else:
                    raise ValueError(f"formset_mode inválido: {formset_mode}")
            else:
                range_formsets = range(num_formsets)

            # Generar las filas
            for i in range_formsets:
                if mode == "edit" and formset_mode in [
                    FillFormsetOptions.KEEP_AND_ADD,
                    FillFormsetOptions.EDIT_AND_ADD,
                ]:
                    index = total_create + i
                else:
                    index = i
                new_form = await self._build_formset_entry(
                    formset_name, formset_data, index, create_on_dependency_page, mode, **kwargs
                )
                self.formset_instances[formset_name][mode].append(new_form)

    async def _build_formset_entry(self, formset_name, formset_data, index, create_on_page_dependency, mode, **kwargs):
        """Construye una fila de formset con los valores y metadatos necesarios.

        Args:
            formset_name (str): Nombre del formset.
            formset_data (dict): Configuración del formset, incluyendo su mapeo de `fields`.
            index (int): Índice de la fila a generar.
            create_on_page_dependency (bool): Valor por defecto para crear dependencias desde su página.
            mode (str): Modo en el que se genera la fila ("create" o "edit").
            **kwargs: Parámetros adicionales.

        Returns:
            dict: Diccionario {selector: FieldsPage/GenericPage} para la fila del formset.
        """
        from utils.utils_functions import camel_to_snake

        new_formset = {}
        fields_formset = list(formset_data["fields"].keys())

        # Procesar dependencias
        for dependency, configuration in self.input_field_dependencies.items():
            fields_configurations_dict = configuration.get(DependencyAction.CREATE, {})
            fields_configurations = fields_configurations_dict.keys()

            if not any(field in fields_formset for field in fields_configurations):
                continue

            dependency_snake = camel_to_snake(
                dependency.__name__.replace("Page", "", 1)
                if dependency.__name__.startswith("Page")
                else dependency.__name__
            )

            num_dependencies = kwargs.get(
                f"num_{dependency_snake}", self._get_num_dependencies_for_dependency(dependency)
            )
            should_create_on_page = kwargs.get(f"create_on_page_{dependency_snake}", create_on_page_dependency)

            if num_dependencies == 0:
                continue

            if should_create_on_page and num_dependencies > 0:
                await self._process_formset_dependency_fields(
                    new_formset,
                    formset_name,
                    formset_data,
                    index,
                    dependency,
                    fields_configurations,
                    num_dependencies,
                    mode,
                    **kwargs,
                )
            else:
                self._add_non_dependency_fields(
                    new_formset,
                    formset_name,
                    formset_data,
                    index,
                    fields_configurations,
                    mode,
                )

        # Agregar campos sin dependencias
        for field, field_instance in formset_data["fields"].items():
            if field not in self.get_keys_dependencies():
                cloned_instance = self._clone_field_for_formset_row(formset_name, index, field, field_instance)
                new_formset[cloned_instance.field_selector] = cloned_instance

        return new_formset

    async def _process_formset_dependency_fields(
        self,
        new_formset,
        formset_name,
        formset_data,
        index,
        dependency,
        fields_configurations,
        num_dependencies,
        mode,
        **kwargs,
    ):
        """Procesa todos los campos de una dependencia para un formset.

        Args:
            new_formset: Diccionario de campos del formset a construir
            formset_name: Nombre del formset
            formset_data: Configuración del formset
            index: Índice de la fila
            dependency: Clase de la dependencia
            fields_configurations: Campos configurados para esta dependencia
            num_dependencies: Número de instancias a crear
            mode: Modo "create" o "edit"
            **kwargs: Parámetros adicionales
        """
        fields_formset = list(formset_data["fields"].keys())

        for num_dependency in range(num_dependencies):
            dependency_instance, selector = await self.create_formset_dependency_instance(
                formset_name, index, dependency, mode, **kwargs
            )

            for field_name in fields_configurations:
                if field_name not in fields_formset:
                    continue

                field_instance = formset_data["fields"].get(field_name)
                if not field_instance:
                    continue

                if field_instance.input_type in [InputType.SELECT2_MULTIPLE, InputType.SELECT2]:
                    if num_dependency == 0:
                        # Primera iteración: crear el FieldsPage
                        cloned_field = self._clone_field_for_formset_row(
                            formset_name, index, field_name, field_instance
                        )
                        self._assign_select2_values(
                            cloned_field, dependency_instance, field_name, num_dependency, is_edit=False
                        )
                        new_formset[selector] = cloned_field
                    else:
                        # Iteraciones subsiguientes: acumular valores
                        if selector in new_formset:
                            self._assign_select2_values(
                                new_formset[selector], dependency_instance, field_name, num_dependency, is_edit=False
                            )
                else:
                    # Para SELECT normales y otros tipos de campos, guardar la dependencia directamente
                    new_formset[selector] = dependency_instance

    def _add_non_dependency_fields(
        self,
        new_formset,
        formset_name,
        formset_data,
        index,
        fields_configurations,
        mode,
    ):
        """Agrega campos sin dependencias al formset.

        Args:
            new_formset: Diccionario de campos del formset
            formset_name: Nombre del formset
            formset_data: Configuración del formset
            index: Índice de la fila
            fields_configurations: Campos que tienen dependencias configuradas
            mode: Modo de operación ("create" o "edit").
        """
        fields_formset = list(formset_data["fields"].keys())

        for field in fields_configurations:
            if field not in fields_formset:
                continue

            field_instance = formset_data["fields"].get(field)
            if not field_instance:
                raise Exception(f"El campo '{field}' requerido en formset '{formset_name}' no está definido.")

            cloned_instance = self._clone_field_for_formset_row(formset_name, index, field, field_instance)
            selector = cloned_instance.field_selector
            new_formset[selector] = cloned_instance

    # ===============================================
    # Sección 2: Llenado de formsets en UI
    # ===============================================

    async def fill_formsets(self, mode="create", **kwargs):
        """Completa las filas de formset en la interfaz según el modo especificado.

        Args:
            mode (str, opcional): Modo de operación, "create" o "edit". Por defecto "create".
            **kwargs: Puede incluir:
                - formset_mode (FillFormsetOptions): Estrategia de llenado en modo edit.
                - num_<formset_name> (int): Cantidad de filas esperadas por formset.

        Efectos:
            - Hace clic en el botón "Agregar" del formset según el conteo requerido.
            - Recorre las instancias del formset en `self.formset_instances[mode]`.
            - Llama a `_fill_formset_instance` para completar cada fila.
            - Respeta la estrategia definida por `formset_mode` en modo edición.
        """
        formset_mode = kwargs.get("formset_mode", FillFormsetOptions.REPLACE_ALL)

        for formset_name, formset_instances in self.formset_instances.items():
            num_formsets = kwargs.get(f"num_{formset_name}", 1)
            add_button = self.formset_fields[formset_name].get("add_button_selector")
            has_initial_row = self.formset_fields[formset_name].get(
                "has_initial_row", True
            )  # Por defecto True, es para saber si ya tiene una fila el formset
            count = len(formset_instances[mode])
            if mode == "create":
                await self._click_add_buttons(add_button, count, has_initial_row=has_initial_row)
            elif mode == "edit":
                if formset_mode == FillFormsetOptions.REPLACE_ALL:
                    count = 0
                else:
                    count = num_formsets + 1
                await self._click_add_buttons(add_button, count, mode, has_initial_row)
            for formset_instance in formset_instances[mode]:
                await self._fill_formset_instance(formset_instance, formset_name)

    async def _click_add_buttons(self, add_button_selector, count, mode="create", has_initial_row=True):
        """Hace clic en el botón de Agregar de un formset la cantidad requerida.

        Args:
            add_button_selector (str): Selector del botón para agregar filas del formset.
            count (int): Número total de filas que deben existir tras los clics.
            mode (str, opcional): Contexto de uso, "create" o "edit". Por defecto "create".
            has_initial_row (bool, opcional): Si el formset ya tiene una fila inicial. Por defecto True.

        Efectos:
            - Espera la visibilidad del botón de agregar.
            - Realiza `count` clics para generar las filas necesarias.

        Nota:
            FIX: Se cambió de `range(count - 1)` a `range(count)` porque cuando count=1,
            range(0) no ejecutaba ningún clic. Ahora si count=1, hace 1 clic correctamente.
        """
        if mode == "edit":
            await self.wait_for_selector(add_button_selector, 2)
            clicks_needed = count - 1 if has_initial_row else count
            for i in range(clicks_needed):
                await self.page.click(add_button_selector)

        elif mode == "create":
            await self.wait_for_selector(add_button_selector, 2)
            clicks_needed = count - 1 if has_initial_row else count
            for _ in range(clicks_needed):
                await self.page.click(add_button_selector)

    async def _fill_formset_instance(self, formset_instance, formset_name):
        """Completa una fila de formset en la UI con los valores preparados.

        Args:
            formset_instance (dict): Mapeo {selector: objeto} donde el objeto puede ser
                una dependencia (`GenericPage`) o un `FieldsPage` con `field_value`.
            formset_name (str): Nombre del formset al que pertenece la fila.

        Efectos:
            - Si el valor es `GenericPage`, delega a `_fill_formset_dependency`.
            - Si el valor es `FieldsPage`, llama a `fill_data` con su `field_value`.
        """
        for selector, obj in formset_instance.items():
            # Importar GenericPage aquí para evitar importación circular
            from tests.pages.core.generic_page import GenericPage

            if isinstance(obj, GenericPage):
                value = self._resolve_dependency_value(obj, self.get_formset_field_name(selector))
                field_name = self.get_formset_field_name(selector)
                field_config = self.formset_fields.get(formset_name, {}).get("fields", {}).get(field_name)
                if field_config:
                    value = field_config.truncate_if_needed(value, "field")
                    value = field_config.generate_select2_value(field_config.input_type, value)
                await self.fill_data({selector: value})

            elif isinstance(obj, FieldsPage):
                await self.fill_data({selector: obj.field_value})

    async def _fill_formset_field(
        self,
        field_name,
        is_valid,
        validate_type,
        custom_value=None,
        custom_message=None,
        target_formset_row_index: int = 0,
    ):
        """Rellena un campo de formset con datos válidos o inválidos.

        Args:
            field_name (str): Nombre del campo a afectar.
            is_valid (bool): Si True usa datos válidos, si False datos inválidos.
            validate_type: Tipo de validación a aplicar (ValidDataType o InvalidDataType).
            custom_value (Any, opcional): Valor personalizado a ingresar.
            custom_message (str, opcional): Mensaje de error esperado.
            target_formset_row_index (int, opcional): Índice de fila del formset que se
                modificará. Por defecto 0.

        Efectos:
            - Busca el campo en formsets.
            - Aplica el valor correspondiente al tipo de validación.
        """
        for formset_name, field_instances in self.formset_instances.items():
            rows = field_instances.get("create", [])
            if not rows:
                continue

            row_index = min(target_formset_row_index, len(rows) - 1)

            for selector, field_object in rows[row_index].items():
                field = None
                original_selector = None
                field_by_selector = self.get_formset_field_name(selector)
                if field_by_selector != field_name:
                    continue

                # Importar GenericPage aquí para evitar importación circular
                from tests.pages.core.generic_page import GenericPage

                if isinstance(field_object, GenericPage):
                    dependency_name = self.input_field_dependencies.get(field_object.__class__, None).get(
                        DependencyAction.CREATE
                    )
                    field = field_object.input_field_instances.get(dependency_name.get(field_name)[0])
                    original_selector = field.field_selector
                    field.field_selector = selector

                elif isinstance(field_object, FieldsPage):
                    field = field_object
                    original_selector = field.field_selector
                    field.field_selector = selector

                if field:
                    # Llamar directamente a los métodos de llenado específicos
                    # en lugar de _fill_field_with_data para evitar recursión
                    if is_valid:
                        await self.fill_specific_field_with_valid_data(field, validate_type, custom_value)
                    else:
                        await self.fill_specific_field_with_invalid_data(
                            field, validate_type, custom_message, custom_value
                        )

                    field.field_selector = original_selector
                    return

    # ===============================================
    # Sección 3: Creación de instancias y selectores
    # ===============================================

    def _build_field_selector(self, formset_name, index, field, input_type):
        """Construye el selector del campo dentro de un formset según su tipo de input.

        Args:
            formset_name (str): Nombre del formset.
            index (int): Índice de la fila dentro del formset.
            field (str): Nombre del campo.
            input_type (InputType): Tipo de input del campo.

        Returns:
            tuple[str, str]: Par (selector_css, nombre_base) donde:
                - selector_css: Selector a usar en la UI.
                - nombre_base: Nombre base del campo (ej. "<formset>-<index>-<field>").
        """
        base_selector = f"{formset_name}-{index}-{field}"
        return FieldSelectorBuilder.quick_build(input_type, base_selector), base_selector

    def _clone_field_for_formset_row(self, formset_name, index, field, field_instance):
        """Crea una instancia clonada de FieldsPage con el selector y nombre apropiados para un formset.

        Args:
            formset_name (str): Nombre del formset.
            index (int): Índice de la fila dentro del formset.
            field (str): Nombre del campo.
            field_instance (FieldsPage): Instancia original del campo a clonar.

        Returns:
            FieldsPage: Nueva instancia clonada con field_selector y name configurados.

        Efectos:
            - Construye el selector y nombre usando _build_field_selector.
            - Asigna field_selector y name a la instancia original.
            - Retorna una copia clonada mediante FieldsPage.from_existing.
        """
        selector, name = self._build_field_selector(formset_name, index, field, field_instance.input_type)
        field_instance.field_selector = selector
        field_instance.name = name
        return FieldsPage.from_existing(field_instance)

    async def create_formset_dependency_instance(
        self, formset_name, index, dependency_class: str, mode: str = "create", **kwargs
    ):
        """Crea y devuelve una instancia de dependencia para un campo de formset.

        Args:
            formset_name (str): Nombre del formset.
            index (int): Índice de la fila del formset.
            dependency_class (type): Clase de la página de dependencia.
            mode (str, opcional): Contexto de creación ("create" o "edit"). Por defecto "create".
            **kwargs: Parámetros adicionales que se pasan a `create_record` de la dependencia.

        Returns:
            Any: Instancia de la página de dependencia creada.

        Efectos:
            - Instancia la dependencia y ejecuta `create_record(**kwargs)` para generar su registro.

        Raises:
            ValueError: Si no existe una clase de dependencia registrada para `field_name`.
        """
        dependency_instance = dependency_class(self.page)
        await dependency_instance.create_record(**kwargs)  # Crear un nuevo registro en la dependencia

        selector, name = None, None
        for current_fields, dependency_fields in (
            self.input_field_dependencies[dependency_class].get(DependencyAction.CREATE).items()
        ):
            # Paso 2: acceder al input_field_instances
            field_instance = self.formset_fields[formset_name]["fields"].get(current_fields)
            if not field_instance:
                continue

            # Paso 3: obtener el input_type
            input_type = field_instance.input_type
            # Paso 4: armar el selector con los valores
            selector, name = self._build_field_selector(formset_name, index, current_fields, input_type)
        return dependency_instance, selector

    # ===============================================
    # Sección 4: Eliminación de filas y dependencias
    # ===============================================

    async def delete_formset_rows(self, formset_name, num_delete_rows, mode, **kwargs):
        """Elimina filas de un formset respetando las restricciones de obligatoriedad.

        Args:
            formset_name (str): Nombre del formset.
            num_delete_rows (int): Cantidad de filas a eliminar.
            mode (str): Modo de operación ("create" o "edit").
            **kwargs: Puede incluir `num_<formset_name>` con el total de filas generadas.

        Efectos:
            - Valida límites según la bandera `required` del formset.
            - Elimina visualmente las filas haciendo clic en sus botones de borrado.
            - Actualiza `self.formset_instances[formset_name][mode]`.
            - Regenera los diccionarios de filtros y validaciones según el modo.

        Raises:
            ValueError: Si se solicitan eliminar más filas de las existentes, o si el formset
                es requerido y la operación lo dejaría sin al menos una fila.
        """
        is_required = self.formset_fields[formset_name].get("has_initial_row", False)
        num_formsets = kwargs.get(f"num_{formset_name}", 0)

        if num_formsets < num_delete_rows:
            raise ValueError(
                f"El número de filas a eliminar ({num_delete_rows}) no puede ser mayor al número de filas del formset ({num_formsets})."
            )

        if is_required and num_formsets <= num_delete_rows:
            raise ValueError(
                f"El número de filas a eliminar ({num_delete_rows}) no puede ser mayor o igual al número de filas del formset ({num_formsets}), ya que este campo es requerido."
            )
        base_delete_button_selector = self.formset_fields[formset_name].get(
            "delete_button_selector", self.delete_row_formset_selector
        )

        # Determinar cuántas filas se pueden eliminar sin afectar `is_required`
        max_deletable_rows = num_formsets - (1 if is_required else 0)
        num_delete_rows = min(num_delete_rows, max_deletable_rows)
        actual_deleted = num_delete_rows
        for i in range(num_formsets - 1, -1, -1):
            if num_delete_rows <= 0:
                break
            delete_button_selector = f"#{formset_name}_formset_div-{i} {base_delete_button_selector}"
            delete_button_locator = self.page.locator(delete_button_selector)

            await self.wait_for_selector(delete_button_selector)
            await delete_button_locator.click()
            await expect(delete_button_locator).not_to_be_visible()

            num_delete_rows -= 1

        if formset_name in self.formset_instances and mode in self.formset_instances[formset_name]:
            remaining = num_formsets - actual_deleted
            self.formset_instances[formset_name][mode] = self.formset_instances[formset_name][mode][:remaining]

        is_edit = True if mode == "edit" else False
        self.generate_filters_and_validate_data(is_edit=is_edit)

    async def delete_formset_dependencies(self, mode: Optional[str] = None):
        """Elimina las dependencias creadas dentro de los formsets según el modo indicado.

        Args:
            mode (str | None, opcional): Modo a procesar:
                - "create" o "edit" para eliminar solo ese grupo.
                - None para eliminar en ambos modos.

        Efectos:
            - Para cada fila de formset en los modos seleccionados:
                * Si el valor es `GenericPage` con `delete_record`, lo elimina.
                * Si el valor es `FieldsPage` marcado como dependencia, crea la página
                  correspondiente y elimina por filtro.
            - Vacía las listas de dependencias por modo en `self.formset_instances`.

        """
        modes = [mode] if mode else ["create", "edit"]

        for dependencies_by_mode in self.formset_instances.values():
            for mode_key in modes:
                for dependency in dependencies_by_mode.get(mode_key, []):
                    for field_page in dependency.values():
                        await self._delete_dependency_instance(field_page)
                dependencies_by_mode[mode_key] = []

    # ===============================================
    # Sección 5: Parseo y helpers de formsets
    # ===============================================

    def change_prefix_formset_name(self, name: str, new_prefix: str) -> str:
        """Quita el wrapper CSS y retorna el nombre con el prefijo reemplazado."""
        token = self._extract_name_attribute(name)
        prefix, index, field = self._parse_formset_structure(token)

        if index:  # Si tiene índice, es formset
            return f"{new_prefix}-{index}-{field}"
        return f"{new_prefix}{token}"

    def get_formset_field_name(self, selector: str) -> str:
        """Obtiene el nombre del campo de un formset."""
        name = self._extract_name_attribute(selector)
        _, _, field = self._parse_formset_structure(name)
        return field if field else name

    def get_all_formset_fields(self) -> Dict[str, FieldsPage]:
        """Obtiene todos los campos de los formsets con sus instancias FieldsPage.

        Returns:
            dict[str, FieldsPage]: Diccionario con todos los campos de todos los formsets.
                - Clave: nombre del campo
                - Valor: instancia `FieldsPage` correspondiente

        Efectos:
            - Itera sobre `self.formset_fields` directamente.
            - Extrae todos los campos de todos los formsets.
        """
        result = {}

        for formset_name, formset_config in self.formset_fields.items():
            fields = formset_config.get("fields", {})
            result.update(fields)

        return result

    # ===============================================
    # Sección 6: Validación y población de formsets
    # ===============================================

    def _add_formset_field_to_dictionaries(
        self,
        field,
        selector: str,
        prefix: str,
        formset_name: Optional[str],
        initial_field_configuration,
        data_filters: Dict,
        data_validate: Dict,
        edit_data_validate: Dict,
        index_data_validate: Dict,
    ):
        """Agrega un campo de formset (GenericPage o FieldsPage) a los diccionarios objetivos."""
        formset_config = self.formset_fields.get(prefix, {})
        prefix_formset_config = formset_config.get("prefix_validate")

        if initial_field_configuration is None:
            # Importar GenericPage aquí para evitar importación circular
            from tests.pages.core.generic_page import GenericPage

            if isinstance(field, GenericPage):
                logger.debug("No se encontró configuración para el campo '%s' en el formset '%s'.", selector, prefix)
                return

        # Importar GenericPage aquí para evitar importación circular
        from tests.pages.core.generic_page import GenericPage

        if isinstance(field, GenericPage):
            field_name = selector
            if initial_field_configuration.input_type in [InputType.SELECT2, InputType.SELECT2_MULTIPLE]:
                field_name = self.extract_field_name_from_selector(selector)

            if prefix_formset_config:
                field_name = self.change_prefix_formset_name(field_name, prefix_formset_config)

            # Resolver todos los valores en una sola llamada
            resolved_values = self._resolve_all_dependency_values(field, formset_name)

            if getattr(initial_field_configuration, "is_data_validate", False):
                data_validate[field_name] = resolved_values["validate"]

            if getattr(initial_field_configuration, "is_filter", False):
                data_filters[initial_field_configuration.filter_selector] = resolved_values["filter"]

            if getattr(initial_field_configuration, "is_indexable", False):
                index_data_validate[initial_field_configuration.name] = resolved_values["index"]

            return

        if not isinstance(field, FieldsPage):
            logger.debug("Campo de formset '%s' no es FieldsPage ni GenericPage; se omite.", selector)
            return

        field_name = (
            self.change_prefix_formset_name(field.name, prefix_formset_config) if prefix_formset_config else field.name
        )

        if getattr(field, "is_data_validate", False):
            validate_value = self._resolve_field_value(field, field.validate_value, DependencyAction.VALIDATE)
            data_validate[field_name] = validate_value

        if getattr(field, "is_editable", False) and field.validate_value:
            edit_data_validate[field.field_selector] = field.validate_value
        if getattr(field, "is_indexable", False) and field.validate_value:
            index_data_validate[field.field_selector] = field.validate_value
        if getattr(field, "is_filter", False) and field.filter_value:
            data_filters[field.filter_selector] = field.filter_value

    async def populate_filter_fields_with_page(self, **kwargs):
        """Población de filtros a partir de valores externos, soportando campos normales y de formsets.

        Args:
            **kwargs: Debe incluir `fields_page` (dict) con pares {nombre_campo: valor}.

        Efectos:
            - REEMPLAZA por completo `self.data_filters` con los valores proporcionados.
            - Mapea cada `filter_selector` de los campos presentes en `input_field_instances` o en formsets
              al valor indicado en `fields_page`, buscando primero en campos normales y luego en formsets.

        Raises:
            ValueError: Si un campo no existe ni en `input_field_instances` ni en formsets.
        """
        fields_page = kwargs.get("fields_page")
        self.data_filters = {}

        for field, value in fields_page.items():
            # Primero intentar buscar en campos normales
            if field in self.input_field_instances:
                field_instance = self.input_field_instances[field]
                filter_value = value
                if field_instance.filter_type in [InputType.SELECT2, InputType.SELECT2_MULTIPLE]:
                    filter_value = field_instance.convert_to_select2_format_value(value)
                self.data_filters[field_instance.filter_selector] = filter_value
                continue

            # Si no está en campos normales, buscar en formsets
            field_found = False
            for formset_name, formset_modes in self.formset_instances.items():
                for mode, formset_rows in formset_modes.items():
                    for row in formset_rows:
                        # Buscar en cada fila del formset
                        for selector, field_instance in row.items():
                            if isinstance(field_instance, FieldsPage):
                                # Extraer el nombre del campo del selector
                                field_name = self.get_formset_field_name(selector)
                                if field_name == field or field_instance.name.endswith(f"-{field}"):
                                    filter_value = value
                                    if field_instance.filter_type in [InputType.SELECT2, InputType.SELECT2_MULTIPLE]:
                                        filter_value = field_instance.convert_to_select2_format_value(value)
                                    self.data_filters[field_instance.filter_selector] = filter_value
                                    field_found = True
                                    break
                        if field_found:
                            break
                    if field_found:
                        break
                if field_found:
                    break

            # Si no se encontró en ningún lugar, lanzar error
            if not field_found:
                raise ValueError(f"El campo '{field}' no existe en los campos de la página ni en los formsets.")

    async def get_field_values(self, attribute="field_value"):
        """Obtiene un mapeo de nombres de campos al valor de un atributo específico.

        Args:
            attribute (str, opcional): Atributo a extraer de cada campo.
                Valores permitidos: "field_value", "validate_value", "filter_value".
                Por defecto "field_value".

        Returns:
            dict: Diccionario {nombre_campo: valor_del_atributo}, incluyendo
            campos del formulario principal y, si existen, los del primer grupo
            de formsets en modo "create".
        """
        values = {}

        # Recorrer campos normales
        for field_name, field_instance in self.input_field_instances.items():
            values[field_name] = getattr(field_instance, attribute, None)

        for formset_name, field_instances in self.formset_instances.items():
            for field_instance in field_instances["create"][0].values():
                if isinstance(field_instance, FieldsPage):
                    values[field_instance.name] = getattr(field_instance, attribute, None)

        return values

    async def get_formset_row_count(self, formset_name: str, mode: str | None = None) -> int:
        """Obtiene la cantidad actual de filas en un formset.

        Args:
            formset_name (str): Nombre del formset.
            mode (str | None): Modo del formset ("create" o "edit"). Si es None,
                se prefiere 'create' si existe, de lo contrario 'edit'.

        Returns:
            int: Número de filas en el formset.

        Raises:
            ValueError: Si el formset no existe en formset_instances.

        Example:
            # Usar modo automático (prefiere 'create', luego 'edit')
            count = await self.get_formset_row_count('activities')
            print(f"Hay {count} actividades")

            # Especificar modo explícitamente
            count = await self.get_formset_row_count('activities', mode='edit')
        """
        if formset_name not in self.formset_instances:
            raise ValueError(f"El formset '{formset_name}' no existe en formset_instances.")

        # Obtener el diccionario de modos (create/edit) para este formset
        formset_modes = self.formset_instances[formset_name]

        # Si no se especifica modo, preferir 'create' si existe, sino usar 'edit'
        if mode is None:
            if "create" in formset_modes and formset_modes["create"]:
                return len(formset_modes["create"])
            elif "edit" in formset_modes and formset_modes["edit"]:
                return len(formset_modes["edit"])
            else:
                return 0

        # Si se especifica modo, usar solo ese modo
        if mode in formset_modes and formset_modes[mode]:
            return len(formset_modes[mode])
        else:
            return 0
