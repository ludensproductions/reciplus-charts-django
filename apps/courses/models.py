from django.db import models
from django.utils.translation import gettext_lazy as _
from safedelete.models import SOFT_DELETE_CASCADE

from apps.comun.models import AbstractModel


class Course(AbstractModel):
    """Course entity with basic metadata and teacher relationship."""

    _safedelete_policy = SOFT_DELETE_CASCADE
    name = models.CharField(_("Nombre"), max_length=255)
    description = models.TextField(_("Descripción"), blank=True, null=True)
    image = models.ImageField(
        _("Imagen"),
        upload_to="classes/",
        max_length=255,
        blank=True,
        null=True,
    )
    teacher = models.ForeignKey(
        "teachers.Teacher",
        verbose_name=_("Profesor"),
        on_delete=models.CASCADE,
        related_name="classes",
    )

    class Meta:
        db_table = "classes"
        verbose_name = _("Clase")
        verbose_name_plural = _("Clases")
        ordering = ["id"]

    def __str__(self):
        """Return the course display name."""
        return self.name
