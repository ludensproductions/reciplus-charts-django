from django.db import models
from safedelete.models import SOFT_DELETE_CASCADE

from apps.comun.models import AbstractNullableModel
from apps.contents import consts as contents_consts


class Content(AbstractNullableModel):
    """Store a content entry with a specific content type.

    This model holds the common data for content records and references a
    specific subtype (article or video). The subtype is managed by separate
    models linked to this record.

    Attributes:
        title (str): Content title.
        content_type (str): Content type identifier.
    """

    _safedelete_policy = SOFT_DELETE_CASCADE
    title = models.CharField(
        max_length=200,
        verbose_name=contents_consts.CONTENT_TITLE_LABEL,
    )
    content_type = models.CharField(
        max_length=20,
        choices=contents_consts.ContentTypes,
        verbose_name=contents_consts.CONTENT_TYPE_FIELD_LABEL,
    )

    def __str__(self):
        """Return the content title for display.

        Returns:
            str: Content title.
        """
        return self.title

    class Meta:
        db_table = "content"
        verbose_name = contents_consts.MODEL_VERBOSE_NAME
        verbose_name_plural = contents_consts.MODEL_VERBOSE_NAME_PLURAL
        ordering = ["-id"]

    def delete_specific_content(self):
        """Delete the related subtype object if it exists.

        Side Effects:
            Deletes the related article or video when present.
        """
        content_map = {
            contents_consts.ContentTypes.ARTICLE: "article",
            contents_consts.ContentTypes.VIDEO: "video",
        }

        related_attr = content_map.get(self.content_type)
        if not related_attr:
            return

        related_obj = getattr(self, related_attr, None)
        if related_obj and not related_obj.deleted:
            related_obj.delete()

    def undelete_specific_content(self):
        """Restore the related subtype object if it was deleted.

        Side Effects:
            Restores the related article or video when present.
        """
        content_map = {
            contents_consts.ContentTypes.ARTICLE: "article",
            contents_consts.ContentTypes.VIDEO: "video",
        }

        related_attr = content_map.get(self.content_type)
        if not related_attr:
            return

        related_obj = getattr(self, related_attr, None)
        if related_obj and related_obj.deleted:
            related_obj.undelete()
