from django.db import models
from safedelete.models import SOFT_DELETE_CASCADE

from apps.categories import consts
from apps.comun.models import AbstractNullableModel


class Category(AbstractNullableModel):
    """Represents a category for grouping items or entities.

    This model is used to organize and classify objects within the application.
    Supports soft deletion and provides a name field for the category label.
    """

    _safedelete_policy = SOFT_DELETE_CASCADE
    name = models.CharField(max_length=100, verbose_name=consts.INDEX_FIELDS["name"])

    def __str__(self):
        """Returns the string representation of the category.

        Returns:
            str: The name of the category.
        """
        return self.name

    class Meta:
        db_table = "category"
        verbose_name = consts.MODULE_VERBOSE_NAME
        verbose_name_plural = consts.MODULE_VERBOSE_NAME_PLURAL
        ordering = consts.DEFAULT_ORDERING
