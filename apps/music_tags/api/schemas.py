from ninja import ModelSchema, Schema
from pydantic import ConfigDict

from apps.music_tags.models import MusicTags


class MusicTagsSchemaOut(ModelSchema):  # noqa
    class Meta:
        model = MusicTags
        fields = ["tag", "created_at"]


class EchoSchemaIn(Schema):  # noqa
    model_config = ConfigDict(extra="forbid")
    text: str


class EchoSchemaOut(Schema):  # noqa
    model_config = ConfigDict(extra="forbid")
    echo: str
