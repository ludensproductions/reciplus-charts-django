from django.db import models
from safedelete.models import SOFT_DELETE_CASCADE

from apps.comun.consts import CRUDOperatorsEnum
from apps.comun.models import AbstractNullableModel

from .consts import (
    FIELD_TAG_LABEL,
    MODEL_MUSIC_TAG_VERBOSE_NAME,
    MODEL_MUSIC_TAG_VERBOSE_NAME_PLURAL,
)


class MusicTags(AbstractNullableModel):
    """Represent a tag used to classify music content.

    This model stores a short tag label that can be associated with songs or
    other music entities for categorization.
    """

    _safedelete_policy = SOFT_DELETE_CASCADE
    tag = models.CharField(FIELD_TAG_LABEL, max_length=100)

    class Meta:
        db_table = "music_tags"
        verbose_name = MODEL_MUSIC_TAG_VERBOSE_NAME
        verbose_name_plural = MODEL_MUSIC_TAG_VERBOSE_NAME_PLURAL
        ordering = ["created_at"]

    class Config:
        crud_operations = [
            CRUDOperatorsEnum.INDEX,
            CRUDOperatorsEnum.CREATE,
            CRUDOperatorsEnum.READ,
            CRUDOperatorsEnum.UPDATE,
            CRUDOperatorsEnum.DELETE,
        ]
        api_operations = [
            CRUDOperatorsEnum.INDEX,
            CRUDOperatorsEnum.CREATE,
            CRUDOperatorsEnum.READ,
            CRUDOperatorsEnum.UPDATE,
            CRUDOperatorsEnum.DELETE,
        ]

    def __str__(self):
        """Return the display label for the music tag.

        Returns:
            str: Tag label.
        """
        # Always return a meaningful value for __str__; use f-strings instead of .format.
        return f"{self.tag}"
