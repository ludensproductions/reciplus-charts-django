from django.db import models
from safedelete.models import SOFT_DELETE_CASCADE

from apps.comun.models import AbstractNullableModel

from .consts import (
    FIELD_THEME_LABEL,
    MODEL_MUSIC_THEME_VERBOSE_NAME,
    MODEL_MUSIC_THEME_VERBOSE_NAME_PLURAL,
)


class MusicThemes(AbstractNullableModel):
    """Represent a music theme used to categorize songs.

    This model stores a short theme label that groups related music content.
    """

    _safedelete_policy = SOFT_DELETE_CASCADE
    theme = models.CharField(FIELD_THEME_LABEL, max_length=100)

    class Meta:
        db_table = "music_themes"
        verbose_name = MODEL_MUSIC_THEME_VERBOSE_NAME
        verbose_name_plural = MODEL_MUSIC_THEME_VERBOSE_NAME_PLURAL
        ordering = ["created_at"]

    def __str__(self):
        """Return the display label for the music theme.

        Returns:
            str: Theme label.
        """
        # Always return a meaningful value for __str__; use f-strings instead of .format.
        return f"{self.theme}"
