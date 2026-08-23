"""Mixin que encapsula métodos helpers/utilidades para GenericPage.

Este mixin proporciona métodos auxiliares de propósito general que ayudan en:
- Búsqueda y acceso a instancias de campos
- Resolución de valores de dependencias
- Extracción de información de campos
- Manipulación de selectores
- Operaciones HTTP para campos adicionales
- Depuración y logging

Author: Copilot
Date: 2026-01-29
"""

import logging
import re
from typing import TYPE_CHECKING, Dict
from urllib.parse import urlencode

import requests

from tests.pages.core.constants import DependencyAction, FieldRef, InputType
from tests.pages.core.fields_page import FieldsPage

if TYPE_CHECKING:
    from tests.pages.core.generic_page import GenericPage

logger = logging.getLogger(__name__)


class HelpersMixin:
    """Mixin con métodos auxiliares y helpers para GenericPage.

    Este mixin proporciona utilidades para:
    - Búsqueda de instancias de campos por atributos
    - Resolución de valores de dependencias
    - Obtención de información de campos y dependencias
    - Extracción de nombres de campos desde selectores
    - Validación de existencia de campos
    - Métodos HTTP para campos adicionales
    - Utilidades de depuración
    """

    current_username_selector = "#username"

    # ============================================================================
    # SECTION 1: BÚSQUEDA Y ACCESO A INSTANCIAS
    # ============================================================================

    def get_input_instance_by_attribute(self, attribute, value):
        """Obtiene una instancia de campo basado en un atributo y su valor.

        Args:
            attribute (str): Nombre del atributo a buscar (ejemplo: 'name', 'field_selector').
            value (Any): Valor del atributo a coincidir.

        Returns:
            FieldsPage | None: Instancia del campo si se encuentra, de lo contrario None.
        """
        for field_instance in self.input_field_instances.values():
            if hasattr(field_instance, attribute) and getattr(field_instance, attribute) == value:
                return field_instance
        return None

    def get_dependency_page_by_field_name(self, field_name):
        """Obtiene la instancia de página de dependencia asociada a un nombre de campo.

        Args:
            field_name (str): Nombre del campo para el cual se busca la página de dependencia.

        Returns:
            GenericPage | None: Instancia de la página de dependencia si se encuentra,
                de lo contrario None.
        """
        for page_cls, config in self.input_field_dependencies.items():
            fields = config.get(DependencyAction.CREATE, {}).keys()
            if field_name in fields:
                return page_cls
        return None

    def get_generated_field_instances(self) -> Dict[str, FieldsPage]:
        """Retorna instancias de FieldsPage que son campos generados.

        Returns:
            Dict[str, FieldsPage]: Diccionario con instancias de campos generados.
        """
        return {
            name: field
            for name, field in self.input_field_instances.items()
            if getattr(field, "is_generated_field", False)
        }

    # ============================================================================
    # SECTION 2: INFORMACIÓN DE DEPENDENCIAS Y CAMPOS
    # ============================================================================

    def get_keys_dependencies(self):
        """Extrae todas las claves de campos que tienen dependencias configuradas.

        Recorre `self.input_field_dependencies` para obtener las claves de todos los campos
        que están definidos como dependencias bajo la acción `DependencyAction.CREATE`.
        Útil para identificar qué campos requieren manejo especial durante la generación
        de datos de formularios o formsets.

        Returns:
            set: Conjunto de nombres de campos que tienen dependencias configuradas.
                Estos campos requieren procesamiento especial y no deben ser tratados
                como campos regulares en el llenado de formularios.

        Efectos:
            - Itera sobre todas las configuraciones de dependencias de campos de entrada.
            - Extrae las claves de los bloques de configuración CREATE.
            - Retorna un conjunto único de nombres de campos con dependencias.
        """
        inner_keys = set()
        for page_cfg in self.input_field_dependencies.values():
            create_block = page_cfg.get(DependencyAction.CREATE, {})
            inner_keys.update(create_block.keys())
        return inner_keys

    def get_dependents_fields(self):
        """Obtiene una lista de nombres de campos que son dependientes de otras entidades.

        Returns:
            list: Lista de instancias de campos que son dependientes.
        """
        dependent_fields = []
        for fields in self.input_field_instances.values():
            if getattr(fields, "is_dependent", False):
                dependent_fields.append(fields)

        return dependent_fields

    # ============================================================================
    # SECTION 3: RESOLUCIÓN DE VALORES
    # ============================================================================

    def _resolve_token_to_instance(self, token, generic_instance: "GenericPage"):
        """Resuelve un token de dependencia a su instancia de FieldsPage.

        Args:
            token (str | FieldRef): Identificador del campo a resolver.
            generic_instance (GenericPage): Instancia de la dependencia que contiene los campos.

        Returns:
            FieldsPage | None: Instancia del campo, o None si no se encuentra.
        """
        if isinstance(token, FieldRef):
            if token.lookup_formset:
                for create_and_edit in generic_instance.formset_instances.values():
                    for selector, instance in create_and_edit.get("create", [])[0].items():
                        if self.get_formset_field_name(selector) == token.name:
                            return instance
                return None
            return generic_instance.input_field_instances.get(token.name)

        # str: comportamiento original — auto-detect (formset tiene prioridad)
        if token in generic_instance.get_all_formset_fields():
            for create_and_edit in generic_instance.formset_instances.values():
                for selector, instance in create_and_edit.get("create", [])[0].items():
                    if self.get_formset_field_name(selector) == token:
                        return instance
            return None
        return generic_instance.input_field_instances.get(token)

    def _resolve_all_dependency_values(
        self,
        generic_instance: "GenericPage",
        field_name: str,
    ) -> dict:
        """Resuelve todos los valores de dependencia (CREATE, VALIDATE, FILTER, INDEX) en una sola llamada.

        Args:
            generic_instance (GenericPage): Instancia de la página de dependencia.
            field_name (str): Nombre del campo cuyo valor se resolverá.

        Returns:
            dict: Diccionario con keys 'create', 'validate', 'filter', 'index', 'separator' y sus valores resueltos.
        """
        result = {"create": "", "validate": "", "filter": "", "index": "", "separator": ""}

        if not generic_instance or not field_name:
            return result

        # Verificar que tiene los atributos necesarios (duck typing)
        if not hasattr(generic_instance, "input_field_instances") or not hasattr(
            generic_instance, "input_field_dependencies"
        ):
            return result

        dep_map = self.input_field_dependencies.get(type(generic_instance), {})

        # Procesar cada acción
        for action in [
            DependencyAction.CREATE,
            DependencyAction.VALIDATE,
            DependencyAction.FILTER,
            DependencyAction.INDEX,
        ]:
            dependencies_for_action = dep_map.get(action, {})
            tokens = dependencies_for_action.get(field_name)

            if not tokens:
                dependencies_for_action = dep_map.get(DependencyAction.CREATE, {})
                tokens = dependencies_for_action.get(field_name)

            if not tokens:
                continue

            # Caso especial para INDEX y VALIDATE: el último token puede ser el separador
            separator = ""
            tokens_to_process = tokens

            if action in [DependencyAction.INDEX, DependencyAction.VALIDATE] and tokens and len(tokens) > 1:
                last_token = tokens[-1]
                is_field = (
                    isinstance(last_token, FieldRef)
                    or last_token in generic_instance.input_field_instances
                    or last_token in generic_instance.get_all_formset_fields()
                )

                if (
                    not is_field
                    and isinstance(last_token, str)
                    and len(last_token.split()) == 1
                    and last_token not in [")", "]", "}"]
                ):
                    separator = last_token
                    tokens_to_process = tokens[:-1]
                    if action == DependencyAction.VALIDATE:
                        result["separator"] = separator

            # Resolver tokens a valores
            resolved_parts = []
            for token in tokens_to_process:
                instance = self._resolve_token_to_instance(token, generic_instance)
                if instance:
                    resolved_parts.append(instance.field_value)
                elif not isinstance(token, FieldRef):
                    resolved_parts.append(str(token))

            resolved_value = "".join(str(part) for part in resolved_parts)

            # Mapear al key correspondiente
            action_key = action.value.lower()  # 'CREATE' -> 'create'
            result[action_key] = resolved_value

        return result

    def _resolve_dependency_value(
        self,
        generic_instance: "GenericPage",
        field_name: str,
        action: DependencyAction = DependencyAction.CREATE,
        accumulated_text: str = "",
    ) -> str:
        """Resuelve el valor de un campo de dependencia según tokens configurados.

        Args:
            generic_instance (GenericPage): Instancia de la página de dependencia.
            field_name (str): Nombre del campo cuyo valor se resolverá.
            action (DependencyAction): Acción para la cual se resuelve (CREATE, INDEX, VALIDATE).
            accumulated_text (str): Texto acumulado previo para concatenar.

        Returns:
            str: Valor resuelto concatenando tokens o texto literal.
        """
        if not generic_instance and not field_name:
            logger.debug("[WARNING] No se proporcionó 'generic_instance' ni 'field_name'; retorno ''.")
            return ""

        # Verificar que tiene los atributos necesarios (duck typing)
        if not hasattr(generic_instance, "input_field_instances") or not hasattr(
            generic_instance, "input_field_dependencies"
        ):
            logger.debug("[WARNING] 'generic_instance' no tiene los atributos necesarios; retorno ''.")
            return ""

        dep_map = self.input_field_dependencies.get(type(generic_instance), {})
        dependencies_for_action = dep_map.get(action, {})

        tokens = dependencies_for_action.get(field_name)
        if not tokens:
            dependencies_for_action = dep_map.get(DependencyAction.CREATE)
            tokens = dependencies_for_action.get(field_name)

        # Caso especial para INDEX y VALIDATE: el último token puede ser el separador
        # Solo se considera separador si NO está vacío Y NO es un campo existente
        separator = ""
        if action in [DependencyAction.INDEX, DependencyAction.VALIDATE] and tokens and len(tokens) > 1:
            last_token = tokens[-1]

            is_field = (
                isinstance(last_token, FieldRef)
                or last_token in generic_instance.input_field_instances
                or last_token in generic_instance.get_all_formset_fields()
            )

            if (
                not is_field
                and isinstance(last_token, str)
                and len(last_token.split()) == 1
                and last_token not in [")", "]", "}"]
            ):
                separator = last_token
                tokens = tokens[:-1]

        # Resolver tokens a valores (field_value si existe, si no literal)
        resolved_parts = []
        for token in tokens:
            instance = self._resolve_token_to_instance(token, generic_instance)
            if instance:
                resolved_parts.append(instance.field_value)
            elif not isinstance(token, FieldRef):
                resolved_parts.append(str(token))

        result = "".join(str(part) for part in resolved_parts)

        # Si hay texto acumulado, concatenar con el separador
        if accumulated_text:
            return accumulated_text + separator + result

        return result

    def _resolve_field_value(self, field: FieldsPage, actual_value: str, action: DependencyAction) -> str:
        """Resuelve el valor de un campo basado en si es dependiente o no.

        Args:
            field (FieldsPage): Instancia del campo a resolver.
            actual_value (str): Valor actual del campo.
            action (DependencyAction): Acción para la cual se resuelve.

        Returns:
            str: Valor resuelto del campo.
        """
        if getattr(field, "is_dependent", False):
            dependency_instance = field.dependency_instance
            dependency_field = field.name

            if not dependency_instance:
                page = self.get_dependency_page_by_field_name(dependency_field)
                dependency_instance = self.dependency_instances.get(page)

            if dependency_instance:
                return self._resolve_dependency_value(dependency_instance, dependency_field, action, actual_value)
            return actual_value

        return actual_value

    # ============================================================================
    # SECTION 4: MANIPULACIÓN DE SELECTORES Y NOMBRES
    # ============================================================================

    def extract_field_name_from_selector(self, selector: str) -> str:
        """Extrae el nombre del campo desde un selector CSS.

        Args:
            selector (str): Selector CSS del campo.

        Returns:
            str: Nombre del campo extraído.
        """
        # Intentar extraer de input[name=...]
        name = self._extract_name_attribute(selector)
        if name != selector:  # Si extrajo algo
            return name

        # Intentar extraer de #div_id_...
        m = re.search(r"#div_id_([\w-]+)", selector)
        if m:
            return m.group(1)

        # Intentar extraer de #id...
        m = re.search(r"#([\w-]+)", selector)
        if m:
            return m.group(1)

        # Último recurso
        return selector.split()[0] if " " in selector else selector

    def field_exists(self, field_name: str) -> bool:
        """Verifica si un campo existe en el formulario principal o en los formsets.

        Args:
            field_name (str): Nombre del campo a buscar.

        Returns:
            bool: True si el campo existe, False en caso contrario.

        Ejemplo:
            if not self.field_exists(field_name):
                raise ValueError(f"El campo '{field_name}' no existe...")
        """
        if field_name in self.input_field_instances:
            return True

        formset_fields = self.get_all_formset_fields()
        return field_name in formset_fields

    # ============================================================================
    # SECTION 5: MANIPULACIÓN DE VALORES DE CAMPOS
    # ============================================================================

    def set_input_instance_value(self, **kwargs):
        """Sobrescribe manualmente los valores de campos específicos con los datos proporcionados.

        Args:
            **kwargs: Pares clave-valor donde:
                - La clave es el nombre del campo (str).
                - El valor es el nuevo valor que se asignará.

        Efectos:
            - Si el campo existe en `input_field_instances`:
                * Para campos `SELECT2` o `SELECT2_MULTIPLE`, se asigna como un diccionario
                  {selector: valor}.
                * Para otros tipos de campos, se asigna directamente el valor.
            - En ambos casos, se actualizan también `validate_value` y `filter_value`.
        """
        for field_name, value in kwargs.items():
            if field_name in self.input_field_instances:
                instance: FieldsPage = self.input_field_instances[field_name]
                if instance.input_type in [
                    InputType.SELECT2_MULTIPLE,
                    InputType.SELECT2,
                ]:
                    instance.field_value = {instance.select2_search_selector: value}
                else:
                    instance.field_value = value

                instance.validate_value = value
                instance.filter_value = value
                instance.index_value = value

                if instance.input_type in [
                    InputType.DATE,
                    InputType.DATE_START,
                    InputType.DATE_END,
                    InputType.RANGE_OF_DATES,
                    InputType.DATE_TIME,
                ]:
                    instance.generate_data_validate()

    # ============================================================================
    # SECTION 6: OPERACIONES HTTP Y CAMPOS ADICIONALES
    # ============================================================================

    async def get_extra_fields_info(self, url: str):
        """Obtiene información de campos adicionales realizando una petición HTTP.

        Los valores de `self.data_validate` se usan como parámetros de consulta.

        Args:
            url (str): URL base del endpoint al que se agregan los parámetros.

        Returns:
            dict: Diccionario con la respuesta JSON del endpoint; en caso de error,
            un diccionario con las claves `error`, `exception_type` y `details`.

        Efectos:
            - Construye la URL final anexando `self.data_validate` como query string.
            - Realiza una petición GET y procesa la respuesta.
            - Normaliza errores de red o de decodificación JSON a un diccionario.
        """
        full_url = f"{url.rstrip('/')}?{urlencode(self.data_validate)}"

        try:
            response = requests.get(full_url)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            return {"error": "Error al realizar la petición", "exception_type": type(e).__name__, "details": str(e)}
        except ValueError as e:
            return {"error": "Error al decodificar la respuesta JSON", "details": str(e)}

    # ============================================================================
    # SECTION 7: CAMPOS GENERADOS
    # ============================================================================

    async def extract_generated_field_values(self):
        """Extrae valores de campos generados automáticamente.

        Estos valores se usan para validaciones en index y detalles.

        Efectos:
            - Itera sobre campos generados y extrae sus valores desde la UI.
            - Actualiza `validate_value`, `index_value` y `filter_value` según corresponda.
            - Regenera diccionarios de filtros y validación.
        """
        for field_name, field in self.get_generated_field_instances().items():
            if getattr(field, "is_generated_field", False):
                value = ""
                # Extraer valor mostrado para validación en detalles
                if "div" in field.field_selector:
                    await self.goto_detail_page()
                    value = await self.get_generated_field_value(field, location="details")
                elif "th" in field.field_selector:
                    await self.goto_index_page()
                    await self.search_records_with_filters()
                    value = await self.get_generated_field_value(field, location="index")

                if not value:
                    raise ValueError(f"No se pudo extraer el valor del campo generado '{field_name}'")

                value = value.strip()

                if field.is_data_validate:
                    field.validate_value = value

                # Extraer valor para mostrar en index
                if field.is_indexable:
                    field.index_value = value

                if getattr(field, "is_filter", False):
                    field.filter_value = value

        self.generate_filters_and_validate_data()

    async def get_generated_field_value(self, field, location="details"):
        """Obtiene el valor de un campo generado desde la interfaz.

        Args:
            field (FieldsPage): Instancia del campo generado.
            location (str): Ubicación desde donde extraer el valor ('details' o 'index').

        Returns:
            str | None: Valor extraído del campo, None si no se encuentra.
        """
        try:
            if location == "details":
                element = await self.page.wait_for_selector(field.field_selector, timeout=5000)
                return await element.text_content()
            elif location == "index":
                return await self.get_cell_value_by_header_th(field.field_selector)
        except:
            return None

    # ============================================================================
    # SECTION 8: UTILIDADES DE DEPURACIÓN
    # ============================================================================

    def print_each_value_instances(self):
        """Imprime los valores de los atributos de cada instancia para depuración.

        Muestra `field_value`, `validate_value`, `filter_value`, `original_value`
        y `is_dependent` de cada instancia en `self.input_field_instances`.
        """
        for field_name, field_instance in self.input_field_instances.items():
            logger.debug("Field: %s", field_name)
            logger.debug("  field_value: %s", field_instance.field_value)
            logger.debug("  validate_value: %s", field_instance.validate_value)
            logger.debug("  filter_value: %s", field_instance.filter_value)
            logger.debug("  original_value: %s", field_instance.original_value)
            logger.debug("  is_dependent: %s", getattr(field_instance, "is_dependent", False))
            logger.debug("--------------------------------------------------")

    async def get_current_username(self) -> str:
        """Obtiene el nombre de usuario del usuario actualmente autenticado.

        Returns:
            str: Nombre de usuario extraído de la interfaz, o 'Unknown' si no se encuentra.
        """
        user_element = await self.page.wait_for_selector(self.current_username_selector, timeout=5000)
        username = await user_element.text_content()
        return username.strip()
