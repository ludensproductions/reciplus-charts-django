from apps.comun.consts import CRUDOperatorsEnum

from .base_generator import BaseGenerator
from .consts import (
    CONST_API_PATH,
    CONST_API_TAG,
    CONST_PERMISSION_ADD,
    CONST_PERMISSION_CHANGE,
    CONST_PERMISSION_DELETE,
    CONST_PERMISSION_VIEW,
    CONST_PERMISSIONS,
    CREATE_SCHEMA_OUT,
    DELETE_SCHEMA_OUT,
    DISPLAY_NAME,
    PATCH_SCHEMA_OUT,
    STR_METHOD,
    UPDATE_SCHEMA_OUT,
)


class APIGenerator(BaseGenerator):
    """Generator for creating API files (controllers, schemas) automatically.

    Generates complete scaffolding for Django Ninja REST APIs including
    controllers, schemas, and integration with filtering and pagination.
    """

    def __init__(self, app_label, model):
        super().__init__(app_label, model)

    def controller(self, operations):
        """Generates the API controller file with specified operations.

        Args:
            operations: List of CRUD operations to include in the controller.

        Returns:
            String with the complete controller.py code.
        """
        ops = set(operations or [])

        # Build needed consts — PERMISSION_VIEW always required for the decorator
        needed_consts = {CONST_API_PATH, CONST_API_TAG, CONST_PERMISSION_VIEW, CONST_PERMISSIONS}

        route_info_lines = []

        if CRUDOperatorsEnum.CREATE in ops:
            needed_consts.add(CONST_PERMISSION_ADD)
            route_info_lines.append(
                """create_route_info = {
        PERMISSIONS: [
            PERMISSION_ADD,
        ],
    }"""
            )

        if CRUDOperatorsEnum.UPDATE in ops:
            needed_consts.add(CONST_PERMISSION_CHANGE)
            route_info_lines.append(
                """update_route_info = {
        PERMISSIONS: [
            PERMISSION_CHANGE,
        ],
    }"""
            )

        if CRUDOperatorsEnum.DELETE in ops:
            needed_consts.add(CONST_PERMISSION_DELETE)
            route_info_lines.append(
                """delete_route_info = {
        PERMISSIONS: [
            PERMISSION_DELETE,
        ],
    }"""
            )

        route_info_block = ("\n\n    " + "\n\n    ".join(route_info_lines)) if route_info_lines else ""

        consts_import = ",\n    ".join(sorted(needed_consts))
        if consts_import:
            consts_import += ","

        module_service = f"{self.model_name}Service"

        code = f'''
from ninja_jwt.authentication import JWTAuth

from apps.comun.api.controller import BaseApiController
from apps.comun.api.decorator import api_controller

from ..consts import (
    {consts_import}
)
from ..models import {self.model_name}
from .service import {module_service}


@api_controller(
    API_PATH,
    tags=[API_TAG],
    auth=JWTAuth(),
    permissions=[
        PERMISSION_VIEW,
    ],
)
class {self.module_controller}(BaseApiController):
    """API controller for {self.model_name} operations."""

    model = {self.model_name}{route_info_block}

    service_type = {module_service}
'''
        return self._format_code(code)

    def service(self):
        """Generates the API service file with a stub class.

        Returns:
            String with the complete service.py code.
        """
        module_service = f"{self.model_name}Service"

        code = f'''
from apps.comun.api.service import GenericModelService

from ..models import {self.model_name}


class {module_service}(GenericModelService):
    """Service for {self.model_name} CRUD operations.

    Inherits all CRUD logic from GenericModelService.
    Override the following methods to customize behavior:

    Lifecycle hooks (set via constructor or override):
        pre_save(request, instance):  Called before saving; must return the instance.
        post_save(request, instance): Called after saving; must return the instance.

    Core operations (override to add custom business logic):
        create(schema, **kwargs)  -> {self.model_name}
        update(instance, schema, **kwargs) -> {self.model_name}
        delete(instance, **kwargs) -> {self.model_name}
        get_all(**kwargs)         -> QuerySet
        get_one(pk, **kwargs)     -> {self.model_name}

    Validation helpers (override to extend or replace validation):
        _validate_instance(instance)                          -> None
        _handle_django_validation_error(e)                    -> raises ValidationError
        _get_auto_fields(instance)                            -> list[str]
        _validate_m2m_options(instance, field_name, values)   -> None

    Internal utilities (override only if you need custom field handling):
        _separate_m2m_fields(data)   -> tuple[dict, dict]
        _sync_display_name(instance) -> None

    Example — inject the current user on create::

        def create(self, schema, **kwargs):
            context = service_resolver(RouteContext)
            kwargs["created_by"] = context.request.user
            return super().create(schema, **kwargs)
    """

    pass
'''
        return self._format_code(code)

    def schemas(self):
        """Generates the API schemas file for request/response serialization.

        Creates Pydantic schemas for input and output, with special handling
        for models that have a display_name field.

        Returns:
            String with the complete schema.py code.
        """
        schemas_fields = [f.name for f in self.model_fields if not isinstance(f, self.FIELDS_EXCLUDED_IN_FILTERS)]

        # Verificar si el modelo tiene un campo display_name
        has_display_name = DISPLAY_NAME in schemas_fields

        # Obtener el campo principal para usar como alias (solo si tiene display_name)
        display_name_alias = self.get_display_name_field_alias() if has_display_name else None

        # Excluir display_name de los schemas de entrada (solo si existe)
        schemas_fields_input = [f for f in schemas_fields if f != DISPLAY_NAME] if has_display_name else schemas_fields

        # Schemas de salida: si no hay display_name, usar todos los campos
        schemas_fields_output = schemas_fields if not has_display_name else schemas_fields

        # Si el modelo tiene display_name, generar schemas con alias
        if has_display_name and display_name_alias and display_name_alias != STR_METHOD:
            code = f'''
from ninja import Field, ModelSchema, Schema
from pydantic import ConfigDict

from ..models import {self.model_name}


class {self.module_schema_in}(ModelSchema):
    """Input schema for {self.model_name} API operations used for create/update."""

    class Meta:
        model = {self.model_name}
        fields = {self._format_fields_list(schemas_fields_input)}


class {self.module_schema_out}(Schema):
    """Output schema for {self.model_name} list and retrieve operations."""

    model_config = ConfigDict(from_attributes=True)

    display_name: str = Field(None, alias="{display_name_alias}")


class {CREATE_SCHEMA_OUT}(Schema):
    """Response schema for {self.model_name} create operations."""

    model_config = ConfigDict(from_attributes=True)

    display_name: str = Field(None, alias="{display_name_alias}")


class {UPDATE_SCHEMA_OUT}(Schema):
    """Response schema for {self.model_name} full update operations."""

    model_config = ConfigDict(from_attributes=True)

    display_name: str = Field(None, alias="{display_name_alias}")


class {PATCH_SCHEMA_OUT}(Schema):
    """Response schema for {self.model_name} partial update operations."""

    model_config = ConfigDict(from_attributes=True)

    display_name: str = Field(None, alias="{display_name_alias}")


class {DELETE_SCHEMA_OUT}(Schema):
    """Response schema for {self.model_name} delete operations."""

    model_config = ConfigDict(from_attributes=True)

    display_name: str = Field(None, alias="{display_name_alias}")


class {self.model_name}SchemaOutExtraFields(ModelSchema):
    """Schema with additional metadata fields for {self.model_name}."""

    class Meta:
        model = {self.model_name}
        fields = ["created_at", "updated_at", "deleted", "id"]
'''
            return self._format_code(code)

        # Si no tiene display_name, generar schemas normales con ModelSchema
        code = f'''
from ninja import ModelSchema

from ..models import {self.model_name}


class {self.module_schema_in}(ModelSchema):
    """Input schema for {self.model_name} API operations used for create/update."""

    class Meta:
        model = {self.model_name}
        fields = {self._format_fields_list(schemas_fields_input)}


class {self.module_schema_out}(ModelSchema):
    """Output schema for {self.model_name} list and retrieve operations."""

    class Meta:
        model = {self.model_name}
        fields = {self._format_fields_list(schemas_fields_output)}


class {CREATE_SCHEMA_OUT}(ModelSchema):
    """Response schema for {self.model_name} create operations."""

    class Meta:
        model = {self.model_name}
        fields = {self._format_fields_list(schemas_fields_output)}


class {UPDATE_SCHEMA_OUT}(ModelSchema):
    """Response schema for {self.model_name} full update operations."""

    class Meta:
        model = {self.model_name}
        fields = {self._format_fields_list(schemas_fields_output)}


class {PATCH_SCHEMA_OUT}(ModelSchema):
    """Response schema for {self.model_name} partial update operations."""

    class Meta:
        model = {self.model_name}
        fields = {self._format_fields_list(schemas_fields_output)}


class {DELETE_SCHEMA_OUT}(ModelSchema):
    """Response schema for {self.model_name} delete operations."""

    class Meta:
        model = {self.model_name}
        fields = {self._format_fields_list(schemas_fields_output)}


class {self.model_name}SchemaOutExtraFields(ModelSchema):
    """Schema with additional metadata fields for {self.model_name}."""

    class Meta:
        model = {self.model_name}
        fields = {self._format_fields_list(["created_at", "updated_at", "deleted", "id"])}
'''
        return self._format_code(code)
