from ninja import Field, ModelSchema, Schema
from pydantic import ConfigDict

from ..models import Genre


class GenreSchemaIn(ModelSchema):  # noqa
    model_config = ConfigDict(extra="forbid")

    class Meta:
        model = Genre
        fields = ["genre"]


class GenreSchemaOut(Schema):  # noqa
    genre: str = Field(None, alias="display_name")
    model_config = ConfigDict(from_attributes=True)


class CreateSchemaOut(Schema):  # noqa
    display_name: str = Field(None, alias="genre")
    model_config = ConfigDict(from_attributes=True)


class UpdateSchemaOut(Schema):  # noqa
    display_name: str = Field(None, alias="genre")
    model_config = ConfigDict(from_attributes=True)


class PatchSchemaOut(Schema):  # noqa
    display_name: str = Field(None, alias="genre")
    model_config = ConfigDict(from_attributes=True)


class DeleteSchemaOut(Schema):  # noqa
    display_name: str = Field(None, alias="genre")
    model_config = ConfigDict(from_attributes=True)


class GenreSchemaOutExtraFields(ModelSchema):  # noqa
    model_config = ConfigDict(extra="forbid")

    class Meta:
        model = Genre
        fields = [
            "created_at",
            "updated_at",
            "deleted",
            "id",
        ]
