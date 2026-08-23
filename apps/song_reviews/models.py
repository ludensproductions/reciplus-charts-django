from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from safedelete.models import SOFT_DELETE_CASCADE

from apps.albums.models import Album, Song
from apps.comun.models import AbstractModel
from apps.song_reviews.consts import (
    FIELD_ALBUM_LABEL,
    FIELD_REVIEW_LABEL,
    FIELD_SCORE_LABEL,
    FIELD_SONG_LABEL,
    MODEL_SONG_REVIEW_VERBOSE_NAME,
    MODEL_SONG_REVIEW_VERBOSE_NAME_PLURAL,
    PARENT_RELATION_ALBUMS_LABEL,
    PARENT_RELATION_SONGS_LABEL,
)


class SongReview(AbstractModel):
    """Represents a review and score for a song within an album context.

    This model stores a numeric score and an optional textual review linked to
    both a song and its album, enabling catalog-level qualitative feedback.

    Side Effects:
        Persists review records and supports soft-delete behavior for audit and
        recovery workflows.

    Relationships:
        - ForeignKey to Album.
        - ForeignKey to Song.
    """

    _safedelete_policy = SOFT_DELETE_CASCADE
    album = models.ForeignKey(Album, verbose_name=FIELD_ALBUM_LABEL, on_delete=models.CASCADE, related_name="reviews")
    song = models.ForeignKey(Song, verbose_name=FIELD_SONG_LABEL, on_delete=models.CASCADE, related_name="reviews")
    score = models.PositiveSmallIntegerField(
        FIELD_SCORE_LABEL,
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
    )
    review = models.TextField(FIELD_REVIEW_LABEL, blank=True, null=True)

    parent_relations = [
        (PARENT_RELATION_ALBUMS_LABEL, "album", "albums:index"),
        (PARENT_RELATION_SONGS_LABEL, "song", "songs:index"),
    ]

    class Meta:
        """Django metadata for table mapping, ordering, and display labels."""

        db_table = "song_reviews"
        verbose_name = MODEL_SONG_REVIEW_VERBOSE_NAME
        verbose_name_plural = MODEL_SONG_REVIEW_VERBOSE_NAME_PLURAL
        ordering = ["-id"]

    def __str__(self):
        """Return a human-readable identifier for the review record.

        Returns:
            str: A string combining song and album names.
        """
        return f"{self.song} - {self.album}"
