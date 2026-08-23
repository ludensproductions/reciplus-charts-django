from django.db import models
from django.utils.translation import gettext_lazy as _
from safedelete.models import SOFT_DELETE_CASCADE

from apps.comun.models import AbstractModel


class Teacher(AbstractModel):
    """Teacher entity with contact details and profile image."""

    _safedelete_policy = SOFT_DELETE_CASCADE
    name = models.CharField(_("Nombre"), max_length=255)
    last_name = models.CharField(_("Apellido"), max_length=255)
    email = models.EmailField(_("Correo electrónico"), max_length=255)
    phone = models.CharField(_("Teléfono"), max_length=255)
    address = models.CharField(_("Dirección"), max_length=255)
    image = models.ImageField(
        _("Imagen"),
        upload_to="profiles/",
        max_length=255,
        blank=True,
        null=True,
        default="/static/assets/img/avatars/blank-profile-pic.png",
    )

    class Meta:
        db_table = "teachers"
        verbose_name = _("Profesor")
        verbose_name_plural = _("Profesores")
        ordering = ["id"]

    def __str__(self):
        """Return the teacher full name for display purposes."""
        return f"{self.name} {self.last_name}"
