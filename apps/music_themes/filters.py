from apps.comun.filters import AbstractFilter

from .consts import MUSIC_THEMES_FILTER_FIELDS
from .models import MusicThemes


class MusicGenresFilter(AbstractFilter):
    """Filter configuration for music theme list views."""

    class Meta:
        model = MusicThemes
        fields = list(MUSIC_THEMES_FILTER_FIELDS.keys())
        fields_dict = MUSIC_THEMES_FILTER_FIELDS
