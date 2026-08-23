from apps.comun.filters import AbstractFilter

from .consts import GENRE_FILTER_FIELDS
from .models import Genre


class GenreFilter(AbstractFilter):
    """Filter set for genres by display name."""

    class Meta:
        model = Genre
        fields = list(GENRE_FILTER_FIELDS.keys())
        fields_dict = GENRE_FILTER_FIELDS
