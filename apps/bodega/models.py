from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.comun.models import AbstractModel


class Bodega(AbstractModel):
    """Warehouse record for products and groceries."""

    bodega = models.CharField(max_length=255, verbose_name=_("Bodega"))
    producto = models.ForeignKey(
        "productos.Producto",
        on_delete=models.CASCADE,
        related_name="productos_bodega",
        related_query_name="bodega_producto",
        null=True,
        blank=True,
        verbose_name=_("Producto"),
    )
    abarrotes = models.ForeignKey(
        "abarrotes.Abarrotes",
        on_delete=models.CASCADE,
        related_name="abarrotes_bodega",
        related_query_name="bodega_abarrote",
        null=True,
        blank=True,
        verbose_name=_("Abarrotes"),
    )
    lote = models.CharField(max_length=100, verbose_name=_("Lote"))

    class Meta:
        db_table = "bodega_producto"
        verbose_name = _("Bodega producto")
        verbose_name_plural = _("Bodega productos")
        ordering = ["-id"]

    def __str__(self):
        """Return the warehouse name.

        Returns:
            str: Warehouse name.
        """
        return self.bodega
