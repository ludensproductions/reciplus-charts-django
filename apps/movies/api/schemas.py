from ninja import ModelSchema
from pydantic import ConfigDict

from apps.movies.models import Movie


class MovieSchemaIn(ModelSchema):  # noqa
    model_config = ConfigDict(extra="forbid")

    class Meta:
        model = Movie
        exclude = [
            "created_at",
            "updated_at",
            "deleted",
            "deleted_by_cascade",
            "updated_by",
            "created_by",
            "id",
        ]


class MovieSchemaOut(ModelSchema):  # noqa
    model_config = ConfigDict(extra="forbid")

    class Meta:
        model = Movie
        fields = [
            "title",
        ]


class CreateSchemaOut(ModelSchema):  # noqa
    model_config = ConfigDict(extra="forbid")

    class Meta:
        model = Movie
        fields = ["title", "plot"]


class UpdateSchemaOut(ModelSchema):  # noqa
    model_config = ConfigDict(extra="forbid")

    class Meta:
        model = Movie
        fields = ["title", "year", "plot"]


class PatchSchemaOut(ModelSchema):  # noqa
    model_config = ConfigDict(extra="forbid")

    class Meta:
        model = Movie
        fields = [
            "title",
            "year",
        ]


class DeleteSchemaOut(ModelSchema):  # noqa
    model_config = ConfigDict(extra="forbid")

    class Meta:
        model = Movie
        fields = ["title", "year", "price", "plot"]


class MovieSchemaOutExtraFields(ModelSchema):  # noqa
    model_config = ConfigDict(extra="forbid")

    class Meta:
        model = Movie
        fields = [
            "created_at",
            "updated_at",
            "deleted",
            "id",
        ]
