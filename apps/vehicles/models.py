from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _
from safedelete.models import SOFT_DELETE_CASCADE

from apps.comun.consts import RegexValidator as RV
from apps.comun.models import AbstractModel


class Vehicle(AbstractModel):
    """Represents a vehicle registered in the fleet."""

    _safedelete_policy = SOFT_DELETE_CASCADE

    model = models.CharField(_("Modelo"), max_length=150)
    year = models.PositiveIntegerField(_("Año"))
    license_plate = models.CharField(
        _("Placa"),
        max_length=20,
        unique=True,
        validators=[RegexValidator(RV.MEX_PLATE_EXTENDED, _("Placa inválida."))],
    )
    name = models.CharField(
        _("Nombre"),
        max_length=150,
        blank=True,
        null=True,
    )
    brand = models.ForeignKey(
        "vehicle_brands.VehicleBrand",
        verbose_name=_("Marca"),
        on_delete=models.CASCADE,
        related_name="vehicles",
    )
    vehicle_type = models.ForeignKey(
        "vehicle_types.VehicleType",
        verbose_name=_("Tipo de vehículo"),
        on_delete=models.CASCADE,
        related_name="vehicles",
    )

    class Meta:
        db_table = "vehicles"
        verbose_name = _("Vehículo")
        verbose_name_plural = _("Vehículos")
        ordering = ["model", "year"]

    def __str__(self):
        """Return a short representation combining brand, model, and year."""
        return f"{self.brand.name} {self.model} ({self.year})"
