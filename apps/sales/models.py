from django.db import models
from django.utils.translation import gettext_lazy as _
from safedelete.models import SOFT_DELETE_CASCADE

from apps.comun.models import AbstractModel


class Sale(AbstractModel):
    """Modelo que representa una venta."""

    _safedelete_policy = SOFT_DELETE_CASCADE

    name = models.CharField(_("Nombre"), max_length=100)
    date = models.DateField(_("Fecha"), auto_now_add=True)
    encargado = models.ForeignKey("users.User", verbose_name=_("Encargado"), on_delete=models.CASCADE)
    total = models.DecimalField(_("Total"), max_digits=15, decimal_places=2, null=True, blank=True)
    folio = models.CharField(_("Folio"), max_length=120, null=False, blank=False, default=None)

    delete_on_cascade = [
        "movie_sale",
    ]

    class Meta:
        db_table = "sales"
        verbose_name = _("Venta")
        verbose_name_plural = _("Ventas")
        ordering = ["-id"]

    def __str__(self):
        """Retorna el nombre de la venta."""
        return self.name
