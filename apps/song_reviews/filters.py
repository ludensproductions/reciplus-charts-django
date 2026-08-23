from apps.comun.filters import AbstractFilter

from .consts import FILTER_ALBUM_LABEL, FILTER_SCORE_LABEL, FILTER_SONG_LABEL
from .models import SongReview

song_review_fields = {
    "score": {"label": FILTER_SCORE_LABEL},
    "album": {"label": FILTER_ALBUM_LABEL},
    "song": {"label": FILTER_SONG_LABEL},
}


class SongReviewFilter(AbstractFilter):
    """Filter configuration for song review list and search views."""

    class Meta:
        model = SongReview
        fields = list(song_review_fields.keys())
        fields_dict = song_review_fields
