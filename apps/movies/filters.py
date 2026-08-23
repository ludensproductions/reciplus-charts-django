from apps.comun.filter_fields import TruncatedModelChoiceFilter
from apps.comun.filters import AbstractFilter

from .consts import FIELD_GENRE_LABEL, MOVIES_FILTER_FIELDS
from .models import Movie


class MoviesFilter(AbstractFilter):
    """Filter set for movies by title, year, and genre."""

    genre = TruncatedModelChoiceFilter(
        queryset=Movie.objects.all(),
        label=FIELD_GENRE_LABEL,
    )

    class Meta:
        model = Movie
        fields = list(MOVIES_FILTER_FIELDS.keys())
        fields_dict = MOVIES_FILTER_FIELDS
