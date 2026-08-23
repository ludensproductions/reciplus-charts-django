from typing import Any, Dict, Generic, List, Optional, Set, Type, Union

from ninja_extra import (
    ModelConfig,
    ModelControllerBase,
    ModelSchemaConfig,
    http_delete,
    http_get,
    http_patch,
    http_post,
    http_put,
)
from pydantic import BaseModel as PydanticModel, Field, field_validator


class BaseApiController(ModelControllerBase):
    # Configuration for ModelController
    model = None
    allowed_routes: List[str] = [
        "create",
        "find_one",
        "update",
        "patch",
        "delete",
        "list",
    ]
    async_routes: bool = False
    create_schema: Type[PydanticModel] | None = None
    retrieve_schema: Type[PydanticModel] | None = None
    update_schema: Type[PydanticModel] | None = None
    patch_schema: Type[PydanticModel] | None = None

    create_route_info: Dict = {}  # extra @post() information
    find_one_route_info: Dict = {}  # extra @get('/{id}') information
    update_route_info: Dict = {}  # extra @put() information
    patch_route_info: Dict = {}  # extra @patch() information
    list_route_info: Dict = {}  # extra @get('/') information
    delete_route_info: Dict = {}  # extra @delete() information

    # Condiguration for Schema config
    exclude_fields: Set[str] | None
    include: Union[str, List[str]] = Field(default="__all__")
    optional: Optional[Union[str, Set[str]]] = Field(default=None)
    write_only_fields: Optional[Union[List[str]]] = Field(default=None)
    read_only_fields: Optional[List[str]] = Field(default=None)

    def __init__(self):
        self.model_config = ModelConfig(
            model=self.model,
            allowed_routes=self.allowed_routes,
            async_routes=self.async_routes,
            create_schema=self.create_schema,
            retrieve_schema=self.retrieve_schema,
            update_schema=self.update_schema,
            patch_schema=self.patch_schema,
            create_route_info=self.create_route_info,
            find_one_route_info=self.find_one_route_info,
            update_route_info=self.update_route_info,
            patch_route_info=self.patch_route_info,
            list_route_info=self.list_route_info,
            delete_route_info=self.delete_route_info,
            schema_config=ModelSchemaConfig(
                exclude={
                    "id",
                    "deleted",
                    "deleted_by_cascade",
                    "created_at",
                    "updated_at",
                    "created_by",
                    "updated_by",
                }
            ),
        )

        if self.exclude_fields:
            self.model_config.schema_config.exclude += self.exclude_fields

        if self.read_only_fields:
            self.model_config.schema_config.read_only_fields = self.read_only_fields
        if self.write_only_fields:
            self.model_config.schema_config.write_only_fields = self.write_only_fields
        if self.optional:
            self.model_config.schema_config.optional = self.optional
        if self.include:
            self.model_config.schema_config.include = self.include
        super().__init__()
