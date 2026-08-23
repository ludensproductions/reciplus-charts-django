from django.db import models
from django.utils.translation import gettext_lazy as _
from safedelete.models import SOFT_DELETE_CASCADE

from apps.comun.models import AbstractNullableModel
from apps.contents.consts import ContentTypes


class Video(AbstractNullableModel):
    """Represents a video entry associated with a content record.

    Attributes:
        content: Content record linked to the video metadata.
        video_url: URL pointing to the stored video file.
    """

    _safedelete_policy = SOFT_DELETE_CASCADE

    content = models.OneToOneField(
        "contents.Content",
        on_delete=models.CASCADE,
        related_name="video",
        verbose_name=_("Contenido"),
    )
    video_url = models.URLField(verbose_name=_("URL del video"))

    def __str__(self):
        """Return the related content title for display."""
        return self.content.title

    class Meta:
        db_table = "video"
        verbose_name = _("Video")
        verbose_name_plural = _("Videos")
        ordering = ["-id"]

    def should_allow_delete_action(self):
        """Return whether the content type still identifies the record as a video.

        Returns:
            bool: True when the linked content has the video content type.
        """
        return self.content.content_type == ContentTypes.VIDEO
