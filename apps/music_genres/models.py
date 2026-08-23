from django.db import models
from safedelete.models import SOFT_DELETE_CASCADE

from apps.comun.models import AbstractNullableModel

from .consts import (
    FIELD_GENRE_LABEL,
    MODEL_MUSIC_GENRE_VERBOSE_NAME,
    MODEL_MUSIC_GENRE_VERBOSE_NAME_PLURAL,
)


class MusicGenres(AbstractNullableModel):
    """Represent a genre used to classify music content.

    This model stores a short genre label that groups related music items.
    """

    _safedelete_policy = SOFT_DELETE_CASCADE
    genre = models.CharField(FIELD_GENRE_LABEL, max_length=100)

    class Meta:
        db_table = "music_genres"
        verbose_name = MODEL_MUSIC_GENRE_VERBOSE_NAME
        verbose_name_plural = MODEL_MUSIC_GENRE_VERBOSE_NAME_PLURAL
        ordering = ["created_at"]

    def __str__(self):
        """Return the display label for the music genre.

        Returns:
            str: Genre label.
        """
        # Always return a meaningful value for __str__; use f-strings instead of .format.
        return f"{self.genre}"
