from django.db import models
from django.utils.translation import gettext_lazy as _
from safedelete.models import SOFT_DELETE_CASCADE

from apps.comun.models import AbstractModel


class VehicleType(AbstractModel):
    """Represents the type of a vehicle and ensures uniqueness."""

    _safedelete_policy = SOFT_DELETE_CASCADE

    name = models.CharField(_("Nombre"), max_length=150, unique=True)

    class Meta:
        db_table = "vehicle_types"
        verbose_name = _("Tipo de vehículo")
        verbose_name_plural = _("Tipos de vehículos")
        ordering = ["name"]

    def __str__(self):
        """Return the localized name of the vehicle type."""
        return self.name
