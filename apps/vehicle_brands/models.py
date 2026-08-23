from django.db import models
from django.utils.translation import gettext_lazy as _
from safedelete.models import SOFT_DELETE_CASCADE

from apps.comun.models import AbstractModel


class VehicleBrand(AbstractModel):
    _safedelete_policy = SOFT_DELETE_CASCADE

    name = models.CharField(_("Name"), max_length=150, unique=True)

    class Meta:
        db_table = "vehicle_brands"
        verbose_name = _("Marca de vehículo")
        verbose_name_plural = _("Marcas de vehículos")
        ordering = ["name"]

    def __str__(self):
        return self.name