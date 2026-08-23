from apps.comun.filters import AbstractFilter

from .consts import MUSIC_TAGS_FILTER_FIELDS
from .models import MusicTags


class MusicTagsFilter(AbstractFilter):
    """Filter configuration for music tag list views."""

    class Meta:
        model = MusicTags
        fields = list(MUSIC_TAGS_FILTER_FIELDS.keys())
        fields_dict = MUSIC_TAGS_FILTER_FIELDS
