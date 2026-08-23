from apps.comun.filter_fields import TruncatedModelChoiceFilter
from apps.comun.filters import AbstractFilter
from apps.movies.models import Movie

from .consts import FIELD_MOVIE_LABEL, FIELD_PRODUCTOR_LABEL
from .models import MovieInventory

movie_inventory_fields = {
    "movie": {"label": FIELD_MOVIE_LABEL},
    "productor": {"label": FIELD_PRODUCTOR_LABEL},
}


class MovieInventoryFilter(AbstractFilter):
    """Filter set for movie inventory list views."""

    movie = TruncatedModelChoiceFilter(
        queryset=Movie.objects.all(),
        label=FIELD_MOVIE_LABEL,
    )

    class Meta:
        model = MovieInventory
        fields = list(movie_inventory_fields.keys())
        fields_dict = movie_inventory_fields

    def __init__(self, *args, **kwargs):
        """Initialize the filter and handle disabled views.

        Args:
            *args: Positional arguments.
            **kwargs: Keyword arguments including `is_disabled_view`.
        """
        is_disabled_view = kwargs.pop("is_disabled_view", False)
        super().__init__(*args, **kwargs)

        if is_disabled_view:
            moview_model = self.filters["movie"].field.queryset.model
            self.filters["movie"].field.queryset = moview_model.all_objects.all()
