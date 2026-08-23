from django.db import models
from safedelete.models import SOFT_DELETE_CASCADE

from apps.articles import consts as articles_consts
from apps.comun.models import AbstractNullableModel
from apps.contents.consts import ContentTypes


class Article(AbstractNullableModel):
    """Store an article associated with a content record.

    This model keeps the article body and its category, linked to a content
    entry that defines the type and shared metadata.

    Attributes:
        content (Content): Parent content record.
        body (str): Article body content.
        category (Category | None): Optional category for the article.
    """

    _safedelete_policy = SOFT_DELETE_CASCADE
    content = models.OneToOneField(
        "contents.Content",
        on_delete=models.CASCADE,
        related_name="article",
        verbose_name=articles_consts.CONTENT_LABEL,
    )
    body = models.TextField(verbose_name=articles_consts.BODY_LABEL)
    category = models.ForeignKey(
        "categories.Category",
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=articles_consts.CATEGORY_LABEL,
    )

    def __str__(self):
        """Return the article title for display.

        Returns:
            str: Article title.
        """
        return self.content.title

    class Meta:
        db_table = "article"
        verbose_name = articles_consts.MODEL_VERBOSE_NAME
        verbose_name_plural = articles_consts.MODEL_VERBOSE_NAME_PLURAL
        ordering = ["-id"]

    def should_allow_delete_action(self):
        """Check whether the delete action should be allowed.

        Returns:
            bool: True when the content type is article.
        """
        return self.content.content_type == ContentTypes.ARTICLE
