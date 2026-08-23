from apps.comun.filters import AbstractFilter

from .consts import MUSIC_GENRES_FILTER_FIELDS
from .models import MusicGenres


class MusicGenresFilter(AbstractFilter):
    """Filter configuration for music genre list views."""

    class Meta:
        model = MusicGenres
        fields = list(MUSIC_GENRES_FILTER_FIELDS.keys())
        fields_dict = MUSIC_GENRES_FILTER_FIELDS
