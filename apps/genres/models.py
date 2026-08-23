from django.core.validators import RegexValidator
from django.db import models

from apps.comun.fields import DisplayNameField
from apps.comun.models import AbstractModel

from .consts import (
    ERROR_LETTERS_BLANKS_ONLY,
    FIELD_DISPLAY_NAME_LABEL,
    FIELD_GENRE_LABEL,
    MODEL_GENRE_VERBOSE_NAME,
    MODEL_GENRE_VERBOSE_NAME_PLURAL,
)

LETTERS_BLANKS_VALIDATOR = RegexValidator(
    regex=r"^[A-Za-zÀ-ÿ\s]+$",
    message=ERROR_LETTERS_BLANKS_ONLY,
)


class Genre(AbstractModel):
    """Represent a music or content genre with validation rules.

    This model stores a canonical genre label and a display name used across
    the catalog.
    """

    genre = models.TextField(FIELD_GENRE_LABEL, validators=[LETTERS_BLANKS_VALIDATOR])
    display_name = DisplayNameField(
        verbose_name=FIELD_DISPLAY_NAME_LABEL,
        display_name="genre",
        max_length=255,
        validators=[LETTERS_BLANKS_VALIDATOR],
    )

    # This list prevents deleting genres when related objects exist.
    child_relations = [
        ("películas", "movie", "movies:index"),
        ("ventas", "movie__movie_sale__sale", "sales:index"),
    ]

    class Meta:
        db_table = "cat_genres"  # cat means this models is a catalogue
        verbose_name = MODEL_GENRE_VERBOSE_NAME
        verbose_name_plural = MODEL_GENRE_VERBOSE_NAME_PLURAL
        ordering = ["-id"]

    def __str__(self):
        """Return the genre display value.

        Returns:
            str: Genre name.
        """
        return self.genre
