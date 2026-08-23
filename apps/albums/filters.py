from apps.comun.filters import AbstractFilter

from . import consts as albums_consts
from .models import Album

album_fields = {
    "title": albums_consts.FILTER_FIELDS["title"],
    "year": albums_consts.FILTER_FIELDS["year"],
    "artist": albums_consts.FILTER_FIELDS["artist"],
}


class AlbumsFilter(AbstractFilter):
    """Filter class for Album model.

    Provides filtering options for album fields such as title, year, and artist.
    Uses centralized, internationalized labels from the app's constants.
    """

    class Meta:
        model = Album
        fields = list(album_fields.keys())
        fields_dict = album_fields
