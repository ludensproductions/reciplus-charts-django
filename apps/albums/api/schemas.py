from ninja import ModelSchema

from apps.albums.models import Album


class AlbumSchemaOut(ModelSchema):  # noqa
    class Meta:
        model = Album
        fields = ["title", "year", "artist"]
