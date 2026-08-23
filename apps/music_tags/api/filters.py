from apps.comun.filters import AbstractFilter
from apps.music_tags.consts import FILTER_FIELDS
from apps.music_tags.models import MusicTags


class MusicTagsFilterSet(AbstractFilter):  # noqa
    class Meta:
        model = MusicTags
        fields_dict = FILTER_FIELDS
        fields = list(FILTER_FIELDS.keys())
