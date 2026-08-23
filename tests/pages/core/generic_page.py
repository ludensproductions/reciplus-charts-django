import ast
import copy
import logging
from typing import Any, Dict, Optional

from playwright.async_api import Page

from tests.pages.core.constants import DeleteModeEnum, DependencyAction, InputType, InvalidDataType, ValidDataType
from tests.pages.core.fields_page import FieldsPage
from tests.pages.core.standard_django_page import StandardDjangoPage
from utils.utils_functions import camel_to_snake, plural_to_singular

from .mixins import FormsetMixin, HelpersMixin, NavigationMixin, ValidationMixin

# Configurar logger para este módulo
logger = logging.getLogger(__name__)


class GenericPage(NavigationMixin, ValidationMixin, FormsetMixin, HelpersMixin, StandardDjangoPage):
    """Página base genérica para flujos CRUD en vistas Django con Playwright.

    Mixins incluidos:
        - NavigationMixin: Navegación entre páginas
        - ValidationMixin: Validación de datos, mensajes y estados de registros
        - FormsetMixin: Generación, llenado, validación y eliminación de formsets
        - HelpersMixin: Métodos auxiliares y utilidades para búsqueda, resolución de valores, etc.

    Provee utilidades para:
        - Navegación (índice, crear, editar, detalle, deshabilitados).
        - Generación/llenado de datos en campos y formsets (incluidas dependencias).
        - Búsqueda y filtrado en la vista índice.
        - Validaciones de éxito, contenido en índice/detalle/edición y estados de borrado/habilitado.
        - Manejo de dependencias entre entidades y limpieza de datos de prueba.

    Parámetros:
        page (Page): Instancia de Playwright para interactuar con la UI.
        module_name (str): Nombre del módulo (usado para títulos/slug).
        navigation (list): Rutas de navegación para alcanzar la vista índice.
        delete_mode (DeleteModeEnum): Estrategia de borrado (NORMAL, DISABLE_INDEX, TOGGLE).

    Atributos principales:
        - Selectores de navegación y acciones: index/create/edit/detail, botones y modales.
        - Campos del formulario: `input_field_instances`, `extra_input_field_instances`.
        - Formsets: `formset_fields`, `formset_instances` y manejo de dependencias en formsets.
        - Dependencias: `dependency_dict`, `dependency_instances`, `input_field_dependencies`.
        - Datos de prueba y validación: `data_filters`, `data_validate`, `edit_data_validate`, `index_data_validate`.
        - Configuración de borrado: `delete_mode`.

    Flujos soportados (resumen):
        - Crear/editar/eliminar/habilitar registros.
        - Generar datos (válidos/ inválidos), llenar SELECT2 y campos normales.
        - Aplicar filtros y validar resultados en índice/detalle/edición.
        - Gestión y limpieza de dependencias y formsets tras cada prueba.

    Notas:
        - `define_common_selectors()` establece selectores comunes derivados de `module_name`.
        - Los métodos asumen componentes estándar (selectores y mensajes) personalizables por módulo.
    """

    # Selectores comunes (atributos de clase)
    enable_modal_selector = "#enable-modal"
    disable_modal_selector = "#disable-modal"
    sidebar_button_selector = 'a:has-text("Catálogos")'
    cancel_disable_button_selector = '#delete-modal button:has-text("Cancelar")'
    cancel_enable_button_selector = '#enable-modal button:has-text("Cancelar")'
    continue_button_selector = 'button:has-text("Continuar")'
    enable_button_selector = 'input[title="Habilitar"]'
    confirm_enable_button_selector = '#enable-modal button:has-text("Habilitar")'
    cancel_modal_button_selector = "button.swal2-cancel"
    cancel_alert_button_selector = "button.btn-cancelar"
    success_message_selector = "#swal2-title"
    swal2_confirm_button_selector = "button.swal2-confirm"
    no_datos_selector = "td.dataTables_empty"
    delete_modal_selector = "#delete-modal"
    delete_row_formset_selector = 'button[title="delete_row"]'

    def __init__(self, page: Page, module_name: str = "", navigation: list = []):
        """Inicializa la página genérica con contexto de navegación, módulo y configuración de borrado.

        Args:
            page (Page): Instancia de Playwright para interactuar con la UI.
            module_name (str, opcional): Nombre visible del módulo. Por defecto "".
            navigation (list, opcional): Rutas de navegación para llegar al índice. Por defecto [].
            delete_mode (DeleteModeEnum, opcional): Modo de eliminación/deshabilitado. Por defecto NORMAL.

        Efectos:
            - Asigna referencias básicas (`page`, `navigation`, `module_name`, `module_slug`).
            - Inicializa selectores, mapeos de dependencias y estructuras de formsets.
            - Crea diccionarios para filtros y validaciones.
            - Llama a `define_common_selectors()` para establecer selectores comunes.
        """
        super().__init__(page)
        self.page = page
        self.navigation = navigation
        self.module_name = module_name
        self.delete_mode = DeleteModeEnum.DEFAULT
        self.module_slug = plural_to_singular(module_name)

        # Atributos de instancia que pueden variar
        self.index_page_button_selector = ""
        self.index_page_title_selector = ""
        self.disabled_index_page_title_selector = ""
        self.create_form_title_selector = ""
        self.edit_form_title_selector = ""
        self.detail_page_title_selector = ""
        self.field_configurations = {}
        # Manejador de dependencias
        self.dependency_instances = {}
        self.input_field_dependencies = {}
        # Campos del formulario
        self.input_field_instances = {}
        # Formsets
        self.formset_fields = {}
        self.formset_instances = {}
        self.formset_dependecy_instances = {}
        # Datos para filtros y validaciones
        self.data_filters = {}
        self.data_validate = {}
        self.edit_data_validate = {}
        self.index_data_validate = {}
        self.define_common_selectors()

    def define_common_selectors(self):
        """Define los selectores de títulos comunes derivados del nombre del módulo.

        Efectos:
            - Configura el selector del título para el formulario de edición
              (`edit_form_title_selector`).
            - Configura el selector del título para la vista de detalle
              (`detail_page_title_selector`).

        Notas:
            - Los selectores de sidebar e índice están comentados porque pueden
              variar según la navegación del proyecto; se pueden descomentar o
              sobrescribir en subclases si es necesario.
            - Usa `self.module_slug` (nombre en singular) para construir los textos.
        """
        self.index_page_title_selector = f'h1:has-text("{self.module_name}")'
        self.edit_form_title_selector = f'h1:has-text("Editar {self.module_slug}")'
        self.detail_page_title_selector = f'h1:has-text("Detalles del {self.module_slug}")'

    async def _delete_dependency_instance(self, dependency):
        """Elimina una dependencia individual según su tipo.

        Args:
            dependency: Instancia de dependencia (GenericPage, FieldsPage u otro tipo).

        Efectos:
            - Si es GenericPage: elimina llamando a delete_record()
            - Si es FieldsPage: valida que sea dependencia registrada, crea la página
              correspondiente y elimina por filtros
            - Muestra advertencia si el campo no es una dependencia registrada
            - Cualquier otro tipo con delete_record: llama al método
        """
        if isinstance(dependency, GenericPage):
            await dependency.delete_record()

        elif isinstance(dependency, FieldsPage):
            field_formset_name = self.get_formset_field_name(dependency.name)
            if field_formset_name not in self.get_keys_dependencies():
                return

            page: GenericPage = self.get_dependency_page_by_field_name(field_formset_name or dependency.name)(
                self.page
            )
            if field_formset_name in self.get_keys_dependencies():
                name = (
                    self.input_field_dependencies.get(page.__class__)
                    .get(DependencyAction.CREATE, {})
                    .get(field_formset_name)[0]
                )
            else:
                name = field_formset_name or dependency.name
            if isinstance(dependency.filter_value, dict):
                # SELECT2 dict format: {selector: value|[values]} — extract the actual value
                actual_value = next(iter(dependency.filter_value.values()))
                if isinstance(actual_value, list):
                    for val in actual_value:
                        await page.populate_filter_fields_with_page(fields_page={name: val})
                        await page.delete_record()
                else:
                    await page.populate_filter_fields_with_page(fields_page={name: actual_value})
                    await page.delete_record()
            elif isinstance(dependency.filter_value, list):
                for val in dependency.filter_value:
                    await page.populate_filter_fields_with_page(fields_page={name: val})
                    await page.delete_record()
            else:
                await page.populate_filter_fields_with_page(fields_page={name: dependency.filter_value})
                await page.delete_record()

        else:
            logger.debug("La dependencia de tipo '%s' no es reconocida para eliminación.", type(dependency))

    async def delete_dependencies(self, mode: Optional[str] = None):
        """Elimina las instancias de dependencias creadas durante la prueba.

        Args:
            mode (str | None, opcional):
                - Si se indica ("create" o "edit"), elimina únicamente las
                  dependencias asociadas a ese modo.
                - Si es None (por defecto), elimina las dependencias de ambos
                  modos ("create" y "edit").

        Efectos:
            - Invoca `delete_record()` en cada instancia de dependencia que lo implemente.
            - Limpia las listas de dependencias dentro de `self.dependency_instances`.

        Raises:
            Exception: Si ocurre un error inesperado durante la eliminación,
            se relanza con un mensaje descriptivo.

        """
        try:
            modes_to_process = [mode] if mode else ["create", "edit"]

            for field_name, dependencies_by_mode in self.dependency_instances.items():
                for mode_key in modes_to_process:
                    for dependency in dependencies_by_mode.get(mode_key, []):
                        await self._delete_dependency_instance(dependency)
                    dependencies_by_mode[mode_key] = []
        except Exception as e:
            raise Exception(f"Error al eliminar dependencias: {e}")

    async def create_dependency_instance(
        self, dependency_class, num_of_dependency, mode: str = "create", **kwargs
    ) -> Any:
        """Crea, registra y rellena los valores de una nueva instancia de dependencia.

        Args:
            dependency_class (type[GenericPage]): Clase de la página de la
                dependencia que se quiere instanciar.
            num_of_dependency (int): Número de la dependencia actual (0-indexed).
            mode (str, opcional): Contexto en el que se crea la dependencia.
                - "create": se almacena en la lista de dependencias de creación.
                - "edit": se almacena en la lista de dependencias de edición.
                Por defecto "create".
            **kwargs: Argumentos adicionales que se pasan a
                `dependency_instance.create_record()`.


        Efectos:
            - Instancia la clase de dependencia y la guarda en
              `self.dependency_instances[dependency_class.__name__]`.
            - Ejecuta `create_record` en la dependencia para generar un registro.
            - Actualiza los valores de los campos dependientes en
              `self.input_field_instances` usando `_assign_values_to_field_instance`.
            - Si la dependencia contiene formsets, copia el valor del campo
              principal al campo actual vinculado.

        Raises:
            KeyError: Si `dependency_class` no está registrado en
            `self.input_field_dependencies`.

        """
        # Inicializar la instancia de dependencia
        dependency_name = dependency_class.__name__
        dependency_instance = dependency_class(self.page)

        # Generar datos para campos dependientes en la dependencia antes de crearla
        context_name = f"Dependencia {dependency_instance.__class__.__name__}"
        self._generate_dependent_fields_if_activated(dependency_instance, context_name)

        # Crear el registro de la dependencia
        await dependency_instance.create_record(**kwargs)

        # SOLO registrar la instancia DESPUÉS de crearla exitosamente
        if dependency_name not in self.dependency_instances:
            self.dependency_instances[dependency_name] = {"create": [], "edit": []}

        self.dependency_instances[dependency_name][mode].append(dependency_instance)

        # Obtener la configuración de campos dependientes
        dependency_field_config = self.input_field_dependencies.get(dependency_class, {}).get(
            DependencyAction.CREATE, {}
        )

        # Asignar valores a los campos que dependen de esta instancia
        for current_field_name, dependency_fields in dependency_field_config.items():
            if current_field_name not in self.input_field_instances:
                continue

            field_instance = self.input_field_instances[current_field_name]

            # Si el campo es dependiente, verificar que será activado antes de asignar valores
            if getattr(field_instance, "is_dependent", False):
                activating_field_name = getattr(field_instance, "activating_field", None)
                activating_values = getattr(field_instance, "activating_values", None)

                # Validar todas las condiciones necesarias en una sola expresión
                if not (
                    activating_field_name and activating_values and activating_field_name in self.input_field_instances
                ):
                    continue

                activating_field_instance = self.input_field_instances[activating_field_name]
                activating_value = getattr(activating_field_instance, "field_value", None)

                # Solo asignar si el campo dependiente será activado
                if activating_value is None or activating_value not in activating_values:
                    continue

            self._assign_values_to_field_instance(
                field_instance,
                dependency_instance,
                current_field_name,
                num_of_dependency,
                False,
            )

    def _get_num_dependencies_for_dependency(self, dependency_class) -> int:
        """Determina cuántas instancias de una dependencia deben crearse.

        Se basa en el atributo num_dependencies de los campos que dependen de ella.

        Args:
            dependency_class: La clase de la dependencia (ej. PageGenerosMusicales)

        Returns:
            int: El número de dependencias a crear. Si ningún campo tiene num_dependencies definido,
                 retorna 1 por defecto.
        """
        dependency_fields = self.input_field_dependencies.get(dependency_class, {}).get(DependencyAction.CREATE, {})

        for field_name in dependency_fields.keys():
            formsets_fields = self.get_all_formset_fields()

            # Verificar si el campo existe en input_field_instances o en formsets_fields
            if field_name in self.input_field_instances or field_name in formsets_fields:
                # Buscar en campos normales primero, luego en campos del formset
                field_instance = self.input_field_instances.get(field_name) or formsets_fields.get(field_name)

                # Si el campo tiene num_dependencies definido, usarlo
                if (
                    field_instance
                    and field_instance.input_type == InputType.SELECT2_MULTIPLE
                    and hasattr(field_instance, "num_dependencies")
                    and field_instance.num_dependencies is not None
                ):
                    return field_instance.num_dependencies

        # Valor por defecto si no se encuentra num_dependencies
        return 1

    def _should_create_dependency(self, dependency_class, **kwargs) -> bool:
        """Verifica si una dependencia debe crearse.

        Se basa en si el campo asociado en la página principal es un campo dependiente y si será activado.

        Args:
            dependency_class: Clase de la página de dependencia.
            **kwargs: Argumentos adicionales que pueden contener valores específicos de campos.

        Returns:
            bool: True si la dependencia debe crearse, False en caso contrario.
        """
        # Obtener la configuración de campos de la dependencia
        dependency_field_config = self.input_field_dependencies.get(dependency_class, {}).get(
            DependencyAction.CREATE, {}
        )
        should_create = False
        # Por cada campo en la página principal que depende de esta dependencia
        for current_field_name in dependency_field_config.keys():
            if current_field_name not in self.input_field_instances:
                continue

            field_instance = self.input_field_instances[current_field_name]

            # Si el campo NO es dependiente, siempre se crea la dependencia
            if not getattr(field_instance, "is_dependent", False):
                return True

            # Si ES dependiente, verificar si será activado
            activating_field_name = getattr(field_instance, "activating_field", None)
            activating_values = getattr(field_instance, "activating_values", None)

            # Validar todas las condiciones necesarias
            if not (
                activating_field_name and activating_values and activating_field_name in self.input_field_instances
            ):
                dep_name = dependency_class.__name__
                logger.debug(
                    "[Validación] Campo dependiente '%s' sin activating_field definido para dependencia %s",
                    current_field_name,
                    dep_name,
                )
                continue

            activating_field_instance = self.input_field_instances[activating_field_name]

            # Obtener el valor del campo activador (puede venir de kwargs o del field_value)
            activating_value = kwargs.get(
                activating_field_name, getattr(activating_field_instance, "field_value", None)
            )

            if activating_value is None:
                should_create = False

            # Si el valor del campo activador activa el campo dependiente, crear la dependencia
            if activating_value in activating_values:
                should_create = True

        # Si no se encontró ningún campo, crear la dependencia por defecto
        return should_create

    def _generate_dependent_fields_if_activated(self, page_instance: "GenericPage", context_name: str = ""):
        """Genera datos para campos dependientes si sus campos activadores los activan.

        Args:
            page_instance (GenericPage): Instancia de la página (puede ser self o una dependencia).
            context_name (str): Nombre del contexto para logs (ej: "Página principal", "Dependencia PageCategorias").

        Efectos:
            - Identifica campos dependientes en la página.
            - Verifica que el campo activador exista y tenga valor.
            - Solo genera datos si el valor del activador está en activating_values.
        """
        for field in page_instance.get_dependents_fields() or []:
            # Validar atributos necesarios del campo
            if not (
                hasattr(field, "activating_field")
                and hasattr(field, "activating_values")
                and field.activating_field
                and field.activating_values
            ):
                continue

            # Validar existencia y valor del campo activador
            activating_field = page_instance.input_field_instances.get(field.activating_field)
            if not (activating_field and activating_field.field_value):
                continue

            # Verificar si el valor activa el campo dependiente
            if activating_field.field_value not in field.activating_values:
                continue

            # Para página principal: no sobrescribir si ya tiene valor
            if page_instance == self:
                dependent_field = page_instance.input_field_instances.get(field.name)
                if not dependent_field:
                    continue

                has_value = dependent_field.field_value and dependent_field.field_value not in [None, "", {}, []]
                if has_value:
                    continue

            # Generar datos válidos
            target_field = page_instance.input_field_instances.get(field.name)
            if not target_field:
                continue

            target_field.generate_valid_data(ignore_dependent_fields=False)

    async def generate_random_data(self, is_edit: bool = False, create_on_dependency_page=True, **kwargs):
        """Genera datos aleatorios para los campos de la página, incluyendo dependencias.

        Args:
            is_edit (bool, opcional):
                - Si es False (por defecto), se generan datos para creación de registros.
                - Si es True, se generan datos pensados para edición.
            create_on_dependency_page (bool, opcional):
                - Valor por defecto para crear dependencias en su propia página.
            **kwargs:
                Valores específicos para sobrescribir los generados automáticamente.
                - `num_<nombre_dependencia>`: Número de instancias a crear (en snake_case).
                - `create_on_page_<nombre_dependencia>`: Control individual de create_on_page (en snake_case).
                  Ejemplo: create_on_page_page_generos_musicales=False

        Efectos:
            - Crea instancias de dependencias definidas en `input_field_dependencies`
              mediante `create_dependency_instance`.
            - Genera datos válidos en los campos del formulario principal según los parámetros.
            - Si se pasan valores explícitos en `kwargs`, se asignan con
              `set_input_instance_value`.

        """
        mode = "edit" if is_edit else "create"

        # PASO 1: Aplicar valores personalizados de kwargs (si existen)
        # Esto sobrescribe los valores por defecto generados en __init__ de FieldsPage
        # Los campos ya tienen valores generados automáticamente al instanciarse
        if kwargs:
            self.set_input_instance_value(**kwargs)

        # PASO 2: Crear dependencias
        # Los campos activadores ya tienen valores (generados en __init__ o sobrescritos por kwargs)
        for dependency in self.input_field_dependencies.keys():
            dependency_name = dependency.__name__
            # Remover prefijo "Page" si existe para nombres más simples
            clean_name = (
                dependency_name.replace("Page", "", 1) if dependency_name.startswith("Page") else dependency_name
            )
            dependency_snake = camel_to_snake(clean_name)

            # Determinar número de instancias
            # Primero intenta obtenerlo de kwargs, sino busca en los fields que dependen de esta dependency
            num_dependencies = kwargs.get(
                f"num_{dependency_snake}", self._get_num_dependencies_for_dependency(dependency)
            )

            # Determinar si crear en página (prioridad: específico > global)
            should_create_on_page = kwargs.get(f"create_on_page_{dependency_snake}", create_on_dependency_page)

            if num_dependencies == 0:
                continue

            if num_dependencies > 0 and should_create_on_page:
                # Esto seria para cuando sea get en el get or create por que ocupa crearlo antes
                for num in range(num_dependencies):
                    # Para verificar que las llaves del input field instances no estén dentro de las llaves del input field dependencies para no crear en caso de no ser necesario
                    if not (
                        self.input_field_instances.keys()
                        & self.input_field_dependencies[dependency][DependencyAction.CREATE].keys()
                    ):
                        continue

                    # Verificar si la dependencia debe crearse según campos dependientes
                    if not self._should_create_dependency(dependency, **kwargs):
                        logger.debug(
                            "[Dependencia %s] No se creará porque el campo dependiente asociado no será activado.",
                            dependency.__name__,
                        )
                        continue

                    await self.create_dependency_instance(dependency, num, mode, **kwargs)
            else:
                # Esto seria para cuando sea create en el get or create por que no ocupa crearlo antes
                await self.convert_select2_values_into_fields_page(dependency, mode)

        # PASO 3: Generar datos para campos dependientes en la página principal
        self._generate_dependent_fields_if_activated(self, "Página principal")

    async def convert_select2_values_into_fields_page(self, dependency, mode):
        """Convierte valores de campos SELECT2/SELECT2_MULTIPLE en instancias de FieldsPage.

        Cuando las dependencias no se crean en su propia página.

        Args:
            dependency: Clase de la página de dependencia.
            mode: Modo de operación ("create" o "edit").

        Efectos:
            - Obtiene los valores de SELECT2/SELECT2_MULTIPLE de los campos.
            - Crea instancias de página de dependencia para cada valor.
            - Registra las instancias en dependency_instances.
        """
        dependency_name = dependency.__name__
        dependency_config = self.input_field_dependencies.get(dependency).get(DependencyAction.CREATE).items()
        for current_fields, dependency_fields in dependency_config:
            if not (
                self.input_field_instances.keys()
                & self.input_field_dependencies.get(dependency).get(DependencyAction.CREATE).keys()
            ):
                continue
            field_page: FieldsPage = self.input_field_instances[current_fields]
            if field_page.input_type in [InputType.SELECT2_MULTIPLE, InputType.SELECT2]:
                values = field_page.get_values_from_select2()
                for value in values:
                    page: GenericPage = self.get_dependency_page_by_field_name(current_fields)(self.page)

                    await page.populate_filter_fields_with_page(
                        fields_page={
                            dependency_fields[0]: value
                        }  # Se agarra el 0 por que solo es un campo el que se llena casi siempre son catalogos o hasta el momento que se desarrolló
                    )
                    if dependency_name not in self.dependency_instances:
                        self.dependency_instances[dependency_name] = {"create": [], "edit": []}

                    # Skip adding edit-mode dependency if the same filter is already tracked
                    # in create mode — avoids double-deletion of the same resource.
                    if mode == "edit":
                        create_deps = self.dependency_instances[dependency_name].get("create", [])
                        already_tracked = any(
                            isinstance(dep, GenericPage) and dep.data_filters == page.data_filters
                            for dep in create_deps
                        )
                        if already_tracked:
                            continue

                    self.dependency_instances[dependency_name][mode].append(page)

    def _assign_select2_values(
        self,
        field_instance: FieldsPage,
        dependency_instance,
        field_name: str,
        num_of_dependencies: int,
        is_edit: bool = False,
    ):
        """Método unificado para asignar valores a campos SELECT2 y SELECT2_MULTIPLE.

        Args:
            field_instance: Instancia del campo SELECT2/SELECT2_MULTIPLE
            dependency_instance: Instancia de la dependencia
            field_name: Nombre del campo
            num_of_dependencies: Número de dependencia actual (0-indexed)
            is_edit: Si está en modo edición

        Efectos:
            - Asigna field_value, validate_value, filter_value, index_value
            - Maneja acumulación para SELECT2_MULTIPLE
            - Guarda original_value si no es edición
        """
        # Resolver y truncar el valor principal
        resolved_value = self._resolve_dependency_value(dependency_instance, field_name)
        # Validar que el valor no sea None o vacío
        if not resolved_value or resolved_value == "None":
            return
        truncated_value = field_instance.truncate_if_needed(resolved_value, "field")
        # Asignar field_value según el tipo
        if field_instance.input_type == InputType.SELECT2_MULTIPLE:
            if num_of_dependencies == 0:
                field_instance.clear_values_to_select2_multiple()
            field_instance.add_value_to_select2_multiple(truncated_value)
            original_value = copy.deepcopy(truncated_value)
        else:  # SELECT2
            val = {field_instance.select2_search_selector: [truncated_value]}
            field_instance.field_value = val
            original_value = copy.deepcopy(val)

        # Guardar valor original si no es edición
        if not is_edit:
            field_instance.original_value = copy.deepcopy(original_value)

        # Procesar valores de validación, filtro e índice
        if field_instance.input_type == InputType.SELECT2_MULTIPLE:
            self._process_select2_multiple_actions(
                field_instance, dependency_instance, field_name, num_of_dependencies
            )
        else:  # SELECT2
            self._process_select2_actions(field_instance, dependency_instance, field_name)

    def _process_select2_multiple_actions(
        self, field_instance: FieldsPage, dependency_instance, field_name: str, num_of_dependencies: int
    ):
        """Procesa VALIDATE, FILTER e INDEX para SELECT2_MULTIPLE con acumulación.

        - Para tablas (table_suffix=True): valores como lista sin concatenación.
        - Para concatenados: valores unidos con separador (" | " por defecto o configurado).
        """
        is_table = getattr(field_instance, "table_suffix", False)

        accumulated_validate = ""
        if num_of_dependencies > 0 and field_instance.validate_value:
            accumulated_validate = field_instance.validate_value

        resolved_values = self._resolve_all_dependency_values(dependency_instance, field_name)

        # VALIDATE
        if resolved_values["validate"]:
            if is_table:
                # Tablas: manejar como lista (sin separador)
                if num_of_dependencies == 0:
                    field_instance.validate_value = [
                        field_instance.truncate_if_needed(resolved_values["validate"], "validate")
                    ]
                else:
                    if not isinstance(field_instance.validate_value, list):
                        field_instance.validate_value = []
                    field_instance.validate_value.append(
                        field_instance.truncate_if_needed(resolved_values["validate"], "validate")
                    )
            else:
                # Concatenados: manejar como string con separador
                if num_of_dependencies > 0 and accumulated_validate:
                    separator = resolved_values.get("separator", "") or " | "
                    truncated_new = field_instance.truncate_if_needed(resolved_values["validate"], "validate")
                    field_instance.validate_value = accumulated_validate + separator + truncated_new
                else:
                    field_instance.validate_value = field_instance.truncate_if_needed(
                        resolved_values["validate"], "validate"
                    )

        # FILTER
        if resolved_values["filter"]:
            if num_of_dependencies == 0:
                field_instance.filter_value = [field_instance.truncate_if_needed(resolved_values["filter"], "filter")]
            else:
                field_instance.filter_value.append(
                    field_instance.truncate_if_needed(resolved_values["filter"], "filter")
                )

        # INDEX
        if resolved_values["index"]:
            if num_of_dependencies == 0:
                field_instance.index_value = [field_instance.truncate_if_needed(resolved_values["index"], "index")]
            else:
                field_instance.index_value.append(field_instance.truncate_if_needed(resolved_values["index"], "index"))

    def _process_select2_actions(self, field_instance: FieldsPage, dependency_instance, field_name: str):
        """Procesa VALIDATE, FILTER e INDEX para SELECT2 normal (sin acumulación)."""
        # Resolver todos los valores en una sola llamada
        resolved_values = self._resolve_all_dependency_values(dependency_instance, field_name)

        # VALIDATE
        field_instance.validate_value = field_instance.truncate_if_needed(resolved_values["validate"], "validate")

        # FILTER
        field_instance.filter_value = field_instance.truncate_if_needed(resolved_values["filter"], "filter")

        # INDEX
        field_instance.index_value = field_instance.truncate_if_needed(resolved_values["index"], "index")

    def _assign_values_to_field_instance(
        self, field_instance: FieldsPage, dependency_instance, field, num_of_dependencies, is_edit
    ):
        """Asigna valores a una instancia de campo según su tipo de input.

        Args:
            field_instance (FieldsPage): Instancia del campo al que se asignarán los valores.
            dependency_instance: Instancia de la dependencia o valor a procesar.
            field (str): Nombre del campo.
            num_of_dependencies (int): Número de dependencias creadas para este campo (0-indexed).
            is_edit (bool): Indica si se está en modo edición.

        Efectos:
            - Para campos SELECT2/SELECT2_MULTIPLE: Usa _assign_select2_values()
            - Para otros campos: Asigna field_value, validate_value, filter_value, index_value
        """
        if field_instance.input_type in [InputType.SELECT2_MULTIPLE, InputType.SELECT2]:
            self._assign_select2_values(field_instance, dependency_instance, field, num_of_dependencies, is_edit)
        else:
            # Resolver todos los valores en una sola llamada para campos normales
            resolved_values = self._resolve_all_dependency_values(dependency_instance, field)

            field_instance.field_value = field_instance.truncate_if_needed(resolved_values["create"], "field")
            field_instance.filter_value = field_instance.truncate_if_needed(resolved_values["filter"], "filter")

            # Para campos de fecha con formato personalizado, regenerar validate_value e index_value
            if field_instance.input_type in [
                InputType.DATE,
                InputType.DATE_START,
                InputType.DATE_MIDDLE,
                InputType.DATE_END,
                InputType.RANGE_OF_DATES,
                InputType.DATE_TIME,
            ] and (field_instance.detail_format_date or field_instance.index_format_date):
                # Regenerar valores de validación respetando los formatos configurados
                field_instance.generate_data_validate()
            else:
                # Para otros tipos de campos, usar los valores resueltos directamente
                field_instance.validate_value = field_instance.truncate_if_needed(
                    resolved_values["validate"], "validate"
                )
                field_instance.index_value = field_instance.truncate_if_needed(
                    resolved_values["index"] or resolved_values["create"], "index"
                )

    def _add_field_to_dictionaries(
        self,
        field: FieldsPage,
        data_filters: Dict,
        data_validate: Dict,
        edit_data_validate: Dict,
        index_data_validate: Dict,
        required_only: bool = False,
    ):
        """Agrega un campo normal a los diccionarios de filtros/validaciones sin efectos secundarios."""
        if required_only and not getattr(field, "is_required", False):
            return

        if getattr(field, "is_filter", False) and field.filter_value is not None:
            if field.input_type == InputType.RANGE_OF_DATES:
                start_date, end_date = field.filter_value
                data_filters[f"input[name='{field.name}_min']"] = start_date
                data_filters[f"input[name='{field.name}_max']"] = end_date
            # TODO - Obtener el primer valor siempre para que filtre correctamente
            elif field.input_type == InputType.SELECT2_MULTIPLE:
                if not isinstance(field.filter_value, list):
                    logger.debug("Advertencia: El valor de filtro para '%s' debe ser una lista.", field.name)
                    return
                data_filters[field.filter_selector] = field.filter_value
            else:
                resolved = self._resolve_field_value(field, field.filter_value, DependencyAction.FILTER)
                ftype = getattr(field, "filter_type", None) or field.input_type
                if ftype in (InputType.SELECT2, InputType.SELECT2_MULTIPLE) and not isinstance(resolved, dict):
                    resolved = field.convert_to_select2_format_value(resolved)
                data_filters[field.filter_selector] = resolved

        if getattr(field, "is_data_validate", False) and field.validate_value is not None:
            validate = self._resolve_field_value(field, field.validate_value, DependencyAction.VALIDATE)

            # Para campos SELECT2_MULTIPLE tipo tabla, expandir lista a entradas individuales con índice
            if (
                field.input_type == InputType.SELECT2_MULTIPLE
                and getattr(field, "table_suffix", False)
                and isinstance(validate, list)
            ):
                # Usar el selector template para generar las claves con índice
                # Ejemplo: "genres-{index}-genre" -> "genres-0-genre", "genres-1-genre", etc.
                for idx, value in enumerate(validate):
                    # Usar el método get_table_selector_for_index() para obtener el selector correcto
                    key = field.get_table_selector_for_index(idx)
                    data_validate[key] = value
            else:
                data_validate[field.title_for_validate] = validate

        if (
            getattr(field, "is_editable", False)
            and getattr(field, "is_data_validate", False)
            and field.field_value is not None
        ):
            # Para campos FILE, usar validate_value (que contiene solo el nombre) en lugar de field_value (que es un dict)
            value_to_use = field.validate_value if field.input_type == InputType.FILE else field.field_value
            edit_data_validate[field.field_selector] = self._resolve_field_value(
                field, value_to_use, DependencyAction.CREATE
            )

        if getattr(field, "is_indexable", False) and field.index_value is not None:
            index = self._resolve_field_value(field, field.index_value, DependencyAction.INDEX)

            # Para campos SELECT2_MULTIPLE tipo tabla, mantener como lista para validación en índice
            # (El método validate_record_information_in_index_view extrae valores de listas automáticamente)
            index_data_validate[field.title_for_validate] = index

    def _build_all_validation_dictionaries(self, required_only: bool, mode: str):
        """Construye los cuatro diccionarios en una sola pasada y sin efectos secundarios."""
        if mode not in ("create", "edit"):
            raise ValueError(f"Modo inválido para generación de diccionarios: {mode}")

        data_filters: Dict = {}
        data_validate: Dict = {}
        edit_data_validate: Dict = {}
        index_data_validate: Dict = {}

        for field in self.input_field_instances.values():
            self._add_field_to_dictionaries(
                field,
                data_filters,
                data_validate,
                edit_data_validate,
                index_data_validate,
                required_only,
            )

        for prefix, formset_mode_dict in self.formset_instances.items():
            rows = formset_mode_dict.get(mode, [])

            if rows is not None and not isinstance(rows, list):
                raise ValueError(
                    f"La colección de filas del formset '{prefix}' para el modo '{mode}' debe ser una lista."
                )

            for formset_group in rows or []:
                for selector, field in formset_group.items():
                    formset_name = self.get_formset_field_name(selector) if selector else None
                    initial_field_configuration = None

                    if formset_name and self.formset_fields.get(prefix):
                        initial_field_configuration = self.formset_fields[prefix].get("fields", {}).get(formset_name)

                    self._add_formset_field_to_dictionaries(
                        field,
                        selector,
                        prefix,
                        formset_name,
                        initial_field_configuration,
                        data_filters,
                        data_validate,
                        edit_data_validate,
                        index_data_validate,
                    )

        return data_filters, data_validate, edit_data_validate, index_data_validate

    def generate_filters_and_validate_data(self, required_only=False, is_edit=False):
        """Construye los diccionarios de filtros y validaciones para los campos de la página.

        Incluye tanto campos normales como los provenientes de formsets.

        Args:
            required_only (bool): Si solo procesar campos requeridos.
            is_edit (bool): Si está en modo edición.

        Efectos:
            Llena: data_filters, data_validate, edit_data_validate, index_data_validate.
        """
        mode = "edit" if is_edit else "create"

        for prefix, formset_mode_dict in self.formset_instances.items():
            formset_rows = formset_mode_dict.get(mode)
            if formset_rows is not None and not isinstance(formset_rows, list):
                raise ValueError(
                    f"Las filas del formset '{prefix}' para el modo '{mode}' deben ser una lista (se obtuvo {type(formset_rows)})."
                )

        (
            self.data_filters,
            self.data_validate,
            self.edit_data_validate,
            self.index_data_validate,
        ) = self._build_all_validation_dictionaries(required_only, mode)

    def _resolve_field_value(self, field: FieldsPage, actual_value: str, action: DependencyAction) -> str:
        """Resuelve el valor de un campo para filtros/validaciones.

        Args:
            field: Instancia del campo
            actual_value: Valor actual del campo (puede ser string, lista, etc.)
            action: Acción de dependencia (VALIDATE, FILTER, INDEX)

        Returns:
            Valor resuelto como string, con separadores aplicados si corresponde,
            o lista para campos SELECT2_MULTIPLE tipo tabla
        """
        # Caso especial: SELECT2_MULTIPLE necesita manejo de listas con separadores
        if field.input_type == InputType.SELECT2_MULTIPLE:
            # Para tablas formset, mantener como lista (no concatenar)
            if getattr(field, "table_suffix", False) and isinstance(actual_value, list):
                return actual_value

            # Normalizar el valor a lista
            if isinstance(actual_value, list):
                values_list = actual_value
            elif isinstance(actual_value, str) and actual_value.startswith("[") and actual_value.endswith("]"):
                # Intentar parsear string que representa lista: "['val1', 'val2']"
                try:
                    values_list = ast.literal_eval(actual_value)
                    if not isinstance(values_list, list):
                        return actual_value  # No es lista, retornar tal cual
                except:
                    return actual_value  # Parseo falló, retornar tal cual
            else:
                return actual_value  # Ya es un string procesado

            return " | ".join(str(v) for v in values_list)

        # Valor simple sin configuración especial
        return actual_value

    async def search_records_with_filters(
        self,
        data_filters: Optional[Dict] = None,
        validate_on_index: bool = True,
        search_disabled: bool = False,
        index_many_results: bool = False,
    ):
        """Busca registros aplicando los filtros en la vista de índice.

        Args:
            data_filters (dict, opcional): Diccionario con los filtros a aplicar.
                Si no se especifica, se usan los valores en `self.data_filters`.
            validate_on_index (bool, opcional):
                Si es True (por defecto), valida que la información mostrada en
                la tabla del índice corresponda con `self.index_data_validate`.
            search_disabled (bool, opcional):
                Si es True, realiza la búsqueda en la página de registros deshabilitados.
            index_many_results (bool, opcional):
                Si es True, en la validación de la vista índice, aplica un filtro a nivel de fila para encontrar una coincidencia específica antes de validar los valores.

        Efectos:
            - Navega a la página de índice.
            - Llena los filtros con `fill_data`.
            - Ejecuta la búsqueda haciendo clic en el botón de filtrar.
            - Opcionalmente valida los resultados en la vista índice.
        """
        if search_disabled:
            await self.goto_disabled_index_page()
        else:
            await self.goto_index_page()
        await self.fill_data(data_filters or self.data_filters)
        await self.page.click(self.filter_button_selector)
        if validate_on_index:
            logger.debug("Diccionario del index: %s", self.index_data_validate)
            await self.validate_record_information_in_index_view(
                self.index_data_validate, index_many_results=index_many_results
            )

    async def create_record(
        self,
        only_required=False,
        generate_formset_data=True,
        submit=True,
        validate_record=False,
        validate_dependencies=False,
        **kwargs,
    ):
        """Crea un nuevo registro en el sistema, llenando los campos del formulario y validando el resultado.

        Args:
            only_required (bool, opcional):
                Si es True, genera y llena únicamente los campos requeridos.
                Por defecto False.
            generate_formset_data (bool, opcional):
                Si es True (por defecto), genera datos también para los formsets.
            submit (bool, opcional):
                Si es True (por defecto), envía el formulario de creación.
            validate_record (bool, opcional):
                Si es True (por defecto), valida el registro recién creado.
            validate_dependencies (bool, opcional):
                Si es True, valida las dependencias del registro.
            **kwargs:
                Valores adicionales que pueden usarse para sobrescribir o personalizar
                los datos generados.

        Efectos:
            - Genera datos aleatorios o personalizados para el formulario.
            - Navega a la página de creación.
            - Llena los campos del formulario principal y de formsets.
            - Opcionalmente envía el formulario y valida el mensaje de éxito.
            - Opcionalmente valida que el registro se haya creado correctamente en la base de datos o UI.
        """
        kwargs["validate_record"] = validate_dependencies
        if generate_formset_data:
            await self.generate_formset_data(**kwargs)
        """Crea o edita un registro."""
        await self.generate_random_data(**kwargs)
        self.generate_filters_and_validate_data(only_required)
        await self.goto_create_page()
        await self.fill_input_fields(only_required=only_required)
        await self.fill_formsets(**kwargs)

        if submit:
            await self.submit_form(self.submit_create_form_selector)
            # TODO - Se podria hacer que en caso de ser un double_confirm enviar el selector del boton de confirmación
            await self.validate_success_message_and_continue(
                self.modal_message_selector,
                self.continue_button_selector,
                self.success_create_message_text,
                **kwargs,
            )

            await self.extract_generated_field_values()

        if validate_record:
            await self.validate_record()

    async def edit_record(self, only_required=False, submit=True, **kwargs):
        """Edita un registro existente llenando el formulario de edición y validando el resultado.

        Args:
            only_required (bool, opcional):
                Si es True, genera y llena únicamente los campos requeridos.
                Por defecto False.
            submit (bool, opcional):
                Si es True (por defecto), envía el formulario de edición.
            **kwargs:
                Valores adicionales que pueden usarse para sobrescribir o personalizar
                los datos generados.

        Efectos:
            - Genera datos aleatorios o personalizados para edición.
            - Navega al formulario de edición.
            - Limpia valores en campos SELECT2 antes de rellenar.
            - Llena los campos del formulario principal y formsets en modo edición.
            - Opcionalmente envía el formulario y valida el mensaje de éxito.
            - Actualiza los diccionarios de filtros y validaciones según el modo edición.
        """
        if self.formset_fields:
            await self.generate_formset_data(mode="edit", **kwargs)
        await self.generate_random_data(is_edit=True, **kwargs)
        await self.goto_edit_page()
        # Si hay un multi select, elimina los valores
        await self.clear_select2_on_edit()
        await self.fill_input_fields(is_edit=True, only_required=only_required)
        if self.formset_fields:
            await self.fill_formsets(mode="edit", **kwargs)
        if submit:
            await self.submit_form(self.submit_create_form_selector)
            await self.validate_success_message_and_continue(
                self.modal_message_selector,
                self.continue_button_selector,
                self.success_edit_message_text,
            )

        self.generate_filters_and_validate_data(only_required, is_edit=True)

    async def clear_select2_on_edit(self):
        """Limpia los valores de los campos SELECT2 y SELECT2_MULTIPLE en el formulario de edición.

        Efectos:
            - Omite campos marcados como no editables.
            - Para SELECT2_MULTIPLE:
                * Espera el selector del campo.
                * Elimina las opciones previamente seleccionadas.
                * Cierra el menú desplegable con la tecla Escape.
            - Para SELECT2:
                * Espera el selector del campo.
                * Elimina la opción previamente seleccionada.
        """
        for field, instance in self.input_field_instances.items():
            if instance.is_editable is False:
                continue
            if instance.input_type == InputType.SELECT2_MULTIPLE:
                await self.page.wait_for_selector(instance.field_selector)
                await instance.clear_multi_selector_options(instance.original_value)
                await self.page.keyboard.press("Escape")

            if instance.input_type == InputType.SELECT2:
                await self.page.wait_for_selector(instance.field_selector)
                await instance.clear_select2_options()

    async def delete_record(self, delete_dependencies=True):
        """Elimina, deshabilita o habilita un registro según la configuración del modo de borrado.

        Args:
            delete_dependencies (bool, opcional):
                Si es True (por defecto), elimina también las dependencias registradas.

        Efectos:
            - Recarga la página y busca el registro actual.
            - Obtiene el botón de acción correspondiente (eliminar, deshabilitar o habilitar).
            - Confirma la acción en el modal.
            - Valida que el registro ya no esté visible en la lista.
            - Opcionalmente elimina dependencias y formsets asociados.
        """
        await self.page.reload()
        await self.search_records_with_filters(validate_on_index=False)

        # Obtener el selector del botón de acción (eliminar, deshabilitar, habilitar)
        action_button_selector = await self.get_delete_button_selector()

        if action_button_selector:
            # Hacer clic en el botón de acción (eliminar, deshabilitar, habilitar)
            await self.wait_for_selector(action_button_selector, 1)
            await self.page.locator(action_button_selector).first.click()

            # Lógica según el tipo de acción: eliminar, deshabilitar o habilitar
            await self.confirm_delete_in_modal()

            # Verificar que el registro ya no esté en la lista
            await self.validate_record_state(is_deleted=True)
        else:
            raise ValueError("No se encontró el botón de acción para eliminar/deshabilitar/habilitar.")

        # Eliminar dependencias asociadas si es necesario
        if delete_dependencies:
            await self.delete_dependencies()
            await self.delete_formset_dependencies()

        # # Verificar si existen formsets y eliminarlos si es necesario
        # if self.formset_fields and delete_dependencies:

    async def confirm_delete_in_modal(self):
        """Confirma la acción de eliminar o deshabilitar en el modal correspondiente.

        Efectos:
            - Espera la visibilidad del modal de eliminación (con timeout corto).
            - Si aparece el modal, hace clic en el botón de confirmación correspondiente.
            - Si no aparece modal, continúa directamente a validar el mensaje de éxito.
            - Valida que se muestre el mensaje de éxito tras la acción.
        """
        try:
            # Intentar esperar el modal con un timeout corto (1 segundo)
            await self.page.wait_for_selector(self.delete_modal_selector, state="visible", timeout=1000)

            # Si el modal apareció, buscar y hacer clic en el botón de confirmación
            if await self.page.locator(self.delete_confirm_button_selector).is_visible():
                await self.page.click(self.delete_confirm_button_selector)
            elif await self.page.locator(self.confirm_disable_button_selector).is_visible():
                await self.page.click(self.confirm_disable_button_selector)
            else:
                raise ValueError("No se encontró ningún botón de confirmación válido en el modal.")

        except Exception:
            # Si el modal no apareció en 1 segundo, asumimos que no hay confirmación
            # y continuamos directamente a validar el mensaje de éxito
            pass

        await self.validate_success_message_and_continue(
            self.modal_message_selector, self.continue_button_selector, self.success_delete_message_text
        )

    async def confirm_enable_modal(self):
        """Confirma la acción de habilitar en el modal correspondiente.

        Efectos:
            - Espera la visibilidad del modal de habilitación.
            - Hace clic en el botón de confirmación de habilitación.
            - Lanza un error si no se encuentra el botón válido.
            - Valida que se muestre el mensaje de éxito tras la acción.
        """
        await self.wait_for_selector(self.enable_modal_selector, 1)
        if await self.page.locator(self.confirm_enable_button_selector).is_visible():
            await self.page.click(self.confirm_enable_button_selector)
        else:
            logger.debug("No se encontró ningún botón de confirmación de habilitación.")

    async def enable_record(self):
        """Habilita un registro que fue previamente deshabilitado.

        Efectos:
            - Busca el registro en la lista de deshabilitados (si existe) o en la lista normal.
            - Hace clic en el botón de habilitar y confirma la acción en el modal.
            - Valida que se muestre el mensaje de éxito y continúa el flujo.
        """
        if self.delete_mode == DeleteModeEnum.DISABLE_INDEX:
            await self.search_records_with_filters(search_disabled=True)
        else:
            await self.search_records_with_filters()

        enable_button = await self.get_enable_button_selector()
        await self.wait_for_selector(enable_button)
        await self.page.locator(enable_button).first.click()

        await self.confirm_enable_modal()

        await self.validate_success_message_and_continue(
            self.modal_message_selector,
            self.continue_button_selector,
            self.success_restore_message_text,
        )
        await self.validate_record_state(is_deleted=False)

    async def fill_input_fields(self, is_edit=False, only_required=False):
        """Llena los campos del formulario con los valores generados.

        Args:
            is_edit (bool, opcional):
                Si es True, solo llena campos editables. Por defecto False.
            only_required (bool, opcional):
                Si es True, solo llena campos obligatorios. Por defecto False.

        Efectos:
            - Recorre las instancias de campos (`input_field_instances`).
            - Determina qué campos deben rellenarse según las banderas dadas.
            - Llama a `fill_data` para completar cada campo seleccionado.
        """
        for field_name, field_instance in self.input_field_instances.items():
            should_fill = True
            if only_required and not field_instance.is_required:
                should_fill = False
            if is_edit and not getattr(field_instance, "is_editable", True):
                should_fill = False
            if field_instance.is_generated_field:
                should_fill = False
            if getattr(field_instance, "is_dependent", False):
                activating_field_name = getattr(field_instance, "activating_field", None)
                activating_values = getattr(field_instance, "activating_values", None)

                if not activating_field_name:
                    should_fill = False
                elif not activating_values:
                    should_fill = False
                elif activating_field_name not in self.input_field_instances:
                    should_fill = False
                else:
                    activating_field = self.input_field_instances[activating_field_name]
                    activating_value = getattr(activating_field, "field_value", None)
                    if activating_value is None or activating_value not in activating_values:
                        should_fill = False

            if should_fill:
                data_to_fill = {field_instance.field_selector: field_instance.field_value}
                if field_instance.input_type == InputType.RANGE_OF_DATES:
                    start_selector = f'input[name="{field_instance.name}_0"]'
                    end_selector = f'input[name="{field_instance.name}_1"]'
                    start_value, end_value = field_instance.field_value
                    data_to_fill = {start_selector: start_value, end_selector: end_value}
                await self.fill_data(data_to_fill)

    async def fill_specific_field_with_invalid_data(
        self,
        field_instance: FieldsPage,
        validate_type: InvalidDataType,
        custom_message: Optional[str] = None,
        custom_value: Optional[str] = None,
        submit=True,
    ):
        """Llena un campo con datos inválidos para una validación específica.

        :param validate_type: Tipo de validación a realizar.
        :param custom_message: Mensaje personalizado para mostrar en caso de error.
        :param custom_value: Valor personalizado para usar en la validación.
        """
        invalid_value, error_message = await field_instance.invalid_data_factory.get_strategy(
            invalid_data_type=validate_type
        ).generate_data()

        if custom_value:
            field_instance.custom_value = custom_value
            invalid_value = custom_value

        if custom_message:
            error_message = custom_message

        if field_instance.input_type in [InputType.SELECT2, InputType.SELECT2_MULTIPLE]:
            invalid_value = field_instance.convert_to_select2_format_value(invalid_value)

        await self.fill_data({field_instance.field_selector: invalid_value})

        await self.wait_for_selector(self.submit_create_form_selector, 1)
        if submit:
            await self.submit_form(self.submit_create_form_selector)
            await self.check_error_message(
                error_selectors=[self.error_message_selector, self.modal_message_selector],
                error_message=error_message,
                continue_button_selector=self.continue_button_selector,
            )

        field_instance.validate_value = invalid_value

    async def fill_specific_field_with_valid_data(
        self,
        field_instance: FieldsPage,
        validate_data_type: ValidDataType,
        custom_value: Optional[str] = None,
        submit=True,
    ):
        """Llena un campo con datos válidos para una validación específica.

        :param validate_data_type: Tipo de validación a realizar.
        :param custom_message: Mensaje personalizado para mostrar en caso de error.
        :param custom_value: Valor personalizado para usar en la validación.
        """
        field_instance = await field_instance.valid_data_factory.get_strategy(
            valid_data_type=validate_data_type
        ).generate_data()

        if custom_value:
            self.set_input_instance_value(**{field_instance.name: custom_value})

        await self.fill_data({field_instance.field_selector: field_instance.field_value})
        if submit:
            await self.submit_form(self.submit_create_form_selector)

        if validate_data_type == ValidDataType.DISABLED:
            field_instance.field_value = field_instance.original_value

        if ValidDataType.EMPTY == validate_data_type and field_instance.validate_value_for_nullable:
            value = None
            if field_instance.input_type in [InputType.SELECT2, InputType.SELECT2_MULTIPLE]:
                value = field_instance.generate_select2_value(
                    field_instance.input_type, field_instance.validate_value_for_nullable
                )
            else:
                value = field_instance.validate_value_for_nullable
            field_instance.validate_value = value

    async def filter_by_specific_field(self, field, custom_value=None, lookup_formset=False):
        """Aplica un filtro por un campo específico y valida los resultados.

        Ya sea del formulario principal o de un formset.

        Args:
            field (str): Nombre del campo a filtrar.
            custom_value (Any, opcional): Valor a usar para el filtro; si no se provee,
                se utiliza el `filter_value` del propio campo.
            lookup_formset (bool, opcional): Si es True, busca el campo en formsets en lugar
                del formulario principal cuando el campo existe en ambos. Por defecto False.

        Efectos:
            - Navega a la página de índice.
            - Determina el origen del campo (principal o formset) y aplica el filtro.
            - Ejecuta la búsqueda y valida los resultados en la tabla índice.

        Raises:
            ValueError: Si el campo no existe en `input_field_instances`, `formset_instances`
                ni en `formset_fields`.
        """
        if not self.field_exists(field):
            raise ValueError(f"El campo '{field}' no existe en los campos de la página ni en formsets.")

        # Caso 1: Verificar si el campo está en input_field_instances (filtros normales)
        field_founded = False
        search_field: FieldsPage = self.input_field_instances.get(field)
        await self.goto_index_page()
        field_in_formset = any(
            field in formset_data.get("fields", {}) for formset_data in self.formset_fields.values()
        )
        if search_field and not (lookup_formset and field_in_formset):
            field_founded = True
            # Esto es para probar los filtros de campos generador por back, esos campos están definidos como is_generated_field
            # por lo que no tienen valor inicial nunca
            if search_field.is_generated_field:
                search_field.generate_valid_data(ignore_generated_fields=False)
            value = (
                custom_value
                if custom_value
                else self._resolve_field_value(search_field, search_field.filter_value, DependencyAction.FILTER)
            )
            await self._apply_filter_and_validate_index(search_field.filter_selector, value)

        # Caso 2: Si no está en input_field_instances, buscar en formset_instances
        for formset_name, formset_types in self.formset_instances.items():
            for action_type, form_instances in formset_types.items():
                for form_instance in form_instances:
                    field_metadata = self.formset_fields.get(formset_name, {}).get("fields", {}).get(field)
                    if not field_metadata:
                        continue  # Si el campo no está en la configuración, omitir
                    for field_selector, field_object in form_instance.items():
                        value = None
                        filter_selector = field_metadata.filter_selector
                        filter_value = None
                        if isinstance(field_object, GenericPage):
                            if field == self.get_formset_field_name(field_selector):
                                field_founded = True
                                filter_value = self._resolve_dependency_value(
                                    field_object, self.get_formset_field_name(field_selector), DependencyAction.FILTER
                                )
                                await self._apply_filter_and_validate_index(filter_selector, filter_value)
                        elif isinstance(field_object, FieldsPage):
                            # Esto es para probar los filtros de campos generador por back, esos campos están definidos como is_generated_field
                            # por lo que no tienen valor inicial nunca
                            field_value_instance = field_object
                            filter_value = field_value_instance.filter_value
                            if field_value_instance.is_generated_field:
                                field_value_instance.generate_valid_data(ignore_generated_fields=False)
                                filter_value = field_value_instance.filter_value
                            if field == self.get_formset_field_name(field_value_instance.field_selector):
                                field_founded = True

                                # Aplicar validación después de filtrar
                                await self._apply_filter_and_validate_index(filter_selector, filter_value)

        # Caso 3: Si el campo se encuentra en los fields de self.formset_fields
        # Esto es para cuando quieras probar filtros invalidos
        if not field_founded:
            for formset_name, formset_types in self.formset_fields.items():
                for field_name, field_atributtes in formset_types["fields"].items():
                    if field_name == field:
                        field_founded = True
                        if not field_atributtes.filter_value:
                            field_atributtes.generate_valid_data()
                        await self._apply_filter_and_validate_index(
                            field_atributtes.filter_selector, field_atributtes.filter_value
                        )
                        # Aplicar validación después de filtrar
                        await self.page.click(self.filter_button_selector)
        # Si el campo no se encuentra en ningún diccionario, lanzar un error
        if not field_founded:
            raise ValueError(
                f"El campo '{field}' no se encontró en input_field_instances ni en formset_instances ni en formset_fields."
            )

    async def _apply_filter_and_validate_index(self, selector, value):
        """Aplica un valor de filtro y valida los resultados en la vista índice.

        Args:
            selector (str | list[str]): Selector(es) del campo de filtro.
            value (Any): Valor o lista de valores a aplicar.

        Efectos:
            - Aplica el filtro con `_apply_filter_and_validate_index`.
            - Ejecuta la búsqueda.
            - Valida los resultados en la tabla índice con `self.index_data_validate`.
        """
        if isinstance(selector, list):
            for sub_value in value:
                await self.fill_data({selector: sub_value})
        else:
            await self.fill_data({selector: value})
        await self.page.click(self.filter_button_selector)
        await self.validate_record_information_in_index_view(self.index_data_validate)
