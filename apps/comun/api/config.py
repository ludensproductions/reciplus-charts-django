from typing import Optional, Type

from ninja_extra import (
    ModelConfig as NinjaExtraModelConfig,
)
from ninja_schema.errors import ConfigError
from pydantic import BaseModel as PydanticModel


class ModelConfig(NinjaExtraModelConfig):
    """Custom Model Config meant to store the response schemas for each auto-generated endpoint type."""

    create_response_schema: Optional[Type[PydanticModel]] = None
    update_response_schema: Optional[Type[PydanticModel]] = None
    patch_response_schema: Optional[Type[PydanticModel]] = None
    delete_response_schema: Optional[Type[PydanticModel]] = None

    def _get_retrieve_schema_fields(self, working_fields: set, model_pk: str) -> set:
        retrieve_schema_fields = set(working_fields) - set(self.schema_config.write_only_fields or [])
        if self.schema_config.read_only_fields:
            invalid_key = set(self.schema_config.read_only_fields) - retrieve_schema_fields
            if invalid_key:
                raise ConfigError(f"Field(s) {invalid_key} included to working fields.")
        return set(list(retrieve_schema_fields))
